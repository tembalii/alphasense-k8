import os, sys, json
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIG_PATH = os.getenv("CONFIG_PATH", "/etc/myapp/config.yaml")
PORT = int(os.getenv("PORT", "5000"))

# Hard fail if the config file isn't there (simulates the real app dependency)
if not os.path.exists(CONFIG_PATH):
    print(f"[FATAL] Config file not found at {CONFIG_PATH}", flush=True)
    sys.exit(1)

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok", "config_path": CONFIG_PATH, "port": PORT})
        else:
            # Keep it simple; just confirm the server is up
            self._send_json({"message": "alphasense test app running", "config_present": True})

    # Quiet the default logs a bit
    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    print(f"[INFO] Starting HTTP server on 0.0.0.0:{PORT}", flush=True)
    print(f"[INFO] Using config at {CONFIG_PATH}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
