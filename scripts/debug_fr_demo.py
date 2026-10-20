import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('fr/demo.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in fr/demo.html: {len(lines)}")

# 1. Search for conflict markers
for idx, line in enumerate(lines):
    if line.startswith('<<<<<<<') or line.startswith('=======') or line.startswith('>>>>>>>'):
        print(f"Conflict marker on line {idx+1}: {line.strip()}")

# 2. Check lines around 880-890
print("\n--- Lines 878-888 ---")
for idx in range(877, min(888, len(lines))):
    print(f"{idx+1}: {lines[idx].rstrip()}")

# 3. Check lines around 1740-1755
print("\n--- Lines 1743-1752 ---")
for idx in range(1742, min(1752, len(lines))):
    print(f"{idx+1}: {lines[idx].rstrip()}")

# 4. Check lines around 2605-2615
print("\n--- Lines 2608-2615 ---")
for idx in range(2607, min(2615, len(lines))):
    print(f"{idx+1}: {lines[idx].rstrip()}")
