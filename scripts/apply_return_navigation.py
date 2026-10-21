# -*- coding: utf-8 -*-
"""
Apply luxury return navigation bars, modal return buttons,
and floating back buttons across preview-work.html, preview-software.html,
and index.html (as well as multilingual index files).
"""

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update preview-work.html
pw = read_file('preview-work.html')

if 'sr-software-apps.css' not in pw:
    pw = pw.replace(
        '<link rel="stylesheet" href="./css/enterprise-suite.min.css">',
        '<link rel="stylesheet" href="./css/enterprise-suite.min.css">\n    <link rel="stylesheet" href="./css/sr-software-apps.css?v=20261021">'
    )

navbar_work = """    <!-- شريط الملاحة والرجوع الفاخر العلوي -->
    <header class="sr-preview-navbar">
        <div class="sr-preview-navbar__inner">
            <a href="./preview-software.html" class="sr-btn-back-link" title="الرجوع لسوق البرمجيات والمنصات">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                <span>الرجوع إلى سوق البرمجيات</span>
            </a>
            <div class="sr-preview-navbar__brand">
                <img src="./assets/sr-core-emblem.svg?v=sovereign2026" alt="S&R CoreSync" width="28" height="28">
                <span class="sr-brand-name">S&R CoreSync™ Solutions</span>
                <span class="sr-preview-chip">معرض الأعمال والمنصات السيادية</span>
            </div>
            <a href="./index.html" class="sr-btn-home-link" title="العودة للبوابة الرئيسية">
                <span>الرئيسية 🏠</span>
            </a>
        </div>
    </header>"""

if 'sr-preview-navbar' not in pw:
    pw = pw.replace('<body>', '<body>\n' + navbar_work, 1)

modal_actions_work = """                    <!-- شريط أزرار الرجوع السريع أسفل تفاصيل المشروع -->
                    <div class="project-modal-bottom-actions">
                        <button type="button" class="btn-modal-return" onclick="closeProjectModal()" title="إغلاق المعاينة والعودة لقائمة المنصات">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                            <span>رجوع إلى قائمة المنصات</span>
                        </button>
                        <a href="./preview-software.html" class="btn-modal-software-hub" title="الانتقال المباشر لسوق البرمجيات">
                            <span>سوق البرمجيات 🏛️</span>
                        </a>
                    </div>"""

target_pills = '<div class="project-modal-techs" id="projectModalTechPills"></div>'
if target_pills in pw and 'project-modal-bottom-actions' not in pw:
    pw = pw.replace(target_pills, target_pills + '\n' + modal_actions_work, 1)

floating_btn_work = """    <!-- زر الرجوع العائم الذكي -->
    <a href="./preview-software.html" class="sr-floating-back-btn" title="الرجوع المباشر لسوق البرمجيات">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        <span>رجوع لسوق البرمجيات</span>
    </a>"""

if 'sr-floating-back-btn' not in pw:
    pw = pw.replace('</body>', floating_btn_work + '\n</body>', 1)

write_file('preview-work.html', pw)
print("Updated preview-work.html successfully!")


# 2. Update preview-software.html
ps = read_file('preview-software.html')

navbar_soft = """    <!-- شريط الملاحة والرجوع الفاخر العلوي -->
    <header class="sr-preview-navbar">
        <div class="sr-preview-navbar__inner">
            <a href="./index.html#software-hub" class="sr-btn-back-link" title="الرجوع للبوابة الرئيسية">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                <span>الرجوع للبوابة الرئيسية</span>
            </a>
            <div class="sr-preview-navbar__brand">
                <img src="./assets/sr-core-emblem.svg?v=sovereign2026" alt="S&R CoreSync" width="28" height="28">
                <span class="sr-brand-name">S&R CoreSync™ Solutions</span>
                <span class="sr-preview-chip">سوق البرمجيات والمنصات الجاهزة</span>
            </div>
            <a href="./preview-work.html#platforms" class="sr-btn-home-link" title="معاينة قسم المنصات والأعمال">
                <span>معرض الأعمال 💼</span>
            </a>
        </div>
    </header>"""

