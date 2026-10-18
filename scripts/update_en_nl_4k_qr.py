"""
Update en/index.html and nl/index.html with:
1. 4K Ultra HD download buttons
2. Smart Digital vCard QR modals & buttons
3. Enhanced Lightbox toolbar with 4K / HD download and QR trigger
"""

import os
import re

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync Solutions\Project"

def update_en():
    path = os.path.join(PROJECT_DIR, "en", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    css_en = """
        /* 4K Ultra HD & QR vCard Actions */
        .showcase-action-btn.showcase-action-4k {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.22) 0%, rgba(243, 223, 186, 0.08) 100%);
            border-color: rgba(243, 223, 186, 0.6);
            color: #ffffff !important;
            font-weight: 700;
        }
        .showcase-action-btn.showcase-action-4k:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #010907 !important;
            box-shadow: 0 0 20px rgba(243, 223, 186, 0.5);
            transform: translateY(-2px);
        }
        .showcase-action-btn.showcase-action-qr {
            background: rgba(197, 168, 128, 0.12);
            border-color: var(--primary-gold-bright, #e8d3b3);
            color: var(--primary-gold-bright, #e8d3b3);
        }
        .showcase-action-btn.showcase-action-qr:hover {
            background: var(--primary-gold-bright, #e8d3b3);
            color: #010907;
            box-shadow: 0 0 16px rgba(197, 168, 128, 0.4);
            transform: translateY(-2px);
        }
        .founders-lightbox-toolbar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 14px 20px;
            background: rgba(4, 9, 7, 0.94);
            border-top: 1px solid rgba(197, 168, 128, 0.3);
            flex-wrap: wrap;
            width: 100%;
        }
        .founders-lightbox-tool-btn {
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
            border: 1px solid rgba(197, 168, 128, 0.35);
            color: #ffffff;
            transition: all 0.25s ease;
            font-family: inherit;
        }
        .founders-lightbox-tool-btn:hover {
            background: #c5a880;
            color: #040807;
            transform: translateY(-2px);
        }
        .founders-lightbox-tool-btn.sr-btn-gold {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.35) 0%, rgba(243, 223, 186, 0.15) 100%);
            border-color: #f3dfba;
            color: #f3dfba;
        }
        .founders-lightbox-tool-btn.sr-btn-gold:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807;
            box-shadow: 0 0 20px rgba(197, 168, 128, 0.5);
        }
        .founders-qr-modal {
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
        .founders-qr-modal.active {
            display: flex;
        }
        .founders-qr-card {
            position: relative;
            width: 100%;
            max-width: 460px;
            background: linear-gradient(180deg, rgba(12, 24, 19, 0.98) 0%, rgba(4, 9, 7, 0.99) 100%);
            border: 1px solid rgba(197, 168, 128, 0.4);
            border-radius: 24px;
            padding: 32px 26px;
            text-align: center;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.95), 0 0 45px rgba(197, 168, 128, 0.22);
            animation: qrModalPop 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .founders-qr-close {
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(197, 168, 128, 0.3);
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
        .founders-qr-close:hover {
            background: #e11d48;
            border-color: #e11d48;
            transform: scale(1.1);
        }
        .founders-qr-badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(197, 168, 128, 0.14);
            border: 1px solid rgba(197, 168, 128, 0.4);
            border-radius: 999px;
            color: #f3dfba;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 14px;
        }
        .founders-qr-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
        }
        .founders-qr-role {
            font-size: 0.88rem;
            color: #c5a880;
            margin-bottom: 20px;
            line-height: 1.4;
        }
        .founders-qr-frame {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 22px;
        }
        .founders-qr-image {
            width: 230px;
            height: 230px;
            border-radius: 18px;
            border: 2px solid rgba(197, 168, 128, 0.4);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85), 0 0 30px rgba(197, 168, 128, 0.25);
            background: #040807;
            object-fit: contain;
        }
        .founders-qr-scan-hint {
            margin-top: 14px;
            font-size: 0.82rem;
            color: rgba(255, 255, 255, 0.78);
        }
        .founders-qr-actions {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .founders-qr-btn {
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
        .founders-qr-btn-primary {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807 !important;
            box-shadow: 0 4px 18px rgba(197, 168, 128, 0.35);
        }
        .founders-qr-btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(197, 168, 128, 0.6);
        }
        .founders-qr-btn-outline {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(197, 168, 128, 0.4);
            color: #ffffff !important;
        }
        .founders-qr-btn-outline:hover {
            background: rgba(197, 168, 128, 0.15);
            border-color: #f3dfba;
            color: #f3dfba !important;
            transform: translateY(-2px);
        }
        .founders-qr-btn-whatsapp {
            background: rgba(37, 211, 102, 0.12);
            border: 1px solid rgba(37, 211, 102, 0.4);
            color: #25d366 !important;
        }
        .founders-qr-btn-whatsapp:hover {
            background: #25d366;
            color: #010907 !important;
            transform: translateY(-2px);
        }
"""
    if ".showcase-action-btn.showcase-action-4k" not in html:
        html = html.replace("    </style>", css_en + "\n    </style>")

    # English Lightbox Modal and QR Modal
    old_lb_en = """    <!-- Founders Executive Banner Lightbox Modal -->
    <div id="foundersLightboxModal" class="founders-lightbox-modal" onclick="closeFoundersLightbox()">
        <button type="button" class="founders-lightbox-close" onclick="closeFoundersLightbox()" title="Close">&times;</button>
        <div class="founders-lightbox-box" onclick="event.stopPropagation()">
            <img id="foundersLightboxImg" src="" alt="" class="founders-lightbox-img">
        </div>
    </div>"""

    new_lb_en = """    <!-- Founders Executive Banner Lightbox Modal -->
    <div id="foundersLightboxModal" class="founders-lightbox-modal" onclick="closeFoundersLightbox()">
        <button type="button" class="founders-lightbox-close" onclick="closeFoundersLightbox()" title="Close">&times;</button>
        <div class="founders-lightbox-box" onclick="event.stopPropagation()">
            <img id="foundersLightboxImg" src="" alt="" class="founders-lightbox-img">
            <div class="founders-lightbox-toolbar" id="foundersLightboxToolbar">
                <a id="foundersLb4k" href="#" download="" class="founders-lightbox-tool-btn sr-btn-gold" title="Download Ultra HD 4K Quality">
                    <span>Download 4K Ultra HD (3840×2160) 🌟</span>
                </a>
                <a id="foundersLbHd" href="#" download="" class="founders-lightbox-tool-btn" title="Download Standard Web HD">
                    <span>Download Web HD 📥</span>
                </a>
                <button type="button" id="foundersLbQrBtn" class="founders-lightbox-tool-btn" onclick="openQrFromFoundersLightbox()" title="View Contact Card QR">
                    <span>Contact Card (QR vCard) 📲</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Smart Digital vCard QR Modal -->
    <div id="foundersQrModal" class="founders-qr-modal" onclick="closeFoundersQrModal()">
        <div class="founders-qr-card" onclick="event.stopPropagation()">
            <button type="button" class="founders-qr-close" onclick="closeFoundersQrModal()" title="Close">&times;</button>
            
            <div class="founders-qr-header">
                <div class="founders-qr-badge">👑 Certified Digital Business Card • Smart vCard</div>
                <h3 class="founders-qr-title" id="foundersQrName">Ing. Mohammad Salim Aziza</h3>
                <p class="founders-qr-role" id="foundersQrRole">Chief Technology Officer & Principal Cloud / AI Architect</p>
            </div>
            
            <div class="founders-qr-frame">
                <img id="foundersQrImg" src="../assets/qr-founder-salim.png" alt="Smart QR Code" class="founders-qr-image">
                <div class="founders-qr-scan-hint">
                    <span>📸 Scan with your smartphone camera to save contact instantly</span>
                </div>
            </div>
            
            <div class="founders-qr-actions">
                <a id="foundersQrVcf" href="../assets/salim-aziza.vcf" download="Mohammad-Salim-Aziza-CoreSync.vcf" class="founders-qr-btn founders-qr-btn-primary">
                    <span>📇 Save Contact to Phone (.vcf)</span>
                </a>
                <a id="foundersQrDl" href="../assets/qr-founder-salim.png" download="SR-CoreSync-QR-Salim-Aziza.png" class="founders-qr-btn founders-qr-btn-outline">
                    <span>📥 Download High-Res QR Code</span>
                </a>
                <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="founders-qr-btn founders-qr-btn-whatsapp">
                    <span>💬 Direct WhatsApp Chat</span>
                </a>
            </div>
        </div>
    </div>"""

    if old_lb_en in html:
        html = html.replace(old_lb_en, new_lb_en)

    # JavaScript logic
    js_en = """
            const foundersQrRegistry = {
                salim: {
                    name: 'Ing. Mohammad Salim Aziza',
                    role: 'Chief Technology Officer & Principal Cloud & AI Architect',
                    qrImg: '../assets/qr-founder-salim.png',
                    vcfFile: '../assets/salim-aziza.vcf',
                    vcfDownload: 'Mohammad-Salim-Aziza-CoreSync.vcf',
                    qrDownload: 'SR-CoreSync-QR-Salim-Aziza.png'
                },
                raed: {
                    name: 'Mohammad Raed Kaaka',
                    role: 'Chief Financial Officer & Senior Financial ERP Consultant',
                    qrImg: '../assets/qr-founder-raed.png',
                    vcfFile: '../assets/raed-kaaka.vcf',
                    vcfDownload: 'Mohammad-Raed-Kaaka-CoreSync.vcf',
                    qrDownload: 'SR-CoreSync-QR-Raed-Kaaka.png'
                },
                emblem: {
                    name: 'S&R CoreSync Solutions',
                    role: 'Official Corporate Emblem • For Intelligent Solutions',
                    qrImg: '../assets/qr-company-emblem.png',
                    vcfFile: '../assets/sr-coresync.vcf',
                    vcfDownload: 'SR-CoreSync-Official.vcf',
                    qrDownload: 'SR-CoreSync-Official-QR.png'
                }
            };

            let currentFoundersTarget = 'salim';

            window.openFoundersQrModal = function(type) {
                const data = foundersQrRegistry[type] || foundersQrRegistry.salim;
                const modal = document.getElementById('foundersQrModal');
                if (!modal) return;
                
                document.getElementById('foundersQrName').textContent = data.name;
                document.getElementById('foundersQrRole').textContent = data.role;
                document.getElementById('foundersQrImg').src = data.qrImg;
                
                const vcfLink = document.getElementById('foundersQrVcf');
                vcfLink.href = data.vcfFile;
                vcfLink.setAttribute('download', data.vcfDownload);
                
                const qrDl = document.getElementById('foundersQrDl');
                qrDl.href = data.qrImg;
                qrDl.setAttribute('download', data.qrDownload);
                
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            };

            window.closeFoundersQrModal = function() {
                const modal = document.getElementById('foundersQrModal');
                if (modal) {
                    modal.classList.remove('active');
                    document.body.style.overflow = '';
                }
            };

            window.openFoundersLightbox = function(src, alt, targetType) {
                currentFoundersTarget = targetType || (src.includes('raed') ? 'raed' : (src.includes('emblem') ? 'emblem' : 'salim'));
                const modal = document.getElementById('foundersLightboxModal');
                const img = document.getElementById('foundersLightboxImg');
                if (modal && img) {
                    img.src = src;
                    img.alt = alt;
                    
                    const src4k = src.replace('.jpg', '-4k.jpg');
                    const dl4k = document.getElementById('foundersLb4k');
                    if (dl4k) {
                        dl4k.href = src4k;
                        dl4k.setAttribute('download', src4k.split('/').pop());
                    }
                    const dlHd = document.getElementById('foundersLbHd');
                    if (dlHd) {
                        dlHd.href = src;
                        dlHd.setAttribute('download', src.split('/').pop());
                    }
                    
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            };

            window.openQrFromFoundersLightbox = function() {
                window.closeFoundersLightbox();
                window.openFoundersQrModal(currentFoundersTarget);
            };
"""

    old_lb_js_en = """            // Fullscreen Lightbox View
            window.openFoundersLightbox = function(src, alt) {
                const modal = document.getElementById('foundersLightboxModal');
                const img = document.getElementById('foundersLightboxImg');
                if (modal && img) {
                    img.src = src;
                    img.alt = alt;
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            };"""

    if old_lb_js_en in html:
        html = html.replace(old_lb_js_en, js_en)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("en/index.html updated successfully!")

def update_nl():
    path = os.path.join(PROJECT_DIR, "nl", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    css_nl = """
        /* 4K Ultra HD & QR vCard Actions */
        .showcase-action-btn.showcase-action-4k {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.22) 0%, rgba(243, 223, 186, 0.08) 100%);
            border-color: rgba(243, 223, 186, 0.6);
            color: #ffffff !important;
            font-weight: 700;
        }
        .showcase-action-btn.showcase-action-4k:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #010907 !important;
            box-shadow: 0 0 20px rgba(243, 223, 186, 0.5);
            transform: translateY(-2px);
        }
        .showcase-action-btn.showcase-action-qr {
            background: rgba(197, 168, 128, 0.12);
            border-color: var(--primary-gold-bright, #e8d3b3);
            color: var(--primary-gold-bright, #e8d3b3);
        }
        .showcase-action-btn.showcase-action-qr:hover {
            background: var(--primary-gold-bright, #e8d3b3);
            color: #010907;
            box-shadow: 0 0 16px rgba(197, 168, 128, 0.4);
            transform: translateY(-2px);
        }
        .founders-lightbox-toolbar {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: 14px 20px;
            background: rgba(4, 9, 7, 0.94);
            border-top: 1px solid rgba(197, 168, 128, 0.3);
            flex-wrap: wrap;
            width: 100%;
        }
        .founders-lightbox-tool-btn {
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
            border: 1px solid rgba(197, 168, 128, 0.35);
            color: #ffffff;
            transition: all 0.25s ease;
            font-family: inherit;
        }
        .founders-lightbox-tool-btn:hover {
            background: #c5a880;
            color: #040807;
            transform: translateY(-2px);
        }
        .founders-lightbox-tool-btn.sr-btn-gold {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.35) 0%, rgba(243, 223, 186, 0.15) 100%);
            border-color: #f3dfba;
            color: #f3dfba;
        }
        .founders-lightbox-tool-btn.sr-btn-gold:hover {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807;
            box-shadow: 0 0 20px rgba(197, 168, 128, 0.5);
        }
        .founders-qr-modal {
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
        .founders-qr-modal.active {
            display: flex;
        }
        .founders-qr-card {
            position: relative;
            width: 100%;
            max-width: 460px;
            background: linear-gradient(180deg, rgba(12, 24, 19, 0.98) 0%, rgba(4, 9, 7, 0.99) 100%);
            border: 1px solid rgba(197, 168, 128, 0.4);
            border-radius: 24px;
            padding: 32px 26px;
            text-align: center;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.95), 0 0 45px rgba(197, 168, 128, 0.22);
            animation: qrModalPop 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .founders-qr-close {
            position: absolute;
            top: 16px;
            right: 16px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(197, 168, 128, 0.3);
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
        .founders-qr-close:hover {
            background: #e11d48;
            border-color: #e11d48;
            transform: scale(1.1);
        }
        .founders-qr-badge {
            display: inline-block;
            padding: 6px 16px;
            background: rgba(197, 168, 128, 0.14);
            border: 1px solid rgba(197, 168, 128, 0.4);
            border-radius: 999px;
            color: #f3dfba;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 14px;
        }
        .founders-qr-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
        }
        .founders-qr-role {
            font-size: 0.88rem;
            color: #c5a880;
            margin-bottom: 20px;
            line-height: 1.4;
        }
        .founders-qr-frame {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 22px;
        }
        .founders-qr-image {
            width: 230px;
            height: 230px;
            border-radius: 18px;
            border: 2px solid rgba(197, 168, 128, 0.4);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85), 0 0 30px rgba(197, 168, 128, 0.25);
            background: #040807;
            object-fit: contain;
        }
        .founders-qr-scan-hint {
            margin-top: 14px;
            font-size: 0.82rem;
            color: rgba(255, 255, 255, 0.78);
        }
        .founders-qr-actions {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .founders-qr-btn {
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
        .founders-qr-btn-primary {
            background: linear-gradient(135deg, #c5a880 0%, #f3dfba 100%);
            color: #040807 !important;
            box-shadow: 0 4px 18px rgba(197, 168, 128, 0.35);
        }
        .founders-qr-btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(197, 168, 128, 0.6);
        }
        .founders-qr-btn-outline {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(197, 168, 128, 0.4);
            color: #ffffff !important;
        }
        .founders-qr-btn-outline:hover {
            background: rgba(197, 168, 128, 0.15);
            border-color: #f3dfba;
            color: #f3dfba !important;
            transform: translateY(-2px);
        }
        .founders-qr-btn-whatsapp {
            background: rgba(37, 211, 102, 0.12);
            border: 1px solid rgba(37, 211, 102, 0.4);
            color: #25d366 !important;
        }
        .founders-qr-btn-whatsapp:hover {
            background: #25d366;
            color: #010907 !important;
            transform: translateY(-2px);
        }
"""
    if ".showcase-action-btn.showcase-action-4k" not in html:
        html = html.replace("    </style>", css_nl + "\n    </style>")

    # Dutch Lightbox Modal and QR Modal
    old_lb_nl = """    <!-- Founders Executive Banner Lightbox Modal -->
    <div id="foundersLightboxModal" class="founders-lightbox-modal" onclick="closeFoundersLightbox()">
        <button type="button" class="founders-lightbox-close" onclick="closeFoundersLightbox()" title="Sluiten">&times;</button>
        <div class="founders-lightbox-box" onclick="event.stopPropagation()">
            <img id="foundersLightboxImg" src="" alt="" class="founders-lightbox-img">
        </div>
    </div>"""

    new_lb_nl = """    <!-- Founders Executive Banner Lightbox Modal -->
    <div id="foundersLightboxModal" class="founders-lightbox-modal" onclick="closeFoundersLightbox()">
        <button type="button" class="founders-lightbox-close" onclick="closeFoundersLightbox()" title="Sluiten">&times;</button>
        <div class="founders-lightbox-box" onclick="event.stopPropagation()">
            <img id="foundersLightboxImg" src="" alt="" class="founders-lightbox-img">
            <div class="founders-lightbox-toolbar" id="foundersLightboxToolbar">
                <a id="foundersLb4k" href="#" download="" class="founders-lightbox-tool-btn sr-btn-gold" title="Download Ultra HD 4K Kwaliteit">
                    <span>Download 4K Ultra HD (3840×2160) 🌟</span>
                </a>
                <a id="foundersLbHd" href="#" download="" class="founders-lightbox-tool-btn" title="Download Standaard Web HD">
                    <span>Download Web HD 📥</span>
                </a>
                <button type="button" id="foundersLbQrBtn" class="founders-lightbox-tool-btn" onclick="openQrFromFoundersLightbox()" title="Bekijk Visitekaart QR">
                    <span>Contactkaart (QR vCard) 📲</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Smart Digitale vCard QR Modal -->
    <div id="foundersQrModal" class="founders-qr-modal" onclick="closeFoundersQrModal()">
        <div class="founders-qr-card" onclick="event.stopPropagation()">
            <button type="button" class="founders-qr-close" onclick="closeFoundersQrModal()" title="Sluiten">&times;</button>
            
            <div class="founders-qr-header">
                <div class="founders-qr-badge">👑 Gecertificeerde Digitale Visitekaart • Smart vCard</div>
                <h3 class="founders-qr-title" id="foundersQrName">Ing. Mohammad Salim Aziza</h3>
                <p class="founders-qr-role" id="foundersQrRole">Chief Technology Officer & Principal Cloud / AI Architect</p>
            </div>
            
            <div class="founders-qr-frame">
                <img id="foundersQrImg" src="../assets/qr-founder-salim.png" alt="Smart QR Code" class="founders-qr-image">
                <div class="founders-qr-scan-hint">
                    <span>📸 Scan met uw smartphonecamera om direct contact op te slaan</span>
                </div>
            </div>
            
            <div class="founders-qr-actions">
                <a id="foundersQrVcf" href="../assets/salim-aziza.vcf" download="Mohammad-Salim-Aziza-CoreSync.vcf" class="founders-qr-btn founders-qr-btn-primary">
                    <span>📇 Contact opslaan op telefoon (.vcf)</span>
                </a>
                <a id="foundersQrDl" href="../assets/qr-founder-salim.png" download="SR-CoreSync-QR-Salim-Aziza.png" class="founders-qr-btn founders-qr-btn-outline">
                    <span>📥 Download Hoge Resolutie QR-code</span>
                </a>
                <a href="https://wa.me/31618111116" target="_blank" rel="noopener noreferrer" class="founders-qr-btn founders-qr-btn-whatsapp">
                    <span>💬 Direct WhatsApp Contact</span>
                </a>
            </div>
        </div>
    </div>"""

    if old_lb_nl in html:
        html = html.replace(old_lb_nl, new_lb_nl)

    # JavaScript logic
    js_nl = """
            const foundersQrRegistry = {
                salim: {
                    name: 'Ing. Mohammad Salim Aziza',
                    role: 'Chief Technology Officer & Principal Cloud & AI Architect',
                    qrImg: '../assets/qr-founder-salim.png',
                    vcfFile: '../assets/salim-aziza.vcf',
                    vcfDownload: 'Mohammad-Salim-Aziza-CoreSync.vcf',
                    qrDownload: 'SR-CoreSync-QR-Salim-Aziza.png'
                },
                raed: {
                    name: 'Mohammad Raed Kaaka',
                    role: 'Chief Financial Officer & Senior Financieel ERP Consultant',
                    qrImg: '../assets/qr-founder-raed.png',
                    vcfFile: '../assets/raed-kaaka.vcf',
                    vcfDownload: 'Mohammad-Raed-Kaaka-CoreSync.vcf',
                    qrDownload: 'SR-CoreSync-QR-Raed-Kaaka.png'
                },
                emblem: {
                    name: 'S&R CoreSync Solutions',
                    role: 'Officieel Directie Embleem • For Intelligent Solutions',
                    qrImg: '../assets/qr-company-emblem.png',
                    vcfFile: '../assets/sr-coresync.vcf',
                    vcfDownload: 'SR-CoreSync-Official.vcf',
                    qrDownload: 'SR-CoreSync-Official-QR.png'
                }
            };

            let currentFoundersTarget = 'salim';

            window.openFoundersQrModal = function(type) {
                const data = foundersQrRegistry[type] || foundersQrRegistry.salim;
                const modal = document.getElementById('foundersQrModal');
                if (!modal) return;
                
                document.getElementById('foundersQrName').textContent = data.name;
                document.getElementById('foundersQrRole').textContent = data.role;
                document.getElementById('foundersQrImg').src = data.qrImg;
                
                const vcfLink = document.getElementById('foundersQrVcf');
                vcfLink.href = data.vcfFile;
                vcfLink.setAttribute('download', data.vcfDownload);
                
                const qrDl = document.getElementById('foundersQrDl');
                qrDl.href = data.qrImg;
                qrDl.setAttribute('download', data.qrDownload);
                
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            };

            window.closeFoundersQrModal = function() {
                const modal = document.getElementById('foundersQrModal');
                if (modal) {
                    modal.classList.remove('active');
                    document.body.style.overflow = '';
                }
            };

            window.openFoundersLightbox = function(src, alt, targetType) {
                currentFoundersTarget = targetType || (src.includes('raed') ? 'raed' : (src.includes('emblem') ? 'emblem' : 'salim'));
                const modal = document.getElementById('foundersLightboxModal');
                const img = document.getElementById('foundersLightboxImg');
                if (modal && img) {
                    img.src = src;
                    img.alt = alt;
                    
                    const src4k = src.replace('.jpg', '-4k.jpg');
                    const dl4k = document.getElementById('foundersLb4k');
                    if (dl4k) {
                        dl4k.href = src4k;
                        dl4k.setAttribute('download', src4k.split('/').pop());
                    }
                    const dlHd = document.getElementById('foundersLbHd');
                    if (dlHd) {
                        dlHd.href = src;
                        dlHd.setAttribute('download', src.split('/').pop());
                    }
                    
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            };

            window.openQrFromFoundersLightbox = function() {
                window.closeFoundersLightbox();
                window.openFoundersQrModal(currentFoundersTarget);
            };
"""

    old_lb_js_nl = """            // Fullscreen Lightbox View
            window.openFoundersLightbox = function(src, alt) {
                const modal = document.getElementById('foundersLightboxModal');
                const img = document.getElementById('foundersLightboxImg');
                if (modal && img) {
                    img.src = src;
                    img.alt = alt;
                    modal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
            };"""

    if old_lb_js_nl in html:
        html = html.replace(old_lb_js_nl, js_nl)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("nl/index.html updated successfully!")

if __name__ == "__main__":
    update_en()
    update_nl()
