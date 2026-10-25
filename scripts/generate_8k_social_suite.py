import os
import sys
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BRANDING_DIR = os.path.join(ASSETS_DIR, "social-8k-branding")

# Color Palette
COLOR_OBSIDIAN_DEEP = (2, 7, 5, 255)            # #020705
COLOR_OBSIDIAN_MID = (6, 18, 14, 255)           # #06120e
COLOR_OBSIDIAN_LIGHT = (14, 38, 29, 255)        # #0e261d
COLOR_GOLD_PRIMARY = (197, 168, 128, 255)       # #c5a880
COLOR_GOLD_BRIGHT = (230, 206, 168, 255)        # #e6cea8
COLOR_GOLD_MUTED = (140, 115, 80, 255)
COLOR_WHITE = (248, 250, 252, 255)
COLOR_TEXT_MUTED = (165, 185, 178, 255)
COLOR_EMERALD_ACCENT = (16, 185, 129, 255)

def get_font(size, bold=False):
    font_names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for fn in font_names:
        if os.path.exists(fn):
            try:
                return ImageFont.truetype(fn, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_text_centered(draw, xy, text, font, fill=COLOR_WHITE):
    cx, cy = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((cx - w // 2, cy - h // 2), text, font=font, fill=fill)
    return w, h

def draw_luxury_borders(draw, width, height, margin=120, line_w=4):
    """Draws subtle golden luxury double frames with corner accents."""
    draw.rectangle(
        [margin, margin, width - margin, height - margin],
        outline=(197, 168, 128, 80),
        width=line_w
    )
    inner_m = margin + 30
    draw.rectangle(
        [inner_m, inner_m, width - inner_m, height - inner_m],
        outline=(197, 168, 128, 35),
        width=max(2, line_w // 2)
    )
    corners = [
        (margin, margin),
        (width - margin, margin),
        (margin, height - margin),
        (width - margin, height - margin)
    ]
    for cx, cy in corners:
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=COLOR_GOLD_PRIMARY)

def create_luxury_base(width, height, glow_pos=None):
    """Creates an ultra-deep obsidian canvas with warm golden & emerald radial glows."""
    base = Image.new("RGBA", (width, height), COLOR_OBSIDIAN_DEEP)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    cx, cy = glow_pos if glow_pos else (width // 2, int(height * 0.42))
    glow_radius = int(min(width, height) * 0.48)
    
    # Golden glow
    steps = 30
    for i in range(steps, 0, -1):
        r = int(glow_radius * (i / steps))
        alpha = int(28 * (1.0 - (i / steps) ** 1.3))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(197, 168, 128, alpha))
        
    # Lower emerald ambient glow
    em_radius = int(min(width, height) * 0.5)
    for i in range(25, 0, -1):
        r = int(em_radius * (i / 25))
        alpha = int(22 * (1.0 - (i / 25)))
        glow_draw.ellipse([width // 2 - r, height - r // 2, width // 2 + r, height + r * 1.5], fill=(16, 75, 50, alpha))
        
    base = Image.alpha_composite(base, glow)
    return base

def load_emblem(target_size):
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem-official.png")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as im:
            return im.convert("RGBA").resize((target_size, target_size), Image.Resampling.LANCZOS)
    return None

def save_multiformat(img, out_base_path, formats=("png", "webp", "jpg"), quality=95):
    os.makedirs(os.path.dirname(out_base_path), exist_ok=True)
    results = {}
    if "png" in formats:
        p_png = out_base_path + ".png"
        img.save(p_png, "PNG", optimize=True)
        results["png"] = p_png
    if "webp" in formats:
        p_webp = out_base_path + ".webp"
        img.convert("RGB").save(p_webp, "WEBP", quality=quality, method=6)
        results["webp"] = p_webp
    if "jpg" in formats:
        p_jpg = out_base_path + ".jpg"
        img.convert("RGB").save(p_jpg, "JPEG", quality=quality, optimize=True)
        results["jpg"] = p_jpg
    return results

# -------------------------------------------------------------
# 1. Universal Corporate 8K Avatars
# -------------------------------------------------------------
def generate_universal_avatars():
    print("-> Generating Universal 8K Corporate & Founder Avatars...")
    folder = os.path.join(BRANDING_DIR, "universal")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 1.1 Master Emblem Avatar (3840 x 3840)
    w, h = 3840, 3840
    im = create_luxury_base(w, h, (w // 2, h // 2))
    draw = ImageDraw.Draw(im)
    
    # Outer gold circular frame
    pad = 180
    draw.ellipse([pad, pad, w - pad, h - pad], outline=COLOR_GOLD_PRIMARY, width=16)
    draw.ellipse([pad + 40, pad + 40, w - pad - 40, h - pad - 40], outline=(197, 168, 128, 60), width=6)
    
    # Center Emblem
    emblem = load_emblem(2000)
    if emblem:
        im.paste(emblem, (w // 2 - 1000, h // 2 - 1050), emblem)
        
    # Text below emblem
    f_brand = get_font(130, bold=True)
    f_sub = get_font(72, bold=False)
    draw_text_centered(draw, (w // 2, h // 2 + 1150), "S&R CORESYNC", f_brand, COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, h // 2 + 1300), "FOR INTELLIGENT SOLUTIONS • AMSTERDAM", f_sub, COLOR_TEXT_MUTED)
    
    base_name = os.path.join(folder, "sr-coresync-profile-avatar-8k")
    save_multiformat(im, base_name, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "universal-avatar-official",
        "title": "S&R CoreSync Official Profile Avatar 8K",
        "resolution": "3840×3840",
        "aspect_ratio": "1:1",
        "platform": "Universal (All 9 Networks)",
        "file": "assets/social-8k-branding/universal/sr-coresync-profile-avatar-8k.png",
        "description": "Master profile avatar with official gold emblem, concentric rings, and verified status."
    })

    # 1.2 Founder Avatars (Salim & Raed)
    for name, title, role_ar, file_src in [
        ("salim", "Eng. Mohammad Salim Aziza", "CTO & Principal Cloud/AI Architect", "founder-banner-salim-4k.jpg"),
        ("raed", "Mohammad Raed Kaakeh", "CFO & Enterprise Systems Director", "founder-banner-raed-4k.jpg")
    ]:
        src_path = os.path.join(ASSETS_DIR, file_src)
        if os.path.exists(src_path):
            with Image.open(src_path) as src_im:
                # Crop square around founder
                sw, sh = src_im.size
                # Founders are centered/slightly right
                sq_dim = min(sw, sh)
                crop_x = int(sw * 0.45 - sq_dim * 0.45)
                crop_y = int(sh * 0.05)
                founder_sq = src_im.crop((crop_x, crop_y, crop_x + sq_dim, crop_y + sq_dim)).resize((3840, 3840), Image.Resampling.LANCZOS)
                
                # Apply circular mask with royal border
                mask = Image.new("L", (3840, 3840), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([pad + 50, pad + 50, 3840 - pad - 50, 3840 - pad - 50], fill=255)
                
                base_f = create_luxury_base(3840, 3840, (1920, 1920))
                base_f.paste(founder_sq, (0, 0), mask)
                
                # Gold rings
                f_draw = ImageDraw.Draw(base_f)
                f_draw.ellipse([pad + 50, pad + 50, 3840 - pad - 50, 3840 - pad - 50], outline=COLOR_GOLD_PRIMARY, width=20)
                f_draw.ellipse([pad + 85, pad + 85, 3840 - pad - 85, 3840 - pad - 85], outline=(197, 168, 128, 90), width=6)
                
                # Mini emblem badge at top-right
                mini_emblem = load_emblem(500)
                if mini_emblem:
                    base_f.paste(mini_emblem, (3840 - pad - 600, pad + 100), mini_emblem)
                    
                # Executive lower ribbon
                ribbon_y = 3840 - pad - 420
                f_draw.rectangle([pad + 200, ribbon_y, 3840 - pad - 200, ribbon_y + 240], fill=(2, 7, 5, 235), outline=COLOR_GOLD_PRIMARY, width=4)
                f_name = get_font(96, bold=True)
                f_role = get_font(56, bold=False)
                draw_text_centered(f_draw, (1920, ribbon_y + 70), title, f_name, COLOR_GOLD_BRIGHT)
                draw_text_centered(f_draw, (1920, ribbon_y + 160), role_ar, f_role, COLOR_WHITE)
                
                out_p = os.path.join(folder, f"sr-coresync-profile-avatar-{name}-8k")
                save_multiformat(base_f, out_p, ("png", "webp", "jpg"))
                manifest_entries.append({
                    "id": f"universal-avatar-{name}",
                    "title": f"{title} Executive Profile Avatar 8K",
                    "resolution": "3840×3840",
                    "aspect_ratio": "1:1",
                    "platform": "Universal (All 9 Networks)",
                    "file": f"assets/social-8k-branding/universal/sr-coresync-profile-avatar-{name}-8k.png",
                    "description": f"Executive 8K avatar portrait with golden frame, official seal, and role credentials."
                })

    return manifest_entries

# -------------------------------------------------------------
# 2. LinkedIn 8K Suite
# -------------------------------------------------------------
def generate_linkedin_suite():
    print("-> Generating LinkedIn 8K Suite (4:1 Cover, Landscape Post, Carousel Cover)...")
    folder = os.path.join(BRANDING_DIR, "linkedin")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 2.1 LinkedIn Company Cover (6336 x 1584 - True 4:1 Ultra HD)
    w, h = 6336, 1584
    im = create_luxury_base(w, h, (int(w * 0.75), int(h * 0.5)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=70, line_w=4)
    
    # Left Emblem & Brand Typography
    emblem = load_emblem(900)
    if emblem:
        im.paste(emblem, (160, (h - 900) // 2), emblem)
        
    f_title = get_font(150, bold=True)
    f_tagline = get_font(72, bold=False)
    f_badges = get_font(46, bold=True)
    
    draw.text((1120, 360), "S&R CORESYNC", font=f_title, fill=COLOR_GOLD_BRIGHT)
    draw.text((1125, 540), "FOR INTELLIGENT SOLUTIONS", font=get_font(90, bold=False), fill=COLOR_WHITE)
    draw.text((1125, 680), "Enterprise Cloud Architecture • AI Automation • Global ERP Engineering", font=f_tagline, fill=COLOR_TEXT_MUTED)
    
    # Right feature badges
    bx = 4200
    badges = [
        "👑 OFFICIAL HEADQUARTERS • AMSTERDAM, NETHERLANDS",
        "⚡ NEXT-GEN CLOUD INFRASTRUCTURE & MULTI-REGION HIGH AVAILABILITY",
        "🤖 ADVANCED AI AUTOMATION & SECURE ENTERPRISE INTEGRATION",
        "🌐 GLOBAL STANDARDS • MULTI-CURRENCY • ZERO-DOWNTIME SLAs"
    ]
    by = 380
    for b in badges:
        draw.rectangle([bx - 10, by, bx + 1950, by + 90], fill=(4, 14, 10, 200), outline=(197, 168, 128, 90), width=2)
        draw.text((bx + 30, by + 22), b, font=f_badges, fill=COLOR_GOLD_BRIGHT)
        by += 130
        
    out_p = os.path.join(folder, "linkedin-company-cover-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "linkedin-company-cover",
        "title": "LinkedIn Corporate Master Cover 8K",
        "resolution": "6336×1584",
        "aspect_ratio": "4:1",
        "platform": "LinkedIn Company Page",
        "file": "assets/social-8k-branding/linkedin/linkedin-company-cover-8k.png",
        "description": "Ultra-HD corporate banner with emblem, enterprise credentials, and headquarters."
    })

    # 2.2 LinkedIn Landscape Announcement Post (7680 x 4320 - 16:9 Master)
    w, h = 7680, 4320
    im = create_luxury_base(w, h, (w // 2, int(h * 0.4)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=160, line_w=8)
    
    emblem = load_emblem(1800)
    if emblem:
        im.paste(emblem, (w // 2 - 900, 600), emblem)
        
    draw_text_centered(draw, (w // 2, 2600), "EMPOWERING ENTERPRISES WORLDWIDE", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, 2880), "INTELLIGENT CLOUD & AI SOLUTIONS", get_font(120, bold=False), COLOR_WHITE)
    draw_text_centered(draw, (w // 2, 3140), "S&R CoreSync For Intelligent Solutions • Official Corporate Launch 2026", get_font(76, bold=False), COLOR_TEXT_MUTED)
    
    # Bottom Bar
    draw.rectangle([200, 3600, w - 200, 3950], fill=(4, 14, 10, 230), outline=COLOR_GOLD_PRIMARY, width=4)
    draw_text_centered(draw, (w // 2, 3775), "AMSTERDAM, NETHERLANDS  •  WWW.SR-CORESYNC.COM  •  VERIFIED ENTERPRISE PARTNER", get_font(72, bold=True), COLOR_GOLD_BRIGHT)
    
    out_p = os.path.join(folder, "linkedin-post-landscape-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "linkedin-post-landscape",
        "title": "LinkedIn Executive Post Card 8K",
        "resolution": "7680×4320",
        "aspect_ratio": "16:9",
        "platform": "LinkedIn Feed",
        "file": "assets/social-8k-branding/linkedin/linkedin-post-landscape-8k.png",
        "description": "Master 16:9 post card for major company announcements, whitepapers, and milestones."
    })

    # 2.3 LinkedIn Document / Carousel Cover (4320 x 5400 - 4:5 Master)
    w, h = 4320, 5400
    im = create_luxury_base(w, h, (w // 2, int(h * 0.35)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=140, line_w=6)
    
    emblem = load_emblem(1400)
    if emblem:
        im.paste(emblem, (w // 2 - 700, 700), emblem)
        
    draw_text_centered(draw, (w // 2, 2400), "ENTERPRISE ARCHITECTURE", get_font(160, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, 2640), "BLUEPRINT & EXECUTION GUIDE", get_font(120, bold=True), COLOR_WHITE)
    draw_text_centered(draw, (w // 2, 2920), "Next-Generation Cloud, Sovereign AI & High-Availability ERP", get_font(76, bold=False), COLOR_TEXT_MUTED)
    
    # 3 Bullet Key Takeaways
    bx = 400
    by = 3300
    takeaways = [
        "01 / S&R Autonomous Multi-Cloud Synchronization Framework",
        "02 / Zero-Trust AI Workflow Integration for Scaled Operations",
        "03 / Verified 99.99% Reliability & High-Efficiency ROI Metrics"
    ]
    for t in takeaways:
        draw.rectangle([bx, by, w - bx, by + 220], fill=(4, 14, 10, 230), outline=(197, 168, 128, 100), width=3)
        draw.text((bx + 80, by + 65), t, font=get_font(68, bold=True), fill=COLOR_GOLD_BRIGHT)
        by += 280
        
    draw_text_centered(draw, (w // 2, 4900), "SWIPE FOR FULL WHITEPAPER ➔", get_font(84, bold=True), COLOR_GOLD_PRIMARY)

    out_p = os.path.join(folder, "linkedin-carousel-cover-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "linkedin-carousel-cover",
        "title": "LinkedIn PDF Carousel Cover 8K",
        "resolution": "4320×5400",
        "aspect_ratio": "4:5",
        "platform": "LinkedIn Documents / Carousels",
        "file": "assets/social-8k-branding/linkedin/linkedin-carousel-cover-8k.png",
        "description": "4:5 master cover designed specifically for multi-slide document carousels."
    })

    return manifest_entries

# -------------------------------------------------------------
# 3. X / Twitter 8K Suite
# -------------------------------------------------------------
def generate_x_suite():
    print("-> Generating X / Twitter 8K Suite (3:1 Header, Landscape Post)...")
    folder = os.path.join(BRANDING_DIR, "x-twitter")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 3.1 X Header Banner (7680 x 2560 - 3:1 Ultra HD)
    w, h = 7680, 2560
    im = create_luxury_base(w, h, (int(w * 0.7), int(h * 0.45)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=90, line_w=6)
    
    # Left Emblem
    emblem = load_emblem(1300)
    if emblem:
        im.paste(emblem, (250, (h - 1300) // 2), emblem)
        
    draw.text((1700, 680), "S&R CORESYNC", font=get_font(210, bold=True), fill=COLOR_GOLD_BRIGHT)
    draw.text((1710, 950), "FOR INTELLIGENT SOLUTIONS", font=get_font(120, bold=False), fill=COLOR_WHITE)
    draw.text((1710, 1140), "Architecting Sovereign AI • Autonomous Cloud • Resilient ERP Systems", font=get_font(84, bold=False), fill=COLOR_TEXT_MUTED)
    
    # Safe zone indicator info on right
    draw.rectangle([5400, 650, 7350, 1900], fill=(4, 14, 10, 220), outline=COLOR_GOLD_PRIMARY, width=3)
    draw_text_centered(draw, (6375, 820), "CORE CAPABILITIES", get_font(80, bold=True), COLOR_GOLD_BRIGHT)
    
    features = [
        "• Autonomous AI Engineering",
        "• Scalable Cloud Architecture",
        "• Enterprise ERP Platforms",
        "• Multi-National Governance"
    ]
    fy = 1000
    for f in features:
        draw.text((5520, fy), f, font=get_font(68, bold=False), fill=COLOR_WHITE)
        fy += 160
        
    draw_text_centered(draw, (6375, 1750), "HQ: AMSTERDAM • GLOBAL OPERATIONS", get_font(56, bold=True), COLOR_GOLD_MUTED)

    out_p = os.path.join(folder, "x-header-cover-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "x-header-cover",
        "title": "X / Twitter Header Cover 8K",
        "resolution": "7680×2560",
        "aspect_ratio": "3:1",
        "platform": "X (formerly Twitter)",
        "file": "assets/social-8k-branding/x-twitter/x-header-cover-8k.png",
        "description": "3:1 panoramic header banner with exact avatar safety zone allowances."
    })
    return manifest_entries

# -------------------------------------------------------------
# 4. YouTube 8K Suite
# -------------------------------------------------------------
def generate_youtube_suite():
    print("-> Generating YouTube 8K Suite (Channel Master Banner with Safe Zones, Master Thumbnail)...")
    folder = os.path.join(BRANDING_DIR, "youtube")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 4.1 Master Channel Banner (7680 x 4320 - 16:9 with TV/Desktop/Mobile safe guides)
    w, h = 7680, 4320
    im = create_luxury_base(w, h, (w // 2, h // 2))
    draw = ImageDraw.Draw(im)
    
    # TV Safe is full 7680 x 4320
    # Desktop Safe is 7680 x 1272 (middle strip)
    # Mobile/Text Safe is 4620 x 1272 (middle center)
    strip_h = int(h * (423 / 1440))  # approx 1270px
    strip_y1 = (h - strip_h) // 2
    strip_y2 = strip_y1 + strip_h
    
    # Highlight safe zone
    draw.rectangle([0, strip_y1, w, strip_y2], fill=(4, 16, 12, 180), outline=(197, 168, 128, 80), width=4)
    
    # Mobile safe zone box
    mob_w = int(w * (1546 / 2560)) # approx 4640px
    mob_x1 = (w - mob_w) // 2
    mob_x2 = mob_x1 + mob_w
    draw.rectangle([mob_x1, strip_y1, mob_x2, strip_y2], outline=COLOR_GOLD_PRIMARY, width=6)
    
    # Content inside safe area
    emblem = load_emblem(850)
    if emblem:
        im.paste(emblem, (mob_x1 + 180, strip_y1 + (strip_h - 850) // 2), emblem)
        
    draw.text((mob_x1 + 1150, strip_y1 + 280), "S&R CORESYNC", font=get_font(170, bold=True), fill=COLOR_GOLD_BRIGHT)
    draw.text((mob_x1 + 1155, strip_y1 + 490), "FOR INTELLIGENT SOLUTIONS", font=get_font(105, bold=False), fill=COLOR_WHITE)
    draw.text((mob_x1 + 1155, strip_y1 + 640), "Enterprise Cloud • Sovereign AI Automation • Intelligent ERP Platforms", font=get_font(68, bold=False), fill=COLOR_TEXT_MUTED)
    draw.text((mob_x1 + 1155, strip_y1 + 760), "SUBSCRIBE FOR EXECUTIVE TECH BRIEFINGS & CLOUD MASTERCLASSES", font=get_font(54, bold=True), fill=COLOR_GOLD_MUTED)

    # TV Area background elegance outside strip
    draw_text_centered(draw, (w // 2, 600), "S&R CORESYNC FOR INTELLIGENT SOLUTIONS • AMSTERDAM", get_font(90, bold=True), (197, 168, 128, 70))
    draw_text_centered(draw, (w // 2, 3800), "INTELLIGENT ENTERPRISE SOLUTIONS • AI & CLOUD ARCHITECTURE", get_font(90, bold=True), (197, 168, 128, 70))

    out_p = os.path.join(folder, "youtube-channel-banner-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "youtube-channel-banner",
        "title": "YouTube Master Channel Banner 8K",
        "resolution": "7680×4320",
        "aspect_ratio": "16:9",
        "platform": "YouTube Channel",
        "file": "assets/social-8k-branding/youtube/youtube-channel-banner-8k.png",
        "description": "Full TV/Desktop/Mobile safe-zone certified master banner."
    })

    # 4.2 YouTube Master Video Thumbnail (7680 x 4320 - 16:9 High Contrast Click-Worthy)
    im_thumb = create_luxury_base(w, h, (int(w * 0.8), h // 2))
    d_thumb = ImageDraw.Draw(im_thumb)
    draw_luxury_borders(d_thumb, w, h, margin=140, line_w=8)
    
    # Left Massive Text with High Contrast Obsidian Glass
    d_thumb.rectangle([300, 600, 4800, 3600], fill=(2, 7, 5, 230), outline=COLOR_GOLD_PRIMARY, width=6)
    
    d_thumb.text((500, 850), "EXECUTIVE BRIEFING", font=get_font(130, bold=True), fill=COLOR_GOLD_PRIMARY)
    d_thumb.text((500, 1150), "THE FUTURE OF", font=get_font(210, bold=True), fill=COLOR_WHITE)
    d_thumb.text((500, 1420), "ENTERPRISE AI", font=get_font(280, bold=True), fill=COLOR_GOLD_BRIGHT)
    d_thumb.text((500, 1850), "& CLOUD SYNC", font=get_font(250, bold=True), fill=COLOR_WHITE)
    
    d_thumb.rectangle([500, 2400, 4500, 2750], fill=(16, 75, 50, 200), outline=(197, 168, 128, 120), width=4)
    d_thumb.text((600, 2480), "4K/8K ARCHITECTURE DEMO & BENCHMARKS", font=get_font(90, bold=True), fill=COLOR_GOLD_BRIGHT)
    
    d_thumb.text((500, 3100), "PRESENTER: ENG. MOHAMMAD SALIM AZIZA (CTO)", font=get_font(84, bold=True), fill=COLOR_TEXT_MUTED)
    d_thumb.text((500, 3250), "GUEST: MOHAMMAD RAED KAAKEH (CFO) • AMSTERDAM", font=get_font(74, bold=False), fill=COLOR_GOLD_MUTED)

    # Right Huge Emblem
    emblem_lg = load_emblem(2300)
    if emblem_lg:
        im_thumb.paste(emblem_lg, (5000, (h - 2300) // 2), emblem_lg)

    out_thumb = os.path.join(folder, "youtube-thumbnail-master-8k")
    save_multiformat(im_thumb, out_thumb, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "youtube-thumbnail-master",
        "title": "YouTube Master Video Thumbnail 8K",
        "resolution": "7680×4320",
        "aspect_ratio": "16:9",
        "platform": "YouTube Videos",
        "file": "assets/social-8k-branding/youtube/youtube-thumbnail-master-8k.png",
        "description": "High-impact video master thumbnail with high-contrast text and 8K gold emblem."
    })

    return manifest_entries

# -------------------------------------------------------------
# 5. Instagram Suite
# -------------------------------------------------------------
def generate_instagram_suite():
    print("-> Generating Instagram 8K Suite (1:1 Square, 4:5 Portrait, 9:16 Story, 5 Highlights)...")
    folder = os.path.join(BRANDING_DIR, "instagram")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 5.1 Square Post (4320 x 4320 - 1:1)
    w, h = 4320, 4320
    im = create_luxury_base(w, h, (w // 2, int(h * 0.42)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=140, line_w=6)
    
    emblem = load_emblem(1600)
    if emblem:
        im.paste(emblem, (w // 2 - 800, 600), emblem)
        
    draw_text_centered(draw, (w // 2, 2550), "S&R CORESYNC", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, 2800), "FOR INTELLIGENT SOLUTIONS", get_font(110, bold=False), COLOR_WHITE)
    draw_text_centered(draw, (w // 2, 3050), "Architecting Enterprise Excellence in Cloud & AI", get_font(80, bold=False), COLOR_TEXT_MUTED)
    
    # Location Pill
    draw.rectangle([1100, 3350, 3220, 3550], fill=(4, 16, 12, 220), outline=COLOR_GOLD_PRIMARY, width=3)
    draw_text_centered(draw, (2160, 3450), "📍 AMSTERDAM • NETHERLANDS", get_font(72, bold=True), COLOR_GOLD_BRIGHT)

    out_p = os.path.join(folder, "instagram-post-square-8k")
    save_multiformat(im, out_p, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "instagram-post-square",
        "title": "Instagram Master Square Post 8K",
        "resolution": "4320×4320",
        "aspect_ratio": "1:1",
        "platform": "Instagram Feed",
        "file": "assets/social-8k-branding/instagram/instagram-post-square-8k.png",
        "description": "True 8K square feed asset for branding and flagship announcements."
    })

    # 5.2 Portrait Post (4320 x 5400 - 4:5 High-Engagement Feed Post)
    w, h = 4320, 5400
    im_p = create_luxury_base(w, h, (w // 2, int(h * 0.38)))
    draw_p = ImageDraw.Draw(im_p)
    draw_luxury_borders(draw_p, w, h, margin=150, line_w=6)
    
    emblem = load_emblem(1500)
    if emblem:
        im_p.paste(emblem, (w // 2 - 750, 750), emblem)
        
    draw_text_centered(draw_p, (w // 2, 2550), "ENTERPRISE INTELLIGENCE", get_font(170, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw_p, (w // 2, 2800), "BUILT FOR THE MODERN DECADE", get_font(110, bold=True), COLOR_WHITE)
    draw_text_centered(draw_p, (w // 2, 3080), "Multi-Region Cloud Sync • Private LLMs • ERP Orchestration", get_font(74, bold=False), COLOR_TEXT_MUTED)
    
    # Glass Feature Card
    draw_p.rectangle([350, 3450, 3970, 4850], fill=(2, 7, 5, 230), outline=COLOR_GOLD_PRIMARY, width=4)
    draw_text_centered(draw_p, (2160, 3650), "EXECUTIVE PILLARS", get_font(90, bold=True), COLOR_GOLD_BRIGHT)
    
    pillars = [
        "1. Sovereign Cloud Deployments with Zero Vendor Lock-in",
        "2. Domain-Trained AI Agents Driving 40%+ Cost Efficiency",
        "3. Financial & Operational ERP Custom-Fitted to Scale",
        "4. Continuous 24/7 Redundant Telemetry & SRE Support"
    ]
    py = 3850
    for pill in pillars:
        draw_p.text((450, py), pill, font=get_font(68, bold=False), fill=COLOR_WHITE)
        py += 180

    out_port = os.path.join(folder, "instagram-post-portrait-8k")
    save_multiformat(im_p, out_port, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "instagram-post-portrait",
        "title": "Instagram Master Portrait Post 8K",
        "resolution": "4320×5400",
        "aspect_ratio": "4:5",
        "platform": "Instagram Feed Portrait",
        "file": "assets/social-8k-branding/instagram/instagram-post-portrait-8k.png",
        "description": "Full-bleed 4:5 vertical feed post to dominate mobile screen real estate."
    })

    # 5.3 Instagram Story (4320 x 7680 - 9:16 Vertical Story Master)
    w, h = 4320, 7680
    im_story = create_luxury_base(w, h, (w // 2, int(h * 0.4)))
    d_story = ImageDraw.Draw(im_story)
    draw_luxury_borders(d_story, w, h, margin=180, line_w=8)
    
    # Top safe zone margin note: avatar & close button area (top 800px)
    d_story.text((350, 600), "S&R CORESYNC INTELLIGENCE", font=get_font(70, bold=True), fill=COLOR_GOLD_PRIMARY)
    
    # Center Emblem
    emblem_s = load_emblem(1800)
    if emblem_s:
        im_story.paste(emblem_s, (w // 2 - 900, 1600), emblem_s)
        
    draw_text_centered(d_story, (w // 2, 3800), "DISCOVER THE FUTURE", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(d_story, (w // 2, 4100), "OF AUTONOMOUS CLOUD & AI", get_font(120, bold=True), COLOR_WHITE)
    draw_text_centered(d_story, (w // 2, 4400), "Amsterdam • Global Enterprise Solutions", get_font(84, bold=False), COLOR_TEXT_MUTED)
    
    # Story Swipe Up / Interactive Link Area (above bottom 900px safe zone)
    d_story.rectangle([500, 5600, 3820, 6100], fill=(4, 16, 12, 230), outline=COLOR_GOLD_PRIMARY, width=6)
    draw_text_centered(d_story, (2160, 5800), "VISIT OFFICIAL PORTAL", get_font(100, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(d_story, (2160, 5950), "SR-CORESYNC.COM ➔", get_font(80, bold=True), COLOR_WHITE)

    out_story = os.path.join(folder, "instagram-story-8k")
    save_multiformat(im_story, out_story, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "instagram-story-frame",
        "title": "Instagram Master Story Frame 8K",
        "resolution": "4320×7680",
        "aspect_ratio": "9:16",
        "platform": "Instagram Stories",
        "file": "assets/social-8k-branding/instagram/instagram-story-8k.png",
        "description": "Full-screen vertical story template with safe zones for UI elements and link stickers."
    })

    # 5.4 Story Highlight Icons (5 Highlights at 2160 x 2160)
    hl_folder = os.path.join(BRANDING_DIR, "story-highlights-8k")
    os.makedirs(hl_folder, exist_ok=True)
    highlights = [
        ("about", "👑", "ABOUT US", "About S&R CoreSync"),
        ("services", "⚡", "SERVICES", "Enterprise Solutions"),
        ("cloud", "☁️", "CLOUD", "Cloud & DevOps"),
        ("ai", "🤖", "AI AGENTS", "AI Automation"),
        ("founders", "🤝", "FOUNDERS", "Executive Team")
    ]
    for hid, symbol, title, desc in highlights:
        hw, hh = 2160, 2160
        h_im = create_luxury_base(hw, hh, (hw // 2, hh // 2))
        h_draw = ImageDraw.Draw(h_im)
        
        # Golden Ring
        h_draw.ellipse([200, 200, hw - 200, hh - 200], outline=COLOR_GOLD_PRIMARY, width=16)
        h_draw.ellipse([250, 250, hw - 250, hh - 250], outline=(197, 168, 128, 70), width=6)
        
        # Center Emblem Mini
        emb_m = load_emblem(900)
        if emb_m:
            h_im.paste(emb_m, (hw // 2 - 450, hh // 2 - 500), emb_m)
            
        draw_text_centered(h_draw, (hw // 2, hh // 2 + 550), title, get_font(90, bold=True), COLOR_GOLD_BRIGHT)
        
        h_out = os.path.join(hl_folder, f"story-highlight-{hid}-8k")
        save_multiformat(h_im, h_out, ("png", "webp", "jpg"))
        manifest_entries.append({
            "id": f"story-highlight-{hid}",
            "title": f"Story Highlight: {title}",
            "resolution": "2160×2160",
            "aspect_ratio": "1:1",
            "platform": "Instagram / Facebook Highlights",
            "file": f"assets/social-8k-branding/story-highlights-8k/story-highlight-{hid}-8k.png",
            "description": f"Highlight cover icon for {desc}."
        })

    return manifest_entries

# -------------------------------------------------------------
# 6. TikTok & Snapchat & Telegram & WhatsApp
# -------------------------------------------------------------
def generate_other_platforms():
    print("-> Generating TikTok, Snapchat, Telegram, WhatsApp Suites...")
    manifest_entries = []

    # 6.1 TikTok 9:16 Vertical Cover (4320 x 7680)
    tt_folder = os.path.join(BRANDING_DIR, "tiktok")
    os.makedirs(tt_folder, exist_ok=True)
    w, h = 4320, 7680
    tt_im = create_luxury_base(w, h, (w // 2, int(h * 0.45)))
    tt_draw = ImageDraw.Draw(tt_im)
    draw_luxury_borders(tt_draw, w, h, margin=180, line_w=8)
    
    emblem = load_emblem(1800)
    if emblem:
        tt_im.paste(emblem, (w // 2 - 900, 1500), emblem)
        
    draw_text_centered(tt_draw, (w // 2, 3700), "TECH ARCHITECTURE IN 60 SECONDS", get_font(150, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(tt_draw, (w // 2, 4000), "S&R CORESYNC • AMSTERDAM", get_font(110, bold=True), COLOR_WHITE)
    draw_text_centered(tt_draw, (w // 2, 4300), "Cloud Computing • AI Automation • ERP Systems", get_font(80, bold=False), COLOR_TEXT_MUTED)
    
    out_tt = os.path.join(tt_folder, "tiktok-video-cover-8k")
    save_multiformat(tt_im, out_tt, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "tiktok-video-cover",
        "title": "TikTok Master Video Cover 8K",
        "resolution": "4320×7680",
        "aspect_ratio": "9:16",
        "platform": "TikTok",
        "file": "assets/social-8k-branding/tiktok/tiktok-video-cover-8k.png",
        "description": "Vertical cover for TikTok short-form technical reels and explainers."
    })

    # 6.2 Snapchat Story / Lens Frame (4320 x 7680)
    sc_folder = os.path.join(BRANDING_DIR, "snapchat")
    os.makedirs(sc_folder, exist_ok=True)
    sc_im = create_luxury_base(w, h, (w // 2, int(h * 0.4)))
    sc_draw = ImageDraw.Draw(sc_im)
    draw_luxury_borders(sc_draw, w, h, margin=160, line_w=8)
    
    if emblem:
        sc_im.paste(emblem, (w // 2 - 900, 1600), emblem)
    draw_text_centered(sc_draw, (w // 2, 3800), "S&R CORESYNC", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(sc_draw, (w // 2, 4100), "OFFICIAL SNAPCHAT CHANNEL", get_font(110, bold=False), COLOR_WHITE)
    
    out_sc = os.path.join(sc_folder, "snapchat-story-frame-8k")
    save_multiformat(sc_im, out_sc, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "snapchat-story-frame",
        "title": "Snapchat Official Story Frame 8K",
        "resolution": "4320×7680",
        "aspect_ratio": "9:16",
        "platform": "Snapchat",
        "file": "assets/social-8k-branding/snapchat/snapchat-story-frame-8k.png",
        "description": "Full vertical story geofilter & lens branding template."
    })

    # 6.3 Telegram Post Card & Channel Banner (7680 x 4320)
    tg_folder = os.path.join(BRANDING_DIR, "telegram")
    os.makedirs(tg_folder, exist_ok=True)
    tg_w, tg_h = 7680, 4320
    tg_im = create_luxury_base(tg_w, tg_h, (tg_w // 2, tg_h // 2))
    tg_draw = ImageDraw.Draw(tg_im)
    draw_luxury_borders(tg_draw, tg_w, tg_h, margin=160, line_w=8)
    
    emb_lg = load_emblem(1800)
    if emb_lg:
        tg_im.paste(emb_lg, (tg_w // 2 - 900, 600), emb_lg)
    draw_text_centered(tg_draw, (tg_w // 2, 2650), "S&R CORESYNC OFFICIAL TELEGRAM", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(tg_draw, (tg_w // 2, 2950), "Real-Time Tech Announcements & Sovereign Insights", get_font(110, bold=False), COLOR_WHITE)
    draw_text_centered(tg_draw, (tg_w // 2, 3250), "Direct Executive Feed: @SRCoreSync", get_font(84, bold=True), COLOR_EMERALD_ACCENT)
    
    out_tg = os.path.join(tg_folder, "telegram-post-card-8k")
    save_multiformat(tg_im, out_tg, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "telegram-post-card",
        "title": "Telegram Official Channel Card 8K",
        "resolution": "7680×4320",
        "aspect_ratio": "16:9",
        "platform": "Telegram",
        "file": "assets/social-8k-branding/telegram/telegram-post-card-8k.png",
        "description": "Master channel broadcast card for Telegram community updates."
    })

    # 6.4 WhatsApp Business Catalog & Header (7680 x 4320)
    wa_folder = os.path.join(BRANDING_DIR, "whatsapp")
    os.makedirs(wa_folder, exist_ok=True)
    wa_im = create_luxury_base(tg_w, tg_h, (tg_w // 2, tg_h // 2))
    wa_draw = ImageDraw.Draw(wa_im)
    draw_luxury_borders(wa_draw, tg_w, tg_h, margin=160, line_w=8)
    
    if emb_lg:
        wa_im.paste(emb_lg, (tg_w // 2 - 900, 600), emb_lg)
    draw_text_centered(wa_draw, (tg_w // 2, 2650), "S&R CORESYNC VERIFIED BUSINESS", get_font(180, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(wa_draw, (tg_w // 2, 2950), "Intelligent Enterprise Solutions • Official WhatsApp Concierge", get_font(110, bold=False), COLOR_WHITE)
    draw_text_centered(wa_draw, (tg_w // 2, 3250), "Direct Line: +31 20 123 4567 • Amsterdam, Netherlands", get_font(84, bold=True), COLOR_GOLD_MUTED)
    
    out_wa = os.path.join(wa_folder, "whatsapp-catalog-header-8k")
    save_multiformat(wa_im, out_wa, ("png", "webp", "jpg"))
    manifest_entries.append({
        "id": "whatsapp-catalog-header",
        "title": "WhatsApp Business Catalog Header 8K",
        "resolution": "7680×4320",
        "aspect_ratio": "16:9",
        "platform": "WhatsApp Business",
        "file": "assets/social-8k-branding/whatsapp/whatsapp-catalog-header-8k.png",
        "description": "Official business catalog header banner for enterprise customer service."
    })

    return manifest_entries

# -------------------------------------------------------------
# 7. Video Shorts & Reels 8K Studio Overlays (9:16 Transparent PNG)
# -------------------------------------------------------------
def generate_video_shorts_overlays():
    print("-> Generating 8K Video Shorts & Reels Master Overlays (Transparent 9:16 Guides & Lower Thirds)...")
    folder = os.path.join(BRANDING_DIR, "video-shorts-reels-8k")
    os.makedirs(folder, exist_ok=True)
    manifest_entries = []

    # 7.1 True 8K Transparent Video Frame (4320 x 7680)
    w, h = 4320, 7680
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame)
    
    # 1. Subtle royal outer border (just inside video edge)
    margin = 80
    draw.rectangle([margin, margin, w - margin, h - margin], outline=(197, 168, 128, 120), width=6)
    
    # 2. Top-Right Watermark Emblem
    emb_watermark = load_emblem(650)
    if emb_watermark:
        # Subtle alpha watermark
        wm = emb_watermark.copy()
        r, g, b, a = wm.split()
        a = a.point(lambda p: int(p * 0.75))
        wm.putalpha(a)
        frame.paste(wm, (w - 750 - margin, margin + 250), wm)
        
    # 3. Top-Left Channel Tag
    draw.text((margin + 120, margin + 280), "S&R CORESYNC", font=get_font(90, bold=True), fill=(230, 206, 168, 220))
    draw.text((margin + 125, margin + 390), "INTELLIGENT SOLUTIONS", font=get_font(56, bold=False), fill=(248, 250, 252, 180))

    # 4. Bottom Lower-Third Executive Brand Bar (Height 850px, above YouTube Shorts / TikTok bottom margin)
    # The bottom 1200px has caption & music disk on TikTok/Reels, so lower third is placed between y=5400 and y=6300
    bar_y1 = 5450
    bar_y2 = 6250
    
    # Obsidian glass pill
    bar_img = Image.new("RGBA", (w - 2 * (margin + 80), bar_y2 - bar_y1), (2, 7, 5, 230))
    bar_draw = ImageDraw.Draw(bar_img)
    bar_draw.rectangle([0, 0, bar_img.width, bar_img.height], outline=COLOR_GOLD_PRIMARY, width=6)
    
    # Mini emblem in bar
    emb_bar = load_emblem(550)
    if emb_bar:
        bar_img.paste(emb_bar, (80, (bar_img.height - 550) // 2), emb_bar)
        
    bar_draw.text((700, 160), "S&R CORESYNC | INTELLIGENT ARCHITECTURE", font=get_font(96, bold=True), fill=COLOR_GOLD_BRIGHT)
    bar_draw.text((705, 300), "Enterprise Cloud • Autonomous AI • Next-Gen ERP Systems", font=get_font(68, bold=False), fill=COLOR_WHITE)
    bar_draw.text((705, 430), "AMSTERDAM, NETHERLANDS  •  WWW.SR-CORESYNC.COM", font=get_font(54, bold=True), fill=COLOR_GOLD_MUTED)
    
    frame.paste(bar_img, (margin + 80, bar_y1), bar_img)
    
    # 5. Safe Area Visual Guide Overlay (Optional inspection copy)
    p_png = os.path.join(folder, "video-short-master-overlay-8k.png")
    frame.save(p_png, "PNG")
    
    # Also save a visual guide showing creators exact safe margins
    guide_im = frame.copy()
    g_draw = ImageDraw.Draw(guide_im)
    # Highlight top safe zone (header/progress bar)
    g_draw.rectangle([margin, margin, w - margin, margin + 650], outline=(255, 75, 75, 160), width=4)
    g_draw.text((w // 2 - 600, margin + 40), "[ TOP SAFE ZONE: SYSTEM & SEARCH UI ]", font=get_font(54, bold=True), fill=(255, 100, 100, 200))
    
    # Highlight right UI action button zone (Like, Comment, Share, Sound Disc)
    g_draw.rectangle([w - 650, 3000, w - margin, 7000], outline=(255, 180, 50, 160), width=4)
    g_draw.text((w - 600, 3100), "RIGHT UI\nBUTTONS\nSAFE ZONE", font=get_font(48, bold=True), fill=(255, 180, 50, 220))
    
    # Highlight bottom caption zone
    g_draw.rectangle([margin, 6350, w - margin, h - margin], outline=(255, 75, 75, 160), width=4)
    g_draw.text((w // 2 - 650, 6450), "[ BOTTOM SAFE ZONE: CAPTIONS & AUDIO DISC ]", font=get_font(54, bold=True), fill=(255, 100, 100, 200))
    
    p_guide = os.path.join(folder, "video-short-safe-zone-guide-8k.png")
    guide_im.save(p_guide, "PNG")
    
    manifest_entries.append({
        "id": "video-short-master-overlay",
        "title": "8K Video Shorts & Reels Master Transparent Overlay",
        "resolution": "4320×7680",
        "aspect_ratio": "9:16",
        "platform": "YouTube Shorts / Instagram Reels / TikTok",
        "file": "assets/social-8k-branding/video-shorts-reels-8k/video-short-master-overlay-8k.png",
        "description": "Transparent 8K video overlay layer with luxury lower-third brand bar and watermark."
    })
    manifest_entries.append({
        "id": "video-short-safe-zone-guide",
        "title": "8K Shorts & Reels Safe Zone Inspection Guide",
        "resolution": "4320×7680",
        "aspect_ratio": "9:16",
        "platform": "Studio Video Production Guide",
        "file": "assets/social-8k-branding/video-shorts-reels-8k/video-short-safe-zone-guide-8k.png",
        "description": "Precision creator template marking UI safe zones for captions, buttons, and system headers."
    })

    return manifest_entries

# -------------------------------------------------------------
# Main Orchestrator
# -------------------------------------------------------------
def main():
    print("=========================================================")
    print("   S&R CoreSync - Master 8K Social Media Suite Engine    ")
    print("=========================================================")
    
    all_manifest = []
    all_manifest.extend(generate_universal_avatars())
    all_manifest.extend(generate_linkedin_suite())
    all_manifest.extend(generate_x_suite())
    all_manifest.extend(generate_youtube_suite())
    all_manifest.extend(generate_instagram_suite())
    all_manifest.extend(generate_other_platforms())
    all_manifest.extend(generate_video_shorts_overlays())
    
    manifest_data = {
        "suite_name": "S&R CoreSync Enterprise 8K Visual & Social Media Identity Suite",
        "version": "2026.1-UHD-8K",
        "total_assets": len(all_manifest),
        "platforms_supported": [
            "LinkedIn", "X (Twitter)", "YouTube", "Meta (Facebook)",
            "Instagram", "TikTok", "Snapchat", "Telegram", "WhatsApp Business"
        ],
        "resolutions": ["7680×4320 (16:9)", "4320×7680 (9:16)", "6336×1584 (4:1)", "7680×2560 (3:1)", "4320×4320 (1:1)", "3840×3840 (1:1)", "4320×5400 (4:5)"],
        "assets": all_manifest
    }
    
    manifest_file = os.path.join(BRANDING_DIR, "manifest.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Master 8K Social Suite generated with {len(all_manifest)} assets.")
    print(f"Manifest saved to: {manifest_file}")

if __name__ == "__main__":
    main()