if 'sr-preview-navbar' not in ps:
    ps = ps.replace('<body>', '<body>\n' + navbar_soft, 1)

floating_btn_soft = """    <!-- زر الرجوع العائم للبوابة الرئيسية -->
    <a href="./index.html" class="sr-floating-back-btn" title="الرجوع للبوابة الرئيسية">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        <span>الرجوع للرئيسية</span>
    </a>"""

if 'sr-floating-back-btn' not in ps:
    ps = ps.replace('</body>', floating_btn_soft + '\n</body>', 1)

write_file('preview-software.html', ps)
print("Updated preview-software.html successfully!")


# 3. Update index.html and multilingual portals:
# Inside the modal in index.html, add the bottom return button so when visitors open any platform or project modal, they have a clear "رجوع لقائمة المنصات" button!
modal_actions_index = """                    <!-- شريط أزرار الرجوع السريع أسفل تفاصيل المشروع -->
                    <div class="project-modal-bottom-actions">
                        <button type="button" class="btn-modal-return" onclick="closeProjectModal()" title="إغلاق المعاينة والعودة لقائمة المنصات">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                            <span>رجوع إلى قائمة المنصات</span>
                        </button>
                        <a href="#software-hub" onclick="closeProjectModal();" class="btn-modal-software-hub" title="الانتقال المباشر لسوق البرمجيات">
                            <span>سوق البرمجيات 🏛️</span>
                        </a>
                    </div>"""

for fpath in ['index.html', 'nl/index.html', 'en/index.html', 'de/index.html']:
    txt = read_file(fpath)
    changed = False
    
    # Add bottom return button to modal if not present
    if target_pills in txt and 'project-modal-bottom-actions' not in txt:
        txt = txt.replace(target_pills, target_pills + '\n' + modal_actions_index, 1)
        changed = True
        
    # Also in platform cards on index.html: make the "دراسة الحالة" button smoothly open the platform on this page!
    # Instead of navigating away to preview-work.html, open the platform right in the work section of the same page!
    old_civi = 'href="./preview-work.html#platforms-civicsync"'
    new_civi = 'href="#work" onclick="navigateToPlatformWork(\'civicsync\'); return false;"'
    if old_civi in txt:
        txt = txt.replace(old_civi, new_civi)
        changed = True
        
    old_hb = 'href="./preview-work.html#platforms-healthbridge"'
    new_hb = 'href="#work" onclick="navigateToPlatformWork(\'healthbridge\'); return false;"'
    if old_hb in txt:
        txt = txt.replace(old_hb, new_hb)
        changed = True
        
    old_bakery = 'href="./preview-work.html#platforms-omnibakery"'
    new_bakery = 'href="#work" onclick="navigateToPlatformWork(\'omnibakery\'); return false;"'
    if old_bakery in txt:
        txt = txt.replace(old_bakery, new_bakery)
        changed = True
        
    # Add navigateToPlatformWork JS helper function if missing
    nav_helper_js = """
        function navigateToPlatformWork(platformId) {
            const platBtn = document.getElementById('tab-btn-platforms');
            if (platBtn) {
                switchWorkTab('platforms', platBtn);
            }
            const workSec = document.getElementById('work');
            if (workSec) {
                workSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            if (projectsDB && projectsDB.platforms) {
                const idx = projectsDB.platforms.findIndex(p => p.id === platformId);
                if (idx !== -1) {
                    selectWorkProject(idx);
                    setTimeout(() => {
                        openCurrentProjectModal();
                    }, 400);
                }
            }
        }
    """
    if 'function navigateToPlatformWork' not in txt:
        marker = "function openCurrentProjectModal()"
        if marker in txt:
            txt = txt.replace(marker, nav_helper_js + '\n        ' + marker, 1)
            changed = True
            
    if changed:
        write_file(fpath, txt)
        print(f"Updated {fpath} with smooth in-page platform navigation & modal return button!")

print("ALL RETURN NAVIGATION UPDATES APPLIED!")
