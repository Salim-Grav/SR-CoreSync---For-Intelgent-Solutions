"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import os
import sys
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

assets_dir = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\assets"

def upgrade_founder_banners():
    print("--- 1. Upgrading Founder Banners ---")
    salim_4k_path = os.path.join(assets_dir, "founder-banner-salim-4k.jpg")
    raed_4k_path = os.path.join(assets_dir, "founder-banner-raed-4k.jpg")

    if os.path.exists(salim_4k_path):
        with Image.open(salim_4k_path) as im:
            print(f"Salim master size: {im.size}, mode: {im.mode}")
            # Target 2560x1440 for web display (Q95) to ensure ultra-sharpness without slow load
            # Also create 3840x2160 UHD webp
            im_rgb = im.convert("RGB")
            
            # Subtle unsharp mask to ensure razor-sharp edges on text and facial details
            sharpened_4k = im_rgb.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=2))
            
            # Save 4k webp
            salim_4k_webp = os.path.join(assets_dir, "founder-banner-salim-4k.webp")
            sharpened_4k.save(salim_4k_webp, "WEBP", quality=95, method=6)
            print(f"Saved: {salim_4k_webp} ({os.path.getsize(salim_4k_webp):,} bytes)")

            # Downsample with Lanczos to 2560x1440 for default high-DPI display
            im_2k = sharpened_4k.resize((2560, 1440), Image.Resampling.LANCZOS)
            
            # Overwrite the old blurry 1024x576 webp and jpg
            salim_webp = os.path.join(assets_dir, "founder-banner-salim.webp")
            im_2k.save(salim_webp, "WEBP", quality=92, method=6)
            print(f"Upgraded {salim_webp}: 2560x1440 ({os.path.getsize(salim_webp):,} bytes)")

            salim_jpg = os.path.join(assets_dir, "founder-banner-salim.jpg")
            im_2k.save(salim_jpg, "JPEG", quality=92, optimize=True)
            print(f"Upgraded {salim_jpg}: 2560x1440 ({os.path.getsize(salim_jpg):,} bytes)")

    if os.path.exists(raed_4k_path):
        with Image.open(raed_4k_path) as im:
            print(f"Raed master size: {im.size}, mode: {im.mode}")
            im_rgb = im.convert("RGB")
            sharpened_4k = im_rgb.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=2))
            
            raed_4k_webp = os.path.join(assets_dir, "founder-banner-raed-4k.webp")
            sharpened_4k.save(raed_4k_webp, "WEBP", quality=95, method=6)
            print(f"Saved: {raed_4k_webp} ({os.path.getsize(raed_4k_webp):,} bytes)")

            im_2k = sharpened_4k.resize((2560, 1440), Image.Resampling.LANCZOS)
            
            raed_webp = os.path.join(assets_dir, "founder-banner-raed.webp")
            im_2k.save(raed_webp, "WEBP", quality=92, method=6)
            print(f"Upgraded {raed_webp}: 2560x1440 ({os.path.getsize(raed_webp):,} bytes)")

            raed_jpg = os.path.join(assets_dir, "founder-banner-raed.jpg")
            im_2k.save(raed_jpg, "JPEG", quality=92, optimize=True)
            print(f"Upgraded {raed_jpg}: 2560x1440 ({os.path.getsize(raed_jpg):,} bytes)")

def upgrade_chair_photos():
    print("\n--- 2. Upgrading Chair Portraits ---")
    for name in ["salim", "raed"]:
        jpg_path = os.path.join(assets_dir, f"hero-founder-{name}-chair.jpg")
        webp_path = os.path.join(assets_dir, f"hero-founder-{name}-chair.webp")
        if os.path.exists(jpg_path):
            with Image.open(jpg_path) as im:
                im_rgb = im.convert("RGB")
                # Enhance sharpness & contrast slightly
                enhancer = ImageEnhance.Sharpness(im_rgb)
                im_sharp = enhancer.enhance(1.3)
                contrast = ImageEnhance.Contrast(im_sharp)
                im_final = contrast.enhance(1.05)
                im_final.save(webp_path, "WEBP", quality=95, method=6)
                print(f"Enhanced chair webp for {name}: {im_final.size} ({os.path.getsize(webp_path):,} bytes)")

if __name__ == "__main__":
    upgrade_founder_banners()
    upgrade_chair_photos()
