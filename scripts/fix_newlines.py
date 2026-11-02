with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    cnt = f.read()

cnt = cnt.replace('`;\\n    const clientWaUrl', '`;\n    const clientWaUrl')
cnt = cnt.replace('`;\\n    const mailtoUrl', '`;\n    const mailtoUrl')

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    f.write(cnt)

print("Fixed literal newline escapes.")

