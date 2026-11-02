import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('srBlueprintPreviewModal')
while idx != -1:
    print('FOUND IN JS AT', idx)
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print('='*50)
    idx = text.find('srBlueprintPreviewModal', idx+1)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
if 'srBlueprintPreviewModal' in html:
    print('FOUND IN index.html!')
else:
    print('NOT in index.html (created dynamically)')
