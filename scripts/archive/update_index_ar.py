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
Script to add the official Luxury Emblem banner as the opening slide (Slide 0)
across index.html, en/index.html, nl/index.html, and preview-founders-showcase.html.
"""

import os
import re

# ==========================================
# 1. Update index.html (Arabic)
# ==========================================
def update_index_ar():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Controls
    old_ctrl = """                    <!-- كونسول التبديل بين أنماط العرض -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>سلايدر تفاعلي متحرك (Auto Slider) 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>م. محمد سليم عزيزة (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>أ. محمد رائد كعكة (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>عرض البانرين معاً (Dual Showcase)</span>
                        </button>
                    </div>"""

    new_ctrl = """                    <!-- كونسول التبديل بين أنماط العرض -->
                    <div class="showcase-controls">
                        <button type="button" class="showcase-tab-btn active" id="tabSlider" onclick="setShowcaseView('slider')">
                            <span class="showcase-tab-dot"></span>
                            <span>سلايدر تفاعلي متحرك (Auto Slider) 🔄</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabEmblem" onclick="setShowcaseView('emblem')">
                            <span class="showcase-tab-dot"></span>
                            <span>شعار الهوية الفاخر (S&amp;R Emblem) 👑</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabSalim" onclick="setShowcaseView('salim')">
                            <span class="showcase-tab-dot"></span>
                            <span>م. محمد سليم عزيزة (CTO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabRaed" onclick="setShowcaseView('raed')">
                            <span class="showcase-tab-dot"></span>
                            <span>أ. محمد رائد كعكة (CFO)</span>
                        </button>
                        <button type="button" class="showcase-tab-btn" id="tabDual" onclick="setShowcaseView('dual')">
                            <span class="showcase-tab-dot"></span>
                            <span>عرض البانرات معاً (Full Showcase)</span>
                        </button>
                    </div>"""

    if old_ctrl in content:
        content = content.replace(old_ctrl, new_ctrl)
        print("Updated index.html controls")
    else:
        print("WARNING: index.html controls not found")

    # 2. Slides Track (Add Emblem Slide as active slide 0)
    old_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- الشريحة 1: م. محمد سليم عزيزة -->
                            <div class="showcase-slide-item active">"""

    new_slides = """                        <div class="showcase-slides-track" id="slidesTrack">
                            <!-- الشريحة 0: شعار وهوية النخبة المؤسسية الفاخرة (S&R CoreSync Emblem) -->
                            <div class="showcase-slide-item active">
                                <div class="showcase-banner-card">
                                    <div class="showcase-img-wrap" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync (For Intelligent Solutions)')">
                                        <img src="./assets/sr-emblem-gold-luxury.jpg" alt="شعار الهوية المؤسسية الفاخر S&amp;R CoreSync" class="showcase-img" loading="eager">
                                    </div>
                                    <div class="showcase-banner-footer">
                                        <div class="showcase-footer-meta">
                                            <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                            <div>
                                                <div class="showcase-footer-title">S&amp;R CoreSync Solutions • الشعار الرسمي المعتمد</div>
                                                <div class="showcase-footer-role">For Intelligent Solutions • المنظومة السحابية والذكاء الاصطناعي وهندسة ERP</div>
                                                <div class="showcase-credentials-badges">
                                                    <span class="cred-badge"><i class="badge-dot"></i> الهوية المؤسسية الرسمية المعتمدة</span>
                                                    <span class="cred-badge"><i class="badge-dot"></i> رمز الابتكار والريادة السحابية</span>
                                                    <span class="cred-badge"><i class="badge-dot"></i> أمستردام • هولندا</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="showcase-footer-actions">
                                            <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
                                                <span>تكبير الشعار (Full HD) 🔍</span>
                                            </button>
                                            <a href="assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                                <span>تحميل الشعار 📥</span>
                                            </a>
                                            <a href="#services" class="showcase-action-btn">
                                                <span>اكتشف المنظومة 🚀</span>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- الشريحة 1: م. محمد سليم عزيزة -->
                            <div class="showcase-slide-item">"""

    if old_slides in content:
        content = content.replace(old_slides, new_slides)
        print("Updated index.html slides")
    else:
        print("WARNING: index.html slides track not found")

    # 3. Dots Timeline
    old_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>م. محمد سليم عزيزة (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>أ. محمد رائد كعكة (CFO)</span>
                            </button>
                        </div>"""

    new_dots = """                        <div class="showcase-dots-group">
                            <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                                <span class="showcase-dot-indicator"></span>
                                <span>شعار الهوية الفاخر (S&amp;R Emblem) 👑</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                                <span class="showcase-dot-indicator"></span>
                                <span>م. محمد سليم عزيزة (CTO)</span>
                            </button>
                            <button type="button" class="showcase-dot-item" id="slideDot2" onclick="goToSlide(2)">
                                <span class="showcase-dot-indicator"></span>
                                <span>أ. محمد رائد كعكة (CFO)</span>
                            </button>
                        </div>"""

    if old_dots in content:
        content = content.replace(old_dots, new_dots)
        print("Updated index.html dots")
    else:
        print("WARNING: index.html dots not found")

    # 4. Add viewEmblem single view before viewSalim
    old_salim_view = """                <!-- 2. مسرح العرض الفردي: م. محمد سليم عزيزة -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    new_emblem_and_salim = """                <!-- مسرح العرض الفردي: شعار الهوية المؤسسية الفاخرة -->
                <div id="viewEmblem" class="showcase-single-view showcase-is-hidden">
                    <div class="showcase-banner-card">
                        <div class="showcase-img-wrap" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync (For Intelligent Solutions)')">
                            <img src="./assets/sr-emblem-gold-luxury.jpg" alt="شعار الهوية المؤسسية الفاخر S&amp;R CoreSync" class="showcase-img" loading="lazy">
                        </div>
                        <div class="showcase-banner-footer">
                            <div class="showcase-footer-meta">
                                <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                <div>
                                    <div class="showcase-footer-title">S&amp;R CoreSync Solutions • الشعار الرسمي المعتمد</div>
                                    <div class="showcase-footer-role">For Intelligent Solutions • المنظومة السحابية والذكاء الاصطناعي وهندسة ERP</div>
                                    <div class="showcase-credentials-badges">
                                        <span class="cred-badge"><i class="badge-dot"></i> الهوية المؤسسية الرسمية المعتمدة</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> رمز الابتكار والريادة السحابية</span>
                                        <span class="cred-badge"><i class="badge-dot"></i> أمستردام • هولندا</span>
                                    </div>
                                </div>
                            </div>
                            <div class="showcase-footer-actions">
                                <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
                                    <span>تكبير الشعار (Full HD) 🔍</span>
                                </button>
                                <a href="assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                    <span>تحميل الشعار 📥</span>
                                </a>
                                <a href="#services" class="showcase-action-btn">
                                    <span>اكتشف المنظومة 🚀</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. مسرح العرض الفردي: م. محمد سليم عزيزة -->
                <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

    if old_salim_view in content:
        content = content.replace(old_salim_view, new_emblem_and_salim)
        print("Added viewEmblem to index.html")
    else:
        print("WARNING: viewSalim not found in index.html")

    # 5. Dual Grid: include emblem banner
    old_dual = """                <!-- 4. مسرح العرض المزدوج: البانران جنباً إلى جنب -->
                <div id="viewDual" class="showcase-dual-grid showcase-is-hidden">
                    <!-- بانر سليم -->"""

    new_dual = """                <!-- 4. مسرح العرض المتكامل: الشعار الرسمي والبانران معاً -->
                <div id="viewDual" class="showcase-dual-grid showcase-is-hidden">
                    <!-- بانر الشعار الفاخر -->
                    <div class="showcase-banner-card">
                        <div class="showcase-img-wrap" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync')">
                            <img src="./assets/sr-emblem-gold-luxury.jpg" alt="شعار الهوية المؤسسية الفاخر" class="showcase-img" loading="lazy">
                        </div>
                        <div class="showcase-banner-footer">
                            <div class="showcase-footer-meta">
                                <div class="showcase-footer-avatar" style="background: linear-gradient(135deg, #c5a880, #f3dfba); color: #050706; font-weight: 900;">👑</div>
                                <div>
                                    <div class="showcase-footer-title">S&amp;R CoreSync Solutions</div>
                                    <div class="showcase-footer-role">الشعار الرسمي المعتمد • For Intelligent Solutions</div>
                                    <div class="showcase-credentials-badges">
                                        <span class="cred-badge"><i class="badge-dot"></i> الهوية المؤسسية الرسمية</span>
                                    </div>
                                </div>
                            </div>
                            <div class="showcase-footer-actions">
                                <button type="button" class="showcase-action-btn" onclick="openFoundersLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
                                    <span>تكبير 🔍</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- بانر سليم -->"""

    if old_dual in content:
        content = content.replace(old_dual, new_dual)
        print("Updated viewDual in index.html")
    else:
        print("WARNING: viewDual not found in index.html")

    # 6. JavaScript Logic
    old_js = """            let currentSlideIndex = 0;
            const totalSlides = 2;"""

    new_js = """            let currentSlideIndex = 0;
            const totalSlides = 3;"""

    content = content.replace(old_js, new_js)

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
        print("Updated index.html JS logic")
    else:
        print("WARNING: index.html JS view logic not found")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("index.html written successfully!")

# Run Arabic
update_index_ar()
