with open('demo.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_str = '<script src="./js/sr-tech-radar.js"></script>\n</body></html>`;'
good_str = '</body></html>`;'

if bad_str in text:
    text = text.replace(bad_str, good_str, 1)
    print('Cleaned up accidental template literal insertion!')
else:
    print('Warning: bad_str not found!')

last_body_idx = text.rfind('</body>')
if last_body_idx != -1:
    text = text[:last_body_idx] + '<script src="./js/sr-tech-radar.js"></script>\n' + text[last_body_idx:]
    print('Inserted sr-tech-radar.js right before the real </body>!')

with open('demo.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done fixing demo.html!')
