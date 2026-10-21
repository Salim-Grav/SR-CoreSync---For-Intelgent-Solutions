# -*- coding: utf-8 -*-
"""
Sync Universal White-Label Platforms (CivicSync, HealthBridge, OmniBakery)
into the international language versions: nl/index.html, en/index.html, de/index.html
"""
import os
import sys

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Read the main Arabic index.html that already has platforms integrated
main_index = read_file('index.html')

# Read preview-software.html for the platform cards HTML
preview_soft = read_file('preview-software.html')
preview_work = read_file('preview-work.html')

# ---- Extract platforms data from preview-work.html (language-neutral JS) ----
p_start = preview_work.find('platforms: [')
# Find end of platforms array - locate the closing ] that corresponds
depth = 0
p_end = p_start
in_platforms = False
for i, ch in enumerate(preview_work[p_start:], start=p_start):
    if ch == '[':
        depth += 1
        in_platforms = True
    elif ch == ']':
        depth -= 1
        if in_platforms and depth == 0:
            p_end = i + 1
            break

platforms_js = preview_work[p_start:p_end]
print(f"Extracted platforms JS ({len(platforms_js)} chars)")

# ---- Extract platform cards HTML from preview-software.html ----
card_start_str = '<!-- ===== منصات S&R العامة القابلة للترخيص'
card_end_str = '<!-- مختبر وبوابة برمجيات المؤسس'
cs = preview_soft.find(card_start_str)
ce = preview_soft.find(card_end_str)
platforms_cards_html = ''
if cs != -1 and ce != -1:
    platforms_cards_html = preview_soft[cs:ce].strip()
    print(f"Extracted platforms cards HTML ({len(platforms_cards_html)} chars)")
else:
    print("WARNING: Could not find platform cards in preview-software.html")

# ---- Platform tab button HTML ----
platforms_tab_btn = """                        <li class="nav-tab-item" role="presentation">
                            <button type="button" role="tab" id="tab-btn-platforms" aria-selected="false" class="tf-btn-tab tf-btn-tab--platforms fw-medium letter-space--1" onclick="switchWorkTab('platforms', this)">
                                <span class="dot-active" aria-hidden="true"></span>
                                <svg class="pricing-tab__icon" viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M12 2l10 5H2l10-5z"/></svg>
                                منصات S&amp;R الجاهزة ★
                            </button>
                        </li>"""

# ---- applyKpiLabels function ----
kpi_logic = """
        const DEFAULT_KPI_LABELS = {
            strip: { speed: 'سرعة التحميل', conv: 'معدل التحويل', sales: 'نمو المبيعات' },
            modal: { speed: 'سرعة الاستجابة', conv: 'معدل التحويل', sales: 'نمو المبيعات' }
        };

        function applyKpiLabels(p) {
            const custom = p && p.kpiLabels;
            const strip = document.querySelectorAll('.work-kpis-strip .work-kpi-lbl');
            const stripKeys = ['speed', 'conv', 'sales'];
            strip.forEach((el, i) => {
                const k = stripKeys[i];
                el.textContent = (custom && custom[k]) || DEFAULT_KPI_LABELS.strip[k];
            });
            const modal = document.querySelectorAll('.project-modal-kpis .project-kpi-lbl');
            const modalKeys = ['conv', 'speed', 'sales'];
            modal.forEach((el, i) => {
                const k = modalKeys[i];
                el.textContent = (custom && custom[k]) || DEFAULT_KPI_LABELS.modal[k];
            });
        }
        """

LANGS = ['nl', 'en', 'de']

# ---- Platform filter pill (language-neutral, product names are brand names) ----
platform_filter_pill = """                    <button type="button" class="software-filter-pill software-filter-pill--platforms" onclick="filterSoftwareMarketplace('platforms', this)">
                        <span>🏛️ White-Label Platforms</span>
                        <span class="pill-count">3 platforms</span>
                    </button>"""

