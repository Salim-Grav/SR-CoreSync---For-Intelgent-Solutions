with open('js/sr-geo-lang.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of sr-geo-lang.js:", len(text))
# Let's search for function i() which is the main entry point
idx = text.find('function i()')
if idx != -1:
    print(text[idx:idx+1500])
