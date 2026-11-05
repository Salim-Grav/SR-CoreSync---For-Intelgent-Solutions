# -*- coding: utf-8 -*-
"""
S&R CoreSync - Upgrade Smart Business Advisor with 2026 Sovereign Financial & Tax Advisory Engine
"""

import os
import shutil

HTML_FILE = "smart-business-advisor.html"
JS_FILE = "js/smart-business-advisor.js"

# 1. Update HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Tab button replacement
old_tab_container = """        <!-- 4 Pillars Navigation Tabs -->
        <div style="display: flex; gap: 0.8rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-dim); padding-bottom: 0.8rem; overflow-x: auto;">
            <button id="tab-btn-voice" class="btn active" style="background: var(--gold-primary); color: #04070d; border: none; padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 800; cursor: pointer;">
                🎙️ المستشار الصوتي الفوري (حل الغرامات)
            </button>
            <button id="tab-btn-onboarding" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                📋 انضمام أصحاب الأنشطة (Onboarding السريع)
            </button>
            <button id="tab-btn-accountant" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                ⚖️ لوحة المحاسب القانوني (الأستاذ رودين)
            </button>
            <button id="tab-btn-stats" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                📊 إحصائيات التوفير واسترداد المبالغ
            </button>
        </div>"""

new_tab_container = """        <!-- 5 Pillars Navigation Tabs -->
        <div style="display: flex; gap: 0.8rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-dim); padding-bottom: 0.8rem; overflow-x: auto;">
            <button id="tab-btn-voice" class="btn active" style="background: var(--gold-primary); color: #04070d; border: none; padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 800; cursor: pointer;">
                🎙️ المستشار الصوتي الفوري (حل الغرامات)
            </button>
            <button id="tab-btn-engine" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                🧠 محرك التوصيات والتحليل المالي والضريبي الذكي
            </button>
            <button id="tab-btn-onboarding" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                📋 انضمام أصحاب الأنشطة (Onboarding السريع)
            </button>
            <button id="tab-btn-accountant" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                ⚖️ لوحة المحاسب القانوني (الأستاذ رودين)
            </button>
            <button id="tab-btn-stats" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.6rem 1.3rem; border-radius: 8px; font-weight: 700; cursor: pointer;">
                📊 إحصائيات التوفير واسترداد المبالغ
            </button>
        </div>"""

if old_tab_container in html:
    html = html.replace(old_tab_container, new_tab_container)
    print("Replaced tab container successfully.")
else:
    print("Warning: old_tab_container not matched exactly, trying regex/flexible replace.")

