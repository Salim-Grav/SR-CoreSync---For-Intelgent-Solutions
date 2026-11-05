(() => {
    const videos = document.querySelectorAll('video[data-lazy-src]');
    if (!videos.length) return;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const loadVideo = (video) => {
        if (video.dataset.lazyPoster) {
            video.poster = video.dataset.lazyPoster;
            delete video.dataset.lazyPoster;
        }
        if (video.dataset.lazySrc) {
            video.src = video.dataset.lazySrc;
            delete video.dataset.lazySrc;
            video.load();
        }
    };

    if (!('IntersectionObserver' in window)) {
        videos.forEach(loadVideo);
        return;
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            const video = entry.target;
            if (entry.isIntersecting) {
                loadVideo(video);
                if (!reducedMotion && video.dataset.lazyAutoplay === 'true') {
                    video.play().catch(() => {});
                }
            } else {
                video.pause();
            }
        });
    }, { rootMargin: '200px 0px' });

    videos.forEach((video) => observer.observe(video));
})();
