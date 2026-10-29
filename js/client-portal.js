/* ==========================================================================
   S&R CoreSync — Client Portal (demo)
   --------------------------------------------------------------------------
   This is a CLIENT-SIDE DEMO gate. It does not authenticate against a server
   and must never be presented as real security. Production requires an auth
   backend (OIDC/SSO) + database. All data stays in this browser.
   ========================================================================== */
(function () {
    'use strict';

    var DEMO_EMAIL = 'client@demo.sr-coresync.com';
    var DEMO_CODE = 'SRX-2026';
    var SESSION_KEY = 'sr-portal-session';
    var TICKETS_KEY = 'sr-portal-tickets';
    var SESSION_MINUTES = 30;
    var REMEMBER_DAYS = 7;

    var el = {};
    var timer = null;

    function $(id) { return document.getElementById(id); }

    function cacheEls() {
        el.auth = $('srpAuth');
        el.main = $('srpMain');
        el.form = $('srpLoginForm');
        el.email = $('srpEmail');
        el.code = $('srpCode');
        el.remember = $('srpRemember');
        el.loginBtn = $('srpLoginBtn');
        el.error = $('srpAuthError');
        el.ok = $('srpAuthOk');
        el.chip = $('srpUserChip');
        el.session = $('srpSession');
        el.countdown = $('srpCountdown');
        el.userName = $('srpUserName');
        el.userRole = $('srpUserRole');
        el.avatar = $('srpAvatar');
        el.heroName = $('srpHeroName');
        el.logout = $('srpLogout');
        el.lastSync = $('srpLastSync');
        el.ticketForm = $('srpTicketForm');
        el.ticketSubject = $('srpTicketSubject');
        el.ticketDetails = $('srpTicketDetails');
        el.ticketPriority = $('srpTicketPriority');
        el.ticketsList = $('srpTicketsList');
        el.ticketCount = $('srpTicketCount');
        el.ticketsBadge = $('srpTicketsBadge');
        el.toast = $('srpToast');
    }

    /* ---------------- storage ---------------- */
    function readSession() {
        var raw = null;
        try { raw = sessionStorage.getItem(SESSION_KEY) || localStorage.getItem(SESSION_KEY); } catch (e) {}
        if (!raw) { return null; }
        try {
            var s = JSON.parse(raw);
            if (!s || !s.expires || s.expires < Date.now()) {
                clearSession();
                return null;
            }
            return s;
        } catch (e) {
            clearSession();
            return null;
        }
    }

    function clearSession() {
        try {
            sessionStorage.removeItem(SESSION_KEY);
            localStorage.removeItem(SESSION_KEY);
        } catch (e) {}
    }

    function writeSession(session, remember) {
        clearSession();
        try {
            (remember ? localStorage : sessionStorage).setItem(SESSION_KEY, JSON.stringify(session));
        } catch (e) {}
    }

    function readTickets() {
        try {
            var raw = localStorage.getItem(TICKETS_KEY);
            return raw ? (JSON.parse(raw) || []) : [];
        } catch (e) { return []; }
    }

    function writeTickets(list) {
        try { localStorage.setItem(TICKETS_KEY, JSON.stringify(list.slice(0, 30))); } catch (e) {}
    }

    /* ---------------- helpers ---------------- */
    function displayName(email) {
        if (email === DEMO_EMAIL) { return 'شركة النور للتجارة'; }
        var local = String(email).split('@')[0] || 'عميل';
        local = local.replace(/[._-]+/g, ' ').trim();
        return local.charAt(0).toUpperCase() + local.slice(1);
    }

    function initials(name) {
        var parts = String(name).trim().split(/\s+/).filter(Boolean);
        if (!parts.length) { return 'ع'; }
        return parts[0].charAt(0) + (parts[1] ? parts[1].charAt(0) : '');
    }

    function showError(msg) {
        el.error.textContent = msg;
        el.error.hidden = false;
    }

    function hideError() {
        el.error.hidden = true;
        el.error.textContent = '';
    }

    function toast(msg) {
        el.toast.textContent = msg;
        el.toast.hidden = false;
        clearTimeout(toast._t);
        toast._t = setTimeout(function () { el.toast.hidden = true; }, 3600);
    }

    function track(name, props) {
        if (typeof window.srTrack === 'function') { window.srTrack(name, props || {}); }
    }

    /* ---------------- session UI ---------------- */
    function renderSession(session) {
        var name = session.name || displayName(session.email);

        el.auth.hidden = true;
        el.main.hidden = false;
        el.chip.hidden = false;
        el.session.hidden = false;
        el.logout.hidden = false;

        el.userName.textContent = name;
        el.avatar.textContent = initials(name);
        el.heroName.textContent = name;

        el.lastSync.textContent = new Date().toLocaleString('ar-NL', {
            dateStyle: 'medium', timeStyle: 'short'
        });

        startCountdown(session.expires);
        renderTickets();
    }

    function renderLoggedOut() {
        el.auth.hidden = false;
        el.main.hidden = true;
        el.chip.hidden = true;
        el.session.hidden = true;
        el.logout.hidden = true;
        if (timer) { clearInterval(timer); timer = null; }
    }

    function startCountdown(expires) {
        if (timer) { clearInterval(timer); }

        function tick() {
            var left = Math.max(0, expires - Date.now());
            if (left <= 0) {
                clearInterval(timer);
                timer = null;
                clearSession();
                renderLoggedOut();
                el.ok.hidden = true;
                showError('انتهت الجلسة تلقائياً بعد 30 دقيقة من عدم النشاط. سجّل الدخول من جديد.');
                el.email.focus();
                return;
            }
            var m = Math.floor(left / 60000);
            var s = Math.floor((left % 60000) / 1000);
            el.countdown.textContent = m + ':' + (s < 10 ? '0' : '') + s;
        }

        tick();
        timer = setInterval(tick, 1000);
    }

    /* ---------------- login ---------------- */
    function validate(email, code) {
        if (!email) { return 'أدخل البريد الإلكتروني.'; }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { return 'صيغة البريد الإلكتروني غير صحيحة.'; }
        if (!code) { return 'أدخل رمز الوصول.'; }
        if (code.trim().toUpperCase() !== DEMO_CODE) {
            return 'رمز الوصول غير صحيح. في النسخة التجريبية استخدم SRX-2026.';
        }
        if (email.toLowerCase() !== DEMO_EMAIL) {
            return 'الحساب غير موجود في النسخة التجريبية. استخدم client@demo.sr-coresync.com.';
        }
        return null;
    }

    function handleLogin(e) {
        e.preventDefault();
        hideError();

        var email = (el.email.value || '').trim().toLowerCase();
        var code = (el.code.value || '').trim();
        var remember = !!(el.remember && el.remember.checked);

        var problem = validate(email, code);
        if (problem) {
            showError(problem);
            el.email.setAttribute('aria-invalid', email ? 'false' : 'true');
            el.code.setAttribute('aria-invalid', code ? 'false' : 'true');
            (email ? el.code : el.email).focus();
            track('portal_login_failed', { reason: 'validation' });
            return;
        }

        el.loginBtn.disabled = true;
        el.loginBtn.textContent = 'جارٍ التحقق…';

        setTimeout(function () {
            var ttl = (remember ? REMEMBER_DAYS * 24 * 60 : SESSION_MINUTES) * 60 * 1000;
            var session = {
                email: email,
                name: displayName(email),
                expires: Date.now() + ttl,
                remember: remember
            };
            writeSession(session, remember);

            el.loginBtn.disabled = false;
            el.loginBtn.textContent = 'دخول آمن ←';
            el.code.value = '';
            el.ok.hidden = false;
            el.ok.textContent = '✅ تم تسجيل الدخول بنجاح.';
            renderSession(session);
            track('portal_login', { remember: remember });
            toast('مرحباً ' + session.name + ' — تم فتح لوحتك.');
        }, 520);
    }

    /* ---------------- logout ---------------- */
    function handleLogout() {
        clearSession();
        renderLoggedOut();
        el.ok.hidden = true;
        hideError();
        el.email.value = '';
        el.code.value = '';
        el.email.focus();
        track('portal_logout', {});
    }

    /* ---------------- tickets ---------------- */
    function ticketItem(ticket) {
        var li = document.createElement('li');
        var ico = document.createElement('span');
        ico.className = 'srp-ico';
        ico.setAttribute('aria-hidden', 'true');
        ico.textContent = '🎫';

        var wrap = document.createElement('span');
        var title = document.createElement('b');
        title.textContent = ticket.subject;

        var meta = document.createElement('span');
        var when = new Date(ticket.at).toLocaleDateString('ar-NL', { day: 'numeric', month: 'short' });
        meta.textContent = '#' + ticket.id + ' · ' + when + ' · ' + ticket.priority;

        wrap.appendChild(title);
        wrap.appendChild(meta);
        li.appendChild(ico);
        li.appendChild(wrap);
        return li;
    }

    function renderTickets() {
        var tickets = readTickets();
        var open = tickets.length + 1;

        if (tickets.length && el.ticketsList) {
            var heading = el.ticketsList.firstElementChild;
            el.ticketsList.innerHTML = '';
            if (heading) { el.ticketsList.appendChild(heading); }
            tickets.forEach(function (t) { el.ticketsList.appendChild(ticketItem(t)); });
        }

        if (el.ticketCount) { el.ticketCount.textContent = String(open); }
        if (el.ticketsBadge) { el.ticketsBadge.textContent = open + ' مفتوحة'; }
    }

    function handleTicket(e) {
        e.preventDefault();
        var subject = (el.ticketSubject.value || '').trim();
        var details = (el.ticketDetails.value || '').trim();

        if (subject.length < 4 || details.length < 10) {
            toast('أكمل الموضوع (4 أحرف) والتفاصيل (10 أحرف) على الأقل.');
            (subject.length < 4 ? el.ticketSubject : el.ticketDetails).focus();
            return;
        }

        var tickets = readTickets();
        var ticket = {
            id: 'SR-' + Math.floor(1000 + Math.random() * 9000),
            subject: subject,
            details: details.slice(0, 600),
            priority: el.ticketPriority ? el.ticketPriority.value : 'عادية',
            at: Date.now()
        };
        tickets.unshift(ticket);
        writeTickets(tickets);

        el.ticketForm.reset();
        renderTickets();
        toast('✅ أُنشئت التذكرة ' + ticket.id + ' (محلياً).');
        track('portal_ticket_created', { priority: ticket.priority });

        if (subject.toLowerCase().indexOf('urgent') !== -1) {
            window.open('https://wa.me/31618111116', '_blank', 'noopener');
        }
    }

    /* ---------------- boot ---------------- */
    function init() {
        cacheEls();

        el.form.addEventListener('submit', handleLogin);
        el.logout.addEventListener('click', handleLogout);
        if (el.ticketForm) { el.ticketForm.addEventListener('submit', handleTicket); }

        el.email.addEventListener('input', function () {
            el.email.setAttribute('aria-invalid', 'false');
            hideError();
        });
        el.code.addEventListener('input', function () {
            el.code.setAttribute('aria-invalid', 'false');
            hideError();
        });

        var existing = readSession();
        if (existing) {
            renderSession(existing);
            track('portal_session_restored', {});
        } else {
            renderLoggedOut();
        }

        document.addEventListener('keydown', function (ev) {
            if (ev.key === 'Escape' && !el.toast.hidden) { el.toast.hidden = true; }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