for lang in LANGS:
    path = f'{lang}/index.html'
    print(f"\n=== Processing {path} ===")
    content = read_file(path)
    changed = False

    # 1. Add platforms tab button after apps tab button
    apps_tab_marker = "id=\"tab-btn-apps\""
    if 'id="tab-btn-platforms"' not in content:
        idx = content.find(apps_tab_marker)
        if idx != -1:
            li_close = content.find('</li>', idx) + len('</li>')
            content = content[:li_close] + '\n' + platforms_tab_btn + content[li_close:]
            print(f"  [OK] Added platforms tab button")
            changed = True
        else:
            print(f"  [WARN] apps tab marker not found")
    else:
        print(f"  [SKIP] platforms tab button already exists")

    # 2. Add platforms filter pill in software filter bar
    if 'software-filter-pill--platforms' not in content:
        # Find the all-filter pill and insert after its closing button tag
        all_pill_marker = "filterSoftwareMarketplace('all', this)"
        idx = content.find(all_pill_marker)
        if idx != -1:
            btn_close = content.find('</button>', idx) + len('</button>')
            content = content[:btn_close] + '\n' + platform_filter_pill + content[btn_close:]
            # Update total count from 6 to 9
            content = content.replace('6 منتجات</span>', '9 منتجات</span>', 1)
            content = content.replace('6 products</span>', '9 products</span>', 1)
            content = content.replace('6 Produkte</span>', '9 Produkte</span>', 1)
            print(f"  [OK] Added platforms filter pill")
            changed = True
        else:
            print(f"  [WARN] filter marketplace marker not found")
    else:
        print(f"  [SKIP] platforms filter pill already exists")

    # 3. Add platform cards to softwareGridContainer
    if platforms_cards_html and 'S&amp;R CivicSync' not in content and 'S&R CivicSync' not in content:
        lab_marker = '<!-- مختبر وبرمجيات المطور م. سليم عزيزة'
        idx = content.find(lab_marker)
        if idx != -1:
            grid_close = content.rfind('</div>', 0, idx)
            content = content[:grid_close] + '\n\n' + platforms_cards_html + '\n' + content[grid_close:]
            print(f"  [OK] Added 3 platform cards to softwareGridContainer")
            changed = True
        else:
            print(f"  [WARN] lab marker not found, trying alternate...")
            # Try alternate: find softwareGridContainer closing
            alt_marker = 'softwareArchitectLab'
            idx2 = content.find(alt_marker)
            if idx2 != -1:
                grid_close2 = content.rfind('</div>', 0, idx2)
                content = content[:grid_close2] + '\n\n' + platforms_cards_html + '\n' + content[grid_close2:]
                print(f"  [OK] Added platform cards via alternate marker")
                changed = True
    else:
        print(f"  [SKIP] platform cards already exist")

    # 4. Add platforms data to projectsDB
    if 'platforms:' not in content:
        cwc_marker = "let currentWorkCategory = 'websites';"
        idx = content.find(cwc_marker)
        if idx != -1:
            # Find the closing }; of projectsDB right before currentWorkCategory
            db_close = content.rfind('};', 0, idx)
            insert_code = ',\n            // S&R Universal White-Label Platforms\n            ' + platforms_js
            content = content[:db_close] + insert_code + '\n        ' + content[db_close:]
            print(f"  [OK] Added platforms to projectsDB")
            changed = True
        else:
            print(f"  [WARN] currentWorkCategory marker not found")
    else:
        print(f"  [SKIP] platforms already in projectsDB")

    # 5. Add applyKpiLabels function
    if 'function applyKpiLabels' not in content:
        cwc_marker = "let currentWorkCategory = 'websites';"
        idx = content.find(cwc_marker)
        if idx != -1:
            content = content[:idx] + kpi_logic + '\n        ' + content[idx:]
            print(f"  [OK] Added applyKpiLabels function")
            changed = True
    else:
        print(f"  [SKIP] applyKpiLabels already defined")

    # 6. Add applyKpiLabels call in renderActiveWork
    if 'applyKpiLabels(activeProject);' not in content:
        render_marker = 'const activeProject = list[currentWorkProjectIdx];'
        if render_marker in content:
            content = content.replace(render_marker, render_marker + '\n            applyKpiLabels(activeProject);', 1)
            print(f"  [OK] Added applyKpiLabels() call in renderActiveWork")
            changed = True
    else:
        print(f"  [SKIP] applyKpiLabels call already present")

    if changed:
        write_file(path, content)
        print(f"  [SAVED] {path} updated successfully")
    else:
        print(f"  [NO CHANGE] {path} was already up to date")

print("\n=== All language files processed! ===")
