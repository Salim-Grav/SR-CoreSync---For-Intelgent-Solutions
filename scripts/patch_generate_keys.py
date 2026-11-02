with open('scripts/generate_auth_keys.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'import sys\nfrom pathlib import Path'
if target in text:
    text = text.replace(target, 'import sys\nfrom pathlib import Path\nif hasattr(sys.stdout, "reconfigure"):\n    sys.stdout.reconfigure(encoding="utf-8")')
elif 'import sys\r\nfrom pathlib import Path' in text:
    text = text.replace('import sys\r\nfrom pathlib import Path', 'import sys\r\nfrom pathlib import Path\r\nif hasattr(sys.stdout, "reconfigure"):\r\n    sys.stdout.reconfigure(encoding="utf-8")')

with open('scripts/generate_auth_keys.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched generate_auth_keys.py successfully.')
