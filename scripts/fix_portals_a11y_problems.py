import os
import re

print("Starting comprehensive accessibility upgrade across all HTML files...")

fixed_files = 0

for root, dirs, files in os.walk('.'):
    if any(skip in root for skip in ['.git', '.gemini', 'node_modules', '_site']):
        continue
    for file in files:
        if not file.endswith('.html'):
            continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            orig = content

            # 1. Add aria-label to role="tablist" if missing
            content = re.sub(
                r'<div class="sr-demo-tab-list" role="tablist"(?! aria-label)>',
                r'<div class="sr-demo-tab-list" role="tablist" aria-label="Demo Tabs">',
                content
            )

            # 2. Ensure buttons in tablist have role="tab" and aria-selected
            if 'id="demoTabBtnErp"' in content:
                content = re.sub(
                    r'(class="sr-demo-tab-btn\s+active")(?!.*role="tab")(\s+id="demoTabBtnErp")',
                    r'\1 role="tab" aria-selected="true"\2',
                    content
                )
            if 'id="demoTabBtnCloud"' in content:
                content = re.sub(
                    r'(class="sr-demo-tab-btn")(?!.*role="tab")(\s+id="demoTabBtnCloud")',
                    r'\1 role="tab" aria-selected="false"\2',
                    content
                )
            if 'id="demoTabBtnGov"' in content:
                content = re.sub(
                    r'(class="sr-demo-tab-btn")(?!.*role="tab")(\s+id="demoTabBtnGov")',
                    r'\1 role="tab" aria-selected="false"\2',
                    content
                )

            # 3. Add explicit <label for="roiCostRange"> to the slider header
            content = re.sub(
                r'<span class="text-white">([^<]*?)</span>(\s*<span class="sr-roi-val-badge" id="roiCostDisplay")',
                r'<label for="roiCostRange" class="text-white">\1</label>\2',
                content
            )

            # 4. Add explicit <label for="roiTeamRange"> to the team slider header
            content = re.sub(
                r'<span class="text-white">([^<]*?)</span>(\s*<span class="sr-roi-val-badge" id="roiTeamDisplay")',
                r'<label for="roiTeamRange" class="text-white">\1</label>\2',
                content
            )

            # 5. Ensure roiCostRange has title, aria-label, and placeholder
            def enhance_cost_range(match):
                tag = match.group(0)
                if 'placeholder=' not in tag:
                    tag = tag.replace('id="roiCostRange"', 'id="roiCostRange" placeholder="6500"')
                if 'title=' not in tag:
                    tag = tag.replace('id="roiCostRange"', 'id="roiCostRange" title="Monthly Operational Cost"')
                if 'aria-label=' not in tag:
                    tag = tag.replace('id="roiCostRange"', 'id="roiCostRange" aria-label="Monthly Operational Cost"')
                return tag

            content = re.sub(r'<input[^>]*id="roiCostRange"[^>]*>', enhance_cost_range, content)

            # 6. Ensure roiTeamRange has title, aria-label, and placeholder
            def enhance_team_range(match):
                tag = match.group(0)
                if 'placeholder=' not in tag:
                    tag = tag.replace('id="roiTeamRange"', 'id="roiTeamRange" placeholder="12"')
                if 'title=' not in tag:
                    tag = tag.replace('id="roiTeamRange"', 'id="roiTeamRange" title="Team Size"')
                if 'aria-label=' not in tag:
                    tag = tag.replace('id="roiTeamRange"', 'id="roiTeamRange" aria-label="Team Size"')
                return tag

            content = re.sub(r'<input[^>]*id="roiTeamRange"[^>]*>', enhance_team_range, content)

            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files += 1
                print(f"Updated: {path}")

        except Exception as e:
            print(f"Error {path}: {e}")

print(f"Done! Comprehensively updated {fixed_files} files.")
