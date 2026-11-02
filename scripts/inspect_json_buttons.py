import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's check the JSON button in generateAiProjectBlueprint:
idx = text.find('downloadBlueprintArchitectureJson')
while idx != -1:
    print("Found at", idx)
    print(text[max(0, idx-100):min(len(text), idx+250)])
    print('='*50)
    idx = text.find('downloadBlueprintArchitectureJson', idx+1)
