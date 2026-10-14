/**
 * S&R CoreSync Solutions - 4K Ultra-HD Image Zoom, Pan & Brand Kit Controller
 * Provides interactive vector & logo inspection with smooth hardware-accelerated pan/zoom
 * and authentic Brand Asset ZIP bundle downloads across all languages (AR, EN, NL).
 */

(function () {
    'use strict';

    let zoomScale = 1.0;
    let panX = 0;
    let panY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let activeBrandProject = null;

    // Detect language context
    function getLang() {
        const htmlLang = (document.documentElement.lang || 'ar').toLowerCase();
        if (htmlLang.startsWith('nl')) return 'nl';
        if (htmlLang.startsWith('en')) return 'en';
        return 'ar';
    }

    const i18n = {
        ar: {
            zoomBadge: 'فحص وتكبير 4K',
            zoomTitleSuffix: '• فحص تفاصيل الشعار والعرض بدقة 4K',
            hint: 'اسحب للتحريك • انقر مرتين للتكبير',
            downloading: '✓ جاري بدء التنزيل...',
            downloadBtn: 'تحميل ملفات الشعار (ZIP)',
            brandHeading: 'حزمة أصول الشعار والهوية المعتمدة',
            brandSub: 'تحميل الأصول المتجهة الفيكتور بدقة غير محدودة مع كود الألوان ودليل الاستخدام.',
            downloadSuccess: 'تم تجهيز باقة الشعار بنجاح!'
        },
        en: {
            zoomBadge: '4K Zoom & Pan',
            zoomTitleSuffix: '• 4K Ultra-HD Detail Inspection',
            hint: 'Drag to pan • Double-click to zoom',
            downloading: '✓ Starting download...',
            downloadBtn: 'Download Brand Kit (ZIP)',
            brandHeading: 'Certified Master Brand Kit',
            brandSub: 'Download infinite resolution vector assets, color palette specs, and official guidelines.',
            downloadSuccess: 'Brand pack ready!'
        },
        nl: {
            zoomBadge: '4K Zoom & Pan',
            zoomTitleSuffix: '• 4K Ultra-HD Detail Inspectie',
            hint: 'Sleep om te bewegen • Dubbelklik om in te zoomen',
            downloading: '✓ Download wordt gestart...',
            downloadBtn: 'Download Merkkit (ZIP)',
            brandHeading: 'Gecertificeerd Meester Merkpakket',
            brandSub: 'Download oneindige resolutie vectorbestanden, kleurcodes en officiële merkrichtlijnen.',
            downloadSuccess: 'Merkpakket gereed!'
        }
    };

    function updateTransform() {
        const stage = document.getElementById('srZoomStage');
        const levelPill = document.getElementById('srZoomLevelText');
        if (stage) {
            stage.style.transform = `translate(${panX}px, ${panY}px) scale(${zoomScale})`;
        }
        if (levelPill) {
            levelPill.textContent = `${Math.round(zoomScale * 100)}%`;
        }
    }

    window.openImageZoom = function (src, title) {
        const modal = document.getElementById('srImageZoomModal');
        const img = document.getElementById('srZoomImage');
        const titleEl = document.getElementById('srZoomModalTitle');
        const hintEl = document.getElementById('srZoomHintText');
        const lang = getLang();

        if (!modal || !img) return;

        img.src = src;
        const displayTitle = title || (activeBrandProject ? `${activeBrandProject.name} ${i18n[lang].zoomTitleSuffix}` : '4K Ultra-HD Vector Inspection');
        if (titleEl) titleEl.textContent = displayTitle;
        if (hintEl) hintEl.textContent = i18n[lang].hint;

        zoomScale = 1.0;
        panX = 0;
        panY = 0;
        updateTransform();

        modal.classList.add('active');
        modal.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    };

    window.closeImageZoom = function () {
        const modal = document.getElementById('srImageZoomModal');
        if (modal) {
            modal.classList.remove('active');
            modal.classList.remove('is-open');
        }
        // If project modal is still open, keep body hidden; otherwise restore
        const projModal = document.getElementById('projectModal');
        if (!projModal || !projModal.classList.contains('active')) {
            document.body.style.overflow = '';
        }
    };

    window.zoomIn = function (step = 0.4) {
        zoomScale = Math.min(5.0, zoomScale + step);
        updateTransform();
    };

    window.zoomOut = function (step = 0.4) {
        zoomScale = Math.max(1.0, zoomScale - step);
        if (zoomScale <= 1.0) {
            panX = 0;
            panY = 0;
        }
        updateTransform();
    };

    window.resetZoom = function () {
        zoomScale = 1.0;
        panX = 0;
        panY = 0;
        updateTransform();
    };

    // Pan & Drag event bindings
    function initZoomInteractions() {
        const viewport = document.getElementById('srZoomViewport');
        if (!viewport) return;

        viewport.addEventListener('mousedown', (e) => {
            if (e.button !== 0) return;
            isDragging = true;
            startX = e.clientX - panX;
            startY = e.clientY - panY;
            viewport.classList.add('is-dragging');
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            panX = e.clientX - startX;
            panY = e.clientY - startY;
            updateTransform();
        });

        window.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                viewport.classList.remove('is-dragging');
            }
        });

        viewport.addEventListener('wheel', (e) => {
            e.preventDefault();
            if (e.deltaY < 0) {
                zoomIn(0.25);
            } else {
                zoomOut(0.25);
            }
        }, { passive: false });

        viewport.addEventListener('dblclick', () => {
            if (zoomScale > 1.2) {
                resetZoom();
            } else {
                zoomScale = 2.5;
                updateTransform();
            }
        });

        // Touch support
        let initialTouchDist = null;
        viewport.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                startX = e.touches[0].clientX - panX;
                startY = e.touches[0].clientY - panY;
            } else if (e.touches.length === 2) {
                initialTouchDist = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
            }
        }, { passive: true });

        viewport.addEventListener('touchmove', (e) => {
            if (isDragging && e.touches.length === 1) {
                panX = e.touches[0].clientX - startX;
                panY = e.touches[0].clientY - startY;
                updateTransform();
            } else if (e.touches.length === 2 && initialTouchDist) {
                const dist = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
                const diff = (dist - initialTouchDist) * 0.01;
                zoomScale = Math.max(1.0, Math.min(5.0, zoomScale + diff));
                initialTouchDist = dist;
                updateTransform();
            }
        }, { passive: true });

        viewport.addEventListener('touchend', () => {
            isDragging = false;
            initialTouchDist = null;
        });

        // Key bindings
        window.addEventListener('keydown', (e) => {
            const modal = document.getElementById('srImageZoomModal');
            if (!modal || !modal.classList.contains('active')) return;

            if (e.key === 'Escape') closeImageZoom();
            else if (e.key === '+' || e.key === '=') zoomIn();
            else if (e.key === '-' || e.key === '_') zoomOut();
            else if (e.key === '0') resetZoom();
        });
    }

    // Brand Kit Download Controller
    window.setActiveBrandProject = function (p) {
        activeBrandProject = p;
        const brandKitBox = document.getElementById('projectModalBrandKit');
        const lang = getLang();

        if (brandKitBox) {
            // Check if current project is identity or has brand kit
            const heading = document.getElementById('brandKitHeadingText');
            const sub = document.getElementById('brandKitSubText');
            const btnText = document.getElementById('brandKitBtnText');

            if (heading) heading.textContent = `${p.name} • ${i18n[lang].brandHeading}`;
            if (sub) sub.textContent = i18n[lang].brandSub;
            if (btnText) btnText.textContent = i18n[lang].downloadBtn;

            brandKitBox.style.display = 'block';
        }
    };

    window.downloadCurrentBrandKit = function () {
        const p = activeBrandProject;
        if (!p) return;

        const lang = getLang();
        const btn = document.getElementById('brandKitDownloadBtn');
        const btnText = document.getElementById('brandKitBtnText');

        if (btnText) btnText.textContent = i18n[lang].downloading;

        const brandId = (p.id || 'coresync').toLowerCase();
        // Determine path relative to root or subfolder
        const isSubfolder = window.location.pathname.includes('/nl/') || window.location.pathname.includes('/en/');
        const prefix = isSubfolder ? '../' : './';
        const zipUrl = `${prefix}downloads/brand-kits/${brandId}-brand-kit.zip`;

        // Create download anchor
        const a = document.createElement('a');
        a.href = zipUrl;
        a.download = `${brandId}-brand-kit.zip`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        setTimeout(() => {
            if (btnText) btnText.textContent = `✓ ${i18n[lang].downloadSuccess}`;
            setTimeout(() => {
                if (btnText) btnText.textContent = i18n[lang].downloadBtn;
            }, 2500);
        }, 800);
    };

    // Auto-initialize when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initZoomInteractions);
    } else {
        initZoomInteractions();
    }
})();
