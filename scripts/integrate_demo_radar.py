import os

def integrate_demo():
    path = 'demo.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert Radar section right before </section> of tab-cloud
    target_cloud = '📑 طلب خطة الترحيل المخصصة (Blueprint)\n                        </button>\n                    </div>\n                </div>\n            </section>'
    
    radar_markup = '''📑 طلب خطة الترحيل المخصصة (Blueprint)
                        </button>
                    </div>
                </div>

                <!-- 🎯 رادار المعمارية والتقنيات السيادية التفاعلي (Interactive Tech Radar & Layered Topology) -->
                <div class="glass-box mt-4" id="section-tech-radar" style="border: 1px solid rgba(197, 168, 128, 0.35); box-shadow: 0 20px 50px rgba(0,0,0,0.6); border-radius: 20px; padding: 26px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; padding: 4px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 800; margin-bottom: 8px;">
                                <span>🎯 رادار المعمارية الحية • S&amp;R Sovereign Interactive Tech Radar</span>
                            </div>
                            <h3 style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 0 0 4px 0;">رادار التقنيات والمخطط المعماري التفاعلي للعملاء والشركاء</h3>
                            <p style="font-size: 0.86rem; color: #94a3b8; margin: 0;">انقر على أي عقدة تقنية في الرادار لاستعراض مواصفات المعمارية وشهادات الاعتماد الأوروبية والضمانات اللحظية:</p>
                        </div>
                        <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; padding: 6px 16px; border-radius: 999px; font-size: 0.78rem; font-weight: 800;">🟢 Live Topology Active</span>
                    </div>

                    <!-- Topology Filter Tabs -->
                    <div style="display: flex; gap: 8px; margin-bottom: 20px; overflow-x: auto; padding-bottom: 4px;">
                        <button type="button" class="demo-topo-tab active" data-layer="all" style="background: #c5a880; color: #010907; border: 1px solid #c5a880; font-family: inherit; font-size: 0.82rem; font-weight: 800; padding: 8px 16px; border-radius: 10px; cursor: pointer; transition: all 0.2s;">🌐 الرادار الكلي (All Tech)</button>
                        <button type="button" class="demo-topo-tab" data-layer="ai" style="background: rgba(0,0,0,0.5); color: #94a3b8; border: 1px solid rgba(197, 168, 128, 0.25); font-family: inherit; font-size: 0.82rem; font-weight: 700; padding: 8px 16px; border-radius: 10px; cursor: pointer; transition: all 0.2s;">🤖 طبقة الذكاء الاصطناعي</button>
                        <button type="button" class="demo-topo-tab" data-layer="cloud" style="background: rgba(0,0,0,0.5); color: #94a3b8; border: 1px solid rgba(197, 168, 128, 0.25); font-family: inherit; font-size: 0.82rem; font-weight: 700; padding: 8px 16px; border-radius: 10px; cursor: pointer; transition: all 0.2s;">☁️ طبقة السحابة والمخازن</button>
                        <button type="button" class="demo-topo-tab" data-layer="security" style="background: rgba(0,0,0,0.5); color: #94a3b8; border: 1px solid rgba(197, 168, 128, 0.25); font-family: inherit; font-size: 0.82rem; font-weight: 700; padding: 8px 16px; border-radius: 10px; cursor: pointer; transition: all 0.2s;">🛡️ طبقة الأمن والفوترة</button>
                    </div>

                    <!-- Radar Grid Display -->
                    <div style="display: grid; grid-template-columns: 1.25fr 1fr; gap: 20px; align-items: stretch;">
                        <!-- Radar Screen -->
                        <div style="background: radial-gradient(circle at center, rgba(16, 185, 129, 0.08) 0%, rgba(0,0,0,0.7) 75%); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 18px; min-height: 380px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;" id="demoTechRadarArea">
                            <div style="position: absolute; width: 100px; height: 100px; border: 1px dashed rgba(197, 168, 128, 0.3); border-radius: 50%; pointer-events: none;"></div>
                            <div style="position: absolute; width: 200px; height: 200px; border: 1px dashed rgba(197, 168, 128, 0.25); border-radius: 50%; pointer-events: none;"></div>
                            <div style="position: absolute; width: 310px; height: 310px; border: 1px dashed rgba(197, 168, 128, 0.2); border-radius: 50%; pointer-events: none;"></div>
                            <div style="position: absolute; width: 320px; height: 320px; border-radius: 50%; background: conic-gradient(from 0deg, rgba(16, 185, 129, 0.25) 0deg, transparent 60deg); animation: radarSweepAnim 5s linear infinite; pointer-events: none;"></div>

                            <!-- Interactive Radar Nodes -->
                            <div class="radar-node-interactive active" style="position: absolute; top: 22%; left: 26%; background: #c5a880; color: #010907; border: 1px solid #c5a880; padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 800; cursor: pointer; box-shadow: 0 0 20px rgba(197, 168, 128, 0.6); z-index: 5;" data-tech="ai-private">🤖 Private LLM Core</div>
                            <div class="radar-node-interactive" style="position: absolute; top: 18%; right: 20%; background: rgba(14, 28, 22, 0.95); color: #ffffff; border: 1px solid rgba(197, 168, 128, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 5;" data-tech="cloud-ams">☁️ Amsterdam DC</div>
                            <div class="radar-node-interactive" style="position: absolute; top: 56%; left: 14%; background: rgba(14, 28, 22, 0.95); color: #ffffff; border: 1px solid rgba(197, 168, 128, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 5;" data-tech="peppol">💳 PEPPOL Gateway</div>
                            <div class="radar-node-interactive" style="position: absolute; bottom: 18%; left: 36%; background: rgba(14, 28, 22, 0.95); color: #ffffff; border: 1px solid rgba(197, 168, 128, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 5;" data-tech="eidas">🛡️ eIDAS Signature</div>
                            <div class="radar-node-interactive" style="position: absolute; top: 58%; right: 16%; background: rgba(14, 28, 22, 0.95); color: #ffffff; border: 1px solid rgba(197, 168, 128, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 5;" data-tech="zerotrust">🔒 Zero-Trust WAF</div>
                            <div class="radar-node-interactive" style="position: absolute; bottom: 18%; right: 26%; background: rgba(14, 28, 22, 0.95); color: #ffffff; border: 1px solid rgba(197, 168, 128, 0.3); padding: 6px 14px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.5); z-index: 5;" data-tech="erp-core">📦 ERP Real-Time</div>
                        </div>

                        <!-- Live Spec Card -->
                        <div style="background: rgba(7, 15, 12, 0.9); border: 1px solid rgba(197, 168, 128, 0.25); border-radius: 18px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <span id="radarSpecBadge" style="display: inline-block; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; padding: 3px 12px; border-radius: 999px; font-size: 0.74rem; font-weight: 800; margin-bottom: 10px;">🤖 الذكاء الاصطناعي السيادي</span>
                                <h4 id="radarSpecTitle" style="font-size: 1.22rem; font-weight: 800; color: #ffffff; margin: 0 0 8px 0;">Private LLM Core • النماذج اللغوية المعزولة</h4>
                                <p id="radarSpecDesc" style="font-size: 0.86rem; color: #94a3b8; line-height: 1.65; margin: 0 0 16px 0;">محرك ذكاء اصطناعي مؤسسي يتم تنصيبه على خوادم سحابية هولندية خاصة، معزولة تماماً عن أي وصول أو تدريب عام لضمان سرية القرارات والمستندات بنسبة 100%.</p>
                                
                                <div id="radarSpecList" style="display: flex; flex-direction: column; gap: 8px;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; font-size:0.84rem;">
                                        <span style="color:#94a3b8;">معيار الأمان والخصوصية</span>
                                        <span style="font-weight:800; color:#f3dfba;">GDPR / AVG &amp; EU AI Act 2026</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; font-size:0.84rem;">
                                        <span style="color:#94a3b8;">زمن الاستجابة اللحظي</span>
                                        <span style="font-weight:800; color:#f3dfba;">&lt; 140 Milliseconds</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; font-size:0.84rem;">
                                        <span style="color:#94a3b8;">توطين البيانات</span>
                                        <span style="font-weight:800; color:#f3dfba;">أمستردام، مملكة هولندا 🇳🇱</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.45); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; font-size:0.84rem;">
                                        <span style="color:#94a3b8;">حالة التفعيل والتشغيل</span>
                                        <span style="font-weight:800; color:#34d399;">جاهز للإنتاج فوراً (Production Ready)</span>
                                    </div>
                                </div>
                            </div>
                            <div style="margin-top: 16px;">
                                <button type="button" class="btn-cert-print" style="width: 100%; text-align: center; justify-content: center;" data-sr-call="openStrategicBookingModal">
                                    📑 اعتماد وتخصيص هذه المعمارية لمشروعك
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>'''

    if target_cloud not in content:
        print('Error: target_cloud not found in demo.html!')
        return False

    content = content.replace(target_cloud, radar_markup, 1)

    # 2. Add radar animation style if needed
    if '@keyframes radarSweepAnim' not in content:
        style_inject = '<style>@keyframes radarSweepAnim { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }</style>\n</head>'
        content = content.replace('</head>', style_inject, 1)

    # 3. Add script tag for js/sr-tech-radar.js before </body>
    if 'src="./js/sr-tech-radar.js"' not in content:
        script_inject = '<script src="./js/sr-tech-radar.js"></script>\n</body>'
        content = content.replace('</body>', script_inject, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: demo.html integrated!')
    return True

if __name__ == '__main__':
    integrate_demo()
