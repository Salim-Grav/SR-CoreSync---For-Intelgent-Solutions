"""
fix_all_current_problems.py
Resolves all warnings and errors reported in current_problems:
1. Fix duplicate IDs for sovereignLangTrigger / sovereignLangSearch in footer across index.html, de/index.html, en/index.html, nl/index.html
2. Fix missing background-clip: text in de/index.html, en/index.html, nl/index.html
3. Fix querySelectorAlle typo in de, en, nl index.html and modernize dropdown JS
4. Remove all inline styles across index.html, de/index.html, en/index.html, nl/index.html, preview-software.html, preview-work.html, preview-estimator.html
"""

import re

def fix_file(path, replacements):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
        else:
            print(f"[{path}] WARNING: Pattern not found:\n{old[:80]}...")
            
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[{path}] Successfully updated!")
    else:
        print(f"[{path}] No changes made.")

# ── 1. Fix index.html ──
fix_file('index.html', [
    (
        '<a href="./preview-whitelabel-calculator.html" class="estimator-btn-vip" style="background: rgba(197, 168, 128, 0.15); border: 1.5px solid rgba(197, 168, 128, 0.45); color: #dfc299; text-decoration: none; text-align: center; margin-top: 4px; display: flex; align-items: center; justify-content: center; gap: 6px;" title="حاسبة تراخيص المنصات السيادية الجاهزة">',
        '<a href="./preview-whitelabel-calculator.html" class="estimator-btn-calc-vip" title="حاسبة تراخيص المنصات السيادية الجاهزة">'
    ),
    (
        '<div class="sr-platforms-calc-cta" style="margin-top: 14px;">\n                                <a href="./preview-whitelabel-calculator.html" class="btn-primary-sovereign" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; background: linear-gradient(135deg, #c5a880, #dfc299); color: #010907; font-weight: 800; text-decoration: none; box-shadow: 0 4px 20px rgba(197, 168, 128, 0.35);">',
        '<div class="sr-platforms-calc-cta">\n                                <a href="./preview-whitelabel-calculator.html" class="sr-platforms-calc-btn">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=civicsync" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص CivicSync الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=civicsync" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص CivicSync الفورية">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=healthbridge" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص HealthBridge الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=healthbridge" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص HealthBridge الفورية">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=omnibakery" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص OmniBakery الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=omnibakery" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص OmniBakery الفورية">'
    ),
    # Footer duplicate IDs in index.html
    (
        '<div class="sovereign-lang-dropdown" id="sovereignLangDropdown">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true"',
        '<div class="sovereign-lang-dropdown" id="sovereignLangDropdownFooter">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerFooter" aria-expanded="false" aria-haspopup="true"'
    ),
    (
        '<div class="sovereign-lang-menu" id="sovereignLangMenu">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearch"',
        '<div class="sovereign-lang-menu" id="sovereignLangMenuFooter">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearchFooter"'
    )
])

# ── 2. Fix de/index.html ──
fix_file('de/index.html', [
    (
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            -webkit-text-fill-color: transparent;',
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            background-clip: text;\n            -webkit-text-fill-color: transparent;'
    ),
    (
        '<div class="sr-platforms-calc-cta" style="margin-top: 14px;">\n                                <a href="../preview-whitelabel-calculator.html" class="btn-primary-sovereign" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; background: linear-gradient(135deg, #c5a880, #dfc299); color: #010907; font-weight: 800; text-decoration: none; box-shadow: 0 4px 20px rgba(197, 168, 128, 0.35);">',
        '<div class="sr-platforms-calc-cta">\n                                <a href="../preview-whitelabel-calculator.html" class="sr-platforms-calc-btn">'
    ),
    (
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdown">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true"',
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdownFooter">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerFooter" aria-expanded="false" aria-haspopup="true"'
    ),
    (
        '<div class="sovereign-lang-menu" id="sovereignLangMenu">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearch"',
        '<div class="sovereign-lang-menu" id="sovereignLangMenuFooter">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearchFooter"'
    ),
    (
        'querySelectorAlle',
        'querySelectorAll'
    )
])

