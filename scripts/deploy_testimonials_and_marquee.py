# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
S&R CoreSync - Deploy Testimonials Slider & Infinite Brand Marquee
Across All 29 Language Portals and Core CSS/JS Suites
"""
import os
import re
import glob

CSS_TESTIMONIALS_MARQUEE = """
/* ==========================================================================
   S&R CORESYNC - NATIVE TESTIMONIAL CAROUSEL & INFINITE BRAND MARQUEE
   Ultra-Smooth Zero-Dependency Architecture (Milestone 31)
   ========================================================================== */

/* 1. Testimonial Section & Carousel */
.section-testimonial {
    position: relative !important;
    overflow: hidden !important;
    padding-top: clamp(48px, 6vw, 84px) !important;
    padding-bottom: clamp(60px, 8vw, 100px) !important;
}

.swiper-testimonial,
.tf-swiper.swiper-testimonial {
    visibility: visible !important;
    opacity: 1 !important;
    overflow: hidden !important;
    position: relative !important;
    width: 100% !important;
    max-width: 1380px !important;
    margin: 0 auto !important;
    padding: 32px 16px 20px !important;
    direction: ltr !important; /* Uniform LTR horizontal slider coordinate system */
}

.swiper-testimonial .swiper-wrapper {
    display: flex !important;
    flex-wrap: nowrap !important;
    width: 100% !important;
    transition: transform 0.65s cubic-bezier(0.22, 1, 0.36, 1) !important;
    will-change: transform !important;
    box-sizing: border-box !important;
}

.swiper-testimonial .swiper-slide {
    flex: 0 0 100% !important;
    max-width: 100% !important;
    width: 100% !important;
    box-sizing: border-box !important;
    padding: 0 14px !important;
    transition: opacity 0.45s ease, transform 0.45s ease !important;
    opacity: 0.45;
    transform: scale(0.96);
    cursor: grab;
}

.swiper-testimonial .swiper-slide:active {
    cursor: grabbing;
}

.swiper-testimonial .swiper-slide.is-active,
.swiper-testimonial .swiper-slide.swiper-slide-active,
.swiper-testimonial .swiper-slide.swiper-slide-visible {
    opacity: 1 !important;
    transform: scale(1) !important;
}

@media (min-width: 768px) {
    .swiper-testimonial .swiper-slide {
        flex: 0 0 50% !important;
        max-width: 50% !important;
        width: 50% !important;
    }
}

@media (min-width: 1200px) {
    .swiper-testimonial .swiper-slide {
        flex: 0 0 33.333333% !important;
        max-width: 33.333333% !important;
        width: 33.333333% !important;
    }
}

/* Luxury Glassmorphic Testimonial Card Styling */
.testimonial-v01 {
    position: relative !important;
    min-height: 320px !important;
    background: radial-gradient(circle at 50% 0%, rgba(26, 36, 30, 0.88) 0%, rgba(9, 14, 12, 0.96) 100%) !important;
    border: 1px solid rgba(197, 168, 128, 0.22) !important;
    border-radius: 22px !important;
    padding: 34px 28px 28px !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.75), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    transition: border-color 0.35s ease, box-shadow 0.35s ease, transform 0.35s ease !important;
}

[dir="rtl"] .testimonial-v01,
html[lang="ar"] .testimonial-v01,
html[lang="ckb"] .testimonial-v01,
html[lang="ku"] .testimonial-v01 {
    direction: rtl !important;
    text-align: right !important;
}

html[dir="ltr"] .testimonial-v01,
html:not([dir="rtl"]) .testimonial-v01 {
    direction: ltr !important;
    text-align: left !important;
}

.testimonial-v01:hover {
    border-color: rgba(212, 175, 55, 0.6) !important;
    box-shadow: 0 25px 50px -10px rgba(0, 0, 0, 0.9), 0 0 25px rgba(212, 175, 55, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-4px) !important;
}

