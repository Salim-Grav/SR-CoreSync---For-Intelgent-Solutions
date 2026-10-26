import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BRANDING_DIR = os.path.join(ASSETS_DIR, "social-8k-branding")

# Color Palette
COLOR_OBSIDIAN_DEEP = (2, 7, 5, 255)
COLOR_GOLD_PRIMARY = (197, 168, 128, 255)
COLOR_GOLD_BRIGHT = (230, 206, 168, 255)
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
    draw.rectangle([margin, margin, width - margin, height - margin], outline=(197, 168, 128, 80), width=line_w)
    inner_m = margin + 30
    draw.rectangle([inner_m, inner_m, width - inner_m, height - inner_m], outline=(197, 168, 128, 35), width=max(2, line_w // 2))
    corners = [(margin, margin), (width - margin, margin), (margin, height - margin), (width - margin, height - margin)]
    for cx, cy in corners:
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=COLOR_GOLD_PRIMARY)

def create_luxury_base(width, height, glow_pos=None):
    base = Image.new("RGBA", (width, height), COLOR_OBSIDIAN_DEEP)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = glow_pos if glow_pos else (width // 2, int(height * 0.45))
    glow_radius = int(min(width, height) * 0.5)
    for i in range(25, 0, -1):
        r = int(glow_radius * (i / 25))
        alpha = int(28 * (1.0 - (i / 25) ** 1.3))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(197, 168, 128, alpha))
    em_radius = int(min(width, height) * 0.45)
    for i in range(20, 0, -1):
        r = int(em_radius * (i / 20))
        alpha = int(20 * (1.0 - (i / 20)))
        glow_draw.ellipse([width // 2 - r, height - r // 2, width // 2 + r, height + r * 1.5], fill=(16, 75, 50, alpha))
    return Image.alpha_composite(base, glow)

def load_emblem(target_size):
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem-official.png")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as im:
            return im.convert("RGBA").resize((target_size, target_size), Image.Resampling.LANCZOS)
    return None

def save_multiformat(img, out_base_path):
    os.makedirs(os.path.dirname(out_base_path), exist_ok=True)
    # PNG
    img.save(out_base_path + ".png", "PNG", optimize=True)
    # WebP
    img.save(out_base_path + ".webp", "WEBP", quality=95, method=6)
    # JPG
    rgb = Image.new("RGB", img.size, (2, 7, 5))
    rgb.paste(img, mask=img.split()[3])
    rgb.save(out_base_path + ".jpg", "JPEG", quality=95)
    print(f"  [SAVED] {os.path.basename(out_base_path)} (PNG, WEBP, JPG)")

def generate_linkedin_company_exact():
    print("-> 1. Generating LinkedIn Company Page Cover (6768 x 1146 - True 5.91:1 Standard)...")
    folder = os.path.join(BRANDING_DIR, "linkedin")
    w, h = 6768, 1146
    im = create_luxury_base(w, h, (int(w * 0.7), int(h * 0.5)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=40, line_w=4)
    
    # Left Emblem & Brand Typography
    emblem = load_emblem(780)
    if emblem:
        im.paste(emblem, (120, (h - 780) // 2), emblem)
        
    f_title = get_font(130, bold=True)
    f_sub = get_font(72, bold=False)
    f_tagline = get_font(52, bold=False)
    f_badges = get_font(38, bold=True)
    
    draw.text((980, 240), "S&R CORESYNC", font=f_title, fill=COLOR_GOLD_BRIGHT)
    draw.text((985, 410), "FOR INTELLIGENT SOLUTIONS", font=f_sub, fill=COLOR_WHITE)
    draw.text((985, 530), "Enterprise Cloud Architecture • AI Automation • Global Sovereign ERP", font=f_tagline, fill=COLOR_TEXT_MUTED)
    draw.text((985, 630), "Official Headquarters: Amsterdam, Netherlands  |  www.sr-coresync.com", font=get_font(44, bold=True), fill=COLOR_GOLD_MUTED)
    
    # Right Badges with proper alignment
    bx = 4250
    badges = [
        "👑 OFFICIAL COMPANY PAGE • S&R CORESYNC",
        "⚡ NEXT-GEN CLOUD INFRASTRUCTURE & MULTI-REGION HIGH AVAILABILITY",
        "🤖 ADVANCED AI AUTOMATION & SECURE ENTERPRISE INTEGRATION",
        "🌐 VERIFIED SOVEREIGN CLOUD ARCHITECTURE & ZERO-DOWNTIME SLAs"
    ]
    by = 220
    for b in badges:
        draw.rectangle([bx, by, bx + 2400, by + 100], fill=(4, 14, 10, 210), outline=(197, 168, 128, 90), width=2)
        draw.text((bx + 35, by + 24), b, font=f_badges, fill=COLOR_GOLD_BRIGHT)
        by += 135
        
    out_p = os.path.join(folder, "linkedin-company-cover-8k")
    save_multiformat(im, out_p)

def generate_facebook_suite():
    print("-> 2. Generating Meta / Facebook Suite (Page Cover 6560x2496, Landscape Post 7680x4020, Square Post 4320x4320)...")
    folder = os.path.join(BRANDING_DIR, "facebook")
    os.makedirs(folder, exist_ok=True)
    
    # 2.1 Facebook Page Cover (6560 x 2496 - True 2.63:1 with Mobile Safe Zone)
    w, h = 6560, 2496
    im = create_luxury_base(w, h, (w // 2, int(h * 0.48)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=80, line_w=6)
    
    # Center-left emblem
    emblem = load_emblem(1200)
    if emblem:
        im.paste(emblem, (450, (h - 1200) // 2), emblem)
        
    f_title = get_font(180, bold=True)
    f_sub = get_font(100, bold=False)
    f_tag = get_font(72, bold=False)
    
    draw.text((1800, 720), "S&R CORESYNC", font=f_title, fill=COLOR_GOLD_BRIGHT)
    draw.text((1805, 960), "FOR INTELLIGENT SOLUTIONS", font=f_sub, fill=COLOR_WHITE)
    draw.text((1805, 1140), "Enterprise Cloud Infrastructure • AI Executive Systems • Global ERP", font=f_tag, fill=COLOR_TEXT_MUTED)
    draw.text((1805, 1290), "Amsterdam, Netherlands  •  Official Meta Business Page: @SRCoreSync", font=get_font(60, bold=True), fill=COLOR_EMERALD_ACCENT)
    
    # Safe zone badge bottom
    draw.rectangle([450, 1950, w - 450, 2250], fill=(4, 14, 10, 220), outline=COLOR_GOLD_PRIMARY, width=3)
    draw_text_centered(draw, (w // 2, 2100), "POWERING MODERN DIGITAL TRANSFORMATION ACROSS EUROPE & THE ARABIAN GULF", get_font(64, bold=True), COLOR_GOLD_BRIGHT)
    
    out_cover = os.path.join(folder, "facebook-page-cover-8k")
    save_multiformat(im, out_cover)
    
    # 2.2 Facebook Landscape Announcement Post (7680 x 4020 - 1.91:1)
    w, h = 7680, 4020
    im = create_luxury_base(w, h, (w // 2, int(h * 0.42)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=150, line_w=8)
    
    emblem_lg = load_emblem(1600)
    if emblem_lg:
        im.paste(emblem_lg, (w // 2 - 800, 500), emblem_lg)
        
    draw_text_centered(draw, (w // 2, 2400), "S&R CORESYNC FOR INTELLIGENT SOLUTIONS", get_font(170, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, 2680), "OFFICIAL FACEBOOK LAUNCH • ENTERPRISE SUITE 2026", get_font(110, bold=False), COLOR_WHITE)
    draw_text_centered(draw, (w // 2, 2920), "Next-Generation Sovereign Cloud • Autonomous AI • Mission-Critical ERP", get_font(76, bold=False), COLOR_TEXT_MUTED)
    
    draw.rectangle([250, 3350, w - 250, 3700], fill=(4, 14, 10, 230), outline=COLOR_GOLD_PRIMARY, width=4)
    draw_text_centered(draw, (w // 2, 3525), "FOLLOW US ON FACEBOOK: @SRCoreSync  •  WWW.SR-CORESYNC.COM  •  AMSTERDAM", get_font(70, bold=True), COLOR_GOLD_BRIGHT)
    
    out_post = os.path.join(folder, "facebook-post-landscape-8k")
    save_multiformat(im, out_post)

    # 2.3 Facebook Square Feed Post (4320 x 4320 - 1:1)
    w, h = 4320, 4320
    im = create_luxury_base(w, h, (w // 2, int(h * 0.4)))
    draw = ImageDraw.Draw(im)
    draw_luxury_borders(draw, w, h, margin=140, line_w=8)
    
    if emblem_lg:
        im.paste(emblem_lg, (w // 2 - 800, 600), emblem_lg)
        
    draw_text_centered(draw, (w // 2, 2550), "S&R CORESYNC", get_font(190, bold=True), COLOR_GOLD_BRIGHT)
    draw_text_centered(draw, (w // 2, 2830), "INTELLIGENT SOLUTIONS", get_font(130, bold=False), COLOR_WHITE)
    draw_text_centered(draw, (w // 2, 3100), "Official Corporate Channel @SRCoreSync", get_font(84, bold=True), COLOR_EMERALD_ACCENT)
    
    draw.rectangle([200, 3550, w - 200, 3950], fill=(4, 14, 10, 230), outline=COLOR_GOLD_PRIMARY, width=4)
    draw_text_centered(draw, (w // 2, 3750), "GLOBAL B2B SOLUTIONS  •  AMSTERDAM HQ", get_font(72, bold=True), COLOR_GOLD_BRIGHT)
    
    out_sq = os.path.join(folder, "facebook-post-square-8k")
    save_multiformat(im, out_sq)

if __name__ == "__main__":
    generate_linkedin_company_exact()
    generate_facebook_suite()
    print("ALL ASSETS GENERATED SUCCESSFULLY!")
