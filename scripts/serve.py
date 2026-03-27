"""Minimal live-preview server for Typst CV.

Serves build/preview/ via HTTP and auto-reloads the browser when the SVG
changes.  Uses only the Python standard library + a tiny JS polling snippet.
"""

from __future__ import annotations

import http.server
import os
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"
PREVIEW_DIR = BUILD_DIR / "preview"
SVG_FILE = PREVIEW_DIR / "resume.svg"


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CV Preview</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #e0e0e0; display: flex; flex-direction: column;
         align-items: center; padding: 24px 0; gap: 24px; min-height: 100vh; }
  .page { background: #fff; box-shadow: 0 2px 12px rgba(0,0,0,.15);
          width: 210mm; min-height: 297mm; }
  .page img { width: 100%%; display: block; }
</style>
</head>
<body>
<script>
// Discover pages and render them; poll for changes every 500ms
let lastModified = "";
async function loadPages() {
  const body = document.body;
  body.querySelectorAll(".page").forEach(el => el.remove());
  for (let i = 1; i <= 20; i++) {
    const url = `resume-${i}.svg`;
    const r = await fetch(url, { method: "HEAD", cache: "no-store" });
    if (!r.ok) break;
    const div = document.createElement("div");
    div.className = "page";
    const img = document.createElement("img");
    img.src = url + "?t=" + Date.now();
    img.alt = `Page ${i}`;
    div.appendChild(img);
    body.appendChild(div);
  }
}
loadPages();
setInterval(async () => {
  try {
    const r = await fetch("resume-1.svg", { method: "HEAD", cache: "no-store" });
    const lm = r.headers.get("last-modified") || "";
    if (lastModified && lm !== lastModified) { loadPages(); }
    lastModified = lm;
  } catch {}
}, 500);
</script>
</body>
</html>
"""


def ensure_preview_dir() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    index = PREVIEW_DIR / "index.html"
    index.write_text(HTML_TEMPLATE, encoding="utf-8")


def start_http_server(port: int) -> http.server.HTTPServer:
    os.chdir(PREVIEW_DIR)

    handler = http.server.SimpleHTTPRequestHandler

    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Live-preview CV in browser.")
    parser.add_argument(
        "--port", type=int, default=8787, help="HTTP port (default: 8787)"
    )
    parser.add_argument(
        "--no-open", action="store_true", help="Don't auto-open browser"
    )
    args = parser.parse_args()

    ensure_preview_dir()

    print(f"Starting HTTP server on http://127.0.0.1:{args.port}")
    start_http_server(args.port)

    if not args.no_open:
        webbrowser.open(f"http://127.0.0.1:{args.port}")

    # Keep alive — Ctrl-C to stop
    print("Press Ctrl-C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