# ── 3. Fix en/index.html ──
fix_file('en/index.html', [
    (
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            -webkit-text-fill-color: transparent;',
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            background-clip: text;\n            -webkit-text-fill-color: transparent;'
    ),
    (
        '<div class="sr-platforms-calc-cta" style="margin-top: 14px;">\n                                <a href="../preview-whitelabel-calculator.html" class="btn-primary-sovereign" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; background: linear-gradient(135deg, #c5a880, #dfc299); color: #010907; font-weight: 800; text-decoration: none; box-shadow: 0 4px 20px rgba(197, 168, 128, 0.35);">',
        '<div class="sr-platforms-calc-cta">\n                                <a href="../preview-whitelabel-calculator.html" class="sr-platforms-calc-btn">'
    ),
    (
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdown">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true"',
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdownFooter">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerFooter" aria-expanded="false" aria-haspopup="true"'
    ),
    (
        '<div class="sovereign-lang-menu" id="sovereignLangMenu">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearch"',
        '<div class="sovereign-lang-menu" id="sovereignLangMenuFooter">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearchFooter"'
    ),
    (
        'querySelectorAlle',
        'querySelectorAll'
    )
])

# ── 4. Fix nl/index.html ──
fix_file('nl/index.html', [
    (
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            -webkit-text-fill-color: transparent;',
        'background: linear-gradient(135deg, #ffffff 10%, #f3dfba 55%, #c5a880 100%);\n            -webkit-background-clip: text;\n            background-clip: text;\n            -webkit-text-fill-color: transparent;'
    ),
    (
        '<div class="sr-platforms-calc-cta" style="margin-top: 14px;">\n                                <a href="../preview-whitelabel-calculator.html" class="btn-primary-sovereign" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; background: linear-gradient(135deg, #c5a880, #dfc299); color: #010907; font-weight: 800; text-decoration: none; box-shadow: 0 4px 20px rgba(197, 168, 128, 0.35);">',
        '<div class="sr-platforms-calc-cta">\n                                <a href="../preview-whitelabel-calculator.html" class="sr-platforms-calc-btn">'
    ),
    (
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdown">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTrigger" aria-expanded="false" aria-haspopup="true"',
        '<li><!-- Sovereign Global Multilingual Hub (28 Languages: EU Official + EEA + Regional) -->\n<div class="sovereign-lang-dropdown" id="sovereignLangDropdownFooter">\n    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerFooter" aria-expanded="false" aria-haspopup="true"'
    ),
    (
        '<div class="sovereign-lang-menu" id="sovereignLangMenu">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearch"',
        '<div class="sovereign-lang-menu" id="sovereignLangMenuFooter">\n        <div class="sovereign-lang-search-box">\n            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n            <input type="text" class="sovereign-lang-search-input" id="sovereignLangSearchFooter"'
    ),
    (
        'querySelectorAlle',
        'querySelectorAll'
    )
])

