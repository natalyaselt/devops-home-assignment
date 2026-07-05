#!/usr/bin/env python3
"""Tiny dependency-free mock of the external epoch service.

Exposes POST /epoch which accepts {"date": "<ISO-8601>"} and returns
{"epoch": <unix seconds>}. Used only for local end-to-end testing of
now-time-service. Not for production use.
"""
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8081


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/epoch":
            self._send(404, {"error": "not found"})
            return

        raw = self._read_body() or b"{}"
        try:
            date_str = json.loads(raw)["date"]
            # Support trailing 'Z' (UTC) which datetime.fromisoformat handles on 3.11+,
            # but normalise for safety across versions.
            normalised = date_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalised)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            epoch = int(dt.timestamp())
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": f"invalid request: {exc}"})
            return

        self._send(200, {"epoch": epoch})

    def _read_body(self):
        """Read the request body whether sent with Content-Length or chunked."""
        if "chunked" in self.headers.get("Transfer-Encoding", "").lower():
            data = b""
            while True:
                size_line = self.rfile.readline().strip()
                if not size_line:
                    continue
                size = int(size_line.split(b";")[0], 16)
                if size == 0:
                    self.rfile.readline()  # consume trailing CRLF
                    break
                data += self.rfile.read(size)
                self.rfile.readline()  # consume CRLF after each chunk
            return data
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # quieter logs
        pass


if __name__ == "__main__":
    print(f"Mock epoch service listening on http://localhost:{PORT}/epoch")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
