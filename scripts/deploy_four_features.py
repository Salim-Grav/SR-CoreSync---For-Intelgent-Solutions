# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - 4 High-Conversion Enterprise Features Injector
Injects:
1. VIP Branded Client Proposal Engine Banner (with instant company name input)
2. Interactive Smart ROI & Cost Savings Calculator Tab (3 sliders + live gold counters)
3. Direct VIP Founders Hotline Widget (Pre-filled Localized WhatsApp & Direct Call)
4. Enhanced E-Invoicing Simulator with custom client details
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(BASE_DIR, 'demo.html')
DEMO_EN_PATH = os.path.join(BASE_DIR, 'en', 'demo.html')

# HTML Component: Feature 1 (VIP Proposal Banner - Arabic)
VIP_BANNER_AR = """
            <!-- Feature 1: مولّد عروض الأسعار اللحظي باسم شركة العميل -->
            <div class="vip-proposal-banner">
                <div class="vip-banner-content">
                    <div class="vip-badge">✨ محرك عروض الأسعار التنفيذية المخصصة</div>
                    <h4 class="vip-title">توليد عرض رسمي فوري باسم شركتك (Branded Proposal Dossier)</h4>
                    <p class="vip-desc">أدخل اسم شركتك وسيتم توليد ملف PDF تنفيذي فوري متكامل معتمد يحمل اسم منشأتك والتسعير والضريبة المحلية.</p>
                </div>
                <div class="vip-banner-actions">
                    <input type="text" id="quickClientNameInput" class="vip-input" placeholder="أدخل اسم شركتك هنا..." oninput="updatePdfClientName(this.value)" />
                    <button type="button" class="vip-btn-gold" onclick="openExecutivePdfModal()">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                        <span>تصدير عرض السعر (PDF)</span>
                    </button>
                </div>
            </div>
"""

# HTML Component: Feature 1 (VIP Proposal Banner - English)
VIP_BANNER_EN = """
            <!-- Feature 1: Instant Branded Client Proposal Engine -->
            <div class="vip-proposal-banner">
                <div class="vip-banner-content">
                    <div class="vip-badge">✨ Enterprise Branded Proposal Engine</div>
                    <h4 class="vip-title">Generate Official Quotation Brief for Your Enterprise</h4>
                    <p class="vip-desc">Enter your company name to instantly export a customized executive PDF quotation with certified modules and local VAT scheme.</p>
                </div>
                <div class="vip-banner-actions">
                    <input type="text" id="quickClientNameInput" class="vip-input" placeholder="Enter Your Company Name..." oninput="updatePdfClientName(this.value)" />
                    <button type="button" class="vip-btn-gold" onclick="openExecutivePdfModal()">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                        <span>Export Branded PDF Brief</span>
                    </button>
                </div>
            </div>
"""

# HTML Component: Feature 2 (Smart ROI Tab - Arabic)
ROI_TAB_AR = """
        <!-- Feature 2: قسم حاسبة العائد على الاستثمار التفاعلية ROI -->
        <section class="tab-section" id="tab-roi">
            <div class="section-header">
                <div>
                    <h3 class="section-title">حاسبة التوفير والعائد على الاستثمار الذكية (Interactive ROI Engine)</h3>
                    <p class="section-desc">محاكاة دقيقة لحجم التوفير المالي وساعات العمل التي ستحققها شركتك سنوياً عند التحول لبنية S&R CoreSync السحابية.</p>
                </div>
            </div>

            <div class="roi-portal-card">
                <div class="roi-sliders-grid">
                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>👥 حجم الفريق / الموظفين</span>
                            <span class="roi-val-display" id="dispRoiTeam">20 موظف</span>
                        </div>
                        <input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam" oninput="calcPortalRoi()" />
                    </div>

                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>⏱️ ساعات المعاملات اليدوية / أسبوعياً</span>
                            <span class="roi-val-display" id="dispRoiHours">18 ساعة/أسبوع</span>
                        </div>
                        <input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours" oninput="calcPortalRoi()" />
                    </div>

                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>💶 متوسط تكلفة الساعة للكوادر (€)</span>
                            <span class="roi-val-display" id="dispRoiCost">€ 45 / ساعة</span>
                        </div>
                        <input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost" oninput="calcPortalRoi()" />
                    </div>
                </div>

                <div class="roi-results-row">
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-gold font-num" id="resRoiSavings">€ 31,590</div>
                        <div class="roi-metric-lbl">التوفير المالي المباشر سنوياً</div>
                    </div>
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-white font-num" id="resRoiHours">702 ساعة</div>
                        <div class="roi-metric-lbl">ساعات عمل موفرة سنوياً من الأتمتة</div>
                    </div>
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-gold font-num" id="resRoiYield">780% Net</div>
                        <div class="roi-metric-lbl">العائد الصافي على الاستثمار (Estimated ROI)</div>
                    </div>
                </div>

                <div class="text-center mt-4">
                    <button type="button" class="btn-sync-consultation" onclick="syncDemoToConsultation()">
                        <span>🚀 تثبيت هذا العائد وحجز استشارة مع المؤسسين</span>
                    </button>
                </div>
            </div>
        </section>
"""

