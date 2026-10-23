import io, os, re
pat = re.compile(r'onsubmit="submitContactForm\(event\)"(?!\s)[^>]*?(?=data-success-msg=)')
hits = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "_site", "node_modules")]
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(root, f)
            c = io.open(p, encoding="utf-8", errors="ignore").read()
            m = pat.search(c)
            if m:
                hits.append((p, m.group(0)[:80]))
print("files with stray text after onsubmit:", len(hits))
for p, s in hits[:40]:
    print(p, "->", s)
