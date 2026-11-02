import os

def integrate_index():
    path = 'index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    target = '</section>\n\n        <!-- 3. قسم الأعمال والمشاريع المختارة'
    if target not in content:
        print('Target not found in index.html!')
        return False

    pillar_html = '''</section>

        <!-- 2.5 قسم الركائز التكنولوجية السيادية الست (The 6 Sovereign Tech Pillars) -->
        <section class="flat-spacing section-tech-pillars" id="tech-pillars" data-section style="padding: 4.5rem 0 3.5rem; position: relative;">
            <div class="container">
                <div class="text-center" style="max-width: 820px; margin: 0 auto 3rem;">
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); color: #f3dfba; padding: 6px 18px; border-radius: 999px; font-size: 0.82rem; font-weight: 800; margin-bottom: 14px;">
                        <span>🏛️ الركائز التكنولوجية السيادية • S&amp;R Sovereign Tech Ecosystem</span>
                    </div>
                    <h2 class="text-display-2 letter-space--3" style="font-size: clamp(1.8rem, 3vw, 2.4rem); font-weight: 900; margin-bottom: 12px; background: linear-gradient(135deg, #ffffff 40%, #c5a880); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        هندسة تكنولوجية سيادية للمؤسسات الكبرى والدبلوماسية
                    </h2>
                    <p style="color: #94a3b8; font-size: 1rem; line-height: 1.65; margin: 0;">
                        ستة أقسام هندسية متكاملة تضمن الامتثال الأوروبي الصارم، عزل البيانات اللحظي، وأداءً فائقاً لا يقبل المساومة لعملائنا في هولندا والاتحاد الأوروبي والشرق الأوسط.
                    </p>
                </div>

                <div class="pillars-showcase-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px; margin-bottom: 30px;">
                    <!-- 1. AI Agents -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">🤖</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 معزول • 99.99%</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">الذكاء الاصطناعي السيادي والوكلاء</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">Autonomous AI Agents &amp; Enterprise LLMs</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                وكلاء أذكياء ذاتيو التشغيل لتنفيذ المهام المعقدة، مع نماذج لغوية مؤسسية خاصة (Private LLMs) معزولة 100% عن أي تدريب خارجي لحماية البيانات والقرارات الدبلوماسية والتجارية.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Private LLM</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">RAG Pipelines</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">EU AI Act 2026</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">&lt; 140ms</div><div style="font-size: 0.68rem; color: #94a3b8;">سرعة الاستجابة</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">100%</div><div style="font-size: 0.68rem; color: #94a3b8;">عزل البيانات</div></div>
                        </div>
                    </div>

                    <!-- 2. Sovereign Cloud -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">☁️</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 أمستردام AMS-IX</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">الحوسبة السحابية والبنية المعزولة</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">Sovereign Zero-Trust Cloud &amp; Microservices</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                خوادم سحابية فائقة الأمان في مراكز بيانات أمستردام، ترحيل سحابي بلا توقف (Zero-Downtime)، مع الامتثال الصارم لتوجيهات الاتحاد الأوروبي NIS2 و GDPR.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Amsterdam Tier-IV</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Kubernetes</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">NIS2 Compliant</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">99.995%</div><div style="font-size: 0.68rem; color: #94a3b8;">ضمان SLA</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">&lt; 8ms</div><div style="font-size: 0.68rem; color: #94a3b8;">زمن الوصول بأوروبا</div></div>
                        </div>
                    </div>

                    <!-- 3. ERP & Core -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">📦</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 تدفق فوري</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">النظم المؤسسية وسلاسل الإمداد</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">Next-Gen Enterprise ERP &amp; Real-Time Sync</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                إدارة الموارد والمستودعات وسلاسل الإمداد وتتبع الشحنات والطلبات التلقائية بدقة متناهية، مع لوحات قيادة تنفيذية تعكس الأداء المالي اللحظي.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Enterprise ERP</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">PostgreSQL</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Redis Cache</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">100K+</div><div style="font-size: 0.68rem; color: #94a3b8;">عملية بالدقيقة</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">0 Latency</div><div style="font-size: 0.68rem; color: #94a3b8;">مزامنة المخازن</div></div>
                        </div>
                    </div>

                    <!-- 4. FinTech & PEPPOL -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">💳</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 معتمد PEPPOL</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">التكنولوجيا المالية والامتثال الضريبي</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">FinTech, PEPPOL &amp; ViDA Compliance</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                الفوترة الإلكترونية عبر شبكة PEPPOL الدولية، الربط الضريبي اللحظي مع Belastingdienst الهولندي، والتكامل المباشر مع iDEAL و SEPA و Stripe.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">PEPPOL UBL 2.1</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Belastingdienst</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">iDEAL / SEPA</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">28 دولة</div><div style="font-size: 0.68rem; color: #94a3b8;">نظام ضريبي مدعوم</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">100%</div><div style="font-size: 0.68rem; color: #94a3b8;">مطابقة ViDA</div></div>
                        </div>
                    </div>

                    <!-- 5. Cybersecurity & eIDAS -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">🛡️</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 معتمد eIDAS</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">الأمن السيبراني والتوقيع الرقمي</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">Cybersecurity, Cryptography &amp; eIDAS</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                توقيع العقود والمستندات الرقمية المعتمد قانونياً بمحاكم الاتحاد الأوروبي (eIDAS No 910/2014)، تشفير عسكري AES-256، وبوابات Zero-Trust ضد الاختراق.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">eIDAS Qualified</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">AES-256 GCM</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Zero-Trust WAF</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">256-bit</div><div style="font-size: 0.68rem; color: #94a3b8;">تشفير سيادي</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">100%</div><div style="font-size: 0.68rem; color: #94a3b8;">إلزامية المحاكم</div></div>
                        </div>
                    </div>

                    <!-- 6. Next-Gen Web -->
                    <div class="pillar-showcase-card" style="background: rgba(10, 24, 18, 0.85); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 20px; padding: 26px 22px; backdrop-filter: blur(16px); display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                        <div>
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                                <div style="width: 50px; height: 50px; border-radius: 12px; background: rgba(197, 168, 128, 0.12); border: 1px solid rgba(197, 168, 128, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.6rem;">⚡</div>
                                <span style="font-size: 0.74rem; color: #34d399; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700;">🟢 100/100 Core Vitals</span>
                            </div>
                            <h3 style="font-size: 1.18rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">منصات وتطبيقات الويب الفائقة</h3>
                            <div style="font-size: 0.78rem; color: #c5a880; font-weight: 700; margin-bottom: 10px;">Next-Gen Web Platforms &amp; Headless UI</div>
                            <p style="font-size: 0.86rem; color: #94a3b8; line-height: 1.6; margin-bottom: 16px;">
                                منصات وبوابات عملاء سحابية فائقة السرعة بتصميم زجاجي معتم فاخر، استوديو العلامة البيضاء المخصص (White-Label)، ودعم تلقائي لـ 28 لغة وعملة.
                            </p>
                            <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px;">
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">Glassmorphism</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">White-Label</span>
                                <span style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #e2e8f0; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px;">PWA / Edge Cache</span>
                            </div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 10px; text-align: center;">
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">&lt; 0.6s</div><div style="font-size: 0.68rem; color: #94a3b8;">سرعة التحميل</div></div>
                            <div><div style="color: #c5a880; font-weight: 900; font-size: 1.1rem;">100/100</div><div style="font-size: 0.68rem; color: #94a3b8;">نقاط الأداء</div></div>
                        </div>
                    </div>
                </div>

                <div class="text-center" style="margin-top: 15px;">
                    <a href="demo.html" class="btn-live-sandbox-header" style="font-size: 0.92rem; padding: 11px 26px; display: inline-flex; align-items: center; gap: 10px;">
                        <span>🎯 تجربة رادار المعمارية والتقنيات التفاعلي المباشر (Interactive Tech Radar)</span>
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </a>
                </div>
            </div>
        </section>

        <!-- 3. قسم الأعمال والمشاريع المختارة'''

    updated_content = content.replace(target, pillar_html, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print('SUCCESS: index.html integrated!')
    return True

if __name__ == '__main__':
    integrate_index()
