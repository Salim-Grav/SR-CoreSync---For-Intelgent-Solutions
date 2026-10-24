"""
Update preview-founders-showcase.html with 4K Download buttons & Digital QR vCard Modals.
"""

import re

FILE_PATH = r"i:\I-Ai\App\S&R CoreSync Solutions\Project\preview-founders-showcase.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add CSS for 4K buttons, QR Modal, and Lightbox Toolbar before </style>
css_additions = """
        /* زر التحميل الفائق 4K */
        .showcase-action-btn.showcase-action-4k {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.22) 0%, rgba(243, 223, 186, 0.08) 100%);
            border-color: rgba(243, 223, 186, 0.6);
            color: #ffffff;
            font-weight: 700;
        }

        .showcase-action-btn.showcase-action-4k:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #010907;
            box-shadow: 0 0 20px rgba(243, 223, 186, 0.5);
            transform: translateY(-2px);
        }

        .showcase-action-btn.showcase-action-qr {
            background: rgba(197, 168, 128, 0.12);
            border-color: var(--primary-gold-bright);
            color: var(--primary-gold-bright);
        }

        .showcase-action-btn.showcase-action-qr:hover {
            background: var(--primary-gold-bright);
            color: #010907;
            box-shadow: 0 0 16px rgba(197, 168, 128, 0.4);
        }

        /* تولبار نافذة التكبير الكبيرة Lightbox Toolbar */
        .sr-lightbox-toolbar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 14px 20px;
            background: rgba(4, 9, 7, 0.92);
            border-top: 1px solid var(--border-gold);
            flex-wrap: wrap;
            width: 100%;
        }

        .sr-lightbox-tool-btn {
            padding: 9px 20px;
            border-radius: 999px;
            font-size: 0.88rem;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-gold);
            color: #ffffff;
            transition: all 0.25s ease;
            font-family: inherit;
        }

        .sr-lightbox-tool-btn:hover {
            background: var(--primary-gold);
            color: #040807;
            transform: translateY(-2px);
        }

        .sr-lightbox-tool-btn.sr-btn-gold {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.35) 0%, rgba(243, 223, 186, 0.15) 100%);
            border-color: var(--primary-gold-bright);
            color: var(--primary-gold-bright);
        }

        .sr-lightbox-tool-btn.sr-btn-gold:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807;
            box-shadow: 0 0 20px rgba(197, 168, 128, 0.5);
        }

        /* نافذة البطاقة الرقمية الذكية (Digital vCard QR Modal) */
        .sr-qr-modal {
            position: fixed;
            inset: 0;
            background: rgba(1, 9, 7, 0.94);
            -webkit-backdrop-filter: blur(14px);
            backdrop-filter: blur(14px);
            z-index: 1000000;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .sr-qr-modal.active {
            display: flex;
        }

        .sr-qr-card {
            position: relative;
            width: 100%;
            max-width: 460px;
            background: linear-gradient(180deg, rgba(12, 24, 19, 0.98) 0%, rgba(4, 9, 7, 0.99) 100%);
            border: 1px solid var(--border-gold-glow);
            border-radius: 24px;
            padding: 32px 26px;
            text-align: center;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.95), 0 0 45px rgba(197, 168, 128, 0.22);
            animation: qrModalPop 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes qrModalPop {
            from { opacity: 0; transform: scale(0.92) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        .sr-qr-close {
            position: absolute;
            top: 16px;
            left: 16px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-gold);
            color: #ffffff;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            font-size: 1.3rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }

        .sr-qr-close:hover {
            background: #e11d48;
            border-color: #e11d48;
            transform: scale(1.1);
        }

        .sr-qr-badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(197, 168, 128, 0.14);
            border: 1px solid var(--border-gold);
            border-radius: 999px;
            color: var(--primary-gold-bright);
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .sr-qr-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
        }

        .sr-qr-role {
            font-size: 0.88rem;
            color: var(--primary-gold-bright);
            margin-bottom: 20px;
            line-height: 1.4;
        }

        .sr-qr-frame {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 22px;
        }

        .sr-qr-image {
            width: 230px;
            height: 230px;
            border-radius: 18px;
            border: 2px solid var(--border-gold-glow);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85), 0 0 30px rgba(197, 168, 128, 0.25);
            background: #040807;
            object-fit: contain;
        }

        .sr-qr-scan-hint {
            margin-top: 14px;
            font-size: 0.82rem;
            color: rgba(255, 255, 255, 0.78);
        }

        .sr-qr-actions {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .sr-qr-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 12px 20px;
            border-radius: 999px;
            font-size: 0.92rem;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.25s ease;
            font-family: inherit;
            border: none;
        }

        .sr-qr-btn-primary {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807;
            box-shadow: 0 4px 18px rgba(197, 168, 128, 0.35);
        }

        .sr-qr-btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(197, 168, 128, 0.6);
        }

        .sr-qr-btn-outline {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-gold);
            color: #ffffff;
        }

        .sr-qr-btn-outline:hover {
            background: rgba(197, 168, 128, 0.15);
            border-color: var(--primary-gold-bright);
            color: var(--primary-gold-bright);
            transform: translateY(-2px);
        }

        .sr-qr-btn-whatsapp {
            background: rgba(37, 211, 102, 0.12);
            border: 1px solid rgba(37, 211, 102, 0.4);
            color: #25d366;
        }

        .sr-qr-btn-whatsapp:hover {
            background: #25d366;
            color: #010907;
            transform: translateY(-2px);
        }
"""

