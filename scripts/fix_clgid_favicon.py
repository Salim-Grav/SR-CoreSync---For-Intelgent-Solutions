with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

cnt = cnt.replace('assets/favicon.ico', 'assets/favicon-96.png')

with open('clgid-prototype.html', 'w', encoding='utf-8') as f:
    f.write(cnt)

print("Updated favicon in clgid-prototype.html")

