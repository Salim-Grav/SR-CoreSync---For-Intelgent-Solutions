import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPLACEMENTS = [
    ('محمد رائد عزيزة', 'محمد رائد كعكة'),
    ('أ. رائد عزيزة', 'أ. رائد كعكة'),
    ('رائد عزيزة', 'رائد كعكة'),
    ('Mohammad Raed Aziza', 'Mohammad Raed Kaakeh'),
    ('Mr. Mohammad Raed Aziza', 'Mr. Mohammad Raed Kaakeh'),
    ('Dhr. Mohammad Raed Aziza', 'Dhr. Mohammad Raed Kaakeh'),
    ('Hr. Mohammad Raed Aziza', 'Hr. Mohammad Raed Kaakeh'),
    ('Mr. Raed Aziza', 'Mr. Raed Kaakeh'),
    ('Dhr. Raed Aziza', 'Dhr. Raed Kaakeh'),
    ('Hr. Raed Aziza', 'Hr. Raed Kaakeh'),
    ('Raed Aziza', 'Raed Kaakeh'),
    ('Aziza', 'Kaakeh'),
    ('عزيزة', 'كعكة'),
]

modified_files = []

for root, dirs, files in os.walk(ROOT):
    # Skip hidden directories, venv, chrome profiles, node_modules, dist, etc.
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', '_site', '__pycache__', 'scratch']]
    
    for f in files:
        if f.endswith(('.html', '.js', '.json', '.py')):
            # Don't modify git log or this replacement script itself
            if f in ['replace_all_aziza.py', 'find_aziza.py']:
                continue
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
            except Exception:
                continue
                
            orig = content
            for old_str, new_str in REPLACEMENTS:
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    
            if content != orig:
                try:
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    rel_path = os.path.relpath(p, ROOT)
                    modified_files.append(rel_path)
                except Exception as e:
                    print(f"Error writing {p}: {e}")

print(f"Total modified files: {len(modified_files)}")
for mf in modified_files:
    print(f" - {mf}")