if "/* زر التحميل الفائق 4K */" not in html:
    html = html.replace("    </style>", css_additions + "\n    </style>")

# 2. Update lightbox markup
old_lightbox = """    <!-- نافذة الزووم الكبيرة Lightbox -->
    <div id="lightboxModal" class="sr-lightbox-modal" onclick="closeLightbox()">
        <button type="button" class="sr-lightbox-close" onclick="closeLightbox()" title="إغلاق">&times;</button>
        <div class="sr-lightbox-box" onclick="event.stopPropagation()">
            <img id="lightboxImg" src="" alt="" class="sr-lightbox-img">
        </div>
    </div>"""

new_lightbox = """    <!-- نافذة الزووم الكبيرة Lightbox مع شريط التحميل والـ QR -->
    <div id="lightboxModal" class="sr-lightbox-modal" onclick="closeLightbox()">
        <button type="button" class="sr-lightbox-close" onclick="closeLightbox()" title="إغلاق">&times;</button>
        <div class="sr-lightbox-box" onclick="event.stopPropagation()">
            <img id="lightboxImg" src="" alt="" class="sr-lightbox-img">
            <div class="sr-lightbox-toolbar" id="lightboxToolbar">
                <a id="lightboxDownload4k" href="#" download="" class="sr-lightbox-tool-btn sr-btn-gold" title="تحميل بأعلى دقة 4K فائقة">
                    <span>تحميل فائق 4K Ultra HD (3840×2160) 🌟</span>
                </a>
                <a id="lightboxDownloadHd" href="#" download="" class="sr-lightbox-tool-btn" title="تحميل دقة الويب المعتمدة">
                    <span>تحميل ويب HD 📥</span>
                </a>
                <button type="button" id="lightboxQrBtn" class="sr-lightbox-tool-btn" onclick="openQrFromLightbox()" title="عرض بطاقة الاتصال الرقمية">
                    <span>بطاقة اتصال رقمية (QR vCard) 📲</span>
                </button>
            </div>
        </div>
    </div>

    <!-- نافذة البطاقة الرقمية الذكية (Smart vCard & QR Modal) -->
    <div id="qrModal" class="sr-qr-modal" onclick="closeQrModal()">
        <div class="sr-qr-card" onclick="event.stopPropagation()">
            <button type="button" class="sr-qr-close" onclick="closeQrModal()" title="إغلاق">&times;</button>
            
            <div class="sr-qr-header">
                <div class="sr-qr-badge">👑 بطاقة الاتصال الرقمية المعتمدة • Smart vCard</div>
                <h3 class="sr-qr-title" id="qrFounderName">م. محمد سليم عزيزة</h3>
                <p class="sr-qr-role" id="qrFounderRole">المسؤول التقني وكبير مهندسي السحابة والذكاء الاصطناعي</p>
            </div>
            
            <div class="sr-qr-frame">
                <img id="qrDisplayImg" src="assets/qr-founder-salim.png" alt="Smart QR Code" class="sr-qr-image">
                <div class="sr-qr-scan-hint">
                    <span>📸 امسح الرمز بكاميرا هاتفك لحفظ جهة الاتصال فوراً</span>
                </div>
            </div>
            
            <div class="sr-qr-actions">
                <a id="qrVcfLink" href="assets/salim-aziza.vcf" download="Mohammad-Salim-Aziza-CoreSync.vcf" class="sr-qr-btn sr-qr-btn-primary">
                    <span>📇 حفظ جهة الاتصال بالهاتف مباشرة (.vcf)</span>
                </a>
                <a id="qrDownloadLink" href="assets/qr-founder-salim.png" download="SR-CoreSync-QR-Salim-Aziza.png" class="sr-qr-btn sr-qr-btn-outline">
                    <span>📥 تحميل رمز الـ QR عالي الدقة</span>
                </a>
                <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="sr-qr-btn sr-qr-btn-whatsapp">
                    <span>💬 محادثة واتساب فورية</span>
                </a>
            </div>
        </div>
    </div>"""

