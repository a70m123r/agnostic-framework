"""
P-L6 fetch v2 — polite sequential fetcher (v1 hit the 2025+ anonymous-burst 429
throttle on wikimedia.org/api/rest_v1 with 5 threads; this version is sequential
with adaptive delay + Retry-After honoring, and trims candidates via daily
top-1000 lists BEFORE any per-article call).

DESIGN CHANGE vs v1 (disclosed): treated storms are pre-screened by appearance in
the daily top-1000 list within [prot-14, prot+7]. Scope therefore = storms whose
peak clears the en.wiki daily top-1000 floor (~5-10k views/day). Matched controls
are drawn from the SAME lists, so the floor is shared by both arms.

Resumable: every HTTP response cached to disk; --budget N stops cleanly (exit 3).
Same dataset schema as v1 -> pl6_analyze.py unchanged.
"""
import json, os, sys, time, hashlib, datetime as dt, math
import urllib.request, urllib.parse, urllib.error

from pl6_fetch import (parse_events, detect_storm, canon, NS_PREFIXES, BLOCK_EXACT,
                       edit_level, CACHE, DATA, PROT_START, PROT_END, PV_PRE_D,
                       PV_POST_D, PEAK_LO, PEAK_HI, STORM_RATIO, STORM_EXCESS,
                       CTRL_BAND, CTRL_CAND_PER_T, UA)

BUDGET = 540.0
for i, a in enumerate(sys.argv):
    if a == "--budget" and i + 1 < len(sys.argv):
        BUDGET = float(sys.argv[i + 1])
T0 = time.time()

class Budget(Exception):
    pass

class Limiter:
    def __init__(self, base, floor, cap=4.0):
        self.delay, self.floor, self.cap = base, floor, cap
        self.last = 0.0
    def wait(self):
        if time.time() - T0 > BUDGET:
            raise Budget()
        d = self.delay - (time.time() - self.last)
        if d > 0:
            time.sleep(d)
        self.last = time.time()
    def ok(self):
        self.delay = max(self.floor, self.delay * 0.985)
    def throttled(self, retry_after):
        self.delay = min(self.cap, max(self.delay * 1.5, 0.5))
        wait_s = max(retry_after, 5.0)
        if time.time() - T0 + wait_s > BUDGET:
            raise Budget()
        time.sleep(wait_s)

LIM_REST = Limiter(0.45, 0.35)   # wikimedia.org/api/rest_v1
LIM_MW   = Limiter(0.15, 0.10)   # en.wikipedia.org/w/api.php

def log(m):
    print(m, flush=True)

def fetch(url, cache_key, limiter, retries=5):
    path = os.path.join(CACHE, cache_key + ".json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    backoff = 5.0
    for a in range(retries):
        limiter.wait()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                obj = json.loads(r.read().decode("utf-8"))
            limiter.ok()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f)
            return obj
        except urllib.error.HTTPError as e:
            if e.code == 404:
                obj = {"_error": 404}
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(obj, f)
                return obj
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                try:
                    ra = float(ra) if ra else backoff
                except ValueError:
                    ra = backoff
                log("  429 (retry in %.0fs, delay now %.2fs)" % (max(ra, 5.0), limiter.delay))
                limiter.throttled(ra)
                backoff = min(backoff * 2, 120)
                continue
            time.sleep(1 + a)
        except Budget:
            raise
        except Exception:
            time.sleep(1 + a)
    return {"_error": "exhausted"}

def fetch_pv(title, d0, d1):
    key = "pv_" + hashlib.sha1((canon(title) + d0.isoformat() + d1.isoformat()).encode("utf-8")).hexdigest()
    t = urllib.parse.quote(canon(title), safe="")
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           "en.wikipedia/all-access/user/%s/daily/%s/%s"
           % (t, d0.strftime("%Y%m%d"), d1.strftime("%Y%m%d")))
    obj = fetch(url, key, LIM_REST)
    series = {}
    for it in obj.get("items", []):
        ts = it["timestamp"][:8]
        series["%s-%s-%s" % (ts[:4], ts[4:6], ts[6:8])] = it["views"]
    out = {}
    d = d0
    while d <= d1:
        out[d.isoformat()] = series.get(d.isoformat(), 0)
        d += dt.timedelta(days=1)
    out["_err"] = obj.get("_error")
    return out

