#!/usr/bin/env python3
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================

install_git_hooks.py
Configures Git to use .githooks directory for local commit safety checks.
"""

import os
import subprocess
import sys


def main():
    print("==========================================================================")
    print("S&R CoreSync - Installing Sovereign Git Hooks")
    print("==========================================================================")
    
    hook_dir = os.path.abspath(".githooks")
    if not os.path.exists(hook_dir):
        print(f"Error: .githooks directory not found at {hook_dir}")
        sys.exit(1)
        
    try:
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True)
        print("Successfully set Git core.hooksPath -> .githooks")
        print("Pre-commit secret audit is now permanently active on local commits.")
    except Exception as e:
        print(f"Failed to set git config: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
