"""
Apply 4K and QR action buttons to slides and single views in en/index.html and nl/index.html
"""

import os
import re

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync Solutions\Project"

def update_en_buttons():
    path = os.path.join(PROJECT_DIR, "en", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Slide 0
    old_s0 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Official Emblem')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                                <span>Download Emblem 📥</span>
                                            </a>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>Explore Services 🚀</span>
                                            </a>
                                        </div>"""

    new_s0 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Official Emblem', 'emblem')">
                                                <span>Inspect 🔍</span>
                                            </button>
                                            <a href="../assets/sr-emblem-gold-luxury-4k.jpg" download="SR-CoreSync-Luxury-Emblem-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Emblem">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('emblem')" title="View Corporate Contact Card QR">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>Services 🚀</span>
                                            </a>
                                        </div>"""

    # Slide 1
    old_s1 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-salim.jpg', 'Eng. Mohammad Salim Aziza')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-salim.jpg" download="SR-CoreSync-Founder-Salim-Aziza.jpg" class="showcase-action-btn">
                                                <span>Download Banner 📥</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('cloud')">
                                                <span>Book Cloud &amp; AI Session 👔</span>
                                            </button>
                                        </div>"""

    new_s1 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-salim.jpg', 'Eng. Mohammad Salim Aziza', 'salim')">
                                                <span>Inspect 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-salim-4k.jpg" download="SR-CoreSync-Founder-Salim-Aziza-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Banner (3840×2160)">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('salim')" title="View Smart Digital Contact Card (vCard)">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('cloud')">
                                                <span>Consultation 👔</span>
                                            </button>
                                        </div>"""

    # Slide 2
    old_s2 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-raed.jpg', 'Mr. Mohammad Raed Kaaka')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-raed.jpg" download="SR-CoreSync-Founder-Raed-Kaaka.jpg" class="showcase-action-btn">
                                                <span>Download Banner 📥</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('erp')">
                                                <span>Book Financial ERP Session 👔</span>
                                            </button>
                                        </div>"""

    new_s2 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-raed.jpg', 'Mr. Mohammad Raed Kaaka', 'raed')">
                                                <span>Inspect 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-raed-4k.jpg" download="SR-CoreSync-Founder-Raed-Kaaka-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Banner (3840×2160)">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('raed')" title="View Smart Digital Contact Card (vCard)">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('erp')">
                                                <span>Consultation 👔</span>
                                            </button>
                                        </div>"""

    html = html.replace(old_s0, new_s0)
    html = html.replace(old_s1, new_s1)
    html = html.replace(old_s2, new_s2)

    # Update single views
    html = re.sub(
        r'(<div id="viewEmblem"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s0.strip(),
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<div id="viewSalim"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s1.strip(),
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<div id="viewRaed"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s2.strip(),
        html,
        flags=re.DOTALL
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("en/index.html buttons updated!")

def update_nl_buttons():
    path = os.path.join(PROJECT_DIR, "nl", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Slide 0
    old_s0 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Directie Embleem')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                                <span>Download Embleem 📥</span>
                                            </a>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>Ontdek Diensten 🚀</span>
                                            </a>
                                        </div>"""

    new_s0 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Directie Embleem', 'emblem')">
                                                <span>Bekijken 🔍</span>
                                            </button>
                                            <a href="../assets/sr-emblem-gold-luxury-4k.jpg" download="SR-CoreSync-Luxury-Emblem-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Embleem">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('emblem')" title="Bekijk Digitaal Directie Visitekaartje QR">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>Diensten 🚀</span>
                                            </a>
                                        </div>"""

    # Slide 1
    old_s1 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-salim.jpg', 'Ing. Mohammad Salim Aziza')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-salim.jpg" download="SR-CoreSync-Founder-Salim-Aziza.jpg" class="showcase-action-btn">
                                                <span>Download Banner 📥</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('cloud')">
                                                <span>Boek Cloud &amp; AI Sessie 👔</span>
                                            </button>
                                        </div>"""

    new_s1 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-salim.jpg', 'Ing. Mohammad Salim Aziza', 'salim')">
                                                <span>Bekijken 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-salim-4k.jpg" download="SR-CoreSync-Founder-Salim-Aziza-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Banner (3840×2160)">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('salim')" title="Bekijk Slimme Digitale Visitekaart (vCard)">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('cloud')">
                                                <span>Adviesgesprek 👔</span>
                                            </button>
                                        </div>"""

    # Slide 2
    old_s2 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-raed.jpg', 'Dhr. Mohammad Raed Kaaka')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-raed.jpg" download="SR-CoreSync-Founder-Raed-Kaaka.jpg" class="showcase-action-btn">
                                                <span>Download Banner 📥</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('erp')">
                                                <span>Boek Financieel ERP Sessie 👔</span>
                                            </button>
                                        </div>"""

    new_s2 = """                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/founder-banner-raed.jpg', 'Dhr. Mohammad Raed Kaaka', 'raed')">
                                                <span>Bekijken 🔍</span>
                                            </button>
                                            <a href="../assets/founder-banner-raed-4k.jpg" download="SR-CoreSync-Founder-Raed-Kaaka-4K.jpg" class="showcase-action-btn showcase-action-4k" title="Download Ultra HD 4K Banner (3840×2160)">
                                                <span>Download 4K 🌟</span>
                                            </a>
                                            <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openFoundersQrModal('raed')" title="Bekijk Slimme Digitale Visitekaart (vCard)">
                                                <span>vCard QR 📲</span>
                                            </button>
                                            <button type="button" class="showcase-action-btn" onclick="openExecutiveBookingModal('erp')">
                                                <span>Adviesgesprek 👔</span>
                                            </button>
                                        </div>"""

    html = html.replace(old_s0, new_s0)
    html = html.replace(old_s1, new_s1)
    html = html.replace(old_s2, new_s2)

    # Update single views
    html = re.sub(
        r'(<div id="viewEmblem"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s0.strip(),
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<div id="viewSalim"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s1.strip(),
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'(<div id="viewRaed"[^>]*>.*?)(<div class="showcase-footer-actions">.*?</div>)',
        lambda m: m.group(1) + new_s2.strip(),
        html,
        flags=re.DOTALL
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("nl/index.html buttons updated!")

if __name__ == "__main__":
    update_en_buttons()
    update_nl_buttons()
