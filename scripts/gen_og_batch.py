#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_og_batch.py — Generate custom 1200x630 OG images for a list of pages.

Usage:
    python scripts/gen_og_batch.py page1.html page2.html ...
    python scripts/gen_og_batch.py --all-missing   # every *.html without og:image

Steps performed:
  1. Read each page's <title> (used as OG alt + image filename from slug).
  2. Write a temporary OG template HTML (Arabic RTL, S&R brand).
  3. Capture 1200x630 PNG via Edge headless.
  4. Convert to JPG (<250KB) with Pillow.
  5. Inject og:image / twitter:image / width/height/alt into the page.
  6. Print a summary. Commit + push remain manual.

Requires: Microsoft Edge (headless) and Pillow.
"""
import io, os, re, subprocess, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
TMP = os.path.join(os.environ.get("TEMP", r"C:\Users\msali\AppData\Local\Temp"), "opencode")
OGDIR = os.path.join(ROOT, "assets", "og")
os.makedirs(TMP, exist_ok=True)
os.makedirs(OGDIR, exist_ok=True)

BASE_TPL = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1200px; height: 630px; overflow: hidden; }
  body { font-family: 'Alexandria', 'Segoe UI', Tahoma, sans-serif; background: #05100c; color: #fff; position: relative; }
  .glow { position: absolute; inset: 0; background: radial-gradient(620px 380px at 88% 8%, rgba(197,168,128,0.22), transparent 70%), radial-gradient(700px 420px at 5% 100%, rgba(30,120,90,0.20), transparent 72%), linear-gradient(135deg, #040b09 0%, #08160f 55%, #040b09 100%); }
  .frame { position: absolute; inset: 26px; border: 1px solid rgba(197,168,128,0.35); border-radius: 22px; }
  .content { position: relative; height: 100%; padding: 66px 78px; display: flex; flex-direction: column; }
  .brand { display: flex; align-items: center; gap: 16px; }
  .brand img { width: 62px; height: 62px; object-fit: contain; }
  .brand .name { font-size: 26px; font-weight: 600; letter-spacing: 0.4px; }
  .brand .name b { color: #c5a880; font-weight: 800; }
  .brand .tag { margin-inline-start: auto; font-size: 15px; letter-spacing: 3px; color: #c5a880; border: 1px solid rgba(197,168,128,0.45); border-radius: 999px; padding: 7px 16px; font-weight: 600; }
  .body { margin-top: auto; margin-bottom: auto; }
  h1 { font-size: 52px; line-height: 1.32; font-weight: 800; letter-spacing: -0.5px; }
  h1 .gold { color: #c5a880; }
  .sub { margin-top: 22px; font-size: 24px; line-height: 1.6; color: #c3cfc9; font-weight: 400; }
  .foot { display: flex; align-items: center; gap: 14px; font-size: 18px; color: #9fb0a8; }
  .pill { background: rgba(197,168,128,0.14); color: #e4cfa9; border: 1px solid rgba(197,168,128,0.45); border-radius: 999px; padding: 8px 18px; font-weight: 600; font-size: 17px; }
  .dot { width: 6px; height: 6px; border-radius: 50%; background: #c5a880; opacity: 0.7; }
  .domain { margin-inline-start: auto; font-weight: 600; color: #c5a880; letter-spacing: 0.5px; }
</style>
</head>
<body>
  <div class="glow"></div>
  <div class="frame"></div>
  <div class="content">
    <div class="brand">
      <img src="file:///D:/I-Ai/App/S%26R%20CoreSync%20For%20Intelligent%20Solutions/Project/assets/sr-core-emblem-official.webp" alt="">
      <div class="name">S&amp;R <b>CoreSync</b></div>
      <div class="tag">INSIGHTS</div>
    </div>
    <div class="body">
      <h1>__H1__</h1>
      <div class="sub">__SUB__</div>
    </div>
    <div class="foot">
      <span class="pill">__PILL__</span>
      <span class="dot"></span>
      <span>sr-coresync.com</span>
      <span class="domain">2026</span>
    </div>
  </div>
</body>
</html>
"""

def slug_of(page):
    return os.path.splitext(os.path.basename(page))[0]

