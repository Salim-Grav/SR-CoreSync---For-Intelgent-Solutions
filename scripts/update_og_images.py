import os

count = 0
for root, dirs, files in os.walk('.'):
    if any(ex in root for ex in ['.git', '_site', 'node_modules', '.agents']):
        continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                content = fh.read()
            target_str = '<meta property="og:image" content="https://sr-coresync.com/assets/founder-banner-salim.jpg">'
            if target_str in content:
                content = content.replace(target_str, '<meta property="og:image" content="https://sr-coresync.com/assets/og-coresync-official.jpg">')
                content = content.replace('<meta property="og:image:secure_url" content="https://sr-coresync.com/assets/founder-banner-salim.jpg">', '<meta property="og:image:secure_url" content="https://sr-coresync.com/assets/og-coresync-official.jpg">')
                content = content.replace('<meta name="twitter:image" content="https://sr-coresync.com/assets/founder-banner-salim.jpg">', '<meta name="twitter:image" content="https://sr-coresync.com/assets/og-coresync-official.jpg">')
                content = content.replace('<meta property="og:image:width" content="1920">', '<meta property="og:image:width" content="1200">')
                content = content.replace('<meta property="og:image:height" content="1080">', '<meta property="og:image:height" content="628">')
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                count += 1

print(f'Successfully updated {count} HTML files to use og-coresync-official.jpg.')
