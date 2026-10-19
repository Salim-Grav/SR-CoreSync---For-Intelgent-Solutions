"""
S&R CoreSync Solutions - Ultra High-Resolution Print-Ready NFC Smart Cards Generator
Outputs 300 DPI CMYK-Safe CR80 standard physical card layouts (2048 x 1280 px)
for Eng. Mohammad Salim Aziza & Mr. Mohammad Raed Kaaka.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
DOWNLOADS_DIR = os.path.join(PROJECT_DIR, "downloads")

# Palette
OBSIDIAN_BG = (3, 7, 5, 255)
GOLD_BRIGHT = (243, 223, 186, 255)
GOLD_MAIN = (197, 168, 128, 255)
GOLD_MUTED = (140, 115, 75, 255)
TEXT_WHITE = (255, 255, 255, 255)
TEXT_MUTED = (176, 191, 184, 255)

def get_fonts():
    try:
        font_headline = ImageFont.truetype("arialbd.ttf", 62)
        font_sub = ImageFont.truetype("arialbd.ttf", 36)
        font_body = ImageFont.truetype("arial.ttf", 28)
        font_bold = ImageFont.truetype("arialbd.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 22)
        font_micro = ImageFont.truetype("arialbd.ttf", 18)
    except Exception:
        font_headline = font_sub = font_body = font_bold = font_small = font_micro = ImageFont.load_default()
    return font_headline, font_sub, font_body, font_bold, font_small, font_micro

def create_front_card(founder_id, name, title, phone, email, avatar_file, qr_file, out_file):
    w, h = 2048, 1280
    card = Image.new("RGBA", (w, h), OBSIDIAN_BG)
    draw = ImageDraw.Draw(card)
    f_head, f_sub, f_body, f_bold, f_small, f_micro = get_fonts()

    # 1. Subtle luxury grid lines
    for i in range(12):
        y = 100 + i * 90
        draw.line([60, y, w - 60, y], fill=(197, 168, 128, 12), width=1)
    
    # 2. Outer Dual Brushed Gold Card Borders
    draw.rounded_rectangle([30, 30, w - 31, h - 31], radius=48, outline=GOLD_MAIN, width=4)
    draw.rounded_rectangle([45, 45, w - 46, h - 46], radius=40, outline=GOLD_MUTED, width=2)

    # 3. Top Header: Gold Luxury Emblem (Left)
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem-hd.png")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as emb:
            emb = emb.convert("RGBA").resize((130, 130), Image.Resampling.LANCZOS)
            card.paste(emb, (75, 75), emb)
            
    draw.text((225, 95), "S&R CORESYNC SOLUTIONS", fill=TEXT_WHITE, font=f_sub)
    draw.text((225, 145), "ENTERPRISE CLOUD • AI ARCHITECTURE • FINANCIAL ERP", fill=GOLD_MAIN, font=f_micro)

    # 4. NFC Wave Symbol (Top Right)
    nfc_cx, nfc_cy = w - 180, 140
    for idx, r in enumerate([70, 50, 30]):
        draw.arc([nfc_cx - r, nfc_cy - r, nfc_cx + r, nfc_cy + r], start=225, end=315, fill=GOLD_BRIGHT, width=4 - idx)
    draw.ellipse([nfc_cx - 10, nfc_cy - 10, nfc_cx + 10, nfc_cy + 10], fill=GOLD_BRIGHT)
    draw.text((w - 460, 125), "NFC SMART CARD", fill=GOLD_MAIN, font=f_small)

    # 5. Founder Circular Portrait Frame (Middle Left)
    av_path = os.path.join(ASSETS_DIR, avatar_file)
    av_size = 260
    av_x, av_y = 85, 300
    
    # Outer gold halo ring
    draw.ellipse([av_x - 8, av_y - 8, av_x + av_size + 8, av_y + av_size + 8], outline=GOLD_BRIGHT, width=5)
    draw.ellipse([av_x - 16, av_y - 16, av_x + av_size + 16, av_y + av_size + 16], outline=GOLD_MUTED, width=2)
    
    if os.path.exists(av_path):
        with Image.open(av_path) as av_img:
            av_img = av_img.convert("RGBA").resize((av_size, av_size), Image.Resampling.LANCZOS)
            mask = Image.new("L", (av_size, av_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, av_size, av_size], fill=255)
            card.paste(av_img, (av_x, av_y), mask)

    # 6. Founder Credentials & Info
    text_x = 390
    draw.text((text_x, 300), name.upper(), fill=TEXT_WHITE, font=f_head)
    draw.text((text_x, 385), title.upper(), fill=GOLD_BRIGHT, font=f_sub)
    draw.text((text_x, 440), "S&R CORESYNC SOLUTIONS B.V. • AMSTERDAM HQ", fill=GOLD_MAIN, font=f_bold)

    draw.line([text_x, 495, w - 520, 495], fill=GOLD_MUTED, width=2)

    # Contact Details Table
    details = [
        ("DIRECT PHONE:", phone),
        ("OFFICIAL INQUIRIES:", email),
        ("HEADQUARTERS:", "Keizersgracht 482, 1016 GD Amsterdam, Netherlands"),
        ("VERIFIED DIGITAL HUB:", "https://sr-coresync.com/card.html")
    ]
    dy = 525
    for label, val in details:
        draw.text((text_x, dy), label, fill=GOLD_MAIN, font=f_small)
        draw.text((text_x + 310, dy), val, fill=TEXT_WHITE, font=f_body)
        dy += 54

    # 7. Luxury 4K QR Code Box (Middle Right)
    qr_box_x = w - 460
    qr_box_y = 300
    qr_box_w = 380
    qr_box_h = 440

    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h],
                           radius=24, fill=(8, 16, 12, 255), outline=GOLD_MAIN, width=3)
    
    qr_path = os.path.join(ASSETS_DIR, qr_file)
    if os.path.exists(qr_path):
        with Image.open(qr_path) as qr_img:
            qr_sz = 310
            qr_img = qr_img.convert("RGBA").resize((qr_sz, qr_sz), Image.Resampling.LANCZOS)
            card.paste(qr_img, (qr_box_x + 35, qr_box_y + 35), qr_img)

    draw.text((qr_box_x + 55, qr_box_y + 370), "SCAN TO ADD CONTACT", fill=GOLD_BRIGHT, font=f_small)

    # 8. Bottom Security & Certification Specs
    draw.line([60, h - 140, w - 60, h - 140], fill=GOLD_MUTED, width=1)
    draw.text((80, h - 105), "NXP NTAG216 CHIP • 13.56 MHz NFC • ISO/IEC 14443-A STANDARD • 256-BIT ENCRYPTION", fill=TEXT_MUTED, font=f_small)
    draw.text((w - 480, h - 105), f"SERIAL: NL-2026-SR-{founder_id.upper()}", fill=GOLD_MAIN, font=f_small)

    # Save PNG in 300 DPI
    out_path = os.path.join(ASSETS_DIR, out_file)
    card.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated Front Card: {out_file} (2048x1280 @ 300 DPI)")

def create_back_card(founder_id, name, out_file):
    w, h = 2048, 1280
    card = Image.new("RGBA", (w, h), OBSIDIAN_BG)
    draw = ImageDraw.Draw(card)
    f_head, f_sub, f_body, f_bold, f_small, f_micro = get_fonts()

    # Borders
    draw.rounded_rectangle([30, 30, w - 31, h - 31], radius=48, outline=GOLD_MAIN, width=4)
    draw.rounded_rectangle([45, 45, w - 46, h - 46], radius=40, outline=GOLD_MUTED, width=2)

    # Concentric gold NFC Tap Target Rings in Center
    cx, cy = w // 2, h // 2 - 30
    for r in [380, 310, 240, 170]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(197, 168, 128, 35), width=2)

    # Center Emblem
    emblem_path = os.path.join(ASSETS_DIR, "sr-emblem-gold-luxury.jpg")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as emb:
            emb = emb.convert("RGBA").resize((380, 214), Image.Resampling.LANCZOS)
            card.paste(emb, (cx - 190, cy - 107), emb)

    # Tap Instruction
    draw.text((cx - 360, cy + 180), "TAP TOP OF SMARTPHONE HERE TO CONNECT", fill=GOLD_BRIGHT, font=f_sub)
    draw.text((cx - 430, cy + 240), "NO APP REQUIRED • INSTANT SMARTPHONE PROFILE TRANSFER", fill=TEXT_MUTED, font=f_body)

    # Bottom Corporate Branding
    draw.line([120, h - 140, w - 120, h - 140], fill=GOLD_MUTED, width=1)
    draw.text((120, h - 105), "S&R CORESYNC SOLUTIONS B.V. • AMSTERDAM • DUBAI • FRANKFURT", fill=GOLD_MAIN, font=f_small)
    draw.text((w - 520, h - 105), "OFFICIAL SOVEREIGN ISSUANCE 2026", fill=TEXT_MUTED, font=f_small)

    out_path = os.path.join(ASSETS_DIR, out_file)
    card.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated Back Card: {out_file} (2048x1280 @ 300 DPI)")

if __name__ == "__main__":
    # Salim Aziza
    create_front_card(
        "salim",
        "Eng. Mohammad Salim Aziza",
        "Chief Technology Officer & Principal Cloud Architect",
        "+31 6 18111116",
        "info@sr-coresync.com",
        "founder-salim.png",
        "qr-founder-salim.png",
        "nfc-print-card-salim-front.png"
    )
    create_back_card("salim", "Eng. Mohammad Salim Aziza", "nfc-print-card-salim-back.png")

    # Raed Kaaka
    create_front_card(
        "raed",
        "Mr. Mohammad Raed Kaaka",
        "Chief Financial Officer & Senior Financial ERP Consultant",
        "+31 6 18111116",
        "info@sr-coresync.com",
        "founder-raed.png",
        "qr-founder-raed.png",
        "nfc-print-card-raed-front.png"
    )
    create_back_card("raed", "Mr. Mohammad Raed Kaaka", "nfc-print-card-raed-back.png")

    print("\n✅ All 300 DPI Print-Ready NFC Smart Cards Generated Successfully!")
