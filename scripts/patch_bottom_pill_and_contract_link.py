import re

# 1. Update css/sr-geo-lang.css for Bottom-Floating Pill
with open('css/sr-geo-lang.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

old_banner_css = """.sr-geolang-banner {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100000;
    transform: translateY(-110%);
    opacity: 0;
    transition: transform 0.55s cubic-bezier(0.16, 1, 0.3, 1),
                opacity 0.4s ease;
    pointer-events: none;
    font-family: 'Alexandria', 'Plus Jakarta Sans', system-ui, sans-serif;
}

.sr-geolang-banner.visible {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
}

.sr-geolang-banner.hiding {
    transform: translateY(-110%);
    opacity: 0;
    pointer-events: none;
}

/* ── Inner Panel ── */
.sr-geolang-inner {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    padding: 12px 22px;
    background: var(--sr-geolang-bg);
    border-bottom: 1px solid var(--sr-geolang-border);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    backdrop-filter: blur(24px) saturate(180%);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.65),
                0 0 20px rgba(197, 168, 128, 0.08);
    flex-wrap: wrap;
}"""

new_banner_css = """.sr-geolang-banner {
    position: fixed;
    bottom: 24px;
    right: 24px;
    top: auto;
    left: auto;
    max-width: min(580px, calc(100vw - 40px));
    z-index: 100000;
    transform: translateY(130%) scale(0.96);
    opacity: 0;
    transition: transform 0.48s cubic-bezier(0.16, 1, 0.3, 1),
                opacity 0.35s ease;
    pointer-events: none;
    font-family: 'Alexandria', 'Plus Jakarta Sans', system-ui, sans-serif;
}

[dir="rtl"] .sr-geolang-banner,
html[dir="rtl"] .sr-geolang-banner {
    right: auto;
    left: 24px;
}

.sr-geolang-banner.visible {
    transform: translateY(0) scale(1);
    opacity: 1;
    pointer-events: auto;
}

.sr-geolang-banner.hiding {
    transform: translateY(130%) scale(0.96);
    opacity: 0;
    pointer-events: none;
}

/* ── Luxury Bottom Floating Pill ── */
.sr-geolang-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 10px 18px;
    background: rgba(7, 16, 12, 0.94);
    border: 1px solid rgba(197, 168, 128, 0.45);
    border-radius: 999px;
    -webkit-backdrop-filter: blur(28px) saturate(190%);
    backdrop-filter: blur(28px) saturate(190%);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.75),
                0 0 25px rgba(197, 168, 128, 0.18),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
    flex-wrap: nowrap;
}

@media (max-width: 640px) {
    .sr-geolang-banner {
        bottom: 84px;
        left: 12px !important;
        right: 12px !important;
        max-width: calc(100vw - 24px);
    }
    .sr-geolang-inner {
        border-radius: 16px;
        padding: 12px 14px;
        flex-wrap: wrap;
        justify-content: center;
    }
}"""

if old_banner_css in css_text:
    css_text = css_text.replace(old_banner_css, new_banner_css)
    with open('css/sr-geo-lang.css', 'w', encoding='utf-8') as f:
        f.write(css_text)
    print("SUCCESS: Updated css/sr-geo-lang.css with luxury bottom-floating pill!")
else:
    print("WARNING: old_banner_css not matched exactly, trying regex replace...")
    # fallback regex replace
    pattern = r'\.sr-geolang-banner\s*\{.*?/\* ── Inner Panel ── \*/\s*\.sr-geolang-inner\s*\{[^}]*\}'
    if re.search(pattern, css_text, re.DOTALL):
        css_text = re.sub(pattern, new_banner_css, css_text, flags=re.DOTALL)
        with open('css/sr-geo-lang.css', 'w', encoding='utf-8') as f:
            f.write(css_text)
        print("SUCCESS: Updated css/sr-geo-lang.css via regex!")
    else:
        print("ERROR: Could not patch css/sr-geo-lang.css")

# 2. Update js/sr-inline-13eaa28e.js to ensure contract link is prominent in clientWaMsg and emailBody
with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

old_link_block = "`https://sr-coresync.com/clgid-prototype.html\\n\\n` +"
new_link_block = "`https://sr-coresync.com/clgid-prototype.html\\n\\n` +\n        `📜 *رابط مراجعة واعتماد مسودة العقد الرسمي B2B (التوقيع المباشر):*\\n` +\n        `https://sr-coresync.com/clgid-contract.html\\n\\n` +"

if old_link_block in js_text:
    js_text = js_text.replace(old_link_block, new_link_block)
    print("SUCCESS: Embedded live contract link into clientWaMsg!")
else:
    print("Notice: old_link_block not matched in js_text")

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Patching completed.")
