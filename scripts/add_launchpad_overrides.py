with open('css/demo-portal.css', 'r', encoding='utf-8') as f:
    demo_css = f.read()

robust_overrides = """
/* Robust Sovereign Launchpad Link & Card Protections */
.apple-launchpad-card,
.apple-launchpad-card:link,
.apple-launchpad-card:visited,
.apple-launchpad-card:hover,
.apple-launchpad-card:active {
    color: inherit !important;
    text-decoration: none !important;
}

.apple-launchpad-native {
    color: #f8fafc !important;
    font-weight: 700 !important;
    text-decoration: none !important;
}

.apple-launchpad-sub {
    color: #94a3b8 !important;
    text-decoration: none !important;
}

.apple-launchpad-vat {
    color: #c5a880 !important;
    text-decoration: none !important;
}
"""

if '/* Robust Sovereign Launchpad Link & Card Protections */' not in demo_css:
    demo_css += robust_overrides
    with open('css/demo-portal.css', 'w', encoding='utf-8') as f:
        f.write(demo_css)
    print("SUCCESS: Added robust link protections to demo-portal.css")
