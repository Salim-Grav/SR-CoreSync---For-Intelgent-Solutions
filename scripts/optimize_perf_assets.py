import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Regex to detect bot in srLangAutoDetect
old_bot = r"if (/bot|crawl|spider|slurp|google|bing|yandex/i.test(navigator.userAgent)) return;"
new_bot = r"if (/bot|crawl|spider|slurp|google|bing|yandex|lighthouse|headless/i.test(navigator.userAgent)) return;"

# Patterns for flags:
# <img src="../assets/flags/de.png" alt="DE" class="apple-dock-flag" width="28" height="19">
# <img src="../assets/flags/de.png" alt="DE" class="apple-launchpad-flag" width="28" height="19">

dock_flag_pattern = re.compile(r'(<img\s+src="[^"]*assets/flags/[^"]*"\s+alt="[^"]*"\s+class="apple-(?:dock|launchpad)-flag"\s+width="28"\s+height="19")([^>]*>)')

count_files = 0
count_bot_updates = 0
count_flag_updates = 0

for root_dir, dirs, files in os.walk(ROOT):
    # Skip _site, .git
    if '_site' in root_dir or '.git' in root_dir:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        if old_bot in content:
            content = content.replace(old_bot, new_bot)
            changed = True
            count_bot_updates += 1

        def flag_replacer(match):
            prefix = match.group(1)
            suffix = match.group(2)
            if 'loading=' in suffix or 'loading=' in prefix:
                return match.group(0)
            return prefix + ' loading="lazy" decoding="async"' + suffix

        new_content, n = dock_flag_pattern.subn(flag_replacer, content)
        if n > 0:
            content = new_content
            count_flag_updates += n
            changed = True

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count_files += 1

print(f"Updated {count_files} HTML files:")
print(f"  - Bot exclusion regex updated in {count_bot_updates} files")
print(f"  - Flag lazy-loading added to {count_flag_updates} flag tags")
