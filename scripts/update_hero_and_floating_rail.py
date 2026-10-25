# -*- coding: utf-8 -*-
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_floating_follow(is_rtl=True):
    lbl_follow = "تابع S&R CoreSync For Intelligent Solutions على وسائل التواصل" if is_rtl else "Follow S&R CoreSync For Intelligent Solutions on social media"
    lbl_chat = "المساعد الذكي والمحادثة المباشرة" if is_rtl else "AI Concierge & Live Chat"
    title_chat = "المساعد الذكي (AI Concierge) | المحادثة الفورية" if is_rtl else "AI Concierge | Live Chat"
    
    return f"""    <aside class="floating-follow" aria-label="{lbl_follow}">
        <div class="floating-follow__icons">
            <a href="https://wa.me/31687764998" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--whatsapp" aria-label="WhatsApp" title="WhatsApp">
                <svg viewBox="0 0 32 32" aria-hidden="true" focusable="false" width="15" height="15"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z" fill="currentColor"/></svg>
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--linkedin" aria-label="LinkedIn" title="LinkedIn">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76c-.95 0-1.72.77-1.72 1.72s.77 1.73 1.72 1.73a1.73 1.73 0 0 0 1.73-1.73c0-.95-.78-1.72-1.73-1.72m1.39 9.74v-8.37H5.07v8.37h2.78Z"/></svg>
            </a>
            <a href="mailto:info@sr-coresync.com" class="floating-follow__link floating-follow__link--mail" aria-label="Email" title="info@sr-coresync.com">
                <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
            </a>
            <a href="https://facebook.com/SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--facebook" aria-label="Facebook" title="Facebook">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
            <a href="https://instagram.com/SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--instagram" aria-label="Instagram" title="Instagram">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            </a>
            <a href="https://x.com/SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--x" aria-label="X (Twitter)" title="X (Twitter)">
                <svg viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="https://youtube.com/@SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--youtube" aria-label="YouTube" title="YouTube">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
            <a href="https://tiktok.com/@SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--tiktok" aria-label="TikTok" title="TikTok">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.24 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
            </a>
            <a href="https://snapchat.com/add/SRCoreSync" target="_blank" rel="noopener noreferrer" class="floating-follow__link floating-follow__link--snapchat" aria-label="Snapchat" title="Snapchat">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12.003 2c-3.134 0-5.38 2.213-5.38 5.163 0 .762.186 1.678.508 2.378-.85.342-1.854 1.09-1.854 2.135 0 .61.352 1.09.845 1.343-.24.577-.732 1.353-1.677 1.626-.376.109-.645.437-.645.827 0 .536.467.92 1.032.88 1.41-.097 2.65-.63 3.51-1.44.757.545 1.745.856 2.841.856s2.084-.311 2.841-.856c.86.81 2.1 1.343 3.51 1.44.565.04 1.032-.344 1.032-.88 0-.39-.269-.718-.645-.827-.945-.273-1.437-1.049-1.677-1.626.493-.253.845-.733.845-1.343 0-1.045-1.004-1.793-1.854-2.135.322-.7.508-1.616.508-2.378C17.383 4.213 15.137 2 12.003 2z"/></svg>
            </a>
        </div>
        <span class="floating-follow__line" aria-hidden="true"></span>
        <span class="floating-follow__label">S&amp;R CORESYNC</span>
        <span class="floating-follow__line" aria-hidden="true"></span>
        <button type="button" class="floating-follow__link floating-follow__link--chat floating-follow__chat-bottom" id="floatingFollowChatBtn" aria-label="{lbl_chat}" title="{title_chat}" onclick="window.toggleAiChat && window.toggleAiChat()">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a9 9 0 0 1 9 9c0 3.1-1.6 5.9-4 7.5V21a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1v-2.5A9 9 0 0 1 3 11a9 9 0 0 1 9-9z"/><circle cx="9" cy="12" r="1" fill="currentColor"/><circle cx="12" cy="12" r="1" fill="currentColor"/><circle cx="15" cy="12" r="1" fill="currentColor"/></svg>
            <span class="floating-follow__live-dot" aria-hidden="true"></span>
        </button>
    </aside>"""

# Regex matching <aside class="floating-follow"[^>]*>.*?</aside>
FLOATING_FOLLOW_REGEX = re.compile(
    r'<aside class="floating-follow"[^>]*>.*?</aside>',
    re.DOTALL
)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    rel_path = os.path.relpath(filepath, ROOT).replace('\\', '/')
    is_ar = rel_path == 'index.html' or rel_path.startswith('ar/') or rel_path.startswith('ckb/') or rel_path.startswith('ku/')

    # 1. Replace floating-follow
    if FLOATING_FOLLOW_REGEX.search(content):
        content = FLOATING_FOLLOW_REGEX.sub(get_floating_follow(is_rtl=is_ar), content)

    # 2. Update Hero 3D Emblem to be completely unmasked
    # Target badges inside hero-emblem-card-3d
    btn_inspect_txt = "فحص الشعار بدقة 4K Ultra-DPI" if is_ar else "Inspect 4K Ultra-DPI Seal"
    btn_inspect_title = "فحص الشعار بدقة 4K فائقة" if is_ar else "Inspect Luxury 4K Emblem"
    btn_cloud_txt = "Enterprise Cloud &amp; AI Native"

    # Regex targeting from <div class="hero-emblem-badge hero-emblem-badge--top"> until closing of card
    # In index.html:
    # <div class="hero-emblem-badge hero-emblem-badge--top">...</div>
    # ...
    # </div>\s*</div>\s*</div>
    BADGES_BLOCK_REGEX = re.compile(
        r'(<div class="hero-emblem-frame">.*?</div>)\s*(?:<!--.*?-->\s*)?<div class="hero-emblem-badge hero-emblem-badge--top">.*?</div>\s*</div>\s*</div>\s*</div>',
        re.DOTALL
    )

    if BADGES_BLOCK_REGEX.search(content) and 'hero-emblem-actions-bar' not in content:
        repl_str = (
            r'\1\n'
            '                                    </div>\n'
            '                                    <div class="hero-emblem-actions-bar">\n'
            f'                                        <button type="button" class="btn-emblem-pill btn-emblem-inspect" data-sr-call="openLogoLightbox" data-sr-event="1" title="{btn_inspect_title}">\n'
            '                                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>\n'
            f'                                            <span>{btn_inspect_txt}</span>\n'
            '                                        </button>\n'
            '                                        <div class="btn-emblem-pill btn-emblem-cloud">\n'
            '                                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>\n'
            f'                                            <span>{btn_cloud_txt}</span>\n'
            '                                        </div>\n'
            '                                    </div>\n'
            '                                </div>\n'
            '                            </div>'
        )
        content = BADGES_BLOCK_REGEX.sub(repl_str, content)

    if content != orig:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        return True
    return False

count = 0
for dirpath, dirs, files in os.walk(ROOT):
    if any(x in dirpath for x in ['.git', '_site', 'node_modules']):
        continue
    for f in files:
        if f == 'index.html':
            fp = os.path.join(dirpath, f)
            if update_file(fp):
                count += 1
                print(f"[UPDATED] {os.path.relpath(fp, ROOT)}")

print(f"Total index.html updated: {count}")