if "id=\"lightboxToolbar\"" not in html and old_lightbox in html:
    html = html.replace(old_lightbox, new_lightbox)

# 3. Update JavaScript for QR & Lightbox
js_enhancements = """
        // بيانات البطاقات الرقمية ورموز QR
        const qrRegistry = {
            salim: {
                name: 'م. محمد سليم عزيزة',
                role: 'المسؤول التقني وكبير مهندسي السحابة والذكاء الاصطناعي & CTO',
                qrImg: 'assets/qr-founder-salim.png',
                vcfFile: 'assets/salim-aziza.vcf',
                vcfDownload: 'Mohammad-Salim-Aziza-CoreSync.vcf',
                qrDownload: 'SR-CoreSync-QR-Salim-Aziza.png'
            },
            raed: {
                name: 'أ. محمد رائد كعكة',
                role: 'المستشار المالي ومطور نظم ERP & CFO',
                qrImg: 'assets/qr-founder-raed.png',
                vcfFile: 'assets/raed-kaaka.vcf',
                vcfDownload: 'Mohammad-Raed-Kaaka-CoreSync.vcf',
                qrDownload: 'SR-CoreSync-QR-Raed-Kaaka.png'
            },
            emblem: {
                name: 'S&R CoreSync Solutions',
                role: 'الشعار المؤسسي الرسمي • For Intelligent Solutions',
                qrImg: 'assets/qr-company-emblem.png',
                vcfFile: 'assets/sr-coresync.vcf',
                vcfDownload: 'SR-CoreSync-Official.vcf',
                qrDownload: 'SR-CoreSync-Official-QR.png'
            }
        };

        let currentLightboxTarget = 'salim';

        function openQrModal(type) {
            const data = qrRegistry[type] || qrRegistry.salim;
            const modal = document.getElementById('qrModal');
            if (!modal) return;
            
            document.getElementById('qrFounderName').textContent = data.name;
            document.getElementById('qrFounderRole').textContent = data.role;
            document.getElementById('qrDisplayImg').src = data.qrImg;
            
            const vcfLink = document.getElementById('qrVcfLink');
            vcfLink.href = data.vcfFile;
            vcfLink.setAttribute('download', data.vcfDownload);
            
            const qrDl = document.getElementById('qrDownloadLink');
            qrDl.href = data.qrImg;
            qrDl.setAttribute('download', data.qrDownload);
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeQrModal() {
            const modal = document.getElementById('qrModal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }

        function openLightbox(src, alt, targetType) {
            currentLightboxTarget = targetType || (src.includes('raed') ? 'raed' : (src.includes('emblem') ? 'emblem' : 'salim'));
            const modal = document.getElementById('lightboxModal');
            const img = document.getElementById('lightboxImg');
            if (modal && img) {
                img.src = src;
                img.alt = alt;
                
                // Map 4K source
                const src4k = src.replace('.jpg', '-4k.jpg');
                const dl4k = document.getElementById('lightboxDownload4k');
                if (dl4k) {
                    dl4k.href = src4k;
                    dl4k.setAttribute('download', src4k.split('/').pop());
                }
                
                const dlHd = document.getElementById('lightboxDownloadHd');
                if (dlHd) {
                    dlHd.href = src;
                    dlHd.setAttribute('download', src.split('/').pop());
                }
                
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        function openQrFromLightbox() {
            closeLightbox();
            openQrModal(currentLightboxTarget);
        }
"""

# Replace openLightbox and closeLightbox with updated logic
old_js_lightbox = """        // التحكم بنافذة العرض الموسعة Lightbox
        function openLightbox(src, alt) {
            const modal = document.getElementById('lightboxModal');
            const img = document.getElementById('lightboxImg');
            if (modal && img) {
                img.src = src;
                img.alt = alt;
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        function closeLightbox() {
            const modal = document.getElementById('lightboxModal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }"""

