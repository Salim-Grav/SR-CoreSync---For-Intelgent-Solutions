"""
Generate Branded Luxury QR Codes with Embedded HD Gold Emblem in Center
for S&R CoreSync Solutions.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

def generate_branded_qr(data_url, out_filename, title, subtitle):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% recovery tolerance for logo center
        box_size=14,
        border=3,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    # Luxury colors: Obsidian background (#050b09) and Warm Gold modules (#dfc298)
    qr_img = qr.make_image(fill_color=(223, 194, 152), back_color=(5, 11, 9)).convert("RGBA")
    qw, qh = qr_img.size

    pad_top = 80
    pad_bottom = 70
    pad_sides = 40
    total_w = qw + pad_sides * 2
    total_h = qh + pad_top + pad_bottom

    card = Image.new("RGBA", (total_w, total_h), (4, 9, 8, 255))
    draw = ImageDraw.Draw(card)

    # Outer double gold border with rounded corners
    draw.rounded_rectangle([4, 4, total_w - 5, total_h - 5], radius=22, outline=(197, 168, 128, 230), width=2)
    draw.rounded_rectangle([10, 10, total_w - 11, total_h - 11], radius=18, outline=(197, 168, 128, 70), width=1)

    # Paste QR image
    card.paste(qr_img, (pad_sides, pad_top), qr_img)

    # Embed Center HD Gold Emblem
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem-hd.png")
    cx = total_w // 2
    cy = pad_top + qh // 2
    badge_radius = 54  # 108px diameter

    # Draw dark backing circular plate with double gold ring
    draw.ellipse([cx - badge_radius, cy - badge_radius, cx + badge_radius, cy + badge_radius],
                 fill=(5, 11, 9, 255), outline=(223, 194, 152, 255), width=3)
    draw.ellipse([cx - badge_radius + 4, cy - badge_radius + 4, cx + badge_radius - 4, cy + badge_radius - 4],
                 outline=(197, 168, 128, 120), width=1)

    if os.path.exists(emblem_path):
        emblem = Image.open(emblem_path).convert("RGBA")
        emblem_size = 78
        emblem_resized = emblem.resize((emblem_size, emblem_size), Image.Resampling.LANCZOS)
        card.paste(emblem_resized, (cx - emblem_size // 2, cy - emblem_size // 2), emblem_resized)

    # Draw Header & Footer Title text (optional fallback drawing)
    # Header: S&R CoreSync
    # Footer: Scan to Connect
    # Save at high quality
    out_path = os.path.join(ASSETS_DIR, out_filename)
    card.convert("RGB").save(out_path, "PNG")
    print(f"Generated Branded QR: {out_filename} ({total_w}x{total_h}, {os.path.getsize(out_path) // 1024} KB)")

if __name__ == "__main__":
    generate_branded_qr("https://sr-coresync.com/card.html?id=salim", "qr-founder-salim.png", "م. محمد سليم عزيزة", "CTO & Cloud Architect")
    generate_branded_qr("https://sr-coresync.com/card.html?id=raed", "qr-founder-raed.png", "أ. محمد رائد كعكة", "CFO & ERP Architect")
    generate_branded_qr("https://sr-coresync.com/", "qr-company-emblem.png", "S&R CoreSync Solutions", "Enterprise Systems")
    print("All Branded QR codes successfully generated!")
