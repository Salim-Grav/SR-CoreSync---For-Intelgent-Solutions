/**
 * S&R CoreSync - Native Sovereign Testimonials Carousel Engine
 * Zero-dependency, Touch-friendly, Responsive, Auto-looping
 */
(function() {
    function initTestimonialCarousel() {
        var container = document.querySelector('.swiper-testimonial');
        if (!container) return;

        var wrapper = container.querySelector('.swiper-wrapper');
        if (!wrapper) return;

        var slides = Array.from(wrapper.querySelectorAll('.swiper-slide'));
        if (!slides.length) return;

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
                if (!isHovered) {
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

        // Polyfill window.Swiper constructor if anything calls it
        if (typeof window.Swiper === 'undefined') {
            window.Swiper = function() {
                return window.testimonialSwiper;
            };
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTestimonialCarousel);
    } else {
        initTestimonialCarousel();
    }
})();
