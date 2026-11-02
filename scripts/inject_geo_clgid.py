for p in ['clgid-prototype.html', 'clgid-contract.html']:
    with open(p, 'r', encoding='utf-8') as f:
        cnt = f.read()
    if 'sr-geo-lang.js' not in cnt:
        cnt = cnt.replace('</body>', '    <script src="./js/sr-geo-lang.js" defer></script>\n</body>')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(cnt)
        print(f"SUCCESS: Injected sr-geo-lang.js into {p}")
    else:
        print(f"sr-geo-lang.js already in {p}")

