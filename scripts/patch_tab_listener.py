with open('js/smart-business-advisor.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = "if (tabBtns.voice) { tabBtns.voice.addEventListener('click', function () { switchTab('voice'); }); }"
replacement = target + "\n    if (tabBtns.engine) { tabBtns.engine.addEventListener('click', function () { switchTab('engine'); }); }"

if target in text:
    text = text.replace(target, replacement, 1)
    with open('js/smart-business-advisor.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully added tabBtns.engine event listener.')
else:
    print('Target not found.')
