import re

with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

pattern = r'<script>\s*function publishClgidArticle.*?</script>'
if re.search(pattern, cnt, re.DOTALL):
    cnt = re.sub(pattern, '<script src="./js/clgid-prototype.js" defer></script>', cnt, flags=re.DOTALL)
    with open('clgid-prototype.html', 'w', encoding='utf-8') as f:
        f.write(cnt)
    print('SUCCESS: Replaced inline script with external script tag.')
else:
    print('Pattern not matched!')

