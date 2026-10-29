/* ==========================================================================
   S&R CoreSync — NFC card enhancements
   • Native share / copy link
   • vCard + QR download tracking
   • Card view tracking (profile aware)
   ========================================================================== */
(function () {
    'use strict';

    function track(name, props) {
        if (typeof window.srTrack === 'function') { window.srTrack(name, props || {}); }
    }

    function currentProfile() {
        try {
            return new URLSearchParams(location.search).get('id') || 'salim';
        } catch (e) {
            return 'salim';
        }
    }

    function clearUrl() {
        var url = location.origin + location.pathname;
        var id = currentProfile();
        if (id) { url += '?id=' + encodeURIComponent(id); }
        return url;
    }

    function toast(msg) {
        var node = document.getElementById('nfcEnhanceToast');
        if (!node) {
            node = document.createElement('div');
            node.id = 'nfcEnhanceToast';
            node.setAttribute('role', 'status');
            node.setAttribute('aria-live', 'polite');
            node.style.cssText = [
                'position:fixed',
                'inset-inline:1rem',
                'bottom:1rem',
                'z-index:99999',
                'max-width:420px',
                'margin-inline:auto',
                'padding:0.7rem 1rem',
                'border-radius:12px',
                'border:1px solid rgba(16,185,129,0.45)',
                'background:rgba(4,20,14,0.98)',
                'color:#d1fae5',
                'font-family:Alexandria,Tajawal,system-ui,sans-serif',
                'font-size:0.8rem',
                'text-align:center',
                'box-shadow:0 24px 60px -30px rgba(0,0,0,0.9)'
            ].join(';');
            document.body.appendChild(node);
        }
        node.textContent = msg;
        node.hidden = false;
        clearTimeout(toast._t);
        toast._t = setTimeout(function () { node.hidden = true; }, 3200);
    }

    function copyFallback(text) {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
        ta.remove();
        return ok;
    }

    function copyLink() {
        var link = clearUrl();
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(link).then(function () {
                toast('✅ تم نسخ رابط البطاقة.');
                track('nfc_link_copied', { profile: currentProfile() });
            }).catch(function () {
                if (copyFallback(link)) {
                    toast('✅ تم نسخ رابط البطاقة.');
                    track('nfc_link_copied', { profile: currentProfile() });
                } else {
                    toast('تعذّر النسخ — انسخ الرابط من شريط العنوان.');
                }
            });
            return;
        }
        if (copyFallback(link)) {
            toast('✅ تم نسخ رابط البطاقة.');
            track('nfc_link_copied', { profile: currentProfile() });
        } else {
            toast('تعذّر النسخ — انسخ الرابط من شريط العنوان.');
        }
    }

    function shareCard() {
        var data = {
            title: 'S&R CoreSync — بطاقة أعمال رقمية',
            text: 'بطاقة S&R CoreSync الرقمية — احفظ جهة الاتصال أو افتح البطاقة مباشرة.',
            url: clearUrl()
        };

        if (navigator.share) {
            navigator.share(data).then(function () {
                track('nfc_share', { profile: currentProfile(), method: 'native' });
            }).catch(function (err) {
                if (err && err.name === 'AbortError') { return; }
                copyLink();
            });
            return;
        }
        copyLink();
    }

    function buildShareButton() {
        var host = document.querySelector('.nfc-secondary-actions');
        if (!host || document.getElementById('nfcShareBtn')) { return; }

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.id = 'nfcShareBtn';
        btn.className = 'nfc-sub-btn';
        btn.innerHTML = '<span aria-hidden="true">🔗</span><span>مشاركة البطاقة</span>';
        btn.addEventListener('click', shareCard);

        var copy = document.createElement('button');
        copy.type = 'button';
        copy.id = 'nfcCopyBtn';
        copy.className = 'nfc-sub-btn';
        copy.innerHTML = '<span aria-hidden="true">📋</span><span>نسخ الرابط</span>';
        copy.addEventListener('click', copyLink);

        host.appendChild(btn);
        host.appendChild(copy);
    }

    function bindDownloads() {
        var vcf = document.getElementById('cardSaveVcfBtn');
        if (vcf) {
            vcf.addEventListener('click', function () {
                track('nfc_vcf_download', { profile: currentProfile() });
            });
        }

        var qr = document.getElementById('cardQrDownloadLink');
        if (qr) {
            qr.addEventListener('click', function () {
                track('nfc_qr_download', { profile: currentProfile() });
            });
        }
    }

    function init() {
        buildShareButton();
        bindDownloads();
        track('nfc_card_view', { profile: currentProfile() });

        window.addEventListener('hashchange', function () {
            track('nfc_card_view', { profile: currentProfile() });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