# HTML Component: Feature 2 (Smart ROI Tab - English)
ROI_TAB_EN = """
        <!-- Feature 2: Interactive Smart ROI & Cost Savings Tab -->
        <section class="tab-section" id="tab-roi">
            <div class="section-header">
                <div>
                    <h3 class="section-title">Interactive ROI & Cost Reduction Engine</h3>
                    <p class="section-desc">Accurate simulation of annual financial savings and staff work hours saved upon transitioning to S&R CoreSync Cloud ERP architecture.</p>
                </div>
            </div>

            <div class="roi-portal-card">
                <div class="roi-sliders-grid">
                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>👥 Team Size / Employees</span>
                            <span class="roi-val-display" id="dispRoiTeam">20 staff</span>
                        </div>
                        <input type="range" min="3" max="250" value="20" class="roi-range-input" id="slideRoiTeam" oninput="calcPortalRoi()" />
                    </div>

                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>⏱️ Manual Tasks / Hours per Week</span>
                            <span class="roi-val-display" id="dispRoiHours">18 hrs/wk</span>
                        </div>
                        <input type="range" min="5" max="60" value="18" class="roi-range-input" id="slideRoiHours" oninput="calcPortalRoi()" />
                    </div>

                    <div class="roi-slider-box">
                        <div class="roi-slider-header">
                            <span>💶 Average Hourly Rate (€)</span>
                            <span class="roi-val-display" id="dispRoiCost">€ 45 / hr</span>
                        </div>
                        <input type="range" min="15" max="150" value="45" step="5" class="roi-range-input" id="slideRoiCost" oninput="calcPortalRoi()" />
                    </div>
                </div>

                <div class="roi-results-row">
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-gold font-num" id="resRoiSavings">€ 31,590</div>
                        <div class="roi-metric-lbl">Direct Annual Financial Savings</div>
                    </div>
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-white font-num" id="resRoiHours">702 hours</div>
                        <div class="roi-metric-lbl">Work Hours Saved via Automated Cloud Workflows</div>
                    </div>
                    <div class="roi-metric-result">
                        <div class="roi-metric-num text-gold font-num" id="resRoiYield">780% Net</div>
                        <div class="roi-metric-lbl">Estimated Enterprise Return on Investment</div>
                    </div>
                </div>

                <div class="text-center mt-4">
                    <button type="button" class="btn-sync-consultation" onclick="syncDemoToConsultation()">
                        <span>🚀 Lock in These Savings — Book Founders Consultation</span>
                    </button>
                </div>
            </div>
        </section>
"""