# ── 5. Fix preview-software.html ──
fix_file('preview-software.html', [
    (
        '<div style="display: flex; align-items: center; gap: 8px;">\n                <a href="./preview-whitelabel-calculator.html" class="sr-btn-home-link" title="حاسبة تراخيص White-Label الفورية وتوليد PDF" style="background: linear-gradient(135deg, rgba(197, 168, 128, 0.22), rgba(16, 185, 129, 0.22)); border: 1px solid #c5a880; color: #dfc299;">',
        '<div class="sr-preview-navbar-actions">\n                <a href="./preview-whitelabel-calculator.html" class="sr-btn-home-link sr-nav-calc-btn" title="حاسبة تراخيص White-Label الفورية وتوليد PDF">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html" class="sr-hero-btn" style="background: linear-gradient(135deg, #c5a880 0%, #dfc299 100%); color: #010907; font-weight: 900; text-decoration: none; box-shadow: 0 8px 24px rgba(197, 168, 128, 0.35);">',
        '<a href="./preview-whitelabel-calculator.html" class="sr-hero-btn sr-hero-calc-btn">'
    ),
    (
        '<div style="margin-top: 14px;">\n                                <a href="./preview-whitelabel-calculator.html" class="sr-hero-btn" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 22px; border-radius: 999px; background: linear-gradient(135deg, #c5a880, #dfc299); color: #010907; font-weight: 800; text-decoration: none; box-shadow: 0 4px 20px rgba(197, 168, 128, 0.35);">',
        '<div class="sr-platforms-calc-cta">\n                                <a href="./preview-whitelabel-calculator.html" class="sr-platforms-calc-btn">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=civicsync" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص CivicSync الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=civicsync" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص CivicSync الفورية">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=healthbridge" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص HealthBridge الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=healthbridge" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص HealthBridge الفورية">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html?platform=omnibakery" class="btn-live-preview software-btn-sim" style="border-color: rgba(197, 168, 128, 0.5); color: #dfc299;" title="حساب تكلفة ترخيص OmniBakery الفورية">',
        '<a href="./preview-whitelabel-calculator.html?platform=omnibakery" class="btn-live-preview software-btn-sim software-btn-calc" title="حساب تكلفة ترخيص OmniBakery الفورية">'
    )
])

# ── 6. Fix preview-work.html ──
# First add CSS classes to style tag in preview-work.html if not already present
with open('preview-work.html', 'r', encoding='utf-8') as f:
    pw_content = f.read()

if '.sr-nav-calc-btn' not in pw_content:
    pw_css = """
        .sr-preview-navbar-actions { display: flex; align-items: center; gap: 8px; }
        .sr-nav-calc-btn {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.22), rgba(16, 185, 129, 0.22));
            border: 1px solid #c5a880;
            color: #dfc299;
        }
        .btn-modal-calc {
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.2), rgba(16, 185, 129, 0.2));
            border: 1px solid #c5a880;
            color: #dfc299;
        }
    """
    pw_content = pw_content.replace('</style>', pw_css + '\n    </style>')
    with open('preview-work.html', 'w', encoding='utf-8') as f:
        f.write(pw_content)

fix_file('preview-work.html', [
    (
        '<div style="display: flex; align-items: center; gap: 8px;">\n                <a href="./preview-whitelabel-calculator.html" class="sr-btn-home-link" title="حاسبة تراخيص White-Label الفورية" style="background: linear-gradient(135deg, rgba(197, 168, 128, 0.22), rgba(16, 185, 129, 0.22)); border: 1px solid #c5a880; color: #dfc299;">',
        '<div class="sr-preview-navbar-actions">\n                <a href="./preview-whitelabel-calculator.html" class="sr-btn-home-link sr-nav-calc-btn" title="حاسبة تراخيص White-Label الفورية">'
    ),
    (
        '<a href="./preview-whitelabel-calculator.html" class="btn-modal-software-hub" style="background: linear-gradient(135deg, rgba(197, 168, 128, 0.2), rgba(16, 185, 129, 0.2)); border: 1px solid #c5a880; color: #dfc299;" title="حاسبة تراخيص White-Label الفورية">',
        '<a href="./preview-whitelabel-calculator.html" class="btn-modal-software-hub btn-modal-calc" title="حاسبة تراخيص White-Label الفورية">'
    )
])

# ── 7. Fix preview-estimator.html ──
with open('preview-estimator.html', 'r', encoding='utf-8') as f:
    pe_content = f.read()

