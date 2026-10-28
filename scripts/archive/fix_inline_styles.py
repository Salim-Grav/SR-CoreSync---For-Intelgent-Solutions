"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Script to eliminate all inline CSS styles flagged by the IDE linter
in card.html, corporate-profile.html, preview-founders-showcase.html,
index.html, en/index.html, and nl/index.html.
"""

import os
import re

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync Solutions\Project"

def fix_card():
    path = os.path.join(PROJECT_DIR, "card.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS rule to <style>
    css_target = ".nfc-qr-lightbox-img {"
    css_addition = """        .nfc-qr-lightbox-box .nfc-save-btn {
            padding: 10px 18px;
            font-size: 0.88rem;
        }

        .nfc-qr-lightbox-img {"""

    if css_target in content and ".nfc-qr-lightbox-box .nfc-save-btn" not in content:
        content = content.replace(css_target, css_addition, 1)

    # 2. Remove inline style on qrLightboxDl
    old_link = '<a id="qrLightboxDl" href="./assets/qr-founder-salim.png" download="QR-Code.png" class="nfc-save-btn" style="padding: 10px 18px; font-size: 0.88rem;">'
    new_link = '<a id="qrLightboxDl" href="./assets/qr-founder-salim.png" download="QR-Code.png" class="nfc-save-btn">'
    if old_link in content:
        content = content.replace(old_link, new_link, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("card.html fixed!")

def fix_corporate_profile():
    path = os.path.join(PROJECT_DIR, "corporate-profile.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Ensure .page-footer has width: 100% in CSS
    old_footer_css = """.page-footer {
            margin-top: 15px;"""
    new_footer_css = """.page-footer {
            width: 100%;
            margin-top: 15px;"""
    if old_footer_css in content:
        content = content.replace(old_footer_css, new_footer_css, 1)

    # 2. Add .profile-qr-title in CSS
    old_qr_dossier_css = """.qr-dossier-grid {"""
    new_qr_dossier_css = """.profile-qr-title {
            font-size: 1.15rem;
            font-weight: 800;
            color: #ffffff;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        .qr-dossier-grid {"""
    if old_qr_dossier_css in content and ".profile-qr-title" not in content:
        content = content.replace(old_qr_dossier_css, new_qr_dossier_css, 1)

    # 3. Remove inline style on line 441
    old_footer_tag = '<div class="page-footer" style="width: 100%;">'
    new_footer_tag = '<div class="page-footer">'
    if old_footer_tag in content:
        content = content.replace(old_footer_tag, new_footer_tag)

    # 4. Remove inline style on line 546
    old_h3_tag = '<h3 style="font-size: 1.15rem; font-weight: 800; color: #fff; margin-top: 25px; margin-bottom: 10px;">'
    new_h3_tag = '<h3 class="profile-qr-title">'
    if old_h3_tag in content:
        content = content.replace(old_h3_tag, new_h3_tag)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("corporate-profile.html fixed!")

def fix_html_showcase_file(filename):
    path = os.path.join(PROJECT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add CSS helper classes to .showcase-footer-avatar
    css_target = ".showcase-footer-avatar {"
    css_addition = """.showcase-footer-avatar.avatar-crown {
            background: linear-gradient(135deg, #c5a880, #f3dfba);
            color: #050706;
            font-weight: 900;
        }

        .showcase-tab-btn-pdf {
            border-color: rgba(243, 223, 186, 0.6) !important;
            background: rgba(197, 168, 128, 0.15) !important;
            text-decoration: none !important;
        }

        .showcase-tab-btn-pdf .showcase-tab-dot {
            background: #f3dfba !important;
        }

        .showcase-tab-btn-nfc {
            border-color: rgba(16, 185, 129, 0.5) !important;
            background: rgba(16, 185, 129, 0.1) !important;
            text-decoration: none !important;
        }

        .showcase-tab-btn-nfc .showcase-tab-dot {
            background: #10b981 !important;
        }

        .live-dot.dot-gold {
            background: #c5a880 !important;
            box-shadow: 0 0 8px #c5a880 !important;
        }

        .live-dot.dot-cyan {
            background: #38bdf8 !important;
            box-shadow: 0 0 8px #38bdf8 !important;
        }

        .showcase-footer-avatar {"""

    if css_target in content and ".avatar-crown" not in content:
        content = content.replace(css_target, css_addition, 1)

    # 2. Replace avatar inline styles
    old_avatar = '<div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>'
    new_avatar = '<div class="showcase-footer-avatar avatar-crown">👑</div>'
    content = content.replace(old_avatar, new_avatar)

    # 3. Replace PDF and NFC tab buttons inline styles
    content = re.sub(
        r'<a href="([^"]*assets/SR-CoreSync-Corporate-Profile-2026\.pdf)" download="SR-CoreSync-Corporate-Profile-2026\.pdf" class="showcase-tab-btn"[^>]*title="([^"]*)">(\s*)<span class="showcase-tab-dot"[^>]*></span>(\s*)<span>([^<]*)</span>(\s*)</a>',
        r'<a href="\1" download="SR-CoreSync-Corporate-Profile-2026.pdf" class="showcase-tab-btn showcase-tab-btn-pdf" title="\2">\3<span class="showcase-tab-dot"></span>\4<span>\5</span>\6</a>',
        content
    )

    content = re.sub(
        r'<a href="([^"]*card\.html[^"]*)" target="_blank" class="showcase-tab-btn"[^>]*title="([^"]*)">(\s*)<span class="showcase-tab-dot"[^>]*></span>(\s*)<span>([^<]*)</span>(\s*)</a>',
        r'<a href="\1" target="_blank" class="showcase-tab-btn showcase-tab-btn-nfc" title="\2">\3<span class="showcase-tab-dot"></span>\4<span>\5</span>\6</a>',
        content
    )

    # 4. Replace liveBadge inline styles if present
    content = content.replace(
        '<span class="live-dot" style="background:#c5a880;box-shadow:0 0 8px #c5a880;"></span>',
        '<span class="live-dot dot-gold"></span>'
    )
    content = content.replace(
        '<span class="live-dot" style="background:#38bdf8;box-shadow:0 0 8px #38bdf8;"></span>',
        '<span class="live-dot dot-cyan"></span>'
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{filename} fixed!")

if __name__ == "__main__":
    fix_card()
    fix_corporate_profile()
    fix_html_showcase_file("preview-founders-showcase.html")
    fix_html_showcase_file("index.html")
    fix_html_showcase_file(os.path.join("en", "index.html"))
    fix_html_showcase_file(os.path.join("nl", "index.html"))
