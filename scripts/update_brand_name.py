# -*- coding: utf-8 -*-
"""
Update all company name occurrences to:
S&R CoreSync For Intelligent Solutions
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ordered replacements: longest first so specific variants are matched before generic ones
REPLACEMENTS = [
    # Full engineering variants
    ("S&amp;R CoreSync Solutions &amp; Engineering", "S&amp;R CoreSync For Intelligent Solutions"),
    ("S&amp;R CORESYNC SOLUTIONS &amp; ENGINEERING", "S&amp;R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    ("S&R CoreSync Solutions & Engineering", "S&R CoreSync For Intelligent Solutions"),
    ("S&R CORESYNC SOLUTIONS & ENGINEERING", "S&R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    
    # B.V. variants
    ("S&amp;R CoreSync Solutions B.V.", "S&amp;R CoreSync For Intelligent Solutions"),
    ("S&amp;R CORESYNC SOLUTIONS B.V.", "S&amp;R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    ("S&R CoreSync Solutions B.V.", "S&R CoreSync For Intelligent Solutions"),
    ("S&R CoreSync Solutions B. V.", "S&R CoreSync For Intelligent Solutions"),
    ("S&R CORESYNC SOLUTIONS B.V.", "S&R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    ("S&R CORESYNC SOLUTIONS B. V.", "S&R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    
    # Trademark variants
    ("S&amp;R CoreSync™ Solutions", "S&amp;R CoreSync For Intelligent Solutions"),
    ("S&amp;R CORESYNC™ SOLUTIONS", "S&amp;R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    ("S&R CoreSync™ Solutions", "S&R CoreSync For Intelligent Solutions"),
    ("S&R CORESYNC™ SOLUTIONS", "S&R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    
    # General uppercase
    ("S&amp;R CORESYNC SOLUTIONS", "S&amp;R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    ("S&R CORESYNC SOLUTIONS", "S&R CORESYNC FOR INTELLIGENT SOLUTIONS"),
    
    # General variants
    ("S&amp;R CoreSync Solutions", "S&amp;R CoreSync For Intelligent Solutions"),
    ("S&R CoreSync Solutions", "S&R CoreSync For Intelligent Solutions"),
]

changed_files = 0
total_replacements = 0

EXCLUDE_DIRS = {'.git', '_site', 'node_modules', '.tempmediaStorage', '.system_generated', 'archive'}

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if f.endswith(('.html', '.js', '.mjs', '.json', '.md', '.py', '.txt', '.xml')):
            # Don't touch this updater script or git logs
            if f in ('update_brand_name.py', 'scan_brand_replacements.py', 'audit_brand_names.py'):
                continue
            fp = os.path.join(dirpath, f)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    orig = fh.read()
            except Exception:
                continue

            updated = orig
            file_subs = 0
            for old_text, new_text in REPLACEMENTS:
                if old_text in updated:
                    cnt = updated.count(old_text)
                    updated = updated.replace(old_text, new_text)
                    file_subs += cnt

            if file_subs > 0:
                with open(fp, 'w', encoding='utf-8', newline='') as fh:
                    fh.write(updated)
                changed_files += 1
                total_replacements += file_subs
                rel = os.path.relpath(fp, ROOT)
                print(f"[UPDATED] {file_subs:3d} replacements in {rel}")

print("=" * 60)
print(f"DONE: {total_replacements} replacements across {changed_files} files.")
print("=" * 60)
