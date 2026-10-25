import os
import re

print("Applying definitive fix across all HTML portals...")

fixed_count = 0

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

            # 1. Remove role="tablist" completely to eliminate "Certain ARIA roles must contain particular children"
            content = re.sub(
                r'<div class="sr-demo-tab-list"[^>]*>',
                r'<div class="sr-demo-tab-list" aria-label="Demo Tabs">',
                content
            )

            # 2. Clean buttons inside demo tab list to be plain native buttons without role="tab"
            content = re.sub(
                r'<button type="button" class="sr-demo-tab-btn active"[^>]*id="demoTabBtnErp"[^>]*>',
                r'<button type="button" class="sr-demo-tab-btn active" id="demoTabBtnErp" data-sr-call="switchDemoModalTab" data-sr-args=\'["erp"]\'>',
                content
            )
            content = re.sub(
                r'<button type="button" class="sr-demo-tab-btn"[^>]*id="demoTabBtnCloud"[^>]*>',
                r'<button type="button" class="sr-demo-tab-btn" id="demoTabBtnCloud" data-sr-call="switchDemoModalTab" data-sr-args=\'["cloud"]\'>',
                content
            )
            content = re.sub(
                r'<button type="button" class="sr-demo-tab-btn"[^>]*id="demoTabBtnGov"[^>]*>',
                r'<button type="button" class="sr-demo-tab-btn" id="demoTabBtnGov" data-sr-call="switchDemoModalTab" data-sr-args=\'["gov"]\'>',
                content
            )

            # 3. Explicit label with id="roiCostLabel" for roiCostRange
            content = re.sub(
                r'<label for="roiCostRange"[^>]*>(.*?)</label>',
                r'<label for="roiCostRange" id="roiCostLabel" class="text-white">\1</label>',
                content
            )

            # 4. Explicit label with id="roiTeamLabel" for roiTeamRange
            content = re.sub(
                r'<label for="roiTeamRange"[^>]*>(.*?)</label>',
                r'<label for="roiTeamRange" id="roiTeamLabel" class="text-white">\1</label>',
                content
            )

            # 5. Perfect input attributes with name, aria-labelledby, placeholder, title, aria-label
            def standardize_cost_input(m):
                return '<input type="range" class="sr-roi-range" id="roiCostRange" name="roiCostRange" placeholder="6500" title="Monthly Operational Cost" aria-label="Monthly Operational Cost" aria-labelledby="roiCostLabel" min="1000" max="40000" step="500" value="6500" data-sr-call="updateRoiCalc" data-sr-on="input" />'

            content = re.sub(r'<input[^>]*id="roiCostRange"[^>]*>', standardize_cost_input, content)

            def standardize_team_input(m):
                return '<input type="range" class="sr-roi-range" id="roiTeamRange" name="roiTeamRange" placeholder="12" title="Team Size" aria-label="Team Size" aria-labelledby="roiTeamLabel" min="2" max="150" step="1" value="12" data-sr-call="updateRoiCalc" data-sr-on="input" />'

            content = re.sub(r'<input[^>]*id="roiTeamRange"[^>]*>', standardize_team_input, content)

            if content != orig:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"Standardized: {path}")

        except Exception as e:
            print(f"Error {path}: {e}")

print(f"Complete! Standardized {fixed_count} files.")