def title_of(html):
    m = re.search(r'<title>(.*?)</title>', html)
    if not m: return os.path.basename(page)
    t = m.group(1).split(' | ')[0].split(' - ')[0].strip()
    return t or os.path.basename(page)

def process(page):
    page = page.strip()
    if not os.path.isabs(page):
        page = os.path.join(ROOT, page)
    if not os.path.exists(page):
        print("SKIP (missing):", page); return
    html = io.open(page, encoding="utf-8").read()
    if "og:image" in html and "assets/og/" in html:
        print("SKIP (already has custom OG):", os.path.basename(page)); return
    slug = slug_of(page)
    title = title_of(html)
    imgname = "og-" + slug + ".jpg"
    imgurl = "https://sr-coresync.com/assets/og/" + imgname
    # template
    tpl = BASE_TPL.replace("__H1__", title).replace("__SUB__", "S&R CoreSync — " + title).replace("__PILL__", "S&R CoreSync")
    tplpath = os.path.join(TMP, "og-" + slug + ".html")
    io.open(tplpath, "w", encoding="utf-8", newline="\n").write(tpl)
    # capture
    pngpath = os.path.join(TMP, "og-" + slug + ".png")
    jpgpath = os.path.join(OGDIR, imgname)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--user-data-dir=" + os.path.join(TMP, "edgeprof"), "--window-size=1200,630",
                    "--virtual-time-budget=6000", "--screenshot=" + pngpath,
                    "file:///" + tplpath.replace("\\", "/")], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(pngpath):
        print("FAIL capture:", slug); return
    # convert
    try:
        from PIL import Image
        im = Image.open(pngpath).convert("RGB")
        for q in (88, 82, 76, 70):
            im.save(jpgpath, "JPEG", quality=q, optimize=True, progressive=True)
            if os.path.getsize(jpgpath) < 250*1024:
                break
    except ImportError:
        print("Pillow not installed; skipping convert"); return
    # inject meta
    alt = "S&R CoreSync — " + title
    newimg = imgurl
    block = (
        '    <meta property="og:type" content="website">\n'
        '    <meta property="og:site_name" content="S&amp;R CoreSync For Intelligent Solutions">\n'
        '    <meta property="og:title" content="' + title + '">\n'
        '    <meta property="og:url" content="https://sr-coresync.com/' + os.path.basename(page) + '">\n'
        '    <meta property="og:image" content="' + newimg + '">\n'
        '    <meta property="og:image:width" content="1200">\n'
        '    <meta property="og:image:height" content="630">\n'
        '    <meta property="og:image:alt" content="' + alt + '">\n'
        '    <meta name="twitter:card" content="summary_large_image">\n'
        '    <meta name="twitter:image" content="' + newimg + '">\n'
    )
    if "og:image" in html:
        html = re.sub(r'<meta property="og:image" content="[^"]*">',
                      '<meta property="og:image" content="' + newimg + '">\n    <meta property="og:image:width" content="1200">\n    <meta property="og:image:height" content="630">\n    <meta property="og:image:alt" content="' + alt + '">', html, count=1)
        if "twitter:image" in html:
            html = re.sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="' + newimg + '">', html, count=1)
        else:
            html = html.replace("</head>", '    <meta name="twitter:card" content="summary_large_image">\n    <meta name="twitter:image" content="' + newimg + '">\n</head>', 1)
    else:
        assert "</head>" in html
        html = html.replace("</head>", block + "</head>", 1)
    io.open(page, "w", encoding="utf-8", newline="\n").write(html)
    print("OK:", os.path.basename(page), "->", imgname, os.path.getsize(jpgpath), "bytes")

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: gen_og_batch.py page1.html [page2.html ...]  |  --all-missing")
        sys.exit(1)
    if args == ["--all-missing"]:
        pages = []
        for f in glob.glob(os.path.join(ROOT, "*.html")):
            s = io.open(f, encoding="utf-8", errors="ignore").read()
            if "og:image" not in s or "assets/og/" not in s:
                pages.append(os.path.relpath(f, ROOT))
    else:
        pages = args
    print("Processing", len(pages), "page(s)...")
    for p in pages:
        process(p)
    print("Done.")

if __name__ == "__main__":
    main()
