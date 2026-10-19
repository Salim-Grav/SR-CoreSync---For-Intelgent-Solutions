"""
Generate printable physical NFC business card mockup specifications
for Eng. Mohammad Salim Aziza and Mr. Mohammad Raed Kaaka.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

def create_card_mockup(name, title, qr_file, out_file, founder_id="salim"):
    w, h = 1200, 700
    card = Image.new("RGBA", (w, h), (5, 10, 8, 255))
    draw = ImageDraw.Draw(card)
    
    # Outer brushed gold border
    draw.rounded_rectangle([15, 15, w - 16, h - 16], radius=32, outline=(197, 168, 128, 200), width=3)
    draw.rounded_rectangle([24, 24, w - 25, h - 25], radius=26, outline=(197, 168, 128, 60), width=1)
    
    # Subtle gold wave lines
    for i in range(5):
        y = 200 + i * 80
        draw.line([30, y, w - 30, y + 20], fill=(197, 168, 128, 15), width=1)
    
    # Golden Emblem
    emblem_path = os.path.join(ASSETS_DIR, "sr-emblem-gold-luxury.jpg")
    if os.path.exists(emblem_path):
        with Image.open(emblem_path) as emb:
            emb = emb.convert("RGBA").resize((240, 135), Image.Resampling.LANCZOS)
            card.paste(emb, (50, 45), emb)
            
    # NFC Wave Symbol
    cx, cy = w - 100, 90
    draw.arc([cx - 45, cy - 45, cx + 45, cy + 45], start=225, end=315, fill=(243, 223, 186, 255), width=4)
    draw.arc([cx - 32, cy - 32, cx + 32, cy + 32], start=225, end=315, fill=(243, 223, 186, 200), width=3)
    draw.arc([cx - 19, cy - 19, cx + 19, cy + 19], start=225, end=315, fill=(243, 223, 186, 160), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(243, 223, 186, 255))
    
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 36)
        font_med = ImageFont.truetype("arialbd.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 18)
        font_micro = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = font_med = font_small = font_micro = ImageFont.load_default()
        
    draw.text((w - 240, 80), "NFC SMART CARD", fill=(197, 168, 128, 220), font=font_small)
    
    # Founder Info
    draw.text((60, 230), name.upper(), fill=(255, 255, 255, 255), font=font_large)
    draw.text((60, 280), title.upper(), fill=(243, 223, 186, 255), font=font_med)
    draw.text((60, 315), "S&R CORESYNC SOLUTIONS B.V. • AMSTERDAM, NETHERLANDS", fill=(176, 191, 184, 255), font=font_small)
    
    draw.line([60, 360, w - 380, 360], fill=(197, 168, 128, 120), width=1)
    
    draw.text((60, 385), "DIRECT PHONE:  +31 6 18111116", fill=(230, 240, 235, 255), font=font_small)
    draw.text((60, 420), "CORPORATE INQUIRIES:  info@sr-coresync.com", fill=(230, 240, 235, 255), font=font_small)
    draw.text((60, 455), "DIGITAL HUB:  https://sr-coresync.com/card.html", fill=(197, 168, 128, 255), font=font_small)
    draw.text((60, 490), "OFFICE:  Keizersgracht 482, 1016 GD Amsterdam", fill=(176, 191, 184, 255), font=font_small)
    
    # QR Code
    qr_path = os.path.join(ASSETS_DIR, qr_file)
    if os.path.exists(qr_path):
        with Image.open(qr_path) as qr_img:
            qr_img = qr_img.convert("RGBA").resize((250, 250), Image.Resampling.LANCZOS)
            card.paste(qr_img, (w - 320, 330), qr_img)
            
    draw.text((w - 305, 600), "SCAN TO ADD CONTACT", fill=(197, 168, 128, 220), font=font_micro)
    draw.text((60, 620), "NTAG216 ENCRYPTED NFC CHIP (13.56 MHz) • ISO/IEC 14443-A COMPLIANT", fill=(120, 140, 130, 255), font=font_micro)
    
    out_path = os.path.join(ASSETS_DIR, out_file)
    card.convert("RGB").save(out_path, "PNG")
    print(f"Generated Physical NFC Card Mockup: {out_file} ({w}x{h})")

if __name__ == "__main__":
    create_card_mockup(
        "Eng. Mohammad Salim Aziza",
        "Chief Technology Officer & Principal Cloud Architect",
        "qr-founder-salim.png",
        "nfc-card-salim-spec.png",
        "salim"
    )
    create_card_mockup(
        "Mr. Mohammad Raed Kaaka",
        "Chief Financial Officer & Senior ERP Consultant",
        "qr-founder-raed.png",
        "nfc-card-raed-spec.png",
        "raed"
    )
    print("All physical NFC card specifications generated successfully!")
