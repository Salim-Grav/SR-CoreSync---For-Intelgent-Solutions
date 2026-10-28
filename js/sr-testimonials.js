/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

/**
 * S&R CoreSync - Native Sovereign Testimonials Carousel & Interactive ROI Case Studies Modal
 * Zero-dependency, Touch-friendly, Responsive, Auto-looping, Enterprise Verified Metrics
 * Milestone 35 Engine
 */
(function() {
    var CASE_STUDIES = {
        "hendrik": {
            id: "hendrik",
            name: "Hendrik van Dijk",
            flag: "🇳🇱",
            country: "هولندا",
            company: "LogiTrans B.V. — Amsterdam",
            industry: "الخدمات اللوجستية وإدارة سلاسل الإمداد الأوروبية",
            title: "أتمتة إدارة المستودعات والربط المالي السحابي الشامل",
            challenge: "تشتت عمليات التخزين في 3 مستودعات كبرى بهولندا، وتأخر مطابقة الفواتير مع هيئة الضرائب الهولندية (Belastingdienst) لمدة 12 يوماً شهرياً مع نسبة أخطاء جرد تجاوزت 14%.",
            solution: "تطوير نظام ERP سحابي سيادي مخصص يربط ماسحات الباركود بنظام المحاسبة فورياً عبر Microservices سحابية مشفرة، مع فوترة رقمية متوافقة 100% مع معايير الضرائب والـ PEPPOL الأوروبية.",
            metrics: [
                { label: "تسريع العمليات اللوجستية", value: "+310%", note: "معالجة فورية للشحنات" },
                { label: "تقليص أخطاء الجرد", value: "-72%", note: "مطابقة آلية دقيقة" },
                { label: "زمن إقفال الحسابات", value: "3 ساعات", note: "عوضاً عن 12 يوماً" },
                { label: "الامتثال الضريبي الأوروبي", value: "100%", note: "Belastingdienst & BTW" }
            ],
            stack: ["Cloud ERP Core", "PostgreSQL", "Docker", "Node.js", "Redis Cache", "PEPPOL e-Invoicing"],
            roiBadge: "عائد استثماري موثق 420% خلال 6 أشهر"
        },
        "sultan": {
            id: "sultan",
            name: "سلطان الراشد",
            flag: "🇸🇦",
            country: "المملكة العربية السعودية",
            company: "مجموعة الراشد للاستثمار التجاري",
            industry: "التجارة متعددة الفروع والاستثمار المالي",
            title: "التكامل المالي الشامل وإقفال مبيعات 14 فرعاً لحظياً",
            challenge: "صعوبة دمج مبيعات 14 فرعاً تجارياً موزعة بين الرياض وجدة والدمام، وبطء إعداد القوائم المالية الموحدة وحسابات الزكاة والضريبة (ZATCA)، مما استهلك أكثر من 500 ساعة عمل شهرياً.",
            solution: "بناء منصة مالية مركزية متوافقة كلياً مع الفوترة الإلكترونية (ZATCA المرحلة الثانية)، وربط نقاط البيع (POS) بنظام الموازنات والتقارير التنفيذية بذكاء اصطناعي تحليلي يكتشف الفروقات فوراً.",
            metrics: [
                { label: "ساعات العمل الموفرة", value: "+450 س", note: "شهرياً لفريق المحاسبة" },
                { label: "مطابقة المبيعات للفروع", value: "100%", note: "تسوية لحظية 0 خطأ" },
                { label: "الربط مع هيئة الزكاة", value: "0 ثانية", note: "اعتماد الفاتورة فورياً" },
                { label: "دقة التنبؤ المالي", value: "98.4%", note: "بمحرك الذكاء الاصطناعي" }
            ],
            stack: ["Enterprise Financial Suite", "ZATCA Phase 2 API", "Python Analytics", "Vue Dashboard", "TimescaleDB"],
            roiBadge: "توفير تكاليف تشغيلية بأكثر من 680,000 ريال سنوياً"
        },
        "klaus": {
            id: "klaus",
            name: "Klaus Weber",
            flag: "🇩🇪",
            country: "ألمانيا",
            company: "OmniVenture GmbH — Frankfurt",
            industry: "إدارة الأصول والاستثمارات الرقمية الأوروبية",
            title: "لوحات التحكم السيادية وتطبيقات الجوال المشددة سيبرانياً",
            challenge: "الحاجة إلى نظام إدارة استثماري ولوحات تحكم تنفيذية تعمل على الهواتف بأعلى معايير التشفير البنكي والامتثال للائحة حماية البيانات الأوروبية الصارمة (EU GDPR) ومعايير الأمن الألمانية (BSI).",
            solution: "هندسة تطبيق هجين فائق السرعة عبر Flutter مع خوادم خلفية موزعة في فرانكفورت وأمستردام، تشفير End-to-End، ومصادقة بايومترية متعددة المراحل مع نظام تدقيق سجلات غير قابل للتلاعب.",
            metrics: [
                { label: "زمن استجابة المنصة", value: "<65 ms", note: "سرعة خارقة لحظية" },
                { label: "مستوى الأمان والامتثال", value: "100%", note: "ISO 27001 & GDPR" },
                { label: "جاهزية التشغيل (Uptime)", value: "99.999%", note: "استمرارية عمل بدون توقف" },
                { label: "تقييم المستخدمين للتطبيق", value: "4.9 / 5", note: "تجربة مستخدم راقية" }
            ],
            stack: ["Flutter Enterprise", "Go Microservices", "AWS EU (Frankfurt)", "Biometric Auth", "HSM Encryption"],
            roiBadge: "حماية استثمارات تتجاوز 45 مليون يورو بأمان تام"
        },
        "elena": {
            id: "elena",
            name: "Elena Rossi",
            flag: "🇳🇱",
            country: "هولندا",
            company: "Boutique Aurum — Rotterdam",
            industry: "التجارة الإلكترونية للأزياء والمنتجات الفاخرة",
            title: "متجر رقمي ملكي فائق السرعة وتكامل بوابات iDEAL و Apple Pay",
            challenge: "معدل ارتداد عالي بنسبة 68% في صفحة الدفع القديمة، وبطء تحميل صور المنتجات الفاخرة، وعدم توفر بوابات الدفع الهولندية المحلية كـ iDEAL والدفع بالتقسيط Klarna.",
            solution: "إعادة بناء وتصميم المتجر الإلكتروني بنمط واجهات بدون رأس (Headless Commerce)، مع استجابة تحميل بصرية في أقل من 1.2 ثانية، ودمج بوابات الدفع بنقرة واحدة (One-Click Checkout).",
            metrics: [
                { label: "نمو المبيعات الإجمالية", value: "+180%", note: "خلال أول 60 يوماً فقط" },
                { label: "انخفاض التخلي عن السلة", value: "-54%", note: "تجربة دفع سلسة جداً" },
                { label: "سرعة تحميل المتجر", value: "1.1 ث", note: "درجة 99 في Lighthouse" },
                { label: "حجم المعاملات عبر الهاتف", value: "82%", note: "معظمها عبر Apple Pay" }
            ],
            stack: ["Next.js / Headless", "Stripe Connect", "iDEAL API", "Cloudflare CDN", "Shopify/Custom Engine"],
            roiBadge: "مضاعفة أرباح المتجر الصافية بـ 2.8 ضعف"
        },
        "tariq": {
            id: "tariq",
            name: "د. طارق المنصور",
            flag: "🇦🇪",
            country: "الإمارات / هولندا",
            company: "Aurelia Luxury Atelier — Den Haag",
            industry: "العلامات التجارية الفاخرة والاستشارات التصميمية",
            title: "صياغة الهوية المؤسسية الملكية ودليل العلامة العالمية",
            challenge: "تأسيس دار استشارية وتصميمية كبرى في لاهاي تستهدف نخبة المستثمرين في الخليج وأوروبا، مع افتقار العلامة لهوية بصرية توحي بالثقة الملكية وتنافس بيوت التصميم السويسرية والبريطانية.",
            solution: "ابتكار دليل هوية متكامل يشمل الشعار الملكي، نظام الألوان الذهبي والأسود الملكي، النماذج ثلاثية الأبعاد، بطاقات الأعمال الرقمية الذكية (NFC)، وعروض الاستثمار التفاعلية.",
            metrics: [
                { label: "التمويل الاستثماري المحصود", value: "€3.2M", note: "بفضل قوة ملف الهوية" },
                { label: "انطباع كبار المستثمرين", value: "100%", note: "ثقة واعتماد فوري" },
                { label: "الأصول الرقمية المنتجة", value: "+140", note: "هوية، عقود، تصاميم" },
                { label: "التوسع الإقليمي والدولي", value: "3 دول", note: "أمستردام، لندن، دبي" }
            ],
            stack: ["3D Spline / Blender", "Vector Master Suite", "NFC Smart Cards", "Brand Guidelines 4K"],
            roiBadge: "عقد صفقات استشارية كبرى في أول 90 يوماً"
        }
    };

    var caseKeys = ["hendrik", "sultan", "klaus", "elena", "tariq"];

    function getModalElement() {
        var el = document.getElementById('sr-casestudy-modal');
        if (el) return el;

        el = document.createElement('div');
        el.id = 'sr-casestudy-modal';
        el.className = 'sr-casestudy-overlay';
        el.setAttribute('role', 'dialog');
        el.setAttribute('aria-modal', 'true');
        el.innerHTML = [
            '<div class="sr-casestudy-card">',
            '  <button class="sr-casestudy-close" aria-label="إغلاق النافذة">',
            '    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>',
            '  </button>',
            '  <div class="sr-casestudy-header">',
            '    <div class="sr-casestudy-badge">',
            '      <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>',
            '      <span>دراسة حالة معتمدة وعائد استثمار موثق (Verified ROI)</span>',
            '    </div>',
            '    <div class="sr-casestudy-client">',
            '      <h3 class="sr-casestudy-client-name"><span class="modal-name"></span> <span class="modal-flag"></span></h3>',
            '    </div>',
            '    <p class="sr-casestudy-client-company modal-company"></p>',
            '    <h4 class="sr-casestudy-title modal-title"></h4>',
            '  </div>',
            '  <div class="sr-casestudy-metrics modal-metrics"></div>',
            '  <div class="sr-casestudy-section">',
            '    <h5 class="sr-casestudy-sec-title">',
            '      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
            '      <span>التحدي التقني والتشغيلي قبل التدخل:</span>',
            '    </h5>',
            '    <p class="sr-casestudy-sec-desc modal-challenge"></p>',
            '  </div>',
            '  <div class="sr-casestudy-section">',
            '    <h5 class="sr-casestudy-sec-title">',
            '      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
            '      <span>الحل الهندسي والذكاء الاصطناعي المنفذ من S&R CoreSync:</span>',
            '    </h5>',
            '    <p class="sr-casestudy-sec-desc modal-solution"></p>',
            '  </div>',
            '  <div class="sr-casestudy-stack modal-stack"></div>',
            '  <div class="sr-casestudy-footer">',
            '    <div class="sr-casestudy-roi-badge">',
            '      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
            '      <span class="modal-roi"></span>',
            '    </div>',
            '    <a href="https://wa.me/31618111116?text=' + encodeURIComponent('مرحباً، أود استشارة وحل مماثل لدراسات الحالات المعتمدة لدى S&R CoreSync') + '" target="_blank" rel="noopener noreferrer" class="sr-casestudy-cta-btn">',
            '      <span>طلب استشارة وحل مماثل لشركتك</span>',
            '      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
            '    </a>',
            '  </div>',
            '</div>'
        ].join('');

        document.body.appendChild(el);

        // Close handlers
        var closeBtn = el.querySelector('.sr-casestudy-close');
        closeBtn.onclick = function() { closeModal(); };
        el.onclick = function(e) {
            if (e.target === el) closeModal();
        };

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && el.classList.contains('active')) {
                closeModal();
            }
        });

        return el;
    }

    function openModal(data) {
        var modal = getModalElement();
        if (!modal || !data) return;

        modal.querySelector('.modal-name').textContent = data.name;
        modal.querySelector('.modal-flag').textContent = data.flag;
        modal.querySelector('.modal-company').textContent = data.company + ' — ' + data.industry;
        modal.querySelector('.modal-title').textContent = data.title;
        modal.querySelector('.modal-challenge').textContent = data.challenge;
        modal.querySelector('.modal-solution').textContent = data.solution;
        modal.querySelector('.modal-roi').textContent = data.roiBadge;

        // Populate metrics
        var metricsWrap = modal.querySelector('.modal-metrics');
        metricsWrap.innerHTML = '';
        data.metrics.forEach(function(m) {
            var box = document.createElement('div');
            box.className = 'sr-metric-box';
            box.innerHTML = [
                '<div class="sr-metric-value">' + m.value + '</div>',
                '<div class="sr-metric-label">' + m.label + '</div>',
                '<div class="sr-metric-note">' + m.note + '</div>'
            ].join('');
            metricsWrap.appendChild(box);
        });

        // Populate stack
        var stackWrap = modal.querySelector('.modal-stack');
        stackWrap.innerHTML = '';
        data.stack.forEach(function(s) {
            var pill = document.createElement('span');
            pill.className = 'sr-stack-pill';
            pill.textContent = s;
            stackWrap.appendChild(pill);
        });

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        var modal = document.getElementById('sr-casestudy-modal');
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // Expose openCaseStudy globally
    window.openCaseStudy = function(caseId) {
        var data = CASE_STUDIES[caseId];
        if (data) openModal(data);
    };

    function initTestimonialCarousel() {
        var container = document.querySelector('.swiper-testimonial');
        if (!container) return;

        var wrapper = container.querySelector('.swiper-wrapper');
        if (!wrapper) return;

        var slides = Array.from(wrapper.querySelectorAll('.swiper-slide'));
        if (!slides.length) return;

        // Enhance each slide with Case Study trigger & click handling
        slides.forEach(function(slide, idx) {
            var caseKey = caseKeys[idx % caseKeys.length];
            var card = slide.querySelector('.testimonial-v01');
            if (card && !card.querySelector('.tes-case-trigger')) {
                card.setAttribute('data-case-id', caseKey);
                card.setAttribute('title', 'انقر لعرض دراسة الحالة ومؤشرات عائد الاستثمار بالأرقام');
                var trigger = document.createElement('div');
                trigger.className = 'tes-case-trigger';
                trigger.innerHTML = [
                    '<span>عرض دراسة الحالة وعائد الاستثمار (ROI)</span>',
                    '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M7 17L17 7M17 7H7M17 7V17"/></svg>'
                ].join('');
                card.appendChild(trigger);

                card.addEventListener('click', function(e) {
                    // Avoid opening if clicking slider navigation inside if any
                    if (e.target.closest('.group-btn-slider')) return;
                    openModal(CASE_STUDIES[caseKey]);
                });
            }
        });

        var pagination = container.querySelector('.tf-sw-pagination');
        var prevBtn = container.querySelector('.nav-prev-swiper');
        var nextBtn = container.querySelector('.nav-next-swiper');

        var currentIndex = 0;
        var autoPlayTimer = null;
        var isHovered = false;

        function getVisibleCount() {
            var w = window.innerWidth;
            if (w >= 1200) return 3;
            if (w >= 768) return 2;
            return 1;
        }

        function getMaxIndex() {
            var visible = getVisibleCount();
            return Math.max(0, slides.length - visible);
        }

        function buildPagination() {
            if (!pagination) return;
            pagination.innerHTML = '';
            var maxIdx = getMaxIndex();
            for (var i = 0; i <= maxIdx; i++) {
                (function(idx) {
                    var bullet = document.createElement('button');
                    bullet.type = 'button';
                    bullet.className = 'swiper-pagination-bullet' + (idx === currentIndex ? ' swiper-pagination-bullet-active' : '');
                    bullet.setAttribute('aria-label', 'الانتقال إلى الرأي ' + (idx + 1));
                    bullet.addEventListener('click', function(e) {
                        e.preventDefault();
                        goToSlide(idx);
                    });
                    pagination.appendChild(bullet);
                })(i);
            }
        }

        function updateSlideStates() {
            var visible = getVisibleCount();
            var maxIdx = getMaxIndex();
            if (currentIndex > maxIdx) currentIndex = maxIdx;

            var stepPercent = 100 / visible;
            var offset = currentIndex * stepPercent;
            wrapper.style.transform = 'translate3d(-' + offset + '%, 0, 0)';

            slides.forEach(function(slide, idx) {
                var isVisible = idx >= currentIndex && idx < currentIndex + visible;
                if (isVisible) {
                    slide.classList.add('is-active', 'swiper-slide-active', 'swiper-slide-visible');
                } else {
                    slide.classList.remove('is-active', 'swiper-slide-active', 'swiper-slide-visible');
                }
            });

            if (pagination) {
                var bullets = pagination.querySelectorAll('.swiper-pagination-bullet');
                bullets.forEach(function(b, idx) {
                    if (idx === currentIndex) {
                        b.classList.add('swiper-pagination-bullet-active');
                    } else {
                        b.classList.remove('swiper-pagination-bullet-active');
                    }
                });
            }
        }

        function nextSlide() {
            var maxIdx = getMaxIndex();
            if (currentIndex >= maxIdx) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }
            updateSlideStates();
        }

        function prevSlide() {
            var maxIdx = getMaxIndex();
            if (currentIndex <= 0) {
                currentIndex = maxIdx;
            } else {
                currentIndex--;
            }
            updateSlideStates();
        }

        function goToSlide(idx) {
            var maxIdx = getMaxIndex();
            currentIndex = Math.max(0, Math.min(idx, maxIdx));
            updateSlideStates();
        }

        function startAutoplay() {
            stopAutoplay();
            autoPlayTimer = setInterval(function() {
                var modal = document.getElementById('sr-casestudy-modal');
                var isModalOpen = modal && modal.classList.contains('active');
                if (!isHovered && !isModalOpen) {
                    nextSlide();
                }
            }, 5000);
        }

        function stopAutoplay() {
            if (autoPlayTimer) {
                clearInterval(autoPlayTimer);
                autoPlayTimer = null;
            }
        }

        if (nextBtn) {
            nextBtn.onclick = function(e) {
                if (e) e.preventDefault();
                nextSlide();
            };
        }
        if (prevBtn) {
            prevBtn.onclick = function(e) {
                if (e) e.preventDefault();
                prevSlide();
            };
        }

        container.addEventListener('mouseenter', function() { isHovered = true; });
        container.addEventListener('mouseleave', function() { isHovered = false; });

        var touchStartX = 0;
        container.addEventListener('touchstart', function(e) {
            isHovered = true;
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        container.addEventListener('touchend', function(e) {
            isHovered = false;
            var touchEndX = e.changedTouches[0].screenX;
            var diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 40) {
                if (diff > 0) nextSlide();
                else prevSlide();
            }
        }, { passive: true });

        window.addEventListener('resize', function() {
            buildPagination();
            updateSlideStates();
        });

        container.classList.add('swiper-initialized');
        buildPagination();
        updateSlideStates();
        startAutoplay();

        window.testimonialSwiper = {
            slideNext: nextSlide,
            slidePrev: prevSlide,
            slideTo: goToSlide,
            update: updateSlideStates
        };

        if (typeof window.Swiper === 'undefined') {
            window.Swiper = function() {
                return window.testimonialSwiper;
            };
        }

        var urlParams = new URLSearchParams(window.location.search);
        var directCase = urlParams.get('case') || urlParams.get('casestudy');
        if (!directCase && window.location.hash) {
            var hashMatch = window.location.hash.match(/#case-([a-z0-9_-]+)/i);
            if (hashMatch) directCase = hashMatch[1];
        }
        if (directCase && CASE_STUDIES[directCase]) {
            setTimeout(function() {
                openModal(CASE_STUDIES[directCase]);
            }, 400);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTestimonialCarousel);
    } else {
        initTestimonialCarousel();
    }
})();
