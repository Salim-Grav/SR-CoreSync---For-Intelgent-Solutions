import re

with open('demo.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', text)
print("demo.html scripts:", scripts)

with open('de/demo.html', 'r', encoding='utf-8') as f:
    text_de = f.read()

scripts_de = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', text_de)
print("de/demo.html scripts:", scripts_de)
