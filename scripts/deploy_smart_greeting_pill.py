import re
import glob
import os

# 1. Update js/sr-geo-lang.js
with open('js/sr-geo-lang.js', 'r', encoding='utf-8') as f:
    geo_code = f.read()

# Replace the noredirect check that was suppressing the polite banner
old_check = 'try{if("1"===new URLSearchParams(window.location.search).get("noredirect"))return}catch(e){}'
new_check = '/* Allow greeting pill even when noredirect=1 is present, as it is non-intrusive */'

if old_check in geo_code:
    geo_code = geo_code.replace(old_check, new_check)
    print("SUCCESS: Removed aggressive noredirect suppression from sr-geo-lang.js")
else:
    print("Notice: old_check not found exactly in sr-geo-lang.js, checking alternate...")
    geo_code = re.sub(r'if\s*\(\s*["\']1["\']\s*===\s*new\s*URLSearchParams\([^)]*\)\.get\(["\']noredirect["\']\)\s*\)\s*return\s*;?', '', geo_code)

# Add test_lang support in language detection
old_detector = 'const i=function(){try{const e=navigator.languages'
new_detector = """const i=function(){try{
    const urlParams = new URLSearchParams(window.location.search);
    const testLang = urlParams.get('test_lang') || urlParams.get('testlang');
    if (testLang && a[testLang.toLowerCase()]) return testLang.toLowerCase();
    const e=navigator.languages"""

if old_detector in geo_code:
    geo_code = geo_code.replace(old_detector, new_detector)
    print("SUCCESS: Added ?test_lang= URL testing support to sr-geo-lang.js")
else:
    print("Notice: old_detector not matched exactly")

with open('js/sr-geo-lang.js', 'w', encoding='utf-8') as f:
    f.write(geo_code)

# 2. Add sr-geo-lang.js to demo.html and all localized */demo.html files
with open('demo.html', 'r', encoding='utf-8') as f:
    demo_html = f.read()

if 'sr-geo-lang.js' not in demo_html:
    demo_html = demo_html.replace(
        '<script src="./js/sr-events.js"></script>',
        '<script src="./js/sr-events.js"></script>\n    <script src="./js/sr-geo-lang.js" defer></script>'
    )
    with open('demo.html', 'w', encoding='utf-8') as f:
        f.write(demo_html)
    print("SUCCESS: Injected sr-geo-lang.js into demo.html")
else:
    print("sr-geo-lang.js already in demo.html")

# All localized subfolders
localized_demos = glob.glob('*/demo.html')
updated_count = 0
for d in localized_demos:
    if '_site' in d: continue
    with open(d, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'sr-geo-lang.js' not in content:
        content = content.replace(
            '<script src="../js/sr-events.js"></script>',
            '<script src="../js/sr-events.js"></script>\n    <script src="../js/sr-geo-lang.js" defer></script>'
        )
        with open(d, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"SUCCESS: Injected sr-geo-lang.js into {updated_count} localized demo.html pages!")