def get_prot_log_cached():
    events, page = [], 0
    while True:
        path = os.path.join(CACHE, "protlog_p%03d.json" % page)
        if not os.path.exists(path):
            break
        with open(path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        events.extend(obj.get("query", {}).get("logevents", []))
        if not obj.get("continue", {}).get("lecontinue"):
            break
        page += 1
    return events

def main():
    state_p = os.path.join(DATA, "pl6_state.json")
    log("== P-L6 fetch v2 (budget %.0fs) ==" % BUDGET)

    events = get_prot_log_cached()
    if not events:
        log("FATAL: protlog cache missing"); sys.exit(1)
    treated_events, all_logged = parse_events(events)
    log("protlog cached: %d events, %d unique edit-protected titles, %d exclusion titles"
        % (len(events), len(treated_events), len(all_logged)))

    try:
        # ---- stage T: tops for every day in [PROT_START-14, PROT_END+7] ----
        d = PROT_START - dt.timedelta(days=14)
        d_end = PROT_END + dt.timedelta(days=7)
        tops = {}
        n_new = 0
        while d <= d_end:
            key = "top_%s" % d.isoformat()
            had = os.path.exists(os.path.join(CACHE, key + ".json"))
            url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/"
                   "all-access/%04d/%02d/%02d" % (d.year, d.month, d.day))
            obj = fetch(url, key, LIM_REST)
            if not had:
                n_new += 1
            arts = {}
            if obj.get("items"):
                for it in obj["items"][0].get("articles", []):
                    arts[it["article"]] = it["views"]
            tops[d.isoformat()] = arts
            d += dt.timedelta(days=1)
        log("tops: %d days loaded (%d newly fetched)" % (len(tops), n_new))

        # ---- stage 2: trim treated candidates via top appearance ----
        cands = []
        for ev in treated_events:
            pd = dt.date.fromisoformat(ev["prot_date"])
            hit = None
            for off in range(PEAK_LO, PEAK_HI + 1):
                dd = (pd + dt.timedelta(days=off)).isoformat()
                v = tops.get(dd, {}).get(ev["key"])
                if v is not None and (hit is None or v > hit[1]):
                    hit = (dd, v)
            if hit:
                ev2 = dict(ev); ev2["top_hit_date"], ev2["top_hit_views"] = hit
                cands.append(ev2)
        log("treated candidates appearing in top-1000 near protection: %d / %d"
            % (len(cands), len(treated_events)))

        # ---- stage 3: per-article series for treated candidates ----
        treated = []
        fail_counts = {}
        for i, ev in enumerate(cands):
            pd = dt.date.fromisoformat(ev["prot_date"])
            series = fetch_pv(ev["title"], pd - dt.timedelta(days=PV_PRE_D), pd + dt.timedelta(days=PV_POST_D))
            det = detect_storm(series, ev["prot_date"], "treated")
            rec = dict(ev); rec.update(det)
            rec["series"] = {k: v for k, v in series.items() if not k.startswith("_")}
            treated.append(rec)
            fr = det.get("fail_reason") or "QUALIFIES"
            fail_counts[fr] = fail_counts.get(fr, 0) + 1
            if (i + 1) % 25 == 0:
                log("  treated pv %d/%d (delay %.2fs)" % (i + 1, len(cands), LIM_REST.delay))
        qual = [t for t in treated if t["qualifies"]]
        log("storm attrition: %s" % json.dumps(fail_counts))
        log("qualifying treated storms: %d" % len(qual))

        # ---- stage 4: control candidates from tops on treated peak dates ----
        cand = {}
        for t in qual:
            arts = []
            for a, v in tops.get(t["peak_date"], {}).items():
                if a in BLOCK_EXACT or any(a.startswith(p) for p in NS_PREFIXES):
                    continue
                if a in all_logged:
                    continue
                if not (CTRL_BAND[0] * t["peak_views"] <= v <= CTRL_BAND[1] * t["peak_views"]):
                    continue
                arts.append((a, v))
            arts.sort(key=lambda av: abs(math.log10(max(av[1], 1)) - math.log10(max(t["peak_views"], 1))))
            for a, v in arts[:CTRL_CAND_PER_T]:
                cand.setdefault(a, {"title": a.replace("_", " "), "anchors": {}})
                cand[a]["anchors"][t["key"]] = t["peak_date"]
        log("unique control candidates: %d" % len(cand))

        # ---- stage 5: control series ----
        ctrl_pv = {}
        ckeys = sorted(cand.keys())
        for i, akey in enumerate(ckeys):
            anchors = sorted(cand[akey]["anchors"].values())
            d0 = dt.date.fromisoformat(anchors[0]) - dt.timedelta(days=PV_PRE_D)
            d1 = dt.date.fromisoformat(anchors[-1]) + dt.timedelta(days=PV_POST_D)
            ctrl_pv[akey] = fetch_pv(cand[akey]["title"], d0, d1)
            if (i + 1) % 25 == 0:
                log("  ctrl pv %d/%d (delay %.2fs)" % (i + 1, len(ckeys), LIM_REST.delay))

        # ---- stage 6: control protection screening (MediaWiki host) ----
        ctrl_logs = {}
        for i, akey in enumerate(ckeys):
            p = {"action": "query", "list": "logevents", "letype": "protect",
                 "letitle": cand[akey]["title"], "lelimit": "500",
                 "leprop": "ids|title|type|timestamp|comment|details",
                 "format": "json", "formatversion": "2"}
            url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
            ctrl_logs[akey] = fetch(url, "ctlog_" + hashlib.sha1(akey.encode("utf-8")).hexdigest(), LIM_MW)
            if (i + 1) % 50 == 0:
                log("  ctrl logs %d/%d" % (i + 1, len(ckeys)))

        cur_prot = {}
        for b in range(0, len(ckeys), 50):
            batch = ckeys[b:b + 50]
            p = {"action": "query", "prop": "info", "inprop": "protection",
                 "titles": "|".join(cand[k]["title"] for k in batch),
                 "format": "json", "formatversion": "2"}
            url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
            obj = fetch(url, "ctinfo2_b%03d" % (b // 50), LIM_MW)
            for pg in obj.get("query", {}).get("pages", []):
                prot = [pr for pr in pg.get("protection", []) if pr.get("type") == "edit"]
                cur_prot[canon(pg.get("title", ""))] = prot

        controls = []
        for akey in ckeys:
            c = cand[akey]
            series = ctrl_pv.get(akey, {})
            levs = ctrl_logs.get(akey, {}).get("query", {}).get("logevents", [])
            bad, ever = False, False
            for ev in levs:
                if ev.get("action") not in ("protect", "modify"):
                    continue
                det = (ev.get("params", {}) or {}).get("details")
                desc = ((ev.get("params", {}) or {}).get("description", "") or "")
                if edit_level(det) is None and "[edit=" not in desc:
                    continue
                ever = True
                ets = ev.get("timestamp", "")
                try:
                    ed = dt.date(int(ets[:4]), int(ets[5:7]), int(ets[8:10]))
                except Exception:
                    continue
                for D in c["anchors"].values():
                    Dd = dt.date.fromisoformat(D)
                    if Dd - dt.timedelta(days=365) <= ed <= Dd + dt.timedelta(days=40):
                        bad = True
            cur = cur_prot.get(akey, [])
            for D in sorted(set(c["anchors"].values())):
                det = detect_storm(series, D, "control")
                controls.append({"key": akey, "title": c["title"], "anchor_date": D,
                                 "anchor_treated": [tk for tk, dd in c["anchors"].items() if dd == D],
                                 "prot_event_near_window": bad,
                                 "prot_event_ever": ever,
                                 "currently_edit_protected": bool(cur),
                                 "series": {k: v for k, v in series.items() if not k.startswith("_")},
                                 **det})
        n_clean = sum(1 for c in controls if c["qualifies"] and not c["prot_event_near_window"]
                      and not c["currently_edit_protected"])
        log("control storm records: %d ; qualifying+clean: %d" % (len(controls), n_clean))

        dataset = {
            "params": {"PROT_START": PROT_START.isoformat(), "PROT_END": PROT_END.isoformat(),
                       "PV_PRE_D": PV_PRE_D, "PV_POST_D": PV_POST_D,
                       "PEAK_WINDOW": [PEAK_LO, PEAK_HI], "STORM_RATIO": STORM_RATIO,
                       "STORM_EXCESS": STORM_EXCESS, "CTRL_BAND": CTRL_BAND,
                       "top_floor_scope": "treated storms pre-screened by top-1000 appearance near protection (shared floor with controls)",
                       "endpoints": {
                           "protlog": "https://en.wikipedia.org/w/api.php?action=query&list=logevents&letype=protect&lenamespace=0",
                           "pageviews": "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{article}/daily/",
                           "top": "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{y}/{m}/{d}",
                           "ctrl_screen": "https://en.wikipedia.org/w/api.php?action=query&list=logevents&letype=protect&letitle= + prop=info&inprop=protection"},
                       "ua": UA},
            "attrition": fail_counts,
            "treated": treated,
            "controls": controls,
        }
        out = os.path.join(DATA, "pl6_dataset.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(dataset, f)
        log("dataset written: %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
        log("DONE in %.1f s" % (time.time() - T0))
    except Budget:
        log("BUDGET_STOP at %.0fs — rerun to resume (cache persists)" % (time.time() - T0))
        sys.exit(3)

if __name__ == "__main__":
    main()
