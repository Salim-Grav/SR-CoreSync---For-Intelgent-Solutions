#!/usr/bin/env python3
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

apply_license_headers.py
Applies the official S&R CoreSync Proprietary & Confidential IP header
across source files (JS, CSS, Python, SDK, Workers, and Shell scripts).
"""

import os
import sys
from pathlib import Path

# Force UTF-8 on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HEADER_JS_CSS = """/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */
"""

HEADER_PY = '''"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""
'''

HEADER_SH = """# ==============================================================================
# S&R CoreSync For Intelligent Solutions - Sovereign Platform
# PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
# 
# Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
# Unauthorized copying, decompilation, redistribution, or external model training
# of this file, via any medium, is strictly prohibited.
# ==============================================================================
"""

SEARCH_DIRS = ["js", "css", "scripts", "workers", "sdk"]
EXCLUDE_DIRS = {"node_modules", ".git", "__pycache__", "dist", "_site", ".secrets"}
MARKER = "PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY"


def apply_header(filepath: str) -> bool:
    """Applies header to a single file if not already present."""
    p = Path(filepath)
    ext = p.suffix.lower()

    if ext not in {".js", ".mjs", ".css", ".py", ".sh"}:
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    if MARKER in content:
        return False  # Already stamped

    # Select appropriate header
    if ext in {".js", ".mjs", ".css"}:
        header = HEADER_JS_CSS
    elif ext == ".py":
        header = HEADER_PY
    elif ext == ".sh":
        header = HEADER_SH
    else:
        return False

    # Handle shebangs or encoding declarations
    lines = content.splitlines(keepends=True)
    insert_idx = 0

    if lines and (lines[0].startswith("#!") or "coding:" in lines[0]):
        insert_idx = 1
        if len(lines) > 1 and "coding:" in lines[1]:
            insert_idx = 2

    # Reconstruct
    new_content = "".join(lines[:insert_idx]) + header + "\n" + "".join(lines[insert_idx:])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True


def main():
    check_only = "--check" in sys.argv
    print("==========================================================================")
    print("S&R CoreSync - Proprietary Software License Header Engine")
    print(f"Mode: {'Audit Check' if check_only else 'Apply & Update'}")
    print("==========================================================================")

    total_scanned = 0
    updated_files = []
    missing_files = []

    for root_dir in SEARCH_DIRS:
        if not os.path.exists(root_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                ext = Path(fpath).suffix.lower()
                if ext in {".js", ".mjs", ".css", ".py", ".sh"}:
                    total_scanned += 1
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        txt = f.read()
                    if MARKER not in txt:
                        missing_files.append(fpath)
                        if not check_only:
                            if apply_header(fpath):
                                updated_files.append(fpath)

    print(f"Total source files scanned across {SEARCH_DIRS}: {total_scanned}")
    if check_only:
        if missing_files:
            print(f"FAILED: {len(missing_files)} file(s) missing proprietary header:")
            for m in missing_files:
                print(f"  - {m}")
            sys.exit(1)
        else:
            print("PASSED: 100% of scanned source files have the official proprietary header.")
            sys.exit(0)
    else:
        print(f"Successfully applied proprietary license header to {len(updated_files)} file(s).")
        print(f"Already compliant: {total_scanned - len(missing_files)} file(s).")
        print("Status: 100% compliant.")


if __name__ == "__main__":
    main()
