#!/usr/bin/env python3
"""review_server.py — serve the canonical_genealogy viewers WITH the annotation overlay,
and accept the saved reviews.

  python review/review_server.py            # serves on http://localhost:8742

Open any viewer/toy through this server (e.g. http://localhost:8742/viewer_v3.html) and the
review_layer overlay is injected automatically — no edits to the viewer files. Drawings,
boxes, arrows, highlights, typed labels and pin-comments are captured along with a snapshot
of the page state, and POSTed back to /save, which writes:

    reviews/<timestamp>-<name>.review.json   (state + annotations)
    reviews/<timestamp>-<name>.png            (composite screengrab)

Open the SAME pages through the plain preview server (8741) to use them clean, with no overlay.
"""
import http.server, socketserver, os, json, datetime, base64, threading
from urllib.parse import urlparse, parse_qs

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # canonical_genealogy/
REVIEWS = os.path.join(ROOT, 'reviews')
os.makedirs(REVIEWS, exist_ok=True)
PORT = 8742
INJECT = '<script src="/review/review_layer.js"></script>'
PINS_FILE = os.path.join(REVIEWS, 'pins.json')
PINS_LOCK = threading.Lock()


def load_pins():
    try:
        with open(PINS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_pins(pins):
    with open(PINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(pins, f, indent=2, ensure_ascii=False)


def append_pin(rec):
    with PINS_LOCK:
        pins = load_pins()
        pins.append(rec)
        save_pins(pins)
    return rec


# ---- pin lifecycle (Pav asks 3 + 4): ask/give/status, edit, follow-ups, retire ----
ASK_STATUSES = ('open', 'acknowledged', 'answered', 'applied', 'verified', 'retired')


def _now_iso():
    return datetime.datetime.now().astimezone().isoformat()


def update_pin(pin_id, patch):
    """Apply an in-place update to one pin. patch may carry:
       comment (str), status (str), give ({text,by,commit,at}), add_note ({text,by}),
       retired (bool). Status transitions are appended to history[]. Records are never
       destroyed; delete only sets retired=true. Returns the updated pin or None."""
    with PINS_LOCK:
        pins = load_pins()
        idx = next((i for i, p in enumerate(pins) if p.get('id') == pin_id), -1)
        if idx < 0:
            return None
        p = pins[idx]
        p.setdefault('status', 'open')
        p.setdefault('history', [])
        p.setdefault('notes', [])
        if isinstance(patch.get('comment'), str):
            p['comment'] = patch['comment']
        if isinstance(patch.get('annotations'), int):
            p['annotations'] = patch['annotations']
        give = patch.get('give')
        if isinstance(give, dict):
            g = dict(p.get('give') or {})
            for k in ('text', 'by', 'commit'):
                if k in give:
                    g[k] = give[k]
            g['at'] = give.get('at') or _now_iso()
            p['give'] = g
        note = patch.get('add_note')
        if isinstance(note, dict) and isinstance(note.get('text'), str) and note['text'].strip():
            p['notes'].append({'text': note['text'].strip(),
                               'by': note.get('by') or 'reviewer',
                               'at': note.get('at') or _now_iso()})
        st = patch.get('status')
        if isinstance(st, str) and st in ASK_STATUSES and st != p.get('status'):
            p['history'].append({'from': p.get('status'), 'to': st,
                                 'at': _now_iso(), 'by': patch.get('by') or 'reviewer'})
            p['status'] = st
        if patch.get('retired') is True and p.get('status') != 'retired':
            p['history'].append({'from': p.get('status'), 'to': 'retired',
                                 'at': _now_iso(), 'by': patch.get('by') or 'reviewer'})
            p['status'] = 'retired'
            p['retired'] = True
        p['updatedAt'] = _now_iso()
        pins[idx] = p
        save_pins(pins)
        return p


def retire_pin(pin_id, by='reviewer'):
    """DELETE == retire. The pin stays in the registry (retired:true) and its
       .review.json/.png files are kept on disk; records are never destroyed."""
    return update_pin(pin_id, {'retired': True, 'by': by})

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, fmt, *args):
        pass  # quiet; we print our own save lines

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/pins':
            q = parse_qs(urlparse(self.path).query)
            page = (q.get('page') or [''])[0]
            pins = [p for p in load_pins() if p.get('page') == page] if page else load_pins()
            body = json.dumps({'pins': pins}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path.endswith('.html'):
            fs = os.path.join(ROOT, path.lstrip('/').replace('/', os.sep))
            if os.path.isfile(fs):
                with open(fs, 'rb') as f:
                    txt = f.read().decode('utf-8', errors='replace')
                if INJECT not in txt:
                    txt = (txt.replace('</body>', INJECT + '\n</body>', 1)
                           if '</body>' in txt else txt + INJECT)
                out = txt.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(out)))
                self.end_headers()
                self.wfile.write(out)
                return
        return super().do_GET()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _pin_id(self):
        # /pins/<id>  ->  <id>  (URL-decoded, no query)
        from urllib.parse import unquote
        path = urlparse(self.path).path
        if not path.startswith('/pins/'):
            return None
        return unquote(path[len('/pins/'):]).strip('/') or None

    def _read_json_body(self):
        try:
            ln = int(self.headers.get('Content-Length', '0'))
            return json.loads(self.rfile.read(ln).decode('utf-8')) if ln else {}
        except Exception:
            return None

    def do_PATCH(self):
        pid = self._pin_id()
        if not pid:
            return self._json(404, {'ok': False, 'error': 'PATCH only on /pins/<id>'})
        patch = self._read_json_body()
        if patch is None or not isinstance(patch, dict):
            return self._json(400, {'ok': False, 'error': 'bad json body'})
        rec = update_pin(pid, patch)
        if rec is None:
            return self._json(404, {'ok': False, 'error': 'no such pin: %s' % pid})
        print('[review] PATCH pin %s -> status=%s%s' % (pid, rec.get('status'),
              ' (give set)' if rec.get('give') else ''))
        return self._json(200, {'ok': True, 'pin': rec})

    def do_DELETE(self):
        pid = self._pin_id()
        if not pid:
            return self._json(404, {'ok': False, 'error': 'DELETE only on /pins/<id>'})
        rec = retire_pin(pid)
        if rec is None:
            return self._json(404, {'ok': False, 'error': 'no such pin: %s' % pid})
        print('[review] DELETE (retire) pin %s -> status=retired (files kept)' % pid)
        return self._json(200, {'ok': True, 'pin': rec, 'retired': True})

    def do_POST(self):
        if self.path.split('?')[0] != '/save':
            self.send_response(404); self.end_headers(); return
        try:
            ln = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(ln).decode('utf-8'))
        except Exception as e:
            self.send_response(400); self.end_headers()
            self.wfile.write(('bad request: %s' % e).encode()); return
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        raw = (payload.get('meta', {}) or {}).get('name') or 'review'
        safe = ''.join(c for c in raw if c.isalnum() or c in '-_')[:40] or 'review'
        base = '%s-%s' % (stamp, safe)
        png = payload.pop('png', None)
        png_rel = None
        if png and isinstance(png, str) and png.startswith('data:image'):
            try:
                b64 = png.split(',', 1)[1]
                with open(os.path.join(REVIEWS, base + '.png'), 'wb') as f:
                    f.write(base64.b64decode(b64))
                png_rel = base + '.png'
            except Exception:
                pass
        payload.setdefault('meta', {})['png'] = png_rel
        payload['meta']['source_page'] = (payload.get('state', {}) or {}).get('path')
        with open(os.path.join(REVIEWS, base + '.review.json'), 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        n = len(payload.get('annotations', []) or [])
        # permanent pin registry: one gold pin per saved review session
        pin_rec = None
        pin_meta = payload['meta'].get('pin')
        if pin_meta:
            pin_rec = {
                'id': base,
                'page': payload['meta'].get('source_page'),
                'x': pin_meta.get('x'), 'y': pin_meta.get('y'),
                'nx': pin_meta.get('nx'), 'ny': pin_meta.get('ny'),
                'comment': pin_meta.get('comment', ''),
                'savedAt': payload['meta'].get('savedAt'),
                'annotations': n,
                'review': base + '.review.json',
                'png': png_rel,
            }
            append_pin(pin_rec)
        print('[review] saved reviews/%s.review.json  (%d annotations, page %s%s)'
              % (base, n, payload['meta'].get('source_page'),
                 ', pin registered' if pin_rec else ''))
        body = json.dumps({'ok': True, 'path': 'reviews/%s.review.json' % base,
                           'png': png_rel, 'pin': pin_rec}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), Handler) as srv:
        print('[review] serving %s' % ROOT)
        print('[review] open  http://localhost:%d/viewer_v3.html  (overlay injected)' % PORT)
        print('[review] saves land in  %s' % REVIEWS)
        srv.serve_forever()
