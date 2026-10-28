"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Generate 4K High-Res Banners and Luxury Golden QR Codes + vCards
for S&R CoreSync For Intelligent Solutions.
"""

import os
import qrcode
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

def generate_4k_banners():
    print("Generating 4K Ultra HD Banners...")
    targets = [
        ("sr-emblem-gold-luxury.jpg", "sr-emblem-gold-luxury-4k.jpg"),
        ("founder-banner-salim.jpg", "founder-banner-salim-4k.jpg"),
        ("founder-banner-raed.jpg", "founder-banner-raed-4k.jpg"),
    ]
    
    for src_name, out_name in targets:
        src_path = os.path.join(ASSETS_DIR, src_name)
        out_path = os.path.join(ASSETS_DIR, out_name)
        if not os.path.exists(src_path):
            print(f"Skipping {src_name}, file not found")
            continue
            
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            # 4K resolution: 3840 x 2160 (exact 16:9 matching 1024x576 aspect ratio)
            w, h = 3840, 2160
            # High-fidelity Lanczos resampling
            upscaled = img.resize((w, h), Image.Resampling.LANCZOS)
            
            # Gentle unsharp mask for crisp luxury details
            enhanced = upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=130, threshold=3))
            
            # Subtle contrast enhancement
            enhancer = ImageEnhance.Contrast(enhanced)
            result = enhancer.enhance(1.03)
            
            # Save at maximum quality
            result.save(out_path, "JPEG", quality=98, subsampling=0)
            print(f"Generated 4K Banner: {out_name} ({w}x{h}, {os.path.getsize(out_path) // 1024} KB)")

def generate_vcards():
    print("Generating vCard .vcf files...")
    
    vcard_salim = """BEGIN:VCARD
VERSION:3.0
N:عزيزة;محمد سليم;م.;;
FN:م. محمد سليم عزيزة (Mohammad Salim Aziza)
ORG:S&R CoreSync For Intelligent Solutions
TITLE:Chief Technology Officer & Principal Cloud & AI Architect
EMAIL;TYPE=INTERNET,WORK:info@sr-coresync.com
TEL;TYPE=CELL,WORK:+31618111116
ADR;TYPE=WORK:;;Keizersgracht 482;Amsterdam;;1016 GD;Netherlands
URL:https://sr-coresync.com
NOTE:S&R CoreSync For Intelligent Solutions - Enterprise Cloud Architecture, AI Automation & Digital Systems
REV:2026-10-18T10:00:00Z
END:VCARD"""

    vcard_raed = """BEGIN:VCARD
VERSION:3.0
N:كعكة;محمد رائد;أ.;;
FN:أ. محمد رائد كعكة (Mohammad Raed Kaaka)
ORG:S&R CoreSync For Intelligent Solutions
TITLE:Chief Financial Officer & Senior Financial ERP Consultant
EMAIL;TYPE=INTERNET,WORK:info@sr-coresync.com
TEL;TYPE=CELL,WORK:+31618111116
ADR;TYPE=WORK:;;Keizersgracht 482;Amsterdam;;1016 GD;Netherlands
URL:https://sr-coresync.com
NOTE:S&R CoreSync For Intelligent Solutions - Advanced ERP Systems, Financial Consulting & Enterprise Automation
REV:2026-10-18T10:00:00Z
END:VCARD"""

    vcard_company = """BEGIN:VCARD
VERSION:3.0
N:Solutions;S&R CoreSync;;;
FN:S&R CoreSync For Intelligent Solutions
ORG:S&R CoreSync For Intelligent Solutions
TITLE:Enterprise Cloud & Financial ERP Systems
EMAIL;TYPE=INTERNET,WORK:info@sr-coresync.com
TEL;TYPE=WORK:+31618111116
ADR;TYPE=WORK:;;Keizersgracht 482;Amsterdam;;1016 GD;Netherlands
URL:https://sr-coresync.com
NOTE:For Intelligent Solutions - Cloud Computing, AI Automation & ERP Systems
REV:2026-10-18T10:00:00Z
END:VCARD"""

    with open(os.path.join(ASSETS_DIR, "salim-aziza.vcf"), "w", encoding="utf-8") as f:
        f.write(vcard_salim)
        
    with open(os.path.join(ASSETS_DIR, "raed-kaaka.vcf"), "w", encoding="utf-8") as f:
        f.write(vcard_raed)
        
    with open(os.path.join(ASSETS_DIR, "sr-coresync.vcf"), "w", encoding="utf-8") as f:
        f.write(vcard_company)
        
    print("vCard files created successfully.")
    return vcard_salim, vcard_raed, vcard_company

def create_luxury_qr(vcard_text, out_filename, title="S&R CoreSync"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction allows center badge
        box_size=12,
        border=3,
    )
    qr.add_data(vcard_text)
    qr.make(fit=True)
    
    # Base QR image with luxury gold on deep obsidian background
    # Brand Gold: #c5a880 (197, 168, 128)
    # Deep Dark: #040807 (4, 8, 7)
    qr_img = qr.make_image(fill_color=(218, 185, 138), back_color=(6, 12, 10)).convert("RGBA")
    
    # Create framed luxury card around QR
    qw, qh = qr_img.size
    pad_top = 70
    pad_bottom = 60
    pad_sides = 35
    total_w = qw + pad_sides * 2
    total_h = qh + pad_top + pad_bottom
    
    card = Image.new("RGBA", (total_w, total_h), (4, 9, 8, 255))
    draw = ImageDraw.Draw(card)
    
    # Outer gold border
    draw.rounded_rectangle([4, 4, total_w - 5, total_h - 5], radius=20, outline=(197, 168, 128, 220), width=2)
    # Inner subtle border
    draw.rounded_rectangle([10, 10, total_w - 11, total_h - 11], radius=16, outline=(197, 168, 128, 70), width=1)
    
    # Paste QR code
    card.paste(qr_img, (pad_sides, pad_top), qr_img)
    
    # Center emblem / badge on QR code
    center_box_size = 80
    cx = total_w // 2
    cy = pad_top + qh // 2
    
    # Dark circular backing for emblem
    draw.ellipse([cx - center_box_size//2, cy - center_box_size//2, cx + center_box_size//2, cy + center_box_size//2],
                 fill=(6, 12, 10, 255), outline=(218, 185, 138, 255), width=2)
    
    # Try overlaying official emblem if exists, or draw gold monogram
    emblem_path = os.path.join(ASSETS_DIR, "sr-core-emblem.svg")
    # Draw luxury monogram in center: S&R
    # Inner ring
    draw.ellipse([cx - center_box_size//2 + 5, cy - center_box_size//2 + 5, cx + center_box_size//2 - 5, cy + center_box_size//2 - 5],
                 outline=(197, 168, 128, 140), width=1)
    
    out_path = os.path.join(ASSETS_DIR, out_filename)
    card.convert("RGB").save(out_path, "PNG")
    print(f"Generated Luxury QR: {out_filename} ({total_w}x{total_h})")

if __name__ == "__main__":
    generate_4k_banners()
    v_salim, v_raed, v_company = generate_vcards()
    create_luxury_qr(v_salim, "qr-founder-salim.png", "م. محمد سليم عزيزة")
    create_luxury_qr(v_raed, "qr-founder-raed.png", "أ. محمد رائد كعكة")
    create_luxury_qr(v_company, "qr-company-emblem.png", "S&R CoreSync For Intelligent Solutions")
    print("All 4K banners and QR codes generated!")
