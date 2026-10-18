# -*- coding: utf-8 -*-
# Finish multilingual updates

with open('en/index.html', 'r', encoding='utf-8') as f:
    c_en = f.read()

old_en_ctrl = """                    <!-- Showcase Controls -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Interactive Auto Slider 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>Eng. Mohammad Salim Aziza (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>Mr. Mohammad Raed Kaaka (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Dual Founders Showcase</span>
                        </button>
                    </div>"""

new_en_ctrl = """                    <!-- Showcase Controls -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Interactive Auto Slider 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabEmblem" onclick="setShowcaseView('emblem')">
                            <span class="showcase-tab-dot"></span>
                            <span>Corporate Emblem 👑</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>Eng. Mohammad Salim Aziza (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>Mr. Mohammad Raed Kaaka (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Full Suite Showcase</span>
                        </button>
                    </div>"""

if old_en_ctrl in c_en:
    c_en = c_en.replace(old_en_ctrl, new_en_ctrl)
    with open('en/index.html', 'w', encoding='utf-8') as f:
        f.write(c_en)
    print('EN controls updated!')
else:
    print('EN controls NOT found!')

with open('nl/index.html', 'r', encoding='utf-8') as f:
    c_nl = f.read()

old_nl_ctrl = """                    <!-- Showcase Controls -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Interactieve Slider 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>Ing. Mohammad Salim Aziza (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>Dhr. Mohammad Raed Kaaka (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Beide Oprichters Tonen</span>
                        </button>
                    </div>"""

new_nl_ctrl = """                    <!-- Showcase Controls -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Interactieve Slider 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabEmblem" onclick="setShowcaseView('emblem')">
                            <span class="showcase-tab-dot"></span>
                            <span>Directie Embleem 👑</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>Ing. Mohammad Salim Aziza (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>Dhr. Mohammad Raed Kaaka (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>Volledige Presentatie</span>
                        </button>
                    </div>"""

if old_nl_ctrl in c_nl:
    c_nl = c_nl.replace(old_nl_ctrl, new_nl_ctrl)
    print('NL controls updated!')

old_nl_salim = """                <!-- 2. Single View: Ing. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

new_nl_emblem = """                <!-- Individuele Weergave: Officieel Bedrijfsembleem -->
                <div id="viewEmblem" class="showcase-single-view showcase-is-hidden">
                    <div class="showcase-banner-card">
                        <div class="showcase-img-wrap" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Solutions • Officieel Directie Embleem')">
                            <img src="../assets/sr-emblem-gold-luxury.jpg" alt="S&amp;R CoreSync Solutions Officieel Luxe Embleem" class="showcase-img" loading="lazy">
                        </div>
                        <div class="showcase-banner-footer">
                            <div class="showcase-footer-meta">
                                <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                <div>
                                    <div class="showcase-footer-title">S&amp;R CoreSync Solutions • Officieel Directie Embleem</div>
                                    <div class="showcase-footer-role">For Intelligent Solutions • Cloud Architectuur, Enterprise AI &amp; ERP Integratie</div>
                                    <div class="showcase-credentials-badges">
                                        <span class="cred-badge"><i class="badge-dot"></i> Officieel Bedrijfsembleem</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> Symbool van Innovatie</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> Amsterdam, Nederland</span>
                                    </div>
                                </div>
                            </div>
                            <div class="showcase-footer-actions">
                                <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Officieel Embleem')">
                                    <span>Vergroot Full HD 🔍</span>
                                </button>
                                <a href="../assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                    <span>Download Embleem 📥</span>
                                </a>
                                <a href="#services" class="showcase-action-btn">
                                    <span>Ontdek Diensten 🚀</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. Single View: Ing. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

if old_nl_salim in c_nl:
    c_nl = c_nl.replace(old_nl_salim, new_nl_emblem)
    print('NL viewEmblem added!')

with open('nl/index.html', 'w', encoding='utf-8') as f:
    f.write(c_nl)
print('Finished all updates!')
