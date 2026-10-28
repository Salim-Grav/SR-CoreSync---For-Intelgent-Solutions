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
Sync Universal White-Label Platforms (CivicSync, HealthBridge, OmniBakery)
from preview-work.html and preview-software.html into the main index.html
"""

import sys

def main():
    print("Reading files...")
    with open('preview-work.html', 'r', encoding='utf-8') as f:
        preview_work = f.read()

    with open('preview-software.html', 'r', encoding='utf-8') as f:
        preview_software = f.read()

    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()

    # 1. Add platforms tab button to work-tab_btn
    tab_marker = '<button type="button" role="tab" id="tab-btn-apps" aria-selected="false" class="tf-btn-tab fw-medium letter-space--1" onclick="switchWorkTab(\'apps\', this)">'
    new_tab_btn = '''                        <li class="nav-tab-item" role="presentation">
                            <button type="button" role="tab" id="tab-btn-platforms" aria-selected="false" class="tf-btn-tab tf-btn-tab--platforms fw-medium letter-space--1" onclick="switchWorkTab('platforms', this)">
                                <span class="dot-active" aria-hidden="true"></span>
                                <svg class="pricing-tab__icon" viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M12 2l10 5H2l10-5z"/></svg>
                                منصات S&amp;R الجاهزة ★
                            </button>
                        </li>'''

    if 'id="tab-btn-platforms"' not in index_html:
        # Find where apps tab item ends (</li>)
        apps_idx = index_html.find(tab_marker)
        if apps_idx != -1:
            li_close_idx = index_html.find('</li>', apps_idx) + len('</li>')
            index_html = index_html[:li_close_idx] + '\n' + new_tab_btn + index_html[li_close_idx:]
            print("1. Added platforms tab button to index.html")
        else:
            print("WARNING: Could not find tab_marker for apps tab in index.html")
    else:
        print("1. Platforms tab button already in index.html")

    # 2. Add platforms filter pill in software filter bar and update total count to 9
    filter_bar_marker = '<button type="button" class="software-filter-pill active" onclick="filterSoftwareMarketplace(\'all\', this)">'
    new_filter_pill = '''                    <button type="button" class="software-filter-pill software-filter-pill--platforms" onclick="filterSoftwareMarketplace('platforms', this)">
                        <span>🏛️ منصات White-Label الجاهزة</span>
                        <span class="pill-count">3 منصات</span>
                    </button>'''

    if 'class="software-filter-pill software-filter-pill--platforms"' not in index_html:
        if '6 منتجات</span>' in index_html:
            index_html = index_html.replace('6 منتجات</span>', '9 منتجات</span>', 1)
        fb_idx = index_html.find(filter_bar_marker)
        if fb_idx != -1:
            pill_close_idx = index_html.find('</button>', fb_idx) + len('</button>')
            index_html = index_html[:pill_close_idx] + '\n' + new_filter_pill + index_html[pill_close_idx:]
            print("2. Added platforms filter pill in index.html")
        else:
            print("WARNING: Could not find filter_bar_marker in index.html")
    else:
        print("2. Platforms filter pill already in index.html")

    # 3. Add platforms heading and 3 platform cards to softwareGridContainer
    cards_marker = '<!-- مختبر وبرمجيات المطور م. سليم عزيزة'
    # Extract the platforms heading and 3 cards from preview-software.html
    start_str = '<!-- ===== منصات S&R العامة القابلة للترخيص'
    end_str = '<!-- مختبر وبرمجيات المطور م. سليم عزيزة'
    s_idx = preview_software.find(start_str)
    e_idx = preview_software.find(end_str)

    if s_idx != -1 and e_idx != -1:
        platforms_cards_html = preview_software[s_idx:e_idx].strip()
        # Fix relative link in case study buttons so they stay on current page or preview-work
        # preview-work.html#platforms-xxx is great!
        if 'S&R CivicSync™' not in index_html:
            c_idx = index_html.find(cards_marker)
            if c_idx != -1:
                # Find the closing </div> of softwareGridContainer right before cards_marker
                grid_close_idx = index_html.rfind('</div>', 0, c_idx)
                index_html = index_html[:grid_close_idx] + '\n' + platforms_cards_html + '\n' + index_html[grid_close_idx:]
                print("3. Added 3 platform cards to index.html")
            else:
                print("WARNING: Could not find cards_marker in index.html")
        else:
            print("3. Platform cards already in index.html")
    else:
        print("WARNING: Could not extract platform cards from preview-software.html")

    # 4. Add platforms to projectsDB in index.html
    # Extract platforms array from preview-work.html
    p_start = preview_work.find('platforms: [')
    p_end = preview_work.find('DEFAULT_KPI_LABELS', p_start)
    if p_start != -1 and p_end != -1:
        # Find closing brace and semicolon of platforms array
        platforms_code = preview_work[p_start:p_end].strip()
        if platforms_code.endswith(','):
            platforms_code = platforms_code[:-1].strip()
        if 'platforms: [' not in index_html:
            # Insert platforms into projectsDB right before closing of projectsDB: "        };" before "let currentWorkCategory"
            target_str = '        };\n\n        let currentWorkCategory = \'websites\';'
            replacement_str = ',\n            // منصات S&R العامة القابلة للترخيص (White-Label Platforms)\n            ' + platforms_code + '\n        };\n\n        let currentWorkCategory = \'websites\';'
            if target_str in index_html:
                index_html = index_html.replace(target_str, replacement_str, 1)
                print("4. Added platforms to projectsDB in index.html")
            else:
                # Fallback search for currentWorkCategory
                cwc_idx = index_html.find("let currentWorkCategory = 'websites';")
                if cwc_idx != -1:
                    brace_idx = index_html.rfind('};', 0, cwc_idx)
                    index_html = index_html[:brace_idx] + ',\n            ' + platforms_code + '\n        ' + index_html[brace_idx:]
                    print("4. (Fallback) Added platforms to projectsDB in index.html")
                else:
                    print("WARNING: Could not find projectsDB closing in index.html")
        else:
            print("4. platforms already in projectsDB in index.html")

    # 5. Add applyKpiLabels and deep link logic to index.html
    if 'function applyKpiLabels' not in index_html:
        kpi_logic = '''
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
        '''
        cwc_idx = index_html.find("let currentWorkCategory = 'websites';")
        if cwc_idx != -1:
            index_html = index_html[:cwc_idx] + kpi_logic + '\n        ' + index_html[cwc_idx:]
            print("5. Added applyKpiLabels to index.html")

    # Check if applyKpiLabels(activeProject) is called in renderActiveWork
    if 'applyKpiLabels(activeProject);' not in index_html:
        target_render = 'const activeProject = list[currentWorkProjectIdx];'
        if target_render in index_html:
            index_html = index_html.replace(target_render, target_render + '\n            applyKpiLabels(activeProject);', 1)
            print("6. Added applyKpiLabels call to renderActiveWork in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("SUCCESS: index.html has been fully updated and synchronized!")

if __name__ == '__main__':
    main()
