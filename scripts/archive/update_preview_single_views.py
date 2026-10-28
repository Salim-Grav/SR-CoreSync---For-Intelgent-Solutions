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
Update all single views and dual grid action buttons in preview-founders-showcase.html
"""

FILE_PATH = r"i:\I-Ai\App\S&R CoreSync Solutions\Project\preview-founders-showcase.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    c = f.read()

# Replace viewEmblem actions
old_ve_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
                            <span>تكبير الشعار (Full HD) 🔍</span>
                        </button>
                        <a href="assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                            <span>تحميل الشعار 📥</span>
                        </a>
                        <a href="#services" class="showcase-action-btn">
                            <span>اكتشف المنظومة 🚀</span>
                        </a>
                    </div>"""

new_ve_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر', 'emblem')">
                            <span>تكبير 🔍</span>
                        </button>
                        <a href="assets/sr-emblem-gold-luxury-4k.jpg" download="SR-CoreSync-Luxury-Emblem-4K.jpg" class="showcase-action-btn showcase-action-4k" title="تحميل الشعار بدقة 4K فائقة">
                            <span>تحميل 4K 🌟</span>
                        </a>
                        <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openQrModal('emblem')" title="عرض رمز QR المؤسسي المعتمد">
                            <span>بطاقة QR 📲</span>
                        </button>
                        <a href="#services" class="showcase-action-btn">
                            <span>المنظومة 🚀</span>
                        </a>
                    </div>"""

if old_ve_actions in c:
    c = c.replace(old_ve_actions, new_ve_actions)

# Replace viewSalim actions
old_vs_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-salim.jpg', 'م. محمد سليم عزيزة')">
                            <span>تكبير البانر (Full HD) 🔍</span>
                        </button>
                        <a href="assets/founder-banner-salim.jpg" download="SR-CoreSync-Founder-Salim-Aziza.jpg" class="showcase-action-btn">
                            <span>تحميل البانر 📥</span>
                        </a>
                        <a href="#contact" class="showcase-action-btn">
                            <span>حجز استشارة تقنية 👔</span>
                        </a>
                    </div>"""

new_vs_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-salim.jpg', 'م. محمد سليم عزيزة', 'salim')">
                            <span>تكبير 🔍</span>
                        </button>
                        <a href="assets/founder-banner-salim-4k.jpg" download="SR-CoreSync-Founder-Salim-Aziza-4K.jpg" class="showcase-action-btn showcase-action-4k" title="تحميل البانر بدقة 4K فائقة">
                            <span>تحميل 4K 🌟</span>
                        </a>
                        <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openQrModal('salim')" title="عرض بطاقة الاتصال الرقمية الذكية (vCard)">
                            <span>بطاقة QR 📲</span>
                        </button>
                        <a href="#contact" class="showcase-action-btn">
                            <span>استشارة 👔</span>
                        </a>
                    </div>"""

if old_vs_actions in c:
    c = c.replace(old_vs_actions, new_vs_actions)

# Replace viewRaed actions
old_vr_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-raed.jpg', 'أ. محمد رائد كعكة')">
                            <span>تكبير البانر (Full HD) 🔍</span>
                        </button>
                        <a href="assets/founder-banner-raed.jpg" download="SR-CoreSync-Founder-Raed-Kaaka.jpg" class="showcase-action-btn">
                            <span>تحميل البانر 📥</span>
                        </a>
                        <a href="#contact" class="showcase-action-btn">
                            <span>حجز استشارة مالية 👔</span>
                        </a>
                    </div>"""

new_vr_actions = """                    <div class="showcase-footer-actions">
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-raed.jpg', 'أ. محمد رائد كعكة', 'raed')">
                            <span>تكبير 🔍</span>
                        </button>
                        <a href="assets/founder-banner-raed-4k.jpg" download="SR-CoreSync-Founder-Raed-Kaaka-4K.jpg" class="showcase-action-btn showcase-action-4k" title="تحميل البانر بدقة 4K فائقة">
                            <span>تحميل 4K 🌟</span>
                        </a>
                        <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openQrModal('raed')" title="عرض بطاقة الاتصال الرقمية الذكية (vCard)">
                            <span>بطاقة QR 📲</span>
                        </button>
                        <a href="#contact" class="showcase-action-btn">
                            <span>استشارة 👔</span>
                        </a>
                    </div>"""

if old_vr_actions in c:
    c = c.replace(old_vr_actions, new_vr_actions)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated single views in preview-founders-showcase.html")
