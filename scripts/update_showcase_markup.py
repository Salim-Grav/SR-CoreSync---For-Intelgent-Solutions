import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"

def update_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Add social-8k-studio button in showcase tabs if not present
    is_subfolder = os.path.dirname(os.path.abspath(file_path)) != os.path.abspath(PROJECT_ROOT)
    prefix = "../" if is_subfolder else ""

    social_btn_html = f'''                        <a href="{prefix}social-8k-studio.html" target="_blank" class="showcase-tab-btn showcase-tab-btn-social8k" title="8K Social Branding Suite">
                            <span class="showcase-tab-dot"></span>
                            <span>استوديو السوشيال ميديا (8K Suite) 🎬</span>
                        </a>'''

    if "social-8k-studio.html" not in content:
        # insert right after card.html
        pattern_card = r'(<a href="[^"]*card\.html"[^>]*>[\s\S]*?</a>)'
        if re.search(pattern_card, content):
            content = re.sub(pattern_card, r'\1\n' + social_btn_html, content, count=1)

    # 2. Upgrade Salim banner picture tag to use high-DPI srcset
    # Old:
    # <source srcset="(?:\./|\.\./)?assets/founder-banner-salim\.webp" type="image/webp">
    # <img src="(?:\./|\.\./)?assets/founder-banner-salim\.jpg" alt="[^"]*" class="showcase-img" width="1024" height="576" loading="eager">
    salim_assets = f"{prefix}assets"
    
    pattern_salim_pic = r'<picture>\s*<source srcset="(?:\./|\.\./)?assets/founder-banner-salim\.webp" type="image/webp">\s*<img src="(?:\./|\.\./)?assets/founder-banner-salim\.jpg" alt="([^"]*)" class="showcase-img" width="1024" height="576" loading="eager">\s*</picture>'
    repl_salim_pic = f'''<picture>
                                            <source srcset="{salim_assets}/founder-banner-salim-4k.webp 3840w, {salim_assets}/founder-banner-salim.webp 2560w" sizes="(max-width: 1200px) 100vw, 1920px" type="image/webp">
                                            <source srcset="{salim_assets}/founder-banner-salim-4k.jpg 3840w, {salim_assets}/founder-banner-salim.jpg 2560w" sizes="(max-width: 1200px) 100vw, 1920px" type="image/jpeg">
                                            <img src="{salim_assets}/founder-banner-salim.jpg" alt="\\1" class="showcase-img" width="2560" height="1440" loading="eager">
                                        </picture>'''
    content = re.sub(pattern_salim_pic, repl_salim_pic, content)

    # 3. Upgrade Raed banner picture tag
    pattern_raed_pic = r'<picture>\s*<source srcset="(?:\./|\.\./)?assets/founder-banner-raed\.webp" type="image/webp">\s*<img src="(?:\./|\.\./)?assets/founder-banner-raed\.jpg" alt="([^"]*)" class="showcase-img" width="1024" height="576" loading="eager">\s*</picture>'
    repl_raed_pic = f'''<picture>
                                            <source srcset="{salim_assets}/founder-banner-raed-4k.webp 3840w, {salim_assets}/founder-banner-raed.webp 2560w" sizes="(max-width: 1200px) 100vw, 1920px" type="image/webp">
                                            <source srcset="{salim_assets}/founder-banner-raed-4k.jpg 3840w, {salim_assets}/founder-banner-raed.jpg 2560w" sizes="(max-width: 1200px) 100vw, 1920px" type="image/jpeg">
                                            <img src="{salim_assets}/founder-banner-raed.jpg" alt="\\1" class="showcase-img" width="2560" height="1440" loading="eager">
                                        </picture>'''
    content = re.sub(pattern_raed_pic, repl_raed_pic, content)

    # 4. Also upgrade openFoundersLightbox paths to 4k
    # data-sr-args='["assets/founder-banner-salim.jpg" -> data-sr-args='["assets/founder-banner-salim-4k.jpg"
    content = content.replace('founder-banner-salim.jpg", "م. محمد سليم عزيزة', 'founder-banner-salim-4k.jpg", "م. محمد سليم عزيزة')
    content = content.replace('founder-banner-raed.jpg", "أ. محمد رائد كعكة', 'founder-banner-raed-4k.jpg", "أ. محمد رائد كعكة')

    if content != orig_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {os.path.relpath(file_path, PROJECT_ROOT)}")
        return True
    return False

def main():
    updated = 0
    # Update root index.html
    root_index = os.path.join(PROJECT_ROOT, "index.html")
    if os.path.exists(root_index):
        if update_file(root_index):
            updated += 1

    # Check all subdirectories with index.html
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if "node_modules" in root or ".git" in root or "social-8k-branding" in root:
            continue
        for file in files:
            if file == "index.html" and root != PROJECT_ROOT:
                p = os.path.join(root, file)
                if update_file(p):
                    updated += 1

    print(f"Total HTML files updated with 8K showcase & banners: {updated}")

if __name__ == "__main__":
    main()