# HTML Component: Feature 3 (Hotline Widget)
HOTLINE_WIDGET_HTML = """
    <!-- Feature 3: Sovereign VIP Founders Hotline Widget (Pre-filled Localized Contact) -->
    <div class="sovereign-hotline-widget" id="sovereignHotlineWidget">
        <div class="hotline-popover-card" id="hotlinePopoverCard">
            <div class="hotline-header-row">
                <span class="hotline-header-title">Direct Executive Hotline</span>
                <button type="button" class="btn-modal-close-sm font-num" onclick="toggleHotlineWidget(event)" style="background:none;border:none;color:#c5a880;cursor:pointer;font-size:16px;">✕</button>
            </div>
            
            <div class="hotline-founder-box">
                <div class="hotline-founder-info">
                    <div class="hotline-avatar">SA</div>
                    <div class="hotline-names">
                        <span class="hotline-name">Eng. Mohammad Salim Aziza</span>
                        <span class="hotline-role">CTO & Software Architect</span>
                    </div>
                </div>
                <div class="hotline-actions">
                    <a href="https://wa.me/31618111116" target="_blank" class="hotline-btn-wa" id="btnHotlineWaSalim">
                        <span>WhatsApp</span>
                    </a>
                    <a href="tel:+31618111116" class="hotline-btn-call">
                        <span>+31 6 1811 1116</span>
                    </a>
                </div>
            </div>

            <div class="hotline-founder-box">
                <div class="hotline-founder-info">
                    <div class="hotline-avatar">RK</div>
                    <div class="hotline-names">
                        <span class="hotline-name">Mr. Mohammad Raed Kaaka</span>
                        <span class="hotline-role">Managing Director & Operations</span>
                    </div>
                </div>
                <div class="hotline-actions">
                    <a href="https://wa.me/31618111116" target="_blank" class="hotline-btn-wa" id="btnHotlineWaRaed">
                        <span>WhatsApp</span>
                    </a>
                    <a href="tel:+31618111116" class="hotline-btn-call">
                        <span>+31 6 1811 1116</span>
                    </a>
                </div>
            </div>
        </div>

        <button type="button" class="hotline-trigger-pill" id="hotlineTriggerBtn" onclick="toggleHotlineWidget(event)">
            <span class="hotline-pulse-dot"></span>
            <span id="hotlineTriggerText">💬 Contact Founders</span>
        </button>
    </div>
"""

# JavaScript Engine for Features (ROI Calculator & Localized WhatsApp messages)
FEATURES_JS = """
<script id="sovereignFeaturesLogic">
// Feature 2: Live ROI Calculator Logic
function calcPortalRoi() {
    const teamEl = document.getElementById('slideRoiTeam');
    const hoursEl = document.getElementById('slideRoiHours');
    const costEl = document.getElementById('slideRoiCost');
    if (!teamEl || !hoursEl || !costEl) return;

    const team = parseInt(teamEl.value) || 20;
    const hours = parseInt(hoursEl.value) || 18;
    const cost = parseInt(costEl.value) || 45;

    // Display updates
    const dispTeam = document.getElementById('dispRoiTeam');
    if (dispTeam) dispTeam.innerText = team + ' ' + (document.documentElement.lang === 'ar' ? 'موظف' : 'staff');

    const dispHours = document.getElementById('dispRoiHours');
    if (dispHours) dispHours.innerText = hours + ' ' + (document.documentElement.lang === 'ar' ? 'ساعة/أسبوع' : 'hrs/wk');

    const dispCost = document.getElementById('dispRoiCost');
    if (dispCost) dispCost.innerText = '€ ' + cost + ' / ' + (document.documentElement.lang === 'ar' ? 'ساعة' : 'hr');

    // Formulas:
    // CoreSync automates ~75% of manual operational hours
    const hoursSavedYear = Math.round(hours * 52 * 0.75);
    const savingsYear = Math.round(hoursSavedYear * cost);
    const roiPercent = Math.min(1450, Math.max(340, Math.round((savingsYear / 4200) * 100)));

    const resSavings = document.getElementById('resRoiSavings');
    if (resSavings) resSavings.innerText = '€ ' + savingsYear.toLocaleString();

    const resHours = document.getElementById('resRoiHours');
    if (resHours) resHours.innerText = hoursSavedYear.toLocaleString() + ' ' + (document.documentElement.lang === 'ar' ? 'ساعة' : 'hours');

    const resYield = document.getElementById('resRoiYield');
    if (resYield) resYield.innerText = roiPercent + '% Net';
}

// Feature 3: Toggle Hotline Widget & Localize WhatsApp Messages
function toggleHotlineWidget(e) {
    if (e) e.stopPropagation();
    const widget = document.getElementById('sovereignHotlineWidget');
    if (!widget) return;
    widget.classList.toggle('open');
}

document.addEventListener('click', function(e) {
    const widget = document.getElementById('sovereignHotlineWidget');
    if (widget && !widget.contains(e.target)) {
        widget.classList.remove('open');
    }
});

// Configure localized WhatsApp message on load
document.addEventListener('DOMContentLoaded', function() {
    const lang = document.documentElement.lang || 'ar';
    const greetings = {
        'de': 'Guten Tag Eng. Salim, ich interessiere mich für das S&R CoreSync ERP-System für mein Unternehmen...',
        'fr': 'Bonjour Ing. Salim, je souhaite obtenir des informations sur S&R CoreSync ERP pour mon entreprise...',
        'tr': 'Merhaba Salim Bey, şirketim için S&R CoreSync ERP sistemi hakkında bilgi almak istiyorum...',
        'sv': 'Hej Salim, jag är intresserad av S&R CoreSync ERP-systemet för mitt företag...',
        'no': 'Hei Salim, jeg er interessert i S&R CoreSync ERP-systemet for min bedrift...',
        'ku': 'Silav Salim Beg, ez dixwazim li ser pergala S&R CoreSync ERP agahdarî bistînim ji bo karsaziya xwe...',
        'ckb': 'سڵاو ئەندازیار سەلیم، ئارەزووی وەرگرتنی زانیاریم هەیە سەبارەت بە سیستەمی S&R CoreSync ERP بۆ کۆمپانیاکەمان...',
        'nl': 'Hallo Eng. Salim, ik heb interesse in het S&R CoreSync ERP-systeem voor mijn onderneming...',
        'ar': 'مرحباً م. سليم، أود مناقشة اعتماد بنية S&R CoreSync ERP وحجز استشارة تنفيذية لشركتنا...',
        'en': 'Hello Eng. Salim, I would like to consult on deploying S&R CoreSync ERP for my enterprise...'
    };

    const msg = greetings[lang] || greetings['en'];
    const waSalim = document.getElementById('btnHotlineWaSalim');
    if (waSalim) waSalim.href = 'https://wa.me/31618111116?text=' + encodeURIComponent(msg);

    const waRaed = document.getElementById('btnHotlineWaRaed');
    if (waRaed) {
        const msgRaed = msg.replace('Salim', 'Raed').replace('سليم', 'رائد');
        waRaed.href = 'https://wa.me/31618111116?text=' + encodeURIComponent(msgRaed);
    }

    const triggerText = document.getElementById('hotlineTriggerText');
    if (triggerText) {
        if (lang === 'ar') triggerText.innerText = '💬 تواصل مع المؤسسين';
        else if (lang === 'ckb') triggerText.innerText = '💬 پەیوەندی بە دامەزرێنەران';
        else if (lang === 'de') triggerText.innerText = '💬 Gründer-Hotline';
        else if (lang === 'fr') triggerText.innerText = '💬 Ligne Directe Fondateurs';
        else if (lang === 'tr') triggerText.innerText = '💬 Kurucu Hattı';
        else if (lang === 'nl') triggerText.innerText = '💬 Contact Oprichters';
        else triggerText.innerText = '💬 Founder Hotline';
    }

    calcPortalRoi();
});
</script>
"""

