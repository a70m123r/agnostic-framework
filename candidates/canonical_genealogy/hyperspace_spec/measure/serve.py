#!/usr/bin/env python3
"""Static server for the substrate viewer that sends no-cache headers, so a normal browser reload
always picks up the latest viewer/data (a plain http.server lets the browser heuristically cache the
HTML, serving stale pages). Usage: python serve.py [port]  (default 8753, serves this directory)."""
import http.server, socketserver, sys, functools
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8753
DIR = str(Path(__file__).resolve().parent)


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(NoCache, directory=DIR)
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"serving {DIR} on http://localhost:{PORT}  (no-cache)")
        httpd.serve_forever()
