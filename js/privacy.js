/* ==========================================================================
   S&R CoreSync — privacy.html controls
   ========================================================================== */
(function () {
    'use strict';

    function init() {
        var btn = document.getElementById('resetConsent');
        var status = document.getElementById('resetStatus');
        if (!btn) { return; }

        btn.addEventListener('click', function () {
            try {
                localStorage.removeItem('sr-analytics-consent');
                localStorage.removeItem('sr-analytics-events');
                localStorage.removeItem('sr-analytics-vitals');
            } catch (e) {}

            if (status) {
                status.textContent = '✅ تم مسح الخيار والقياسات المحلية. أعد تحميل الصفحة لاختيار من جديد.';
            }

            setTimeout(function () {
                location.reload();
            }, 1600);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