if old_js_lightbox in html:
    html = html.replace(old_js_lightbox, js_enhancements + """
        function closeLightbox() {
            const modal = document.getElementById('lightboxModal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }""")

# 4. Update the Action Buttons in Slide 0, Slide 1, Slide 2, Single views, Dual grid
# Slide 0 Action Buttons:
slide0_old_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر')">
                                        <span>تكبير الشعار (Full HD) 🔍</span>
                                    </button>
                                    <a href="assets/sr-emblem-gold-luxury.jpg" download="SR-CoreSync-Luxury-Emblem.jpg" class="showcase-action-btn">
                                        <span>تحميل الشعار 📥</span>
                                    </a>
                                    <a href="#services" class="showcase-action-btn">
                                        <span>اكتشف المنظومة 🚀</span>
                                    </a>"""

slide0_new_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/sr-emblem-gold-luxury.jpg', 'شعار الهوية المؤسسية الفاخر', 'emblem')">
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
                                    </a>"""

if slide0_old_actions in html:
    html = html.replace(slide0_old_actions, slide0_new_actions)

# Slide 1 (Salim) Actions:
salim_old_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-salim.jpg', 'م. محمد سليم عزيزة')">
                                        <span>تكبير البانر (Full HD) 🔍</span>
                                    </button>
                                    <a href="assets/founder-banner-salim.jpg" download="SR-CoreSync-Founder-Salim-Aziza.jpg" class="showcase-action-btn">
                                        <span>تحميل البانر 📥</span>
                                    </a>
                                    <a href="#contact" class="showcase-action-btn">
                                        <span>حجز استشارة تقنية 👔</span>
                                    </a>"""

salim_new_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-salim.jpg', 'م. محمد سليم عزيزة', 'salim')">
                                        <span>تكبير 🔍</span>
                                    </button>
                                    <a href="assets/founder-banner-salim-4k.jpg" download="SR-CoreSync-Founder-Salim-Aziza-4K.jpg" class="showcase-action-btn showcase-action-4k" title="تحميل البانر بدقة 4K فائقة (3840×2160)">
                                        <span>تحميل 4K 🌟</span>
                                    </a>
                                    <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openQrModal('salim')" title="عرض بطاقة الاتصال الرقمية الذكية (vCard)">
                                        <span>بطاقة QR 📲</span>
                                    </button>
                                    <a href="#contact" class="showcase-action-btn">
                                        <span>استشارة 👔</span>
                                    </a>"""

if salim_old_actions in html:
    html = html.replace(salim_old_actions, salim_new_actions)

# Slide 2 (Raed) Actions:
raed_old_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-raed.jpg', 'أ. محمد رائد كعكة')">
                                        <span>تكبير البانر (Full HD) 🔍</span>
                                    </button>
                                    <a href="assets/founder-banner-raed.jpg" download="SR-CoreSync-Founder-Raed-Kaaka.jpg" class="showcase-action-btn">
                                        <span>تحميل البانر 📥</span>
                                    </a>
                                    <a href="#contact" class="showcase-action-btn">
                                        <span>حجز استشارة مالية 👔</span>
                                    </a>"""

raed_new_actions = """                                    <button type="button" class="showcase-action-btn" onclick="openLightbox('assets/founder-banner-raed.jpg', 'أ. محمد رائد كعكة', 'raed')">
                                        <span>تكبير 🔍</span>
                                    </button>
                                    <a href="assets/founder-banner-raed-4k.jpg" download="SR-CoreSync-Founder-Raed-Kaaka-4K.jpg" class="showcase-action-btn showcase-action-4k" title="تحميل البانر بدقة 4K فائقة (3840×2160)">
                                        <span>تحميل 4K 🌟</span>
                                    </a>
                                    <button type="button" class="showcase-action-btn showcase-action-qr" onclick="openQrModal('raed')" title="عرض بطاقة الاتصال الرقمية الذكية (vCard)">
                                        <span>بطاقة QR 📲</span>
                                    </button>
                                    <a href="#contact" class="showcase-action-btn">
                                        <span>استشارة 👔</span>
                                    </a>"""

if raed_old_actions in html:
    html = html.replace(raed_old_actions, raed_new_actions)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("preview-founders-showcase.html updated successfully with 4K buttons & QR modals!")