.testimonial-v01 .tes-mark--open::before {
    content: "“" !important;
    display: block !important;
    font-size: 54px !important;
    line-height: 1 !important;
    font-family: Georgia, "Times New Roman", serif !important;
    color: #c5a880 !important;
    opacity: 0.8 !important;
    text-shadow: 0 0 15px rgba(197, 168, 128, 0.4) !important;
}

.testimonial-v01 .tes-text {
    font-size: 15px !important;
    line-height: 1.75 !important;
    color: #e5e5e0 !important;
    margin: 16px 0 20px !important;
    font-weight: 300 !important;
    position: relative !important;
    z-index: 1 !important;
}

.testimonial-v01 .tes-author {
    margin-top: auto !important;
    padding-top: 14px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.testimonial-v01 .author_info {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.testimonial-v01 .tes-rating {
    margin: 0 0 10px 0 !important;
    color: #c5a880 !important;
    display: flex !important;
    justify-content: center !important;
}

.testimonial-v01 .tes-rating svg {
    display: block !important;
    fill: #c5a880 !important;
    filter: drop-shadow(0 0 4px rgba(197, 168, 128, 0.45)) !important;
}

.testimonial-v01 .info__name {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #f3dfba !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    margin: 0 0 4px 0 !important;
}

.testimonial-v01 .info__duty {
    font-size: 13px !important;
    color: #9ca3af !important;
    margin: 0 !important;
}

/* Slider Controls & Dots */
.group-btn-slider {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 20px !important;
    margin-top: 36px !important;
    position: relative !important;
    z-index: 10 !important;
}

.group-btn-slider .nav-prev-swiper,
.group-btn-slider .nav-next-swiper {
    width: 44px !important;
    height: 44px !important;
    border-radius: 50% !important;
    background: rgba(12, 21, 17, 0.85) !important;
    border: 1px solid rgba(197, 168, 128, 0.35) !important;
    color: #f3dfba !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
}

.group-btn-slider .nav-prev-swiper:hover,
.group-btn-slider .nav-next-swiper:hover {
    border-color: #f3dfba !important;
    color: #ffffff !important;
    background: rgba(197, 168, 128, 0.25) !important;
    transform: scale(1.08) !important;
    box-shadow: 0 0 20px rgba(197, 168, 128, 0.4) !important;
}

.group-btn-slider .nav-prev-swiper svg,
.group-btn-slider .nav-next-swiper svg {
    pointer-events: none;
}

.tf-sw-pagination {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.tf-sw-pagination .swiper-pagination-bullet {
    width: 8px !important;
    height: 8px !important;
    border-radius: 50% !important;
    background: rgba(255, 255, 255, 0.25) !important;
    border: none !important;
    padding: 0 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.tf-sw-pagination .swiper-pagination-bullet:hover {
    background: rgba(243, 223, 186, 0.6) !important;
}

.tf-sw-pagination .swiper-pagination-bullet.swiper-pagination-bullet-active {
    width: 24px !important;
    border-radius: 8px !important;
    background: #c5a880 !important;
    box-shadow: 0 0 10px rgba(197, 168, 128, 0.55) !important;
}

/* 2. Brand Marquee Continuous Motion */
.section-brand--marquee {
    position: relative !important;
    overflow: hidden !important;
    padding: clamp(32px, 4vw, 56px) 0 clamp(40px, 5vw, 64px) !important;
}

.brand-marquee {
    position: relative !important;
    width: 100% !important;
    overflow: hidden !important;
    direction: ltr !important; /* Uniform LTR horizontal scrolling stream */
    mask-image: linear-gradient(90deg, transparent 0%, rgba(0,0,0,1) 12%, rgba(0,0,0,1) 88%, transparent 100%) !important;
    -webkit-mask-image: linear-gradient(90deg, transparent 0%, rgba(0,0,0,1) 12%, rgba(0,0,0,1) 88%, transparent 100%) !important;
    padding: 16px 0 !important;
}

.brand-marquee__track {
    display: flex !important;
    width: max-content !important;
    will-change: transform !important;
    animation: srBrandInfiniteMarquee 26s linear infinite !important;
}

.brand-marquee:hover .brand-marquee__track {
    animation-play-state: paused !important;
}

.brand-marquee__set {
    display: flex !important;
    align-items: center !important;
    gap: clamp(36px, 5.5vw, 72px) !important;
    padding: 0 clamp(18px, 2.75vw, 36px) !important;
    flex-shrink: 0 !important;
}

.img-brand {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 0.65 !important;
    filter: grayscale(100%) brightness(1.2) !important;
    transition: opacity 0.35s ease, filter 0.35s ease, transform 0.35s ease !important;
    cursor: pointer !important;
}

.img-brand:hover {
    opacity: 1 !important;
    filter: grayscale(0%) brightness(1.35) drop-shadow(0 0 16px rgba(197, 168, 128, 0.45)) !important;
    transform: scale(1.1) translateY(-3px) !important;
}

.img-brand img {
    max-height: 44px !important;
    width: auto !important;
    max-width: 180px !important;
    object-fit: contain !important;
    pointer-events: none !important;
}

@keyframes srBrandInfiniteMarquee {
    0% {
        transform: translate3d(0, 0, 0);
    }
    100% {
        transform: translate3d(-50%, 0, 0);
    }
}
"""

JS_TESTIMONIALS = """/**
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
"""

def main():
    print("1. Writing js/sr-testimonials.js...")
    with open('js/sr-testimonials.js', 'w', encoding='utf-8') as f:
        f.write(JS_TESTIMONIALS)

    print("2. Appending CSS to css/inline-core.css...")
    with open('css/inline-core.css', 'r', encoding='utf-8') as f:
        core_css = f.read()
    if 'srBrandInfiniteMarquee' not in core_css:
        with open('css/inline-core.css', 'a', encoding='utf-8') as f:
            f.write("\n" + CSS_TESTIMONIALS_MARQUEE)
        print("   Appended to css/inline-core.css")
    else:
        print("   Already present in css/inline-core.css")

    print("3. Appending CSS to css/enterprise-suite.css...")
    with open('css/enterprise-suite.css', 'r', encoding='utf-8') as f:
        suite_css = f.read()
    if 'srBrandInfiniteMarquee' not in suite_css:
        with open('css/enterprise-suite.css', 'a', encoding='utf-8') as f:
            f.write("\n" + CSS_TESTIMONIALS_MARQUEE)
        print("   Appended to css/enterprise-suite.css")
    else:
        print("   Already present in css/enterprise-suite.css")

    # Minify enterprise-suite.css to enterprise-suite.min.css
    print("4. Minifying enterprise-suite.css...")
    try:
        minified = re.sub(r'/\*.*?\*/', '', suite_css + "\n" + CSS_TESTIMONIALS_MARQUEE, flags=re.S)
        minified = re.sub(r'\s+', ' ', minified)
        minified = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', minified)
        with open('css/enterprise-suite.min.css', 'w', encoding='utf-8') as f:
            f.write(minified.strip())
        print("   Minified to css/enterprise-suite.min.css")
    except Exception as e:
        print("   Error minifying:", e)

    # 5. Inject script tag into all 29 language portals
    all_portals = ['index.html'] + glob.glob('*/index.html')
    # Filter out archive or non-portal index files if any
    valid_portals = [p for p in all_portals if not p.startswith('_') and not 'archive' in p]
    print(f"5. Injecting script into {len(valid_portals)} language portals...")

    for portal in valid_portals:
        is_sub = '/' in portal or '\\' in portal
        script_path = '../js/sr-testimonials.js' if is_sub else './js/sr-testimonials.js'
        script_tag = f'<script src="{script_path}" defer></script>'

        with open(portal, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'sr-testimonials.js' not in content:
            # Place it right after sr-events.js or before </body>
            if '<script src="' in content and 'sr-events.js' in content:
                content = content.replace('sr-events.js" defer></script>', f'sr-events.js" defer></script>\n    {script_tag}')
            elif '</body>' in content:
                content = content.replace('</body>', f'    {script_tag}\n</body>')
            
            with open(portal, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   Injected in {portal}")
        else:
            print(f"   Already in {portal}")

    print("\nDeployment completed successfully!")

if __name__ == '__main__':
    main()
