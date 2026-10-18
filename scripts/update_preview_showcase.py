# -*- coding: utf-8 -*-
with open('preview-founders-showcase.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_ctrl = """        <div class="showcase-controls">
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

new_ctrl = """        <div class="showcase-controls">
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

if old_ctrl in c:
    c = c.replace(old_ctrl, new_ctrl)
    print("Preview controls updated!")

old_slides = """                <div class="showcase-slides-track" id="slidesTrack">
                    <!-- الشريحة 1: م. محمد سليم عزيزة -->
                    <div class="showcase-slide-item active">"""

new_slides = """                <div class="showcase-slides-track" id="slidesTrack">
                    <!-- الشريحة 0: شعار وهوية النخبة المؤسسية الفاخرة (S&R CoreSync Emblem) -->
                    <div class="showcase-slide-item active">
                        <div class="showcase-banner-card">
                            <div class="showcase-img-wrap" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync (For Intelligent Solutions)')">
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
                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
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

if old_slides in c:
    c = c.replace(old_slides, new_slides)
    print("Preview slides updated!")

old_dots = """                <div class="showcase-dots-group">
                    <button type="button" class="showcase-dot-item active" id="slideDot0" onclick="goToSlide(0)">
                        <span class="showcase-dot-indicator"></span>
                        <span>م. محمد سليم عزيزة (CTO)</span>
                    </button>
                    <button type="button" class="showcase-dot-item" id="slideDot1" onclick="goToSlide(1)">
                        <span class="showcase-dot-indicator"></span>
                        <span>أ. محمد رائد كعكة (CFO)</span>
                    </button>
                </div>"""

new_dots = """                <div class="showcase-dots-group">
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

if old_dots in c:
    c = c.replace(old_dots, new_dots)
    print("Preview dots updated!")

# Total slides = 3
c = c.replace("const totalSlides = 2;", "const totalSlides = 3;")

old_view_js = """        function setShowcaseView(mode) {
            const vSlider = document.getElementById('viewSlider');
            const vSalim = document.getElementById('viewSalim');
            const vRaed = document.getElementById('viewRaed');
            const vDual = document.getElementById('viewDual');

            const tSlider = document.getElementById('tabSlider');
            const tSalim = document.getElementById('tabSalim');
            const tRaed = document.getElementById('tabRaed');
            const tDual = document.getElementById('tabDual');

            [tSlider, tSalim, tRaed, tDual].forEach(t => t.classList.remove('active'));
            [vSlider, vSalim, vRaed, vDual].forEach(v => v.classList.add('showcase-is-hidden'));

            if (mode === 'slider') {
                vSlider.classList.remove('showcase-is-hidden');
                tSlider.classList.add('active');
                isPlaying = true;
                startAutoPlay();
            } else {
                stopAutoPlay();
                if (mode === 'salim') {
                    vSalim.classList.remove('showcase-is-hidden');
                    tSalim.classList.add('active');
                } else if (mode === 'raed') {
                    vRaed.classList.remove('showcase-is-hidden');
                    tRaed.classList.add('active');
                } else if (mode === 'dual') {
                    vDual.classList.remove('showcase-is-hidden');
                    tDual.classList.add('active');
                }
            }
        }"""

new_view_js = """        function setShowcaseView(mode) {
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
                startAutoPlay();
            } else {
                stopAutoPlay();
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
        }"""

if old_view_js in c:
    c = c.replace(old_view_js, new_view_js)
    print("Preview JS updated!")

# viewEmblem single view
old_salim_view = """        <!-- 2. مسرح العرض الفردي: م. محمد سليم عزيزة -->
        <div id="viewSalim" class="showcase-single-view showcase-is-hidden">"""

new_emblem_view = """        <!-- مسرح العرض الفردي: شعار الهوية المؤسسية الفاخرة -->
        <div id="viewEmblem" class="showcase-single-view showcase-is-hidden">
            <div class="showcase-banner-card">
                <div class="showcase-img-wrap" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر - S&amp;R CoreSync')">
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
                        <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
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

if old_salim_view in c:
    c = c.replace(old_salim_view, new_emblem_view)
    print("Preview viewEmblem added!")

with open('preview-founders-showcase.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("preview-founders-showcase.html saved!")