# Function to inject into a demo.html file
def inject_features(file_path, is_english=False):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Inject VIP Banner in Overview Tab
    if 'vip-proposal-banner' not in c:
        banner = VIP_BANNER_EN if is_english else VIP_BANNER_AR
        # Inject right after <section class="tab-section active" id="tab-overview">
        c = re.sub(
            r'(<section class="tab-section active" id="tab-overview">[\s\S]*?<div class="section-header">[\s\S]*?<\/div>)',
            '\\1\n' + banner,
            c,
            count=1
        )

    # 2. Inject ROI Sidebar nav item
    if 'tourNav-roi' not in c:
        roi_label = "Smart ROI Calculator" if is_english else "حاسبة التوفير والعائد (ROI)"
        roi_nav = f"""
            <div class="nav-item" id="tourNav-roi" onclick="switchPortalTab('roi', this)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v12M15 9.5H9.5a2.5 2.5 0 0 0 0 5h5a2.5 2.5 0 0 1 0 5H9"></path></svg>
                <span>{roi_label}</span>
            </div>
"""
        c = re.sub(
            r'(<div class="nav-item"[^>]*id="tourNav-software"[^>]*>[\s\S]*?<\/div>)',
            '\\1\n' + roi_nav,
            c,
            count=1
        )

    # 3. Inject ROI Tab Section
    if 'id="tab-roi"' not in c:
        roi_tab = ROI_TAB_EN if is_english else ROI_TAB_AR
        # Inject before closing </main>
        c = c.replace('</main>', roi_tab + '\n        </main>', 1)

    # 4. Inject Hotline Widget & JS
    if 'sovereign-hotline-widget' not in c:
        c = c.replace('</body>', HOTLINE_WIDGET_HTML + '\n' + FEATURES_JS + '\n</body>', 1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Successfully integrated 4 features into: {os.path.relpath(file_path, BASE_DIR)}")

# Inject into Arabic master and English master
inject_features(DEMO_AR_PATH, is_english=False)
inject_features(DEMO_EN_PATH, is_english=True)

print("4 High-Conversion Enterprise Features injected into masters!")
