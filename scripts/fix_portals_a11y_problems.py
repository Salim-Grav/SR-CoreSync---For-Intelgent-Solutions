import os
import glob
import re

print("Starting accessibility fix across all HTML files...")

fixed_files = 0
fixed_cost = 0
fixed_team = 0
fixed_tabs = 0

for root, dirs, files in os.walk('.'):
    # Skip non-project or cache directories if any
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
            
            # 1. Fix demoTabBtnErp
            if 'id="demoTabBtnErp"' in content and 'role="tab"' not in content[content.find('id="demoTabBtnErp"')-60:content.find('id="demoTabBtnErp"')+60]:
                content = re.sub(
                    r'(class="sr-demo-tab-btn\s+active")(\s+id="demoTabBtnErp")',
                    r'\1 role="tab" aria-selected="true"\2',
                    content
                )
                fixed_tabs += 1

            # 2. Fix demoTabBtnCloud
            if 'id="demoTabBtnCloud"' in content and 'role="tab"' not in content[content.find('id="demoTabBtnCloud"')-60:content.find('id="demoTabBtnCloud"')+60]:
                content = re.sub(
                    r'(class="sr-demo-tab-btn")(\s+id="demoTabBtnCloud")',
                    r'\1 role="tab" aria-selected="false"\2',
                    content
                )

            # 3. Fix demoTabBtnGov
            if 'id="demoTabBtnGov"' in content and 'role="tab"' not in content[content.find('id="demoTabBtnGov"')-60:content.find('id="demoTabBtnGov"')+60]:
                content = re.sub(
                    r'(class="sr-demo-tab-btn")(\s+id="demoTabBtnGov")',
                    r'\1 role="tab" aria-selected="false"\2',
                    content
                )

            # 4. Fix roiCostRange missing title/aria-label
            # Match input where id="roiCostRange" without title=
            def fix_cost_range(match):
                tag = match.group(0)
                if 'title=' not in tag and 'aria-label=' not in tag:
                    # insert title and aria-label before data-sr-call or at the end
                    return tag.replace('id="roiCostRange"', 'id="roiCostRange" title="Monthly Operational Cost" aria-label="Monthly Operational Cost"')
                return tag

            new_content = re.sub(r'<input[^>]*id="roiCostRange"[^>]*>', fix_cost_range, content)
            if new_content != content:
                content = new_content
                fixed_cost += 1

            # 5. Fix roiTeamRange missing title/aria-label
            def fix_team_range(match):
                tag = match.group(0)
                if 'title=' not in tag and 'aria-label=' not in tag:
                    return tag.replace('id="roiTeamRange"', 'id="roiTeamRange" title="Team Size" aria-label="Team Size"')
                return tag

            new_content = re.sub(r'<input[^>]*id="roiTeamRange"[^>]*>', fix_team_range, content)
            if new_content != content:
                content = new_content
                fixed_team += 1

            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files += 1
                print(f"Updated: {path}")

        except Exception as e:
            print(f"Error processing {path}: {e}")

print(f"Done! Updated {fixed_files} files (Fixed tabs in {fixed_tabs}, cost sliders in {fixed_cost}, team sliders in {fixed_team}).")
