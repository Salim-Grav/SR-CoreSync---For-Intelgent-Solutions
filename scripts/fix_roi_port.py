#!/usr/bin/env python3
"""Replace the over-broad ROI block that was ported into the language pages.

The first port attempt copied a 21 KB slice (LuxuryAudio + founder cinema +
ROI) into every language page, which redeclared `const LuxuryAudio` and broke
the page with "Identifier 'LuxuryAudio' has already been declared".

This script removes that slice and inserts only the self-contained ROI
functions, extracted by exact line marks from the Arabic master page.
"""
import io
import os
import re
import sys

ROOT = "."
MASTER = os.path.join(ROOT, "index.html")


def read(path):
    return io.open(path, encoding="utf-8", errors="ignore").read()


def write(path, text):
    io.open(path, "w", encoding="utf-8", newline="").write(text)


master = read(MASTER)

start_mark = "        function setRoiTeamPreset(size) {"
end_mark = "        window.setRoiTeamPreset = setRoiTeamPreset;"

start = master.find(start_mark)
end = master.find(end_mark, start)
if start < 0 or end < 0:
    sys.exit("ROI function block not found in master page")
end += len(end_mark)

clean_block = master[start:end]
print("clean ROI block: %d chars" % len(clean_block))

bad_start_re = re.compile(r"[ \t]*// =+\s*\n[ \t]*//\s*مؤثرات صوتية فاخرة")
bad_end = "        window.setRoiTeamPreset = setRoiTeamPreset;"

langs = [
    d for d in sorted(os.listdir(ROOT))
    if os.path.isdir(os.path.join(ROOT, d))
    and re.match(r"^[a-z]{2}$", d)
    and os.path.isfile(os.path.join(ROOT, d, "index.html"))
]

changed = 0
for lang in langs:
    path = os.path.join(ROOT, lang, "index.html")
    html = read(path)
    original = html

    m = bad_start_re.search(html)
    if m:
        e = html.find(bad_end, m.start())
        if e < 0:
            m = None
        else:
            e += len(bad_end)
            html = html[:m.start()] + clean_block + html[e:]

    if "function updateROICalculator" not in html:
        anchor = "    </script>\n</body>"
        if anchor in html:
            html = html.replace(anchor, clean_block + "\n" + anchor, 1)
        else:
            html = html.replace("</body>", "<script>\n" + clean_block + "\n</script>\n</body>", 1)

    if html != original:
        write(path, html)
        changed += 1
        print("fixed", lang)

print("pages changed:", changed)
