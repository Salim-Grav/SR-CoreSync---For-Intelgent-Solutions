import os
import sys
import math
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BRANDING_DIR = os.path.join(ASSETS_DIR, "social-8k-branding")

# Color Palette
COLOR_OBSIDIAN_DEEP = (2, 7, 5, 255)
COLOR_OBSIDIAN_MID = (6, 18, 14, 255)
COLOR_OBSIDIAN_LIGHT = (14, 38, 29, 255)
COLOR_GOLD_PRIMARY = (197, 168, 128, 255)       # #c5a880
COLOR_GOLD_BRIGHT = (230, 206, 168, 255)        # #e6cea8
COLOR_GOLD_MUTED = (140, 115, 80, 255)
COLOR_WHITE = (248, 250, 252, 255)
COLOR_TEXT_MUTED = (160, 175, 170, 255)

# Fonts
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

def create_gradient_canvas(width, height, c_top=COLOR_OBSIDIAN_DEEP, c_bot=COLOR_OBSIDIAN_LIGHT):
    """Creates a smooth luxury radial/linear gradient background."""
    base = Image.new("RGBA", (width, height), c_top)
    draw = ImageDraw.Draw(base)
    # Radial glow in center-top
    cx, cy = width // 2, int(height * 0.45)
    max_radius = int(math.hypot(width, height) * 0.55)
    
    # We can draw soft concentric circles or linear gradient
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Golden ambient highlight
    glow_radius = int(min(width, height) * 0.4)
    for r in range(glow_radius, 0, -int(glow_radius / 30)):
        alpha = int(22 * (1.0 - (r / glow_radius) ** 1.5))
        glow_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(197, 168, 128, alpha)
        )
    
    # Subtle emerald ambient highlight in lower bottom
    glow_radius_em = int(min(width, height) * 0.5)
    for r in range(glow_radius_em, 0, -int(glow_radius_em / 25)):
        alpha = int(18 * (1.0 - (r / glow_radius_em)))
        glow_draw.ellipse(
            [cx - r, height - r // 2, cx + r, height + r * 1.5],
            fill=(16, 75, 50, alpha)
        )

    base = Image.alpha_composite(base, glow)
    return base

def draw_luxury_borders(draw, width, height, margin=120, line_w=4):
    """Draws subtle golden luxury double frames with corner accents."""
    # Outer frame
    draw.rectangle(
        [margin, margin, width - margin, height - margin],
        outline=(197, 168, 128, 90),
        width=line_w
    )
    # Inner subtle frame
    inner_m = margin + 30
    draw.rectangle(
        [inner_m, inner_m, width - inner_m, height - inner_m],
        outline=(197, 168, 128, 40),
        width=max(2, line_w // 2)
    )
    # Corner diamonds / accents
    corner_len = 80
    corners = [
        (margin, margin),
        (width - margin, margin),
        (margin, height - margin),
        (width - margin, height - margin)
    ]
    for cx, cy in corners:
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=COLOR_GOLD_PRIMARY)

def load_official_emblem(target_size):
    """Loads official transparent emblem scaled with high fidelity."""
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem-official.png")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as im:
            return im.convert("RGBA").resize((target_size, target_size), Image.Resampling.LANCZOS)
    return None

def save_multiformat(img, out_base_path, formats=("png", "webp", "jpg"), quality=95):
    """Saves asset in multiple web & master formats."""
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

print("Generator engine initialized.")
