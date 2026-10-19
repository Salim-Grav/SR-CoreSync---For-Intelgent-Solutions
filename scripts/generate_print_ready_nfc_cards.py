"""
S&R CoreSync Solutions - Ultra High-Resolution Print-Ready NFC Smart Cards Generator
Outputs 300 DPI CMYK-Safe CR80 standard physical card layouts (2048 x 1280 px)
for Eng. Mohammad Salim Aziza & Mr. Mohammad Raed Kaaka.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

# Luxury Colors
OBSIDIAN_BG = (5, 9, 8, 255)
GOLD_BRIGHT = (245, 226, 192, 255)
GOLD_MAIN = (205, 175, 133, 255)
GOLD_DARK = (130, 105, 65, 255)
TEXT_WHITE = (255, 255, 255, 255)
TEXT_MUTED = (165, 185, 175, 255)

def get_fonts():
    try:
        f_name = ImageFont.truetype("arialbd.ttf", 60)
        f_sub = ImageFont.truetype("arialbd.ttf", 34)
        f_body = ImageFont.truetype("arial.ttf", 26)
        f_bold = ImageFont.truetype("arialbd.ttf", 26)
        f_small = ImageFont.truetype("arial.ttf", 22)
        f_micro = ImageFont.truetype("arialbd.ttf", 17)
    except Exception:
        f_name = f_sub = f_body = f_bold = f_small = f_micro = ImageFont.load_default()
    return f_name, f_sub, f_body, f_bold, f_small, f_micro

def draw_smart_chip(draw, x, y, w=160, h=120):
    """Draws realistic gold EMV/NFC contact chip plate."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(195, 160, 110, 255), outline=GOLD_BRIGHT, width=2)
    # Chip contact grooves
    draw.line([x, y + h//2, x + w, y + h//2], fill=(130, 100, 60, 255), width=2)
    draw.line([x + w//3, y, x + w//3, y + h], fill=(130, 100, 60, 255), width=2)
    draw.line([x + (w*2)//3, y, x + (w*2)//3, y + h], fill=(130, 100, 60, 255), width=2)
    draw.rounded_rectangle([x + w//4, y + h//4, x + (w*3)//4, y + (h*3)//4], radius=6, outline=(130, 100, 60, 255), width=2)

def create_front_card(founder_id, name, ar_name, title, ar_title, phone, email, avatar_file, qr_file, out_file):
    w, h = 2048, 1280
    card = Image.new("RGBA", (w, h), OBSIDIAN_BG)
    draw = ImageDraw.Draw(card)
    f_name, f_sub, f_body, f_bold, f_small, f_micro = get_fonts()

    # 1. Outer Dual Gold Card Borders (CR80 standard 3mm corner radius)
    draw.rounded_rectangle([25, 25, w - 26, h - 26], radius=50, outline=GOLD_MAIN, width=4)
    draw.rounded_rectangle([42, 42, w - 43, h - 43], radius=42, outline=GOLD_DARK, width=2)

    # 2. Header: Circular Gold Emblem (Left)
    emblem_path = os.path.join(ASSETS_DIR, "sr-emblem-gold-luxury.jpg")
    if os.path.exists(emblem_path):
        emb_sz = 140
        with Image.open(emblem_path) as emb:
            emb = emb.convert("RGBA").resize((emb_sz, emb_sz), Image.Resampling.LANCZOS)
            mask = Image.new("L", (emb_sz, emb_sz), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.ellipse([0, 0, emb_sz, emb_sz], fill=255)
            card.paste(emb, (70, 65), mask)
            draw.ellipse([68, 63, 70 + emb_sz + 2, 65 + emb_sz + 2], outline=GOLD_BRIGHT, width=3)
            
    draw.text((235, 80), "S&R CORESYNC SOLUTIONS", fill=TEXT_WHITE, font=f_sub)
    draw.text((235, 130), "ENTERPRISE CLOUD • SOVEREIGN AI • FINANCIAL ERP ARCHITECTURE", fill=GOLD_MAIN, font=f_micro)
    draw.text((235, 160), "AMSTERDAM, NETHERLANDS • KEIZERSGRACHT 482", fill=TEXT_MUTED, font=f_micro)

    # 3. NFC Wave Symbol (Top Right)
    nfc_cx, nfc_cy = w - 160, 130
    for idx, r in enumerate([65, 46, 28]):
        draw.arc([nfc_cx - r, nfc_cy - r, nfc_cx + r, nfc_cy + r], start=225, end=315, fill=GOLD_BRIGHT, width=4 - idx)
    draw.ellipse([nfc_cx - 8, nfc_cy - 8, nfc_cx + 8, nfc_cy + 8], fill=GOLD_BRIGHT)
    draw.text((w - 430, 115), "NFC SMART CARD", fill=GOLD_MAIN, font=f_small)

    # Hairline divider
    draw.line([60, 235, w - 60, 235], fill=GOLD_DARK, width=2)

    # 4. Portrait Frame (Middle Left)
    av_path = os.path.join(ASSETS_DIR, avatar_file)
    av_size = 320
    av_x, av_y = 80, 290
    
    # Outer gold rings
    draw.ellipse([av_x - 10, av_y - 10, av_x + av_size + 10, av_y + av_size + 10], outline=GOLD_BRIGHT, width=5)
    draw.ellipse([av_x - 18, av_y - 18, av_x + av_size + 18, av_y + av_size + 18], outline=GOLD_DARK, width=2)
    
    if os.path.exists(av_path):
        with Image.open(av_path) as av_img:
            av_img = av_img.convert("RGBA").resize((av_size, av_size), Image.Resampling.LANCZOS)
            mask = Image.new("L", (av_size, av_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([0, 0, av_size, av_size], fill=255)
            card.paste(av_img, (av_x, av_y), mask)

    # Smart Chip Plate Mockup
    draw_smart_chip(draw, 160, 665, w=160, h=115)

    # 5. Founder Details
    text_x = 445
    draw.text((text_x, 290), name.upper(), fill=TEXT_WHITE, font=f_name)
    draw.text((text_x, 370), title.upper(), fill=GOLD_BRIGHT, font=f_sub)
    draw.text((text_x, 420), ar_title, fill=GOLD_MAIN, font=f_bold)

    draw.line([text_x, 475, w - 500, 475], fill=GOLD_DARK, width=2)

    details = [
        ("EXECUTIVE ID:", f"SR-EXEC-2026-{founder_id.upper()}"),
        ("DIRECT MOBILE:", phone),
        ("OFFICIAL EMAIL:", email),
        ("DUTY STATION:", "Amsterdam HQ • Keizersgracht 482, 1016 GD"),
        ("VERIFIED CARD HUB:", "https://sr-coresync.com/card.html")
    ]
    dy = 505
    for label, val in details:
        draw.text((text_x, dy), label, fill=GOLD_MAIN, font=f_small)
        draw.text((text_x + 280, dy), val, fill=TEXT_WHITE, font=f_body)
        dy += 54

    # 6. Luxury 4K QR Code Box (Middle Right)
    qr_box_x = w - 460
    qr_box_y = 290
    qr_box_w = 380
    qr_box_h = 440

    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h],
                           radius=22, fill=(10, 18, 15, 255), outline=GOLD_MAIN, width=3)
    
    qr_path = os.path.join(ASSETS_DIR, qr_file)
    if os.path.exists(qr_path):
        with Image.open(qr_path) as qr_img:
            qr_sz = 310
            qr_img = qr_img.convert("RGBA").resize((qr_sz, qr_sz), Image.Resampling.LANCZOS)
            card.paste(qr_img, (qr_box_x + 35, qr_box_y + 35), qr_img)

    draw.text((qr_box_x + 50, qr_box_y + 375), "SCAN TO ADD CONTACT", fill=GOLD_BRIGHT, font=f_small)

    # 7. Bottom Security Specifications
    draw.line([60, h - 130, w - 60, h - 130], fill=GOLD_DARK, width=1)
    draw.text((75, h - 95), "NXP NTAG216 CHIP (13.56 MHz) • ISO/IEC 14443-A STANDARD • 256-BIT ENCRYPTED SOVEREIGN PROFILE", fill=TEXT_MUTED, font=f_small)
    draw.text((w - 420, h - 95), "ISSUED BY S&R CORESYNC B.V.", fill=GOLD_MAIN, font=f_small)

    out_path = os.path.join(ASSETS_DIR, out_file)
    card.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated Front Card: {out_file} (2048x1280 @ 300 DPI)")

def create_back_card(founder_id, name, out_file):
    w, h = 2048, 1280
    card = Image.new("RGBA", (w, h), OBSIDIAN_BG)
    draw = ImageDraw.Draw(card)
    f_name, f_sub, f_body, f_bold, f_small, f_micro = get_fonts()

    # Borders
    draw.rounded_rectangle([25, 25, w - 26, h - 26], radius=50, outline=GOLD_MAIN, width=4)
    draw.rounded_rectangle([42, 42, w - 43, h - 43], radius=42, outline=GOLD_DARK, width=2)

    # Concentric gold NFC Tap Target Rings in Center
    cx, cy = w // 2, h // 2 - 40
    for r in [400, 320, 240, 160]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(197, 168, 128, 40), width=2)

    # Center Circular Emblem
    emblem_path = os.path.join(ASSETS_DIR, "sr-emblem-gold-luxury.jpg")
    if os.path.exists(emblem_path):
        emb_sz = 260
        with Image.open(emblem_path) as emb:
            emb = emb.convert("RGBA").resize((emb_sz, emb_sz), Image.Resampling.LANCZOS)
            mask = Image.new("L", (emb_sz, emb_sz), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.ellipse([0, 0, emb_sz, emb_sz], fill=255)
            card.paste(emb, (cx - emb_sz//2, cy - emb_sz//2), mask)
            draw.ellipse([cx - emb_sz//2 - 4, cy - emb_sz//2 - 4, cx + emb_sz//2 + 4, cy + emb_sz//2 + 4], outline=GOLD_BRIGHT, width=4)

    # Tap Instruction
    draw.text((cx - 360, cy + 195), "TAP TOP OF SMARTPHONE HERE TO CONNECT", fill=GOLD_BRIGHT, font=f_sub)
    draw.text((cx - 390, cy + 250), "NO APP REQUIRED • INSTANT DIGITAL VCARD & PORTFOLIO SYNC", fill=TEXT_MUTED, font=f_body)

    # Bottom Corporate Branding
    draw.line([80, h - 130, w - 80, h - 130], fill=GOLD_DARK, width=1)
    draw.text((90, h - 95), "S&R CORESYNC SOLUTIONS B.V. • AMSTERDAM • DUBAI • FRANKFURT", fill=GOLD_MAIN, font=f_small)
    draw.text((w - 480, h - 95), "OFFICIAL PHYSICAL NFC CARD • 2026", fill=TEXT_MUTED, font=f_small)

    out_path = os.path.join(ASSETS_DIR, out_file)
    card.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated Back Card: {out_file} (2048x1280 @ 300 DPI)")

if __name__ == "__main__":
    # 1. Salim Aziza
    create_front_card(
        "salim",
        "Eng. Mohammad Salim Aziza",
        "",
        "Chief Technology Officer & Cloud Architect",
        "EXECUTIVE LEADERSHIP • SOVEREIGN AI & CLOUD SYSTEMS",
        "+31 6 18111116",
        "info@sr-coresync.com",
        "founder-salim.png",
        "qr-founder-salim.png",
        "nfc-print-card-salim-front.png"
    )
    create_back_card("salim", "Eng. Mohammad Salim Aziza", "nfc-print-card-salim-back.png")

    # 2. Raed Kaaka
    create_front_card(
        "raed",
        "Mr. Mohammad Raed Kaaka",
        "",
        "Chief Financial Officer & Senior ERP Consultant",
        "EXECUTIVE LEADERSHIP • FINANCIAL ERP & EU COMPLIANCE",
        "+31 6 18111116",
        "info@sr-coresync.com",
        "founder-raed.png",
        "qr-founder-raed.png",
        "nfc-print-card-raed-front.png"
    )
    create_back_card("raed", "Mr. Mohammad Raed Kaaka", "nfc-print-card-raed-back.png")

    print("Success: Generated luxury 300 DPI print-ready NFC cards!")
