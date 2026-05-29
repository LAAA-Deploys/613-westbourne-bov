# -*- coding: utf-8 -*-
"""Render index.html to PDF (honoring @media print) and a 1200x630 preview.png cover.
Uses the system Chrome via Playwright. Serves the repo over localhost so relative
asset paths (images/) resolve. Maps are hidden in print, so map tiles are not needed.
"""
import http.server, socketserver, threading, functools, os, sys

ROOT = r"C:\Users\gscher\613-westbourne-bov"
PORT = 8731
os.chdir(ROOT)

Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
httpd.allow_reuse_address = True
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()

URL = f"http://127.0.0.1:{PORT}/index.html"

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)

    # ---- PDF (print media) ----
    page = browser.new_page()
    page.goto(URL, wait_until="load", timeout=60000)
    try:
        page.wait_for_function("document.fonts.ready.then(()=>true)", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    page.emulate_media(media="print")
    page.pdf(
        path=os.path.join(ROOT, "613-westbourne-bov.pdf"),
        format="Letter",
        print_background=True,
        prefer_css_page_size=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    page.close()
    print("WROTE 613-westbourne-bov.pdf")

    # ---- preview.png (1200x630 OG card from the cover) ----
    pg2 = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    pg2.goto(URL, wait_until="load", timeout=60000)
    try:
        pg2.wait_for_function("document.fonts.ready.then(()=>true)", timeout=15000)
    except Exception:
        pass
    pg2.wait_for_timeout(1200)
    pg2.screenshot(path=os.path.join(ROOT, "preview.png"),
                   clip={"x": 0, "y": 0, "width": 1200, "height": 630})
    pg2.close()
    print("WROTE preview.png")

    browser.close()

httpd.shutdown()
print("done")
