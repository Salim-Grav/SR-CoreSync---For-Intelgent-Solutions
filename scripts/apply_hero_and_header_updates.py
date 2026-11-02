# -*- coding: utf-8 -*-
import re

def update_file(filepath, is_ckb=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove partner-portal button from header actions
    header_pattern = r'<a href="(?:\.\./)?partner-portal\.html" class="tf-btn btn-partner-portal-header"[^>]*>.*?</a>\s*'
    content = re.sub(header_pattern, '', content, flags=re.DOTALL)

    # 2. Update hero-reference__actions
    dev_href = "../developer-portal.html" if is_ckb else "developer-portal.html"
    partner_href = "../partner-portal.html" if is_ckb else "partner-portal.html"

    hero_pattern = r'<div class="hero-reference__actions[^"]*">.*?</div>\s*(?=<!--\s*شريط مؤشرات الثقة|\s*<div class="hero-trust-metrics-strip")'
    
    new_hero = f'''<div class="hero-reference__actions hero-actions-2x2">
                                        <!-- الصف الأول: الأزرار الذهبية الملكية الفاخرة الموحدة (Live Demo & Executive Booking) -->
                                        <div class="hero-actions-row">
                                            <a href="demo.html" class="tf-btn hero-reference__action hero-btn-gold-pair hero-btn-demo hero-btn-primary-highlight" title="تجربة المنصة السحابية الحية فوراً">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                                                <span>تجربة النظام السحابي الحي (معاينة تفاعلية) ⚡</span>
                                            </a>
                                            <button type="button" class="tf-btn hero-reference__action hero-btn-gold-pair hero-btn-vip" data-sr-call="openExecutiveBookingModal" title="حجز استشارة تنفيذية خاصة مع المؤسسين">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                                                <span>حجز استشارة تنفيذية خاصة 👔</span>
                                            </button>
                                        </div>

                                        <!-- الصف الثاني: بوابات المطورين والوكلاء الزمردية الفاخرة الموحدة (Dev Portal & Agent Portal) -->
                                        <div class="hero-actions-row">
                                            <a href="{dev_href}" class="tf-btn hero-reference__action hero-btn-portal-pair hero-btn-dev-portal" title="بوابة المطورين والواجهات البرمجية والمجسم الذكي ثلاثي الأبعاد">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/></svg>
                                                <span>بوابة المطورين والمجسم التفاعلي ⚡</span>
                                            </a>
                                            <a href="{partner_href}" class="tf-btn hero-reference__action hero-btn-portal-pair hero-btn-partner-portal" title="بوابة شركاء الحلول والوكلاء المعتمدين وتراخيص الامتياز">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                                                <span>بوابة الوكلاء والتراخيص 💼</span>
                                            </a>
                                        </div>
                                    </div>
                                    '''

    content, n = re.subn(hero_pattern, new_hero, content, count=1, flags=re.DOTALL)
    print(f"{filepath}: Replaced {n} hero actions block")

    # 3. Add CSS patch if not present
    if "/* Hero 2x2 Action Grid & Left-Shifted Emblem */" not in content:
        css_patch = '''
/* ==============================================================================
 * S&R CoreSync - Hero 2x2 Action Grid & Left-Shifted Emblem (Desktop Prestige)
 * ============================================================================== */
.hero-reference__actions.hero-actions-2x2 {
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    width: 100% !important;
    max-width: 630px !important;
}

.hero-actions-row {
    display: flex !important;
    align-items: stretch !important;
    gap: 12px !important;
    width: 100% !important;
}

.hero-actions-row .tf-btn.hero-reference__action {
    flex: 1 1 calc(50% - 6px) !important;
    width: calc(50% - 6px) !important;
    min-height: 48px !important;
    padding: 11px 18px !important;
    box-sizing: border-box !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 8px !important;
    font-size: 0.88rem !important;
    border-radius: 14px !important;
    white-space: nowrap !important;
    line-height: 1.2 !important;
    transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

/* Row 1: Gold Luxury Pair (Demo & Executive Booking) */
.hero-btn-gold-pair {
    background: linear-gradient(135deg, #fce0ad 0%, #e8bf7a 50%, #c5a880 100%) !important;
    color: #070e0b !important;
    border: 1px solid rgba(255, 243, 214, 0.85) !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 22px rgba(232, 191, 122, 0.4), 0 0 16px rgba(243, 223, 186, 0.25) !important;
    text-decoration: none !important;
    cursor: pointer !important;
}

.hero-btn-gold-pair:hover {
    background: linear-gradient(135deg, #ffffff 0%, #fae6bd 50%, #dab471 100%) !important;
    color: #000000 !important;
    border-color: #ffffff !important;
    box-shadow: 0 12px 28px rgba(232, 191, 122, 0.65), 0 0 25px rgba(255, 255, 255, 0.45) !important;
    transform: translateY(-2px) !important;
}

.hero-btn-gold-pair svg {
    stroke: #070e0b !important;
    color: #070e0b !important;
    stroke-width: 2.4 !important;
}

/* Row 2: Dark Emerald Glass Portal Pair (Dev Portal & Agent Portal) */
.hero-btn-portal-pair {
    background: rgba(10, 24, 18, 0.85) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    backdrop-filter: blur(14px) !important;
    color: #ecfdf5 !important;
    border: 1px solid rgba(16, 185, 129, 0.45) !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    text-decoration: none !important;
    cursor: pointer !important;
}

.hero-btn-portal-pair:hover {
    background: rgba(16, 185, 129, 0.22) !important;
    color: #ffffff !important;
    border-color: #34d399 !important;
    box-shadow: 0 10px 26px rgba(16, 185, 129, 0.4), 0 0 20px rgba(16, 185, 129, 0.25) !important;
    transform: translateY(-2px) !important;
}

.hero-btn-portal-pair svg {
    stroke: #34d399 !important;
    color: #34d399 !important;
    stroke-width: 2.2 !important;
}

.hero-btn-portal-pair:hover svg {
    stroke: #ffffff !important;
    color: #ffffff !important;
}

/* 4. تقريب الشعار قليلاً لليسار تجاه شريط السوشيال ميديا */
@media (min-width: 992px) {
    .hero-reference__emblem-col {
        transform: translateX(-45px) !important;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
}

@media (max-width: 680px) {
    .hero-actions-row {
        flex-direction: column !important;
        gap: 10px !important;
    }
    .hero-actions-row .tf-btn.hero-reference__action {
        flex: 1 1 100% !important;
        width: 100% !important;
    }
}
'''
        first_style_close = content.find('</style>')
        if first_style_close != -1:
            content = content[:first_style_close] + css_patch + content[first_style_close:]
            print(f"{filepath}: Inserted CSS patch")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{filepath}: Successfully updated and saved")

if __name__ == '__main__':
    update_file('index.html', is_ckb=False)
    update_file('ckb/index.html', is_ckb=True)
