# -*- coding: utf-8 -*-
with open('js/sr-software-apps.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate where the platform code was appended
marker = "// =============================================================\n    // PLATFORM 1: S&R CivicSync™ Simulator"
idx = content.find(marker)

if idx != -1:
    platform_code = content[idx:]
    base_content = content[:idx]

    # Find the closing })(); in base_content
    close_iife = base_content.rfind('})();')
    if close_iife != -1:
        new_content = base_content[:close_iife] + '\n\n    ' + platform_code.strip() + '\n\n})();\n'
        with open('js/sr-software-apps.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: Moved platform functions inside the IIFE!")
    else:
        print("ERROR: Could not find })(); in base content")
else:
    print("ERROR: Marker not found")
