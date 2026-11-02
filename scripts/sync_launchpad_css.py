import sys

with open('css/enterprise-suite.css', 'r', encoding='utf-8') as f:
    suite_css = f.read()

start_marker = '.apple-launchpad-overlay{'
end_marker = '.apple-launchpad-card.hidden{display:none !important;}'

start_idx = suite_css.find(start_marker)
end_idx = suite_css.find(end_marker) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    launchpad_css = suite_css[start_idx:end_idx]
    
    # Also find media queries for launchpad
    mq_marker = '@media (max-width:768px){.apple-launchpad-grid{'
    mq_end = suite_css.find('}}', suite_css.find(mq_marker)) + 2
    if suite_css.find(mq_marker) != -1:
        launchpad_css += "\n" + suite_css[suite_css.find(mq_marker):mq_end]
        
    print(f"Extracted {len(launchpad_css)} bytes of Apple Launchpad CSS.")
    
    with open('css/demo-portal.css', 'r', encoding='utf-8') as f:
        demo_css = f.read()
        
    if '.apple-launchpad-overlay' not in demo_css:
        demo_css += "\n\n/* ==========================================================================\n"
        demo_css += "   Apple Dock Sovereign Launchpad System (28 Sovereign Languages Grid)\n"
        demo_css += "   ========================================================================== */\n"
        demo_css += launchpad_css + "\n"
        
        with open('css/demo-portal.css', 'w', encoding='utf-8') as f:
            f.write(demo_css)
        print("SUCCESS: Appended Apple Launchpad CSS to css/demo-portal.css!")
    else:
        print("Already present in css/demo-portal.css")
else:
    print("ERROR: Markers not found in enterprise-suite.css")
