import glob

count = 0
for path in glob.glob('**/*.html', recursive=True):
    if '_site' in path:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        target = '            <span class="apple-dock-badge">28</span>\n            <span class="apple-dock-dot"></span>\n        </button>'
        repl = '            <span class="apple-dock-badge">28</span>\n        </button>'
        if target in c:
            c = c.replace(target, repl)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            count += 1
    except Exception as e:
        print(f"Error {path}: {e}")

print(f"Updated {count} HTML files.")
