#!/usr/bin/env python3
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

audit_secrets.py
Audit tracked or staged repository files for credentials, private keys,
and proprietary secret exposure. Fails with non-zero exit code if any secret is found.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Force UTF-8 output on Windows consoles to prevent cp1252 errors
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# High-confidence secret detection patterns
SECRET_PATTERNS = [
    (r"-----BEGIN (?:RSA|DSA|EC|OPENSSH|PGP|ENCRYPTED|PRIVATE) KEY-----", "Private Key Header"),
    (r"\b(?:sk|rk)_live_[0-9a-zA-Z]{24,}\b", "Stripe Live Secret Key"),
    (r"\bghp_[0-9a-zA-Z]{36}\b", "GitHub Personal Access Token"),
    (r"\bgithub_pat_[0-9a-zA-Z_]{82}\b", "GitHub Fine-Grained Personal Access Token"),
    (r"\bAIza[0-9A-Za-z\-_]{35}\b", "Google Cloud / Firebase API Key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS Access Key ID"),
    (r"\bxox[baprs]-[0-9a-zA-Z]{10,48}\b", "Slack Token"),
    (r"\b(?:postgres|mysql|mongodb(?:\+srv)?):\/\/(?!demo|example|user:pass)[a-zA-Z0-9_\-\.]+:(?!(?:xxx|\*+|password|REDACTED|ENTER_))[a-zA-Z0-9_\-\.@!#%]+@(?!localhost|example\.com|.*\.internal)[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}(?::\d+)?\/[^\s\"']+", "Real Database Connection String with Credentials"),
    (r"(?:api[_-]?secret|jwt[_-]?secret|private[_-]?token)[\s:=]+['\"][a-zA-Z0-9_\-\.]{32,}['\"]", "Generic High-Entropy Secret Assignment"),
]


# Files explicitly forbidden from git tracking
FORBIDDEN_TRACKED_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_ed25519",
    "master.key",
}

# Directories and paths excluded from file-level inspection
EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".secrets",
    ".zwork",
    "dist",
    "_site",
}

ALLOWED_EXTENSIONS = {
    ".html", ".js", ".mjs", ".css", ".py", ".sh", ".bat", ".ps1",
    ".json", ".xml", ".txt", ".md", ".yml", ".yaml", ".conf",
}


def get_target_files(staged_only=False):
    """Returns list of relative file paths to inspect."""
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged_only else ["git", "ls-files"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        files = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        return files
    except Exception as e:
        print(f"Warning: git command failed ({e}), falling back to filesystem walk.")
        target_files = []
        for root, dirs, fnames in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for fname in fnames:
                p = os.path.relpath(os.path.join(root, fname), ".")
                target_files.append(p.replace("\\", "/"))
        return target_files


def audit_file(filepath: str):
    """Scans a single file for exposed secrets."""
    path_obj = Path(filepath)
    fname = path_obj.name.lower()

    # 1. Check forbidden file names
    if fname in FORBIDDEN_TRACKED_NAMES or (fname.startswith(".env.") and not fname.endswith((".example", ".vault"))):
        return [f"Forbidden secret file tracked in Git: '{filepath}'"]

    # Skip files not in allowed extensions
    if path_obj.suffix.lower() not in ALLOWED_EXTENSIONS and not fname.startswith("."):
        return []

    # Skip example / documentation templates explicitly demonstrating dummy formats
    if fname in {"audit_secrets.py", ".env.example"} or "mock" in fname:
        return []

    issues = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                for pattern, desc in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        # Mask snippet for safety
                        masked = re.sub(pattern, "[*** REDACTED SECRET ***]", line.strip())
                        issues.append(f"Line {line_no}: Exposed {desc} -> {masked}")
    except Exception as err:
        issues.append(f"Could not read file: {err}")

    return issues


def main():
    staged_mode = "--staged" in sys.argv
    mode_label = "Staged Git Index" if staged_mode else "All Tracked Repository Files"
    print(f"==========================================================================")
    print(f"S&R CoreSync Sovereign Secret Scanner - {mode_label}")
    print(f"==========================================================================")

    files = get_target_files(staged_only=staged_mode)
    print(f"Scanning {len(files)} file(s) for credentials, private keys, and API tokens...")

    total_violations = 0
    scanned_count = 0

    for fpath in files:
        if not os.path.exists(fpath):
            continue
        scanned_count += 1
        violations = audit_file(fpath)
        if violations:
            total_violations += len(violations)
            print(f"\n[!] VIOLATION in: {fpath}")
            for v in violations:
                print(f"    - {v}")

    print(f"--------------------------------------------------------------------------")
    if total_violations > 0:
        print(f"FAILED: Found {total_violations} secret exposure violation(s) across tracked files.")
        print(f"Aborting to prevent proprietary credential leakage.")
        sys.exit(1)
    else:
        print(f"PASSED: Clean scan! 0 secrets, 0 private keys, 0 credentials found in {scanned_count} files.")
        sys.exit(0)


if __name__ == "__main__":
    main()
