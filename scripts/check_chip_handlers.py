import glob

for p in glob.glob('*/index.html'):
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'fillHeroPromptSample' in c:
        has_script = 'sr-inline-13eaa28e.js' in c
        print(f"{p}: has chip call, loads 13eaa28e: {has_script}")
