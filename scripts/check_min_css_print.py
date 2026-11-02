with open('css/enterprise-suite.min.css', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('#srBlueprintPreviewModal')
while idx != -1:
    print("Found at", idx)
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print('='*50)
    idx = text.find('#srBlueprintPreviewModal', idx+1)

