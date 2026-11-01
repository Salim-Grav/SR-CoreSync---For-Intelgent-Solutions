import io, re

with io.open('ckb/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

issues = []
for i, line in enumerate(lines):
    # Check for bare assets/ (not preceded by ../ or / or ./)
    matches = re.findall(r'(?<!\.\.)(?<!\.)(?<!\/)(?<!http:\/\/)(?<!https:\/\/)assets\/[a-zA-Z0-9_\-\.]+', line)
    # Also ignore domains like sr-coresync.com/assets/
    real_matches = [m for m in matches if 'sr-coresync.com/' + m not in line]
    if real_matches:
        issues.append((i + 1, real_matches, line.strip()))

print(f"Total issue lines: {len(issues)}")
for line_no, m, line in issues:
    print(f"Line {line_no}: {m} => {line[:100]}")