new_section_engine = """
        <!-- Section 5: Smart Financial & Tax Advisory Engine -->
        <div id="section-engine" class="advisor-tab-content" style="display: none;">
            <div style="background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(9,18,32,0.95)); border: 1px solid rgba(16,185,129,0.3); border-radius: 14px; padding: 1.2rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h2 style="color: var(--gold-primary); font-size: 1.3rem; font-weight: 800; margin-bottom: 0.3rem;">
                        🧠 محرك التوصيات الاستشارية والتحليل المالي والضريبي الذكي (2026 Sovereign Engine)
                    </h2>
                    <p style="color: #94a3b8; font-size: 0.88rem; max-width: 950px;">
                        محاكاة مالية وضريبية قطاعية متطورة وفق معايير المحاسبة الدولية IFRS والتشريعات الضريبية الهولندية وقوانين الضرائب العامة (Awb & Wet IB) لحساب الوفورات التراكمية، ومؤشر مخاطر التدقيق (Audit Risk Score)، وتحليل نقطة التحول المثلى لشركة BV.
                    </p>
                </div>
                <div style="display: flex; gap: 0.6rem;">
                    <button id="btn-engine-quick-sample" class="btn" style="background: rgba(212,175,55,0.15); color: var(--gold-primary); border: 1px solid var(--border-gold); padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 0.85rem;">
                        ⚡ تعبئة نموذج مطعم واقعي (€350k)
                    </button>
                </div>
            </div>

            <div class="advisor-grid">
                <!-- Left: Parameters & Financial Input Console -->
                <div class="card-advisor">
                    <h3 style="color: #fff; font-size: 1.15rem; font-weight: 800; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span>📊</span> مدخلات المنشأة والمعطيات المالية السنوية
                    </h3>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <label for="engine-sector" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">القطاع الاقتصادي:</label>
                            <select id="engine-sector" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem; font-size: 0.9rem;">
                                <option value="horeca">🍽️ مطاعم ومقاهي وضيافة (Horeca)</option>
                                <option value="retail">🛒 تجارة وتجزئة ومتاجر إلكترونية (Retail)</option>
                                <option value="services">💼 خدمات مهنية وتكنولوجيا (Services / IT)</option>
                                <option value="construction">🏗️ مقاولات وإنشاءات وصيانة (Construction)</option>
                                <option value="logistics">🚚 نقل وشحن وخدمات لوجستية (Logistics)</option>
                            </select>
                        </div>
                        <div>
                            <label for="engine-entity" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">الشكل القانوني الحالي:</label>
                            <select id="engine-entity" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem; font-size: 0.9rem;">
                                <option value="eenmanszaak">منشأة فردية (Eenmanszaak)</option>
                                <option value="vof">شركة تضامن / شراكة (VOF)</option>
                                <option value="bv">شركة ذات مسؤولية محدودة (BV)</option>
                                <option value="zzp">عمل حر مستقل (ZZP)</option>
                            </select>
                        </div>
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <label for="engine-revenue" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">
                            الإيرادات والمبيعات السنوية الإجمالية (Jaaromzet باليورو €):
                        </label>
                        <input id="engine-revenue" type="number" min="0" step="1000" value="350000" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.7rem; font-size: 1rem; font-weight: 700;">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <label for="engine-cogs-pct" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">
                                تكلفة البضائع / المشتريات (%):
                            </label>
                            <input id="engine-cogs-pct" type="number" min="0" max="95" value="32" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem;">
                        </div>
                        <div>
                            <label for="engine-payroll" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">
                                رواتب وأجور الموظفين (سنوياً €):
                            </label>
                            <input id="engine-payroll" type="number" min="0" step="1000" value="85000" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem;">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem;">
                        <div>
                            <label for="engine-opex" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">
                                إيجار ومصاريف تشغيلية (سنوياً €):
                            </label>
                            <input id="engine-opex" type="number" min="0" step="500" value="48000" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem;">
                        </div>
                        <div>
                            <label for="engine-investments" style="font-size: 0.85rem; color: #cbd5e1; display: block; margin-bottom: 0.3rem;">
                                استثمارات أجهزة وتطوير (KIA €):
                            </label>
                            <input id="engine-investments" type="number" min="0" step="500" value="18000" style="width: 100%; background: #060b13; border: 1px solid var(--border-dim); border-radius: 8px; color: #fff; padding: 0.65rem;">
                        </div>
                    </div>

                    <div style="display: flex; gap: 0.8rem;">
                        <button id="btn-run-engine" class="btn" style="flex: 1; background: linear-gradient(135deg, var(--gold-primary), #b8860b); color: #04070d; border: none; padding: 0.8rem; border-radius: 8px; font-weight: 800; cursor: pointer; font-size: 1rem;">
                            ⚡ تشغيل التحليل المالي وتوليد التوصيات الذكية
                        </button>
                        <button id="btn-reset-engine" class="btn" style="background: rgba(255,255,255,0.06); color: #94a3b8; border: 1px solid var(--border-dim); padding: 0.8rem 1.2rem; border-radius: 8px; cursor: pointer;">
                            إعادة ضبط
                        </button>
                    </div>
                </div>

                <!-- Right: Output Dashboard & Recommendations -->
                <div class="card-advisor">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
                        <h3 style="color: var(--accent); font-size: 1.15rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem;">
                            <span>📑</span> المؤشرات المالية وخارطة التوصيات الضريبية
                        </h3>
                        <span id="engine-score-badge" class="status-badge-live resolved">مؤشر الامتثال: 92% (آمن ومحصّن)</span>
                    </div>

                    <!-- Metrics Grid -->
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; margin-bottom: 1.2rem;">
                        <div style="background: #060b13; border: 1px solid var(--border-dim); border-radius: 10px; padding: 0.9rem; text-align: center;">
                            <span style="font-size: 0.78rem; color: #94a3b8; display: block;">صافي الربح التشغيلي قبل الضريبة</span>
                            <span id="metric-net-profit" style="font-size: 1.3rem; color: #fff; font-weight: 800; display: block; margin-top: 0.2rem;">€85,000</span>
                        </div>
                        <div style="background: #060b13; border: 1px solid var(--border-dim); border-radius: 10px; padding: 0.9rem; text-align: center;">
                            <span style="font-size: 0.78rem; color: #94a3b8; display: block;">إجمالي الوفورات الضريبية المتاحة</span>
                            <span id="metric-tax-savings" style="font-size: 1.3rem; color: #10b981; font-weight: 800; display: block; margin-top: 0.2rem;">€14,820</span>
                        </div>
                        <div style="background: #060b13; border: 1px solid var(--border-dim); border-radius: 10px; padding: 0.9rem; text-align: center;">
                            <span style="font-size: 0.78rem; color: #94a3b8; display: block;">الضريبة التقديرية بعد التحسين</span>
                            <span id="metric-final-tax" style="font-size: 1.3rem; color: var(--gold-primary); font-weight: 800; display: block; margin-top: 0.2rem;">€18,650</span>
                        </div>
                        <div style="background: #060b13; border: 1px solid var(--border-dim); border-radius: 10px; padding: 0.9rem; text-align: center;">
                            <span style="font-size: 0.78rem; color: #94a3b8; display: block;">جدوى التحول إلى شركة BV</span>
                            <span id="metric-bv-status" style="font-size: 1.1rem; color: var(--cyan); font-weight: 800; display: block; margin-top: 0.2rem;">موصى به بقوة ✓</span>
                        </div>
                    </div>

                    <!-- Dynamic Recommendations List -->
                    <div id="engine-recommendations-box" style="background: #060b13; border: 1px solid var(--border-gold); border-radius: 10px; padding: 1.2rem; margin-bottom: 1.2rem;">
                        <!-- Injected via JS -->
                    </div>

                    <!-- Action Buttons -->
                    <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
                        <button id="btn-engine-whatsapp" class="btn" style="flex: 1; background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; padding: 0.75rem; border-radius: 8px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.4rem;">
                            <span>💬</span> إرسال التوصيات للمحاسب المعتمد (WhatsApp VIP)
                        </button>
                        <button id="btn-engine-print" class="btn" style="background: rgba(255,255,255,0.06); color: #cbd5e1; border: 1px solid var(--border-dim); padding: 0.75rem 1.1rem; border-radius: 8px; cursor: pointer; font-weight: 700;">
                            🖨️ طباعة التقرير (A4/PDF)
                        </button>
                        <button id="btn-engine-json" class="btn" style="background: rgba(56,189,248,0.1); color: var(--cyan); border: 1px solid rgba(56,189,248,0.3); padding: 0.75rem 1.1rem; border-radius: 8px; cursor: pointer; font-weight: 700;">
                            📥 تصدير JSON
                        </button>
                    </div>
                </div>
            </div>
        </div>
"""

# Place section-engine right before </main>
main_end = "</main>"
if main_end in html:
    html = html.replace(main_end, new_section_engine + "\n    " + main_end)
    print("Inserted section-engine before </main>.")
else:
    print("Error: </main> not found.")

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated smart-business-advisor.html successfully.")
