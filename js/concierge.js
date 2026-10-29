/* ==========================================================================
   S&R CoreSync — AI Concierge (client-side retrieval, zero backend)
   --------------------------------------------------------------------------
   Reads a local knowledge base (services, real prices, FAQ, articles),
   scores it against the visitor's question and answers with source links.
   Falls back to a human hand-off on WhatsApp when confidence is low.
   ========================================================================== */
(function () {
    'use strict';

    var WA = 'https://wa.me/31618111116?text=' + encodeURIComponent('مرحباً S&R CoreSync، أود استشارة تنفيذية.');

    var KB = [
        {
            tags: 'خدمات خدماتكم ماذا تقدمون حلول الشركة تخصص',
            q: 'ما الخدمات التي تقدمونها؟',
            a: 'نغطي ستة مجالات: <strong>الهوية البصرية</strong>، <strong>المواقع والمتاجر</strong>، <strong>البرمجيات السحابية وERP</strong>، <strong>تطبيقات الجوال</strong>، <strong>أتمتة العمليات والذكاء الاصطناعي</strong>، و<strong>الأمن والبنية السحابية</strong>.',
            link: './index.html#service', label: 'استعرض الخدمات'
        },
        {
            tags: 'سعر اسعار تكلفة كم بكم ميزانية باقات الباقات',
            q: 'كم تكلفة الخدمات؟',
            a: 'الأسعار المعلنة: الهوية البصرية <strong>€590</strong> · الموقع <strong>€980</strong> · المتجر <strong>€1,450</strong> · باقة السحابة Core Starter <strong>€1,490</strong> · تهيئة ERP <strong>€1,890</strong> · Enterprise Growth <strong>€2,890</strong> · Core MAX <strong>€4,990</strong>. وتوجد باقة انطلاقة شاملة <strong>€1,990</strong> بدلاً من €3,020.',
            link: './index.html#pricing', label: 'كل الباقات'
        },
        {
            tags: 'هوية شعار لوجو تصميم هوية بصرية براند',
            q: 'كم سعر الهوية البصرية؟',
            a: 'الهوية البصرية المتكاملة <strong>€590</strong>: ثلاثة مفاهيم شعار، دليل هوية كامل، لوحة ألوان وخطوط، قرطاسية وبطاقات، وملفات المصدر. التسليم خلال 7–10 أيام عمل.',
            link: './index.html#service', label: 'تفاصيل الهوية'
        },
        {
            tags: 'موقع مواقع ويب تصميم موقع سعر الموقع',
            q: 'كم سعر الموقع الإلكتروني؟',
            a: 'الموقع الفاخر عالي الأداء <strong>€980</strong>: تصميم متجاوب، سرعة تتجاوز 98%، تهيئة SEO، دعم لغات متعددة، ربط واتساب، واستضافة ونطاق لسنة. التسليم 2–4 أسابيع.',
            link: './index.html#service', label: 'تفاصيل المواقع'
        },
        {
            tags: 'متجر متاجر تجارة الكترونية شوب شوبيفاي سلة',
            q: 'كم سعر المتجر الإلكتروني؟',
            a: 'المتجر الإلكتروني المتكامل <strong>€1,450</strong>: سلة ودفع بخطوة واحدة، iDEAL/Mollie/Stripe/Apple Pay، إدارة مخزون، كوبونات، فواتير متوافقة ضريبياً، وربط محاسبي. التسليم 4–6 أسابيع.',
            link: './insights/ecommerce-conversion.html', label: 'دليل رفع التحويل'
        },
        {
            tags: 'erp نظام تخطيط موارد المؤسسات محاسبة مخزون فواتير',
            q: 'هل تقدمون أنظمة ERP؟',
            a: 'نعم. <strong>ERP Setup €1,890</strong> (تهيئة وربط أساسي)، <strong>Full ERP Sync €3,490</strong> (سلاسل إمداد ورواتب وبنوك)، و<strong>Custom ERP €5,990</strong> (بناء مخصص بالكامل).',
            link: './insights/erp-selection-2026.html', label: 'كيف تختار ERP'
        },
        {
            tags: 'سحابة سحابي cloud برمجية برمجيات منصة saas',
            q: 'ما هي باقات البرمجيات السحابية؟',
            a: 'ثلاث باقات: <strong>Core Starter €1,490</strong> لمنصة أولى، <strong>Enterprise Growth €2,890</strong> مع تطبيقات جوال وأتمتة AI، و<strong>Core MAX Synergy €4,990</strong> لمنظومة مؤسسية متعددة الفروع والعملات.',
            link: './index.html#pricing', label: 'مقارنة الباقات'
        },
        {
            tags: 'ذكاء اصطناعي ai أتمتة rpa شات بوت مساعد',
            q: 'هل تستخدمون الذكاء الاصطناعي؟',
            a: 'نعم: أتمتة RPA، استخراج الفواتير، مساعد ذكي مؤسسي (RAG) يقرأ مستندات شركتك ويجيب مع الاستشهاد، وتحليل تنبؤي. الباقة المؤسسية تشمل نموذجاً سيادياً معزولاً على أنظمتك.',
            link: './insights/ai-concierge-rag.html', label: 'مقال RAG'
        },
        {
            tags: 'أمان امن سيبراني اختراق حماية فحص أمني',
            q: 'هل تقدمون فحصاً أمنياً؟',
            a: 'نعم — <strong>Security &amp; Audit €490</strong>: فحص شامل للثغرات البرمجية والمالية مع تقرير رسمي وتوصيات إصلاح مرتبة بالأولوية.',
            link: './index.html#contact', label: 'اطلب فحصاً'
        },
        {
            tags: 'صيانة دعم شهري corecare sla',
            q: 'هل توجد باقة صيانة شهرية؟',
            a: '<strong>CoreCare Monthly €149/شهر</strong>: إدارة سحابية، نسخ احتياطي يومي، مراقبة أداء 24/7، ودعم فوري مع اتفاقية مستوى خدمة (SLA).',
            link: './index.html#pricing', label: 'تفاصيل الدعم'
        },
        {
            tags: 'باقة حزمة عرض توفير خصم انطلاقة bundle',
            q: 'هل توجد باقة موحدة بسعر أقل؟',
            a: 'نعم — <strong>باقة الانطلاقة الشاملة €1,990</strong> بدلاً من €3,020 (توفير 34%): الهوية البصرية + الموقع أو المتجر + الربط المحاسبي المالي.',
            link: './index.html#pricing', label: 'احجز الباقة'
        },
        {
            tags: 'مدة وقت كم يستغرق تسليم جاهز متى',
            q: 'كم يستغرق التنفيذ؟',
            a: 'الهوية 7–10 أيام · الموقع 2–4 أسابيع · المتجر 4–6 أسابيع · ERP 3–6 أسابيع. المدة تبدأ من اعتماد المحتوى والتصاميم، لا من تاريخ العرض.',
            link: './index.html#services-faq', label: 'الأسئلة الشائعة'
        },
        {
            tags: 'دفع دفعكم طرق الدفع stripe mollie ideal paypal تحويل',
            q: 'ما طرق الدفع؟',
            a: 'Stripe (بطاقات)، Mollie (iDEAL / Bancontact)، تحويل بنكي SEPA، وPayPal. الفواتير رسمية ومتوافقة مع ضريبة BTW الهولندية.',
            link: './index.html#pricing', label: 'الأسعار والفوترة'
        },
        {
            tags: 'ضريبة vat btw فاتورة محاسبة خصم',
            q: 'هل الأسعار تشمل الضريبة؟',
            a: 'الأسعار باليورو وتُضاف ضريبة <strong>BTW 21%</strong> حيث ينطبق. للشركات المسجلة في هولندا/الاتحاد الأوروبي الضريبة قابلة للخصم، وتصدر فاتورة رسمية متوافقة مع Belastingdienst.',
            link: './index.html#pricing', label: 'تفاصيل الفوترة'
        },
        {
            tags: 'ملكية كود مصدري ملكية الكود حقوق',
            q: 'هل أملك الكود المصدري؟',
            a: 'نعم، <strong>100%</strong>. تسليم الكود المصدري كاملاً مع الوثائق ونقل الملكية — بلا اشتراكات إجبارية ولا قيود على التعديل.',
            link: './index.html#services-faq', label: 'الأسئلة الشائعة'
        },
        {
            tags: 'استضافة دومين نطاق سيرفر هوستنج',
            q: 'هل تشمل الأسعار الاستضافة والدومين؟',
            a: 'باقة الموقع تشمل استضافة سحابية سريعة ونطاقاً مجانياً لسنة. الباقات السحابية تشمل تهيئة واستضافة مُدارة أولية، ثم يمكن الانتقال إلى CoreCare.',
            link: './index.html#services-faq', label: 'تفاصيل أكثر'
        },
        {
            tags: 'لغات لغة ترجمة عربي انجليزي هولندي',
            q: 'هل الموقع يدعم عدة لغات؟',
            a: 'نعم — الموقع الحالي يدعم <strong>29 لغة</strong> مع اتجاه صحيح للعربية والعبرية والفارسية، وتهيئة SEO لكل لغة على حدة.',
            link: './index.html', label: 'شاهد اللغات'
        },
        {
            tags: 'تجربة ديمو عرض تجريبي جرّب',
            q: 'هل يمكنني تجربة النظام قبل الشراء؟',
            a: 'نعم — النظام التجريبي السحابي متاح مباشرة، ويمكن ترتيب بيئة تجريبية ببياناتك لمدة أسبوعين قبل التوقيع.',
            link: './demo.html', label: 'افتح العرض التجريبي'
        },
        {
            tags: 'تواصل اتصال رقم هاتف واتساب بريد ايميل عنوان',
            q: 'كيف أتواصل معكم؟',
            a: 'واتساب: <a href="' + WA + '" target="_blank" rel="noopener noreferrer">+31 6 1811 1116</a><br>البريد: <a href="mailto:info@sr-coresync.com">info@sr-coresync.com</a><br>المقر: أمستردام، هولندا.',
            link: './index.html#contact', label: 'نموذج التواصل'
        },
        {
            tags: 'استشارة مجانية حجز موعد اجتماع',
            q: 'هل توجد استشارة مجانية؟',
            a: 'نعم — استشارة تنفيذية <strong>30 دقيقة مجاناً</strong>: نراجع وضعك الحالي ونعطيك خطة عملية واضحة بلا التزام.',
            link: WA, label: 'احجز الآن', external: true
        },
        {
            tags: 'مدونة مقالات رؤى insights',
            q: 'هل لديكم مقالات متخصصة؟',
            a: 'نعم — مدونة الرؤى فيها مقالات عن ERP، تكاليف السحابة، RAG، تحويل المتاجر، Zero Trust، وعائد الهوية.',
            link: './blog.html', label: 'افتح المدونة'
        },
        {
            tags: 'شركاء وكيل وكلاء white label ترخيص',
            q: 'هل يوجد برنامج شركاء أو وكلاء؟',
            a: 'نعم — بوابة الشركاء والوكلاء (White-Label) مع تراخيص متعددة الكيانات: خصم 10% لكيانين إلى ثلاثة، و20% لأربعة كيانات أو أكثر.',
            link: './partner-portal.html', label: 'بوابة الشركاء'
        },
        {
            tags: 'خصوصية gdpr بيانات كوكيز',
            q: 'كيف تتعاملون مع الخصوصية؟',
            a: 'نلتزم بلائحة GDPR الأوروبية: لا نبيع بيانات، والقياس مجهول بلا تعريف شخصي، ويمكنك رفض القياس ويبقى الموقع يعمل كاملاً.',
            link: './privacy.html', label: 'سياسة الخصوصية'
        },
        {
            tags: 'تدريب فريق شرح ورشة',
            q: 'هل تقدمون تدريباً للفريق؟',
            a: 'نعم — جلسات تدريب وورشة تشغيل ضمن الباقات المؤسسية، مع وثائق تشغيلية وفيديوهات قصيرة لفريقك.',
            link: './index.html#service', label: 'الخدمات'
        }
    ];

    /* ---------------- text utilities ---------------- */
    function normalize(text) {
        return String(text || '')
            .toLowerCase()
            .replace(/[\u064B-\u0652\u0670\u0640]/g, '')
            .replace(/[أإآٱ]/g, 'ا')
            .replace(/ى/g, 'ي')
            .replace(/ؤ/g, 'و')
            .replace(/ئ/g, 'ي')
            .replace(/ة/g, 'ه')
            .replace(/[^\u0621-\u064Aa-z0-9\s]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function tokenize(text) {
        return normalize(text).split(' ').filter(function (t) { return t.length >= 2; });
    }

    function esc(text) {
        return String(text).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    /* ---------------- retrieval ---------------- */
    function findBest(question) {
        var nq = normalize(question);
        var tokens = tokenize(question);
        var best = null;
        var bestScore = 0;

        KB.forEach(function (item) {
            var tags = normalize(item.tags);
            var qText = normalize(item.q);
            var aText = normalize(item.a);
            var score = 0;

            if (nq.length > 3 && tags.indexOf(nq) !== -1) { score += 10; }

            tokens.forEach(function (t) {
                if (tags.indexOf(t) !== -1) { score += 4; }
                if (qText.indexOf(t) !== -1) { score += 3; }
                if (aText.indexOf(t) !== -1) { score += 1; }
            });

            if (score > bestScore) { bestScore = score; best = item; }
        });

        return { item: best, score: bestScore };
    }

    function greetingReply(text) {
        var n = normalize(text);
        if (/^(مرحبا|اهلا|السلام|هاي|hi|hello|hey|bonjour|hallo)/.test(n)) {
            return 'أهلاً بك في <strong>S&amp;R CoreSync</strong> 👋<br>أنا المساعد الذكي القائم على محتوى الموقع (خدمات، أسعار، مقالات). اسألني ما تشاء، أو اختر من الاقتراحات أدناه.';
        }
        return null;
    }

    function humanReply(text) {
        var n = normalize(text);
        if (/(انسان|موظف|شخص|تحدث مع|اكلم|واتساب|اتصال|مباشر)/.test(n)) {
            return 'بكل تأكيد — التحويل إلى فريق بشري فوري:<br><a href="' + WA + '" target="_blank" rel="noopener noreferrer">فتح واتساب مباشر</a><br>أو البريد: <a href="mailto:info@sr-coresync.com">info@sr-coresync.com</a>';
        }
        return null;
    }

    function answerFor(text) {
        var g = greetingReply(text);
        if (g) { return { html: g }; }

        var h = humanReply(text);
        if (h) { return { html: h }; }

        var result = findBest(text);
        if (result.item && result.score >= 4) {
            var item = result.item;
            var link = item.external ? item.link : item.link;
            var html = item.a + '<br><a href="' + esc(link) + '"' + (item.external ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + esc(item.label) + ' ←</a>';
            return { html: html };
        }

        return {
            html: 'لم أجد إجابة دقيقة في محتوى الموقع لهذا السؤال. يمكنك:<br>' +
                '• تجربة كلمة أخرى (مثلاً: <em>السعر</em>، <em>ERP</em>، <em>مدة التنفيذ</em>)<br>' +
                '• <a href="' + WA + '" target="_blank" rel="noopener noreferrer">التحدث مع فريق بشري على واتساب</a>'
        };
    }

    /* ---------------- DOM ---------------- */
    var fab, panel, body, form, input, chips;
    var history = [];
    var HISTORY_KEY = 'sr-concierge-history';

    function loadHistory() {
        try {
            var raw = sessionStorage.getItem(HISTORY_KEY);
            if (raw) { history = JSON.parse(raw) || []; }
        } catch (e) { history = []; }
    }

    function saveHistory() {
        try {
            sessionStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(-30)));
        } catch (e) {}
    }

    function addMessage(role, html, meta) {
        var el = document.createElement('div');
        el.className = 'srx-msg srx-msg--' + role;
        el.innerHTML = html + (meta ? '<span class="srx-msg__meta">' + meta + '</span>' : '');
        body.appendChild(el);
        body.scrollTop = body.scrollHeight;
        return el;
    }

    function showTyping() {
        var el = document.createElement('div');
        el.className = 'srx-msg srx-msg--bot';
        el.setAttribute('data-typing', '1');
        el.innerHTML = '<span class="srx-typing" aria-label="جارٍ الكتابة"><i></i><i></i><i></i></span>';
        body.appendChild(el);
        body.scrollTop = body.scrollHeight;
        return el;
    }

    function reply(text) {
        var typing = showTyping();
        setTimeout(function () {
            typing.remove();
            var out = answerFor(text);
            addMessage('bot', out.html, 'من محتوى الموقع');
            history.push({ r: 'bot', t: out.html });
            saveHistory();
        }, 420 + Math.random() * 420);
    }

    function send(text) {
        var clean = (text || '').trim();
        if (!clean) { return; }

        addMessage('user', esc(clean));
        history.push({ r: 'user', t: clean });
        saveHistory();

        if (window.srTrack) { window.srTrack('concierge_message', { q: clean.slice(0, 80) }); }

        var n = normalize(clean);
        if (/(عرض سعر|rfq|اقتباس|عرض سعر رسمي)/.test(n)) {
            setTimeout(function () {
                var typing = showTyping();
                setTimeout(function () {
                    typing.remove();
                    var html = 'يمكنك إرسال طلب عرض سعر رسمي مباشرة.' +
                        '<br><button type="button" data-srx-action="rfq" style="margin-top:0.5rem;padding:0.4rem 0.8rem;border-radius:8px;border:1px solid rgba(197,168,128,0.5);background:rgba(197,168,128,0.15);color:#f3dfba;font-family:inherit;font-weight:700;cursor:pointer;">📋 فتح نموذج RFQ</button>' +
                        '<br><a href="' + WA + '" target="_blank" rel="noopener noreferrer">أو اطلبه عبر واتساب ←</a>';
                    var el = addMessage('bot', html, 'طلب عرض سعر');
                    el.querySelector('[data-srx-action="rfq"]').addEventListener('click', function () {
                        if (typeof window.openRfqModal === 'function') {
                            window.openRfqModal('web');
                        } else {
                            window.location.href = WA;
                        }
                        if (window.srTrack) { window.srTrack('concierge_rfq', {}); }
                    });
                }, 500);
            }, 200);
            return;
        }

        reply(clean);
    }

    function renderHistory() {
        if (!history.length) { return; }
        var recent = history.slice(-8);
        recent.forEach(function (m) {
            addMessage(m.r === 'user' ? 'user' : 'bot', m.r === 'user' ? esc(m.t) : m.t);
        });
        addMessage('bot', 'أكمل من حيث توقفت 👇', '');
    }

    function build() {
        fab = document.createElement('button');
        fab.type = 'button';
        fab.className = 'srx-concierge-fab';
        fab.setAttribute('aria-label', 'المساعد الذكي — اسأل عن الخدمات والأسعار');
        fab.setAttribute('aria-controls', 'srConciergePanel');
        fab.setAttribute('aria-expanded', 'false');
        fab.innerHTML = '<span class="srx-concierge-fab__dot" aria-hidden="true"></span> اسأل المساعد 🤖';

        panel = document.createElement('section');
        panel.className = 'srx-concierge';
        panel.id = 'srConciergePanel';
        panel.hidden = true;
        panel.setAttribute('role', 'dialog');
        panel.setAttribute('aria-label', 'المساعد الذكي S&R CoreSync');
        panel.innerHTML =
            '<header class="srx-concierge__head">' +
                '<strong>المساعد الذكي<small>إجابات من محتوى الموقع · متصل</small></strong>' +
                '<span class="srx-spacer"></span>' +
                '<button type="button" data-act="wa" aria-label="التحدث مع فريق بشري على واتساب" title="واتساب">💬</button>' +
                '<button type="button" data-act="close" aria-label="إغلاق المساعد" title="إغلاق">✕</button>' +
            '</header>' +
            '<div class="srx-concierge__body" id="srConciergeBody" role="log" aria-live="polite" aria-relevant="additions"></div>' +
            '<div class="srx-concierge__chips" role="group" aria-label="أسئلة سريعة"></div>' +
            '<form class="srx-concierge__form" autocomplete="off">' +
                '<label for="srConciergeInput" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">سؤالك</label>' +
                '<input id="srConciergeInput" type="text" placeholder="اكتب سؤالك… مثال: كم سعر المتجر؟" maxlength="300">' +
                '<button type="submit" aria-label="إرسال السؤال">➤</button>' +
            '</form>' +
            '<div class="srx-concierge__foot">' +
                '<span>يعمل محلياً — لا تُرسل بياناتك لأي طرف.</span>' +
                '<a href="./blog.html">المدونة ←</a>' +
            '</div>';

        document.body.appendChild(fab);
        document.body.appendChild(panel);

        body = panel.querySelector('#srConciergeBody');
        form = panel.querySelector('form');
        input = panel.querySelector('#srConciergeInput');
        chips = panel.querySelector('.srx-concierge__chips');

        var quick = ['أسعار الباقات', 'ERP', 'مدة التنفيذ', 'ذكاء اصطناعي', 'طلب عرض سعر', 'تحدث مع إنسان'];
        quick.forEach(function (label) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'srx-chip-btn';
            b.textContent = label;
            b.addEventListener('click', function () { send(label); });
            chips.appendChild(b);
        });

        fab.addEventListener('click', open);
        panel.querySelector('[data-act="close"]').addEventListener('click', close);
        panel.querySelector('[data-act="wa"]').addEventListener('click', function () {
            if (window.srTrack) { window.srTrack('concierge_whatsapp', {}); }
            window.open(WA, '_blank', 'noopener');
        });

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var value = input.value;
            input.value = '';
            send(value);
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && !panel.hidden) { close(); }
        });
    }

    var seeded = false;

    function open() {
        panel.hidden = false;
        fab.hidden = true;
        fab.setAttribute('aria-expanded', 'true');

        if (!seeded) {
            seeded = true;
            loadHistory();
            renderHistory();
            if (!history.length) {
                addMessage('bot', 'أهلاً بك 👋 أنا مساعد <strong>S&amp;R CoreSync</strong>.<br>اسألني عن <strong>الأسعار</strong>، <strong>ERP</strong>، <strong>مدة التنفيذ</strong>، أو اطلب <strong>عرض سعر</strong>.', '');
            }
        }
        input.focus();
        if (window.srTrack) { window.srTrack('concierge_open', {}); }
    }

    function close() {
        panel.hidden = true;
        fab.hidden = false;
        fab.setAttribute('aria-expanded', 'false');
        fab.focus();
    }

    function init() {
        build();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
