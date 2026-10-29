/* ==========================================================================
   S&R CoreSync — Insights / Blog interactions
   - category filter + live search (blog.html)
   - reading progress bar (insights/*.html)
   ========================================================================== */
(function () {
    'use strict';

    function initFilters() {
        var grid = document.getElementById('srPostGrid');
        if (!grid) { return; }

        var posts = Array.prototype.slice.call(grid.querySelectorAll('[data-post]'));
        var chips = Array.prototype.slice.call(document.querySelectorAll('.sr-chip'));
        var search = document.getElementById('srPostSearch');
        var empty = document.getElementById('srPostEmpty');
        var activeCat = 'all';

        function apply() {
            var term = search ? search.value.trim().toLowerCase() : '';
            var visible = 0;

            posts.forEach(function (post) {
                var cat = (post.getAttribute('data-cat') || '').toLowerCase();
                var text = (post.textContent || '').toLowerCase();
                var catOk = activeCat === 'all' || cat === activeCat;
                var termOk = !term || text.indexOf(term) !== -1;
                var show = catOk && termOk;
                post.hidden = !show;
                if (show) { visible += 1; }
            });

            if (empty) { empty.hidden = visible !== 0; }

            var status = document.getElementById('srPostStatus');
            if (status) {
                status.textContent = visible === 0
                    ? 'لا توجد نتائج مطابقة.'
                    : 'عدد المقالات المعروضة: ' + visible;
            }
        }

        chips.forEach(function (chip) {
            chip.addEventListener('click', function () {
                activeCat = (chip.getAttribute('data-cat') || 'all').toLowerCase();
                chips.forEach(function (c) {
                    c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
                });
                apply();
            });
        });

        if (search) {
            search.addEventListener('input', apply);
        }

        apply();
    }

    function initProgress() {
        var bar = document.getElementById('srProgress');
        if (!bar) { return; }

        function update() {
            var doc = document.documentElement;
            var max = doc.scrollHeight - doc.clientHeight;
            var ratio = max > 0 ? (doc.scrollTop || document.body.scrollTop) / max : 0;
            bar.style.transform = 'scaleX(' + Math.min(1, Math.max(0, ratio)) + ')';
        }

        window.addEventListener('scroll', update, { passive: true });
        window.addEventListener('resize', update);
        update();
    }

    function init() {
        initFilters();
        initProgress();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
