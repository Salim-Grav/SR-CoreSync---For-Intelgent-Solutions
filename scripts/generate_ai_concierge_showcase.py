# -*- coding: utf-8 -*-
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
S&R CoreSync - Sovereign AI Concierge Showcase Generator (Milestone 67)
========================================================================
Generates a pristine 1920x1080 visual snapshot of the Sovereign AI Concierge
Webhook and Auto-Responder Simulator for WhatsApp Business & Telegram.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAIN_ACTIVE = r"C:\Users\msali\.gemini\antigravity-ide\brain\4298fc12-c0fc-40b5-a892-10065f93c586"
BRAIN_PREV = r"C:\Users\msali\.gemini\antigravity-ide\brain\c2846371-b1e6-4b8f-9fee-01dda36014e9"

def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_showcase():
    W, H = 1920, 1080
    img = Image.new('RGB', (W, H), '#020705')
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(H):
        ratio = y / float(H)
        r = int(2 + ratio * 3)
        g = int(7 + ratio * 8)
        b = int(5 + ratio * 6)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_title = get_font(34, bold=True)
    font_sub = get_font(18, bold=False)
    font_h2 = get_font(24, bold=True)
    font_body = get_font(17, bold=False)
    font_bold = get_font(17, bold=True)
    font_code = get_font(15, bold=False)
    font_small = get_font(13, bold=False)
    font_badge = get_font(14, bold=True)

    # 1. Top Executive Header Bar
    draw.rectangle([(0, 0), (W, 90)], fill='#04130d', outline='#c5a880', width=1)
    
    # Emblem / Logo
    emblem_path = os.path.join(ROOT, 'assets', 'branding', 'coresync-emblem-8k.png')
    if os.path.exists(emblem_path):
        try:
            emb = Image.open(emblem_path).resize((62, 62), Image.Resampling.LANCZOS)
            img.paste(emb, (35, 14), emb if emb.mode == 'RGBA' else None)
        except Exception:
            pass

    draw.text((115, 18), "S&R CoreSync For Intelligent Solutions", fill='#f3dfba', font=font_title)
    draw.text((115, 58), "Sovereign AI Concierge & Webhook Engine | Milestone 67 Complete (WhatsApp & Telegram)", fill='#94a3b8', font=font_sub)

    # Top Status Badge
    badge_x = 1430
    draw.rounded_rectangle([(badge_x, 24), (badge_x + 450, 68)], radius=22, fill='#063523', outline='#10b981', width=2)
    draw.ellipse([(badge_x + 18, 41), (badge_x + 30, 53)], fill='#10b981')
    draw.text((badge_x + 40, 34), "AI Concierge Node: Active (AMS-01 EU)", fill='#34d399', font=font_badge)

    # 2. Left Column: Phone / Chat Simulator (x: 40 to 880, y: 120 to 1040)
    phone_x1, phone_y1 = 40, 120
    phone_x2, phone_y2 = 880, 1040
    draw.rounded_rectangle([(phone_x1, phone_y1), (phone_x2, phone_y2)], radius=24, fill='#081611', outline='#c5a880', width=2)

    # Channel Switcher Bar
    draw.rectangle([(phone_x1, phone_y1), (phone_x2, phone_y1 + 50)], fill='#030a07')
    # WA Tab Active
    draw.rounded_rectangle([(phone_x1 + 10, phone_y1 + 6), (phone_x1 + 410, phone_y1 + 44)], radius=10, fill='#075e54', outline='#128c7e', width=2)
    draw.text((phone_x1 + 50, phone_y1 + 14), "WhatsApp Business (+31 618111116)", fill='#ffffff', font=font_bold)
    # TG Tab
    draw.rounded_rectangle([(phone_x1 + 430, phone_y1 + 6), (phone_x2 - 10, phone_y1 + 44)], radius=10, fill='#0a232f', outline='#176b94', width=1)
    draw.text((phone_x1 + 480, phone_y1 + 14), "Telegram Bot (@SRCoreSyncBot)", fill='#94a3b8', font=font_bold)

    # Chat Header
    draw.rectangle([(phone_x1, phone_y1 + 50), (phone_x2, phone_y1 + 115)], fill='#075e54')
    draw.ellipse([(phone_x1 + 18, phone_y1 + 60), (phone_x1 + 64, phone_y1 + 106)], fill='#020705', outline='#f3dfba', width=2)
    if os.path.exists(emblem_path):
        try:
            ch_emb = Image.open(emblem_path).resize((42, 42), Image.Resampling.LANCZOS)
            img.paste(ch_emb, (phone_x1 + 20, phone_y1 + 62), ch_emb if ch_emb.mode == 'RGBA' else None)
        except Exception:
            pass
    draw.text((phone_x1 + 78, phone_y1 + 60), "S&R CoreSync VIP Concierge  [Official Verified Account]", fill='#ffffff', font=font_bold)
    draw.text((phone_x1 + 78, phone_y1 + 86), "Online 24/7 (SLA 99.9%) • Sovereign Automated Response Engine", fill='#d1fae5', font=font_small)

    # Chat Feed Area
    draw.rectangle([(phone_x1 + 2, phone_y1 + 116), (phone_x2 - 2, phone_y2 - 70)], fill='#05100b')

    # Bubble 1 (Incoming Greeting)
    b1_y = phone_y1 + 130
    draw.rounded_rectangle([(phone_x1 + 20, b1_y), (phone_x1 + 790, b1_y + 175)], radius=14, fill='#18251e', outline='#c5a880', width=1)
    draw.text((phone_x1 + 35, b1_y + 12), "Welcome to S&R CoreSync For Intelligent Solutions! [*]", fill='#f3dfba', font=font_bold)
    draw.text((phone_x1 + 35, b1_y + 38), "I am your Enterprise AI Concierge, available 24/7 in AR, EN, NL, and DE.", fill='#f1f5f9', font=font_body)
    draw.text((phone_x1 + 35, b1_y + 64), "[1] Cloud ERP Suite (EUR 1,490/mo)  |  [2] Business Pro ERP+AI (EUR 2,890/mo)", fill='#94a3b8', font=font_body)
    draw.text((phone_x1 + 35, b1_y + 90), "[3] Sovereign Enterprise (EUR 5,400/mo)  |  [4] Book VIP Executive Consultation", fill='#94a3b8', font=font_body)
    draw.rounded_rectangle([(phone_x1 + 35, b1_y + 122), (phone_x1 + 270, b1_y + 158)], radius=8, fill='#23392f', outline='#c5a880', width=1)
    draw.text((phone_x1 + 55, b1_y + 130), "[*] View Pricing Packages", fill='#f3dfba', font=font_bold)
    draw.rounded_rectangle([(phone_x1 + 290, b1_y + 122), (phone_x1 + 530, b1_y + 158)], radius=8, fill='#23392f', outline='#c5a880', width=1)
    draw.text((phone_x1 + 310, b1_y + 130), "[*] Book VIP Consultation", fill='#f3dfba', font=font_bold)
    draw.text((phone_x1 + 710, b1_y + 150), "10:00 AM", fill='#64748b', font=font_small)

    # Bubble 2 (User Outgoing Query)
    b2_y = b1_y + 195
    draw.rounded_rectangle([(phone_x1 + 160, b2_y), (phone_x2 - 30, b2_y + 70)], radius=14, fill='#064e3b', outline='#10b981', width=1)
    draw.text((phone_x1 + 180, b2_y + 12), "I would like pricing and details for the Business Pro ERP + AI Suite,", fill='#ecfdf5', font=font_bold)
    draw.text((phone_x1 + 180, b2_y + 38), "including Dutch PSD2 banking integration and EU GDPR compliance.", fill='#a7f3d0', font=font_body)
    draw.text((phone_x2 - 110, b2_y + 45), "10:01 AM [✓✓]", fill='#34d399', font=font_small)

    # Bubble 3 (AI Concierge Detailed Autonomous Response)
    b3_y = b2_y + 90
    draw.rounded_rectangle([(phone_x1 + 20, b3_y), (phone_x1 + 800, b3_y + 245)], radius=14, fill='#18251e', outline='#c5a880', width=2)
    draw.text((phone_x1 + 35, b3_y + 14), "[AI] Business Pro Suite (ERP + AI) — Most Popular Tier [*]", fill='#f3dfba', font=font_bold)
    draw.text((phone_x1 + 35, b3_y + 42), "• Official Price: EUR 2,890 / Month (SKU: SRC-AI-PRO-2026)", fill='#34d399', font=font_bold)
    draw.text((phone_x1 + 35, b3_y + 70), "• Direct Banking Integration: 100% compliant with Dutch & EU PSD2 standards.", fill='#f1f5f9', font=font_body)
    draw.text((phone_x1 + 35, b3_y + 96), "• Autonomous AI Agents: Streamline sales workflows and automated BTW tax invoices.", fill='#f1f5f9', font=font_body)
    draw.text((phone_x1 + 35, b3_y + 122), "• Sovereign Security: Isolated Amsterdam cloud hosting with 99.9% European SLA.", fill='#f1f5f9', font=font_body)
    
    # Action buttons inside bubble 3
    draw.rounded_rectangle([(phone_x1 + 35, b3_y + 155), (phone_x1 + 260, b3_y + 195)], radius=8, fill='#23392f', outline='#c5a880', width=1)
    draw.text((phone_x1 + 55, b3_y + 165), "[>] Upgrade Package Now", fill='#f3dfba', font=font_bold)
    draw.rounded_rectangle([(phone_x1 + 280, b3_y + 155), (phone_x1 + 510, b3_y + 195)], radius=8, fill='#23392f', outline='#c5a880', width=1)
    draw.text((phone_x1 + 300, b3_y + 165), "[>] Request Custom Quote", fill='#f3dfba', font=font_bold)
    draw.rounded_rectangle([(phone_x1 + 530, b3_y + 155), (phone_x1 + 770, b3_y + 195)], radius=8, fill='#23392f', outline='#c5a880', width=1)
    draw.text((phone_x1 + 550, b3_y + 165), "[>] Book VIP Consultation", fill='#f3dfba', font=font_bold)
    draw.text((phone_x1 + 680, b3_y + 215), "10:01 AM • AI Concierge", fill='#64748b', font=font_small)

    # Chat Input Bar
    draw.rectangle([(phone_x1, phone_y2 - 68), (phone_x2, phone_y2)], fill='#040f0b', outline='#c5a880', width=1)
    draw.rounded_rectangle([(phone_x1 + 20, phone_y2 - 54), (phone_x2 - 80, phone_y2 - 14)], radius=18, fill='#0d231b', outline='#2d5343', width=1)
    draw.text((phone_x1 + 40, phone_y2 - 42), "Type your inquiry (Arabic, English, Dutch, German)...", fill='#64748b', font=font_body)
    draw.ellipse([(phone_x2 - 65, phone_y2 - 54), (phone_x2 - 25, phone_y2 - 14)], fill='#c5a880')
    draw.text((phone_x2 - 50, phone_y2 - 44), ">", fill='#020705', font=font_bold)

    # 3. Right Column: Telemetry & Engine Dashboard (x: 920 to 1880, y: 120 to 1040)
    right_x1, right_y1 = 920, 120
    right_x2, right_y2 = 1880, 1040

    # Panel A: Real-Time AI Diagnostics & Telemetry
    pA_y1, pA_y2 = right_y1, right_y1 + 240
    draw.rounded_rectangle([(right_x1, pA_y1), (right_x2, pA_y2)], radius=20, fill='#081611', outline='#c5a880', width=1)
    draw.text((right_x1 + 24, pA_y1 + 18), "Real-Time AI Intent & Telemetry Metrics", fill='#f3dfba', font=font_h2)
    draw.line([(right_x1 + 24, pA_y1 + 52), (right_x2 - 24, pA_y1 + 52)], fill='#2a4034', width=1)

    # 4 Telemetry Boxes
    metrics = [
        ("DETECTED INTENT", "AI_INQUIRY", '#f3dfba', '#0e3425'),
        ("LANGUAGE CLASSIFIED", "Multilingual (ar/en)", '#34d399', '#08261a'),
        ("RESPONSE LATENCY", "18 ms (Zero-Lag)", '#60a5fa', '#0c2238'),
        ("WEBHOOK PROTOCOL", "WhatsApp Cloud API", '#38bdf8', '#0b273b')
    ]
    box_w = 215
    for i, (lbl, val, col, bg) in enumerate(metrics):
        bx = right_x1 + 24 + i * (box_w + 14)
        by = pA_y1 + 70
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + 135)], radius=14, fill=bg, outline=col, width=1)
        draw.text((bx + 14, by + 18), lbl, fill='#94a3b8', font=font_small)
        draw.text((bx + 14, by + 58), val, fill=col, font=font_bold)
        draw.text((bx + 14, by + 98), "CONFIDENCE: 99.8%", fill='#64748b', font=font_small)

    # Panel B: Matched 8K Catalog Package Preview
    pB_y1, pB_y2 = pA_y2 + 20, pA_y2 + 240
    draw.rounded_rectangle([(right_x1, pB_y1), (right_x2, pB_y2)], radius=20, fill='#081611', outline='#c5a880', width=1)
    draw.text((right_x1 + 24, pB_y1 + 18), "Matched 8K WhatsApp Catalog Card Preview", fill='#f3dfba', font=font_h2)
    draw.line([(right_x1 + 24, pB_y1 + 52), (right_x2 - 24, pB_y1 + 52)], fill='#2a4034', width=1)

    # Catalog Thumbnail
    pro_card_path = os.path.join(ROOT, 'assets', 'social-8k-branding', 'whatsapp', 'catalog', 'whatsapp-catalog-business-pro-8k.png')
    if os.path.exists(pro_card_path):
        try:
            pimg = Image.open(pro_card_path).resize((130, 130), Image.Resampling.LANCZOS)
            img.paste(pimg, (right_x1 + 24, pB_y1 + 68))
        except Exception:
            pass

    draw.rounded_rectangle([(right_x1 + 175, pB_y1 + 65), (right_x1 + 380, pB_y1 + 92)], radius=6, fill='#23392f', outline='#10b981', width=1)
    draw.text((right_x1 + 185, pB_y1 + 70), "MOST POPULAR - B2B PRO", fill='#34d399', font=font_badge)
    draw.text((right_x1 + 175, pB_y1 + 100), "Business Pro Suite (ERP + AI)", fill='#f3dfba', font=font_h2)
    draw.text((right_x1 + 175, pB_y1 + 135), "EUR 2,890 / Month  (SKU: SRC-AI-PRO-2026)", fill='#34d399', font=font_bold)
    draw.text((right_x1 + 175, pB_y1 + 165), "Combines cloud ERP with Autonomous AI Agents, real-time PSD2 banking, and BTW tax compliance.", fill='#94a3b8', font=font_body)

    # Panel C: Executive Founders Escalation Routes
    pC_y1, pC_y2 = pB_y2 + 20, pB_y2 + 200
    draw.rounded_rectangle([(right_x1, pC_y1), (right_x2, pC_y2)], radius=20, fill='#081611', outline='#c5a880', width=1)
    draw.text((right_x1 + 24, pC_y1 + 18), "Executive Founders Direct Escalation Routes", fill='#f3dfba', font=font_h2)
    draw.line([(right_x1 + 24, pC_y1 + 52), (right_x2 - 24, pC_y1 + 52)], fill='#2a4034', width=1)

    # Founder 1 (Salim)
    f1_x = right_x1 + 24
    draw.rounded_rectangle([(f1_x, pC_y1 + 68), (f1_x + 440, pC_y1 + 170)], radius=12, fill='#030a07', outline='#c5a880', width=1)
    salim_avatar = os.path.join(ROOT, 'assets', 'social-8k-branding', 'avatars', 'founder-salim-portrait-8k.png')
    if os.path.exists(salim_avatar):
        try:
            sav = Image.open(salim_avatar).resize((80, 80), Image.Resampling.LANCZOS)
            img.paste(sav, (f1_x + 12, pC_y1 + 78))
        except Exception:
            pass
    draw.text((f1_x + 105, pC_y1 + 78), "Eng. Mohammad Salim Aziza", fill='#ffffff', font=font_bold)
    draw.text((f1_x + 105, pC_y1 + 104), "CTO & Chief Cloud / AI Architect", fill='#c5a880', font=font_small)
    draw.text((f1_x + 105, pC_y1 + 130), "[WA] +31 6 31069433", fill='#34d399', font=font_bold)

    # Founder 2 (Raed)
    f2_x = f1_x + 465
    draw.rounded_rectangle([(f2_x, pC_y1 + 68), (f2_x + 440, pC_y1 + 170)], radius=12, fill='#030a07', outline='#c5a880', width=1)
    raed_avatar = os.path.join(ROOT, 'assets', 'social-8k-branding', 'avatars', 'founder-raed-portrait-8k.png')
    if os.path.exists(raed_avatar):
        try:
            rav = Image.open(raed_avatar).resize((80, 80), Image.Resampling.LANCZOS)
            img.paste(rav, (f2_x + 12, pC_y1 + 78))
        except Exception:
            pass
    draw.text((f2_x + 105, pC_y1 + 78), "Mohammad Raed Kaakeh", fill='#ffffff', font=font_bold)
    draw.text((f2_x + 105, pC_y1 + 104), "CFO & Senior ERP / Financial Consultant", fill='#c5a880', font=font_small)
    draw.text((f2_x + 105, pC_y1 + 130), "[WA] +31 6 36279435", fill='#34d399', font=font_bold)

    # Panel D: Raw Webhook JSON Payload Inspector
    pD_y1, pD_y2 = pC_y2 + 20, right_y2
    draw.rounded_rectangle([(right_x1, pD_y1), (right_x2, pD_y2)], radius=20, fill='#081611', outline='#c5a880', width=1)
    draw.text((right_x1 + 24, pD_y1 + 14), "Raw Cloudflare Worker Webhook JSON Payload (Real-Time Response)", fill='#f3dfba', font=font_bold)
    
    json_lines = [
        '{ "channel": "whatsapp_cloud_api", "endpoint": "/api/whatsapp/webhook", "status": 200, "latencyMs": 18,',
        '  "incomingMessage": { "from": "+31618111116", "text": "I would like pricing and details for Business Pro ERP + AI" },',
        '  "intentClassification": { "intent": "AI_INQUIRY", "language": "en", "matchedSKU": "SRC-AI-PRO-2026" },',
        '  "dispatchTargets": { "whatsapp": "DISPATCHED", "telegram": "STANDBY", "autoEscalate": false } }'
    ]
    for idx, l in enumerate(json_lines):
        draw.text((right_x1 + 24, pD_y1 + 45 + idx * 24), l, fill='#a7f3d0', font=font_code)

    # Save to brain directories
    out1 = os.path.join(BRAIN_ACTIVE, 'live_ai_concierge_simulator_snapshot.png')
    img.save(out1, quality=95)
    print("Saved active snapshot to:", out1)

    if os.path.isdir(BRAIN_PREV):
        out2 = os.path.join(BRAIN_PREV, 'live_ai_concierge_simulator_snapshot.png')
        img.save(out2, quality=95)
        print("Mirrored snapshot to:", out2)

if __name__ == '__main__':
    create_showcase()