if '.est-whitelabel-banner' not in pe_content:
    pe_css = """
        .est-nav-calc-btn {
            background: rgba(197, 168, 128, 0.2);
            border-color: var(--sr-gold);
            color: var(--sr-gold-light);
        }
        .est-whitelabel-banner {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, rgba(197, 168, 128, 0.14), rgba(16, 185, 129, 0.12));
            border: 1.5px solid rgba(197, 168, 128, 0.38);
            border-radius: 16px;
            padding: 18px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        .est-whitelabel-banner-content {
            display: flex;
            align-items: center;
            gap: 14px;
            max-width: 820px;
        }
        .est-whitelabel-banner-icon {
            font-size: 2.2rem;
            filter: drop-shadow(0 0 10px rgba(197, 168, 128, 0.4));
        }
        .est-whitelabel-banner-title {
            color: var(--sr-gold-light);
            font-size: 1.05rem;
            display: block;
            margin-bottom: 4px;
        }
        .est-whitelabel-banner-desc {
            margin: 0;
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.75);
            line-height: 1.5;
        }
        .est-whitelabel-banner-btn {
            background: linear-gradient(135deg, var(--sr-gold), var(--sr-gold-dark));
            color: #010907;
            font-weight: 900;
            padding: 12px 22px;
            font-size: 0.88rem;
            box-shadow: 0 6px 20px rgba(197, 168, 128, 0.35);
            text-decoration: none;
            white-space: nowrap;
        }
    """
    pe_content = pe_content.replace('</style>', pe_css + '\n    </style>')
    with open('preview-estimator.html', 'w', encoding='utf-8') as f:
        f.write(pe_content)

fix_file('preview-estimator.html', [
    (
        '<a href="./preview-whitelabel-calculator.html" class="est-btn-nav" style="background: rgba(197, 168, 128, 0.2); border-color: var(--sr-gold); color: var(--sr-gold-light);">',
        '<a href="./preview-whitelabel-calculator.html" class="est-btn-nav est-nav-calc-btn">'
    ),
    (
        '<div style="grid-column: 1 / -1; background: linear-gradient(135deg, rgba(197, 168, 128, 0.14), rgba(16, 185, 129, 0.12)); border: 1.5px solid rgba(197, 168, 128, 0.38); border-radius: 16px; padding: 18px 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">\n            <div style="display: flex; align-items: center; gap: 14px; max-width: 820px;">\n                <span style="font-size: 2.2rem; filter: drop-shadow(0 0 10px rgba(197, 168, 128, 0.4));">🏛️</span>\n                <div>\n                    <strong style="color: var(--sr-gold-light); font-size: 1.05rem; display: block; margin-bottom: 4px;">هل تبحث عن ترخيص إحدى منصاتنا السيادية الجاهزة (CivicSync™ / HealthBridge™ / OmniBakery™)؟</strong>\n                    <p style="margin: 0; font-size: 0.85rem; color: rgba(255, 255, 255, 0.75); line-height: 1.5;">خصّص عدد المقاعد، نوع التثبيت (SaaS / On-Premise)، الإضافات والذكاء الاصطناعي، واستخرج فوراً عرض سعر PDF معتمد ومفصّل بهوية مؤسستك.</p>\n                </div>\n            </div>\n            <a href="./preview-whitelabel-calculator.html" class="est-btn-nav" style="background: linear-gradient(135deg, var(--sr-gold), var(--sr-gold-dark)); color: #010907; font-weight: 900; padding: 12px 22px; font-size: 0.88rem; box-shadow: 0 6px 20px rgba(197, 168, 128, 0.35); text-decoration: none; white-space: nowrap;">',
        '<div class="est-whitelabel-banner">\n            <div class="est-whitelabel-banner-content">\n                <span class="est-whitelabel-banner-icon">🏛️</span>\n                <div>\n                    <strong class="est-whitelabel-banner-title">هل تبحث عن ترخيص إحدى منصاتنا السيادية الجاهزة (CivicSync™ / HealthBridge™ / OmniBakery™)؟</strong>\n                    <p class="est-whitelabel-banner-desc">خصّص عدد المقاعد، نوع التثبيت (SaaS / On-Premise)، الإضافات والذكاء الاصطناعي، واستخرج فوراً عرض سعر PDF معتمد ومفصّل بهوية مؤسستك.</p>\n                </div>\n            </div>\n            <a href="./preview-whitelabel-calculator.html" class="est-btn-nav est-whitelabel-banner-btn">'
    )
])

print("\nAll files successfully processed!")
