import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

idx = cnt.find('id="pricing"')
if idx != -1:
    print(cnt[idx+1800:idx+3500])
