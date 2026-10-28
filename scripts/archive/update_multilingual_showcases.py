# -*- coding: utf-8 -*-
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
Script to update en/index.html, nl/index.html, and preview-founders-showcase.html
with the Luxury Emblem opening banner (Slide 0).
"""

# ==========================================
# 1. Update en/index.html (English)
# ==========================================
def update_en():
    path = "en/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Controls
    old_ctrl = """                    <!-- Showcase Viewport Console -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Auto-Play Slider 🔄</span>
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

    new_ctrl = """                    <!-- Showcase Viewport Console -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Auto-Play Slider 🔄</span>
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

    if old_ctrl in content:
        content = content.replace(old_ctrl, new_ctrl)
        print("Updated en controls")
    else:
        print("WARNING: en controls not found")

    # Slides
    old_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- Slide 1: Eng. Mohammad Salim Aziza -->
                            <div class="showcase-slide-item active">"""

    new_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- Slide 0: S&R CoreSync Luxury Official Emblem -->
                            <div class="showcase-slide-item active">
                                <div class="showcase-banner-card">
                                    <div class="showcase-img-wrap" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Solutions • Official Corporate Emblem')">
                                        <img src="../assets/sr-emblem-gold-luxury.jpg" alt="S&amp;R CoreSync Solutions Official Luxury Emblem" class="showcase-img" loading="eager">
                                    </div>
                                    <div class="showcase-banner-footer">
                                        <div class="showcase-footer-meta">
                                            <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                            <div>
                                                <div class="showcase-footer-title">S&amp;R CoreSync Solutions • Official Corporate Emblem</div>
                                                <div class="showcase-footer-role">For Intelligent Solutions • Cloud Architecture, AI &amp; Enterprise ERP Systems</div>
                                                <div class="showcase-credentials-badges">
                                                    <span class="cred-badge"><i class="badge-dot"></i> Certified Corporate Emblem</span>
                                                    <span class="cred-badge"><i class="badge-dot"></i> Enterprise Innovation Symbol</span>
                                                    <span class="cred-badge"><i class="badge-dot"></i> Amsterdam, Netherlands</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Official Emblem')">
                                                <span>Inspect Full HD 🔍</span>
                                            </button>
                                            <a href="../assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                                <span>Download Emblem 📥</span>
                                            </a>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>Explore Services 🚀</span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Slide 1: Eng. Mohammad Salim Aziza -->
                            <div class="showcase-slide-item">"""

    if old_slides in content:
        content = content.replace(old_slides, new_slides)
        print("Updated en slides")
    else:
        print("WARNING: en slides not found")

    # Dots
    old_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Eng. Mohammad Salim Aziza (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Mr. Mohammad Raed Kaaka (CFO)</span>
                            </button>
                        </div>"""

    new_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Corporate Emblem 👑</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Eng. Mohammad Salim Aziza (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot2" onclick="goToSlide(2)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Mr. Mohammad Raed Kaaka (CFO)</span>
                            </button>
                        </div>"""

    if old_dots in content:
        content = content.replace(old_dots, new_dots)
        print("Updated en dots")
    else:
        print("WARNING: en dots not found")

    # Single view
    old_salim_view = """                <!-- 2. Single View: Eng. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    new_emblem_and_salim = """                <!-- Single View: Official Corporate Emblem -->
                <div id="viewEmblem" class="showcase-single-view showcase-is-hidden">
                    <div class="showcase-banner-card">
                        <div class="showcase-img-wrap" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Solutions • Official Corporate Emblem')">
                            <img src="../assets/sr-emblem-gold-luxury.jpg" alt="S&amp;R CoreSync Solutions Official Luxury Emblem" class="showcase-img" loading="lazy">
                        </div>
                        <div class="showcase-banner-footer">
                            <div class="showcase-footer-meta">
                                <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                <div>
                                    <div class="showcase-footer-title">S&amp;R CoreSync Solutions • Official Corporate Emblem</div>
                                    <div class="showcase-footer-role">For Intelligent Solutions • Cloud Architecture, AI &amp; Enterprise ERP Systems</div>
                                    <div class="showcase-credentials-badges">
                                        <span class="cred-badge"><i class="badge-dot"></i> Certified Corporate Emblem</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> Enterprise Innovation Symbol</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> Amsterdam, Netherlands</span>
                                    </div>
                                </div>
                            </div>
                            <div class="showcase-footer-actions">
                                <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Official Emblem')">
                                    <span>Inspect Full HD 🔍</span>
                                </button>
                                <a href="../assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                    <span>Download Emblem 📥</span>
                                </a>
                                <a href="#services" class="showcase-action-btn">
                                    <span>Explore Services 🚀</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. Single View: Eng. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    if old_salim_view in content:
        content = content.replace(old_salim_view, new_emblem_and_salim)
        print("Updated en viewEmblem")
    else:
        print("WARNING: en viewSalim not found")

    # JS totalSlides
    old_js = """            let currentSlideIndex = 0;
            const totalSlides = 2;"""

    new_js = """            let currentSlideIndex = 0;
            const totalSlides = 3;"""
    content = content.replace(old_js, new_js)

    # JS view logic
    old_view_js = """            window.setShowcaseView = function(mode) {
                const vSlider = document.getElementById('viewSlider');
                const vSalim = document.getElementById('viewSalim');
                const vRaed = document.getElementById('viewRaed');
                const vDual = document.getElementById('viewDual');

                const tSlider = document.getElementById('tabSlider');
                const tSalim = document.getElementById('tabSalim');
                const tRaed = document.getElementById('tabRaed');
                const tDual = document.getElementById('tabDual');

                [tSlider, tSalim, tRaed, tDual].forEach(t => { if (t) t.classList.remove('active'); });
                [vSlider, vSalim, vRaed, vDual].forEach(v => { if (v) v.classList.add('showcase-is-hidden'); });

                if (mode === 'slider') {
                    if (vSlider) vSlider.classList.remove('showcase-is-hidden');
                    if (tSlider) tSlider.classList.add('active');
                    isPlaying = true;
                    window.startAutoPlay();
                } else {
                    window.stopAutoPlay();
                    if (mode === 'salim') {
                        if (vSalim) vSalim.classList.remove('showcase-is-hidden');
                        if (tSalim) tSalim.classList.add('active');
                    } else if (mode === 'raed') {
                        if (vRaed) vRaed.classList.remove('showcase-is-hidden');
                        if (tRaed) tRaed.classList.add('active');
                    } else if (mode === 'dual') {
                        if (vDual) vDual.classList.remove('showcase-is-hidden');
                        if (tDual) tDual.classList.add('active');
                    }
                }
            };"""

    new_view_js = """            window.setShowcaseView = function(mode) {
                const vSlider = document.getElementById('viewSlider');
                const vEmblem = document.getElementById('viewEmblem');
                const vSalim = document.getElementById('viewSalim');
                const vRaed = document.getElementById('viewRaed');
                const vDual = document.getElementById('viewDual');

                const tSlider = document.getElementById('tabSlider');
                const tEmblem = document.getElementById('tabEmblem');
                const tSalim = document.getElementById('tabSalim');
                const tRaed = document.getElementById('tabRaed');
                const tDual = document.getElementById('tabDual');

                [tSlider, tEmblem, tSalim, tRaed, tDual].forEach(t => { if (t) t.classList.remove('active'); });
                [vSlider, vEmblem, vSalim, vRaed, vDual].forEach(v => { if (v) v.classList.add('showcase-is-hidden'); });

                if (mode === 'slider') {
                    if (vSlider) vSlider.classList.remove('showcase-is-hidden');
                    if (tSlider) tSlider.classList.add('active');
                    isPlaying = true;
                    window.startAutoPlay();
                } else {
                    window.stopAutoPlay();
                    if (mode === 'emblem') {
                        if (vEmblem) vEmblem.classList.remove('showcase-is-hidden');
                        if (tEmblem) tEmblem.classList.add('active');
                    } else if (mode === 'salim') {
                        if (vSalim) vSalim.classList.remove('showcase-is-hidden');
                        if (tSalim) tSalim.classList.add('active');
                    } else if (mode === 'raed') {
                        if (vRaed) vRaed.classList.remove('showcase-is-hidden');
                        if (tRaed) tRaed.classList.add('active');
                    } else if (mode === 'dual') {
                        if (vDual) vDual.classList.remove('showcase-is-hidden');
                        if (tDual) tDual.classList.add('active');
                    }
                }
            };"""

    if old_view_js in content:
        content = content.replace(old_view_js, new_view_js)
        print("Updated en JS view logic")
    else:
        print("WARNING: en JS view logic not found")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("en/index.html updated successfully!")


# ==========================================
# 2. Update nl/index.html (Dutch)
# ==========================================
def update_nl():
    path = "nl/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Controls
    old_ctrl = """                    <!-- Showcase Weergave Console -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Automatische Slider 🔄</span>
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

    new_ctrl = """                    <!-- Showcase Weergave Console -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>Automatische Slider 🔄</span>
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

    if old_ctrl in content:
        content = content.replace(old_ctrl, new_ctrl)
        print("Updated nl controls")
    else:
        print("WARNING: nl controls not found")

    # Slides
    old_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- Slide 1: Ing. Mohammad Salim Aziza -->
                            <div class="showcase-slide-item active">"""

    new_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- Slide 0: S&R CoreSync Luxe Officieel Embleem -->
                            <div class="showcase-slide-item active">
                                <div class="showcase-banner-card">
                                    <div class="showcase-img-wrap" onclick="openFoundersLightbox('../assets/sr-emblem-gold-luxury.jpg', 'S&amp;R CoreSync Solutions • Officieel Directie Embleem')">
                                        <img src="../assets/sr-emblem-gold-luxury.jpg" alt="S&amp;R CoreSync Solutions Officieel Luxe Embleem" class="showcase-img" loading="eager">
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

                            <!-- Slide 1: Ing. Mohammad Salim Aziza -->
                            <div class="showcase-slide-item">"""

    if old_slides in content:
        content = content.replace(old_slides, new_slides)
        print("Updated nl slides")
    else:
        print("WARNING: nl slides not found")

    # Dots
    old_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Ing. Mohammad Salim Aziza (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Dhr. Mohammad Raed Kaaka (CFO)</span>
                            </button>
                        </div>"""

    new_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Directie Embleem 👑</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Ing. Mohammad Salim Aziza (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot2" onclick="goToSlide(2)">
                                <span class="showcase-dot-indicator"></span>
                                <span>Dhr. Mohammad Raed Kaaka (CFO)</span>
                            </button>
                        </div>"""

    if old_dots in content:
        content = content.replace(old_dots, new_dots)
        print("Updated nl dots")
    else:
        print("WARNING: nl dots not found")

    # Single view
    old_salim_view = """                <!-- 2. Individuele Weergave: Ing. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    new_emblem_and_salim = """                <!-- Individuele Weergave: Officieel Bedrijfsembleem -->
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

                <!-- 2. Individuele Weergave: Ing. Mohammad Salim Aziza -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    if old_salim_view in content:
        content = content.replace(old_salim_view, new_emblem_and_salim)
        print("Updated nl viewEmblem")
    else:
        print("WARNING: nl viewSalim not found")

    # JS totalSlides
    old_js = """            let currentSlideIndex = 0;
            const totalSlides = 2;"""

    new_js = """            let currentSlideIndex = 0;
            const totalSlides = 3;"""
    content = content.replace(old_js, new_js)

    # JS view logic
    old_view_js = """            window.setShowcaseView = function(mode) {
                const vSlider = document.getElementById('viewSlider');
                const vSalim = document.getElementById('viewSalim');
                const vRaed = document.getElementById('viewRaed');
                const vDual = document.getElementById('viewDual');

                const tSlider = document.getElementById('tabSlider');
                const tSalim = document.getElementById('tabSalim');
                const tRaed = document.getElementById('tabRaed');
                const tDual = document.getElementById('tabDual');

                [tSlider, tSalim, tRaed, tDual].forEach(t => { if (t) t.classList.remove('active'); });
                [vSlider, vSalim, vRaed, vDual].forEach(v => { if (v) v.classList.add('showcase-is-hidden'); });

                if (mode === 'slider') {
                    if (vSlider) vSlider.classList.remove('showcase-is-hidden');
                    if (tSlider) tSlider.classList.add('active');
                    isPlaying = true;
                    window.startAutoPlay();
                } else {
                    window.stopAutoPlay();
                    if (mode === 'salim') {
                        if (vSalim) vSalim.classList.remove('showcase-is-hidden');
                        if (tSalim) tSalim.classList.add('active');
                    } else if (mode === 'raed') {
                        if (vRaed) vRaed.classList.remove('showcase-is-hidden');
                        if (tRaed) tRaed.classList.add('active');
                    } else if (mode === 'dual') {
                        if (vDual) vDual.classList.remove('showcase-is-hidden');
                        if (tDual) tDual.classList.add('active');
                    }
                }
            };"""

    new_view_js = """            window.setShowcaseView = function(mode) {
                const vSlider = document.getElementById('viewSlider');
                const vEmblem = document.getElementById('viewEmblem');
                const vSalim = document.getElementById('viewSalim');
                const vRaed = document.getElementById('viewRaed');
                const vDual = document.getElementById('viewDual');

                const tSlider = document.getElementById('tabSlider');
                const tEmblem = document.getElementById('tabEmblem');
                const tSalim = document.getElementById('tabSalim');
                const tRaed = document.getElementById('tabRaed');
                const tDual = document.getElementById('tabDual');

                [tSlider, tEmblem, tSalim, tRaed, tDual].forEach(t => { if (t) t.classList.remove('active'); });
                [vSlider, vEmblem, vSalim, vRaed, vDual].forEach(v => { if (v) v.classList.add('showcase-is-hidden'); });

                if (mode === 'slider') {
                    if (vSlider) vSlider.classList.remove('showcase-is-hidden');
                    if (tSlider) tSlider.classList.add('active');
                    isPlaying = true;
                    window.startAutoPlay();
                } else {
                    window.stopAutoPlay();
                    if (mode === 'emblem') {
                        if (vEmblem) vEmblem.classList.remove('showcase-is-hidden');
                        if (tEmblem) tEmblem.classList.add('active');
                    } else if (mode === 'salim') {
                        if (vSalim) vSalim.classList.remove('showcase-is-hidden');
                        if (tSalim) tSalim.classList.add('active');
                    } else if (mode === 'raed') {
                        if (vRaed) vRaed.classList.remove('showcase-is-hidden');
                        if (tRaed) tRaed.classList.add('active');
                    } else if (mode === 'dual') {
                        if (vDual) vDual.classList.remove('showcase-is-hidden');
                        if (tDual) tDual.classList.add('active');
                    }
                }
            };"""

    if old_view_js in content:
        content = content.replace(old_view_js, new_view_js)
        print("Updated nl JS view logic")
    else:
        print("WARNING: nl JS view logic not found")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("nl/index.html updated successfully!")


# Run both
update_en()
update_nl()
