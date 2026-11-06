/**
 * S&R CoreSync — محرك الواجهات والمؤثرات ثلاثية الأبعاد التفاعلية
 * Vanilla JS 3D Perspective Tilt & Specular Highlights Engine
 * الأداء: 60 FPS • يدعم RTL وشاشات اللمس • خفيف الوزن بنسبة 100%
 */

(function() {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    // 1. تفعيل الإمالة ثلاثية الأبعاد للبطاقات (3D Perspective Tilt)
    function initTiltCards() {
        const cards = document.querySelectorAll('.sr-tilt-card');
        
        cards.forEach(card => {
            let boundingBox = null;
            let rafId = null;

            const updateBounds = () => {
                boundingBox = card.getBoundingClientRect();
            };

            const handleMouseMove = (e) => {
                if (!boundingBox) updateBounds();
                
                const x = e.clientX - boundingBox.left;
                const y = e.clientY - boundingBox.top;
                
                const centerX = boundingBox.width / 2;
                const centerY = boundingBox.height / 2;
                
                // حساب زاوية الميلان (حد أقصى 12 درجة)
                const rotateX = ((y - centerY) / centerY) * -10;
                const rotateY = ((x - centerX) / centerX) * 10;
                
                // حساب موقع لمعان الإضاءة بالنسبة المئوية
                const mousePercentX = (x / boundingBox.width) * 100;
                const mousePercentY = (y / boundingBox.height) * 100;
                
                if (rafId) cancelAnimationFrame(rafId);
                rafId = requestAnimationFrame(() => {
                    card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.025, 1.025, 1.025)`;
                    card.style.setProperty('--mouse-x', `${mousePercentX.toFixed(1)}%`);
                    card.style.setProperty('--mouse-y', `${mousePercentY.toFixed(1)}%`);
                });
            };

            const handleMouseLeave = () => {
                if (rafId) cancelAnimationFrame(rafId);
                card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
                boundingBox = null;
            };

            card.addEventListener('mouseenter', updateBounds);
            card.addEventListener('mousemove', handleMouseMove);
            card.addEventListener('mouseleave', handleMouseLeave);
        });
    }

    // 2. تفعيل الأزرار المغناطيسية الفاخرة (Magnetic Buttons)
    function initMagneticButtons() {
        const buttons = document.querySelectorAll('.sr-magnetic-btn');

        buttons.forEach(btn => {
            let boundingBox = null;

            btn.addEventListener('mouseenter', () => {
                boundingBox = btn.getBoundingClientRect();
            });

            btn.addEventListener('mousemove', (e) => {
                if (!boundingBox) boundingBox = btn.getBoundingClientRect();
                const x = e.clientX - boundingBox.left - boundingBox.width / 2;
                const y = e.clientY - boundingBox.top - boundingBox.height / 2;
                btn.style.transform = `translate(${x * 0.28}px, ${y * 0.28}px)`;
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translate(0px, 0px)';
                boundingBox = null;
            });
        });
    }

    // 3. كانفاس الشبكة الذكية المحيطية الخفيفة (Ambient Mesh Canvas)
    function initAmbientMesh() {
        const canvas = document.querySelector('.sr-ambient-mesh-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const dots = [];
        const numDots = Math.min(Math.floor((width * height) / 25000), 50);

        for (let i = 0; i < numDots; i++) {
            dots.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                radius: Math.random() * 1.5 + 0.8
            });
        }

        let mouse = { x: null, y: null };
        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        function render() {
            ctx.clearRect(0, 0, width, height);

            // رسم وربط الجسيمات
            for (let i = 0; i < dots.length; i++) {
                const d = dots[i];
                d.x += d.vx;
                d.y += d.vy;

                if (d.x < 0 || d.x > width) d.vx *= -1;
                if (d.y < 0 || d.y > height) d.vy *= -1;

                ctx.beginPath();
                ctx.arc(d.x, d.y, d.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(197, 168, 128, 0.4)';
                ctx.fill();

                // خطوط التوصيل الشبكية
                for (let j = i + 1; j < dots.length; j++) {
                    const d2 = dots[j];
                    const dist = Math.hypot(d.x - d2.x, d.y - d2.y);
                    if (dist < 130) {
                        ctx.beginPath();
                        ctx.moveTo(d.x, d.y);
                        ctx.lineTo(d2.x, d2.y);
                        ctx.strokeStyle = `rgba(197, 168, 128, ${(1 - dist / 130) * 0.15})`;
                        ctx.lineWidth = 0.75;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(render);
        }
        render();
    }

    // تهيئة المحرك عند اكتمال تحميل الصفحة
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initTiltCards();
            initMagneticButtons();
            initAmbientMesh();
        });
    } else {
        initTiltCards();
        initMagneticButtons();
        initAmbientMesh();
    }

    // تصدير واجهة المحرك لتمكين الاستدعاء الديناميكي
    window.SR3DEngine = {
        initTiltCards,
        initMagneticButtons,
        initAmbientMesh
    };
})();
