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
Add Corporate Profile PDF and NFC Smart Card buttons to showcase controls
across index.html, preview-founders-showcase.html, en/index.html, and nl/index.html.
"""

import os

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"

def add_to_ar():
    path = os.path.join(PROJECT_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    target = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>عرض البانرات معاً (Full Showcase)</span>
                        </button>"""

    replacement = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>عرض البانرات معاً (Full Showcase)</span>
                        </button>
                        <a href="assets/SR-CoreSync-Corporate-Profile-2026.pdf" download="SR-CoreSync-Corporate-Profile-2026.pdf" class="showcase-tab-btn" style="border-color: rgba(243, 223, 186, 0.6); background: rgba(197, 168, 128, 0.15); text-decoration: none;" title="تحميل الملف التعريفي المؤسسي المعتمد PDF">
                            <span class="showcase-tab-dot" style="background: #f3dfba;"></span>
                            <span>الملف التعريفي المؤسسي (PDF) 📄</span>
                        </a>
                        <a href="card.html" target="_blank" class="showcase-tab-btn" style="border-color: rgba(16, 185, 129, 0.5); background: rgba(16, 185, 129, 0.1); text-decoration: none;" title="عرض وتجربة بطاقة الهوية الرقمية وتقنية NFC">
                            <span class="showcase-tab-dot" style="background: #10b981;"></span>
                            <span>بطاقة NFC الذكية 📲</span>
                        </a>"""

    if target in html and "SR-CoreSync-Corporate-Profile-2026.pdf" not in html:
        html = html.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("index.html updated with PDF & NFC buttons!")

def add_to_preview():
    path = os.path.join(PROJECT_DIR, "preview-founders-showcase.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    target = """                <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                    <span class="showcase-tab-dot"></span>
                    <span>عرض البانرات معاً (Full Showcase)</span>
                </button>"""

    replacement = """                <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                    <span class="showcase-tab-dot"></span>
                    <span>عرض البانرات معاً (Full Showcase)</span>
                </button>
                <a href="assets/SR-CoreSync-Corporate-Profile-2026.pdf" download="SR-CoreSync-Corporate-Profile-2026.pdf" class="showcase-tab-btn" style="border-color: rgba(243, 223, 186, 0.6); background: rgba(197, 168, 128, 0.15); text-decoration: none;" title="تحميل الملف التعريفي المؤسسي المعتمد PDF">
                    <span class="showcase-tab-dot" style="background: #f3dfba;"></span>
                    <span>الملف التعريفي المؤسسي (PDF) 📄</span>
                </a>
                <a href="card.html" target="_blank" class="showcase-tab-btn" style="border-color: rgba(16, 185, 129, 0.5); background: rgba(16, 185, 129, 0.1); text-decoration: none;" title="عرض وتجربة بطاقة الهوية الرقمية وتقنية NFC">
                    <span class="showcase-tab-dot" style="background: #10b981;"></span>
                    <span>بطاقة NFC الذكية 📲</span>
                </a>"""

    if target in html and "SR-CoreSync-Corporate-Profile-2026.pdf" not in html:
        html = html.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("preview-founders-showcase.html updated!")

def add_to_en():
    path = os.path.join(PROJECT_DIR, "en", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    target = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Full Suite Showcase</span>
                        </button>"""

    replacement = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Full Suite Showcase</span>
                        </button>
                        <a href="../assets/SR-CoreSync-Corporate-Profile-2026.pdf" download="SR-CoreSync-Corporate-Profile-2026.pdf" class="showcase-tab-btn" style="border-color: rgba(243, 223, 186, 0.6); background: rgba(197, 168, 128, 0.15); text-decoration: none;" title="Download Official Corporate Profile PDF">
                            <span class="showcase-tab-dot" style="background: #f3dfba;"></span>
                            <span>Corporate Profile (PDF) 📄</span>
                        </a>
                        <a href="../card.html?lang=en" target="_blank" class="showcase-tab-btn" style="border-color: rgba(16, 185, 129, 0.5); background: rgba(16, 185, 129, 0.1); text-decoration: none;" title="View Smart NFC Digital Business Card">
                            <span class="showcase-tab-dot" style="background: #10b981;"></span>
                            <span>Smart NFC Card 📲</span>
                        </a>"""

    if target in html and "SR-CoreSync-Corporate-Profile-2026.pdf" not in html:
        html = html.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("en/index.html updated!")

def add_to_nl():
    path = os.path.join(PROJECT_DIR, "nl", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    target = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Volledige Presentatie</span>
                        </button>"""

    replacement = """                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Volledige Presentatie</span>
                        </button>
                        <a href="../assets/SR-CoreSync-Corporate-Profile-2026.pdf" download="SR-CoreSync-Corporate-Profile-2026.pdf" class="showcase-tab-btn" style="border-color: rgba(243, 223, 186, 0.6); background: rgba(197, 168, 128, 0.15); text-decoration: none;" title="Download Officieel Bedrijfsprofiel PDF">
                            <span class="showcase-tab-dot" style="background: #f3dfba;"></span>
                            <span>Bedrijfsprofiel (PDF) 📄</span>
                        </a>
                        <a href="../card.html?lang=nl" target="_blank" class="showcase-tab-btn" style="border-color: rgba(16, 185, 129, 0.5); background: rgba(16, 185, 129, 0.1); text-decoration: none;" title="Bekijk Slimme Digitale NFC Visitekaart">
                            <span class="showcase-tab-dot" style="background: #10b981;"></span>
                            <span>Slimme NFC Kaart 📲</span>
                        </a>"""

    if target in html and "SR-CoreSync-Corporate-Profile-2026.pdf" not in html:
        html = html.replace(target, replacement)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("nl/index.html updated!")

if __name__ == "__main__":
    add_to_ar()
    add_to_preview()
    add_to_en()
    add_to_nl()
