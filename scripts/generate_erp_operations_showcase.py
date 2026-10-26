# -*- coding: utf-8 -*-
"""
S&R CoreSync - Sovereign ERP Live Operations & CRM Invoicing Dashboard Showcase (Milestone 69)
=============================================================================================
Generates an ultra-HD 1920x1080 visual snapshot showcasing:
1. Executive Obsidian-Gold ERP Operations & Real-Time Treasury KPIs.
2. Enterprise Client Roster with Live Status, Tier Badges & PSD2 Settlement Channels.
3. Interactive Dutch BTW (21%) & EU Cross-Border Tax-Compliant Sovereign Invoice.
4. Cryptographic Ledger Hash Verification, PSD2 Instant Settlement & VIP Concierge Dispatch.
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

    # Background gradient
    for y in range(H):
        ratio = y / float(H)
        r = int(3 + ratio * 3)
        g = int(8 + ratio * 8)
        b = int(6 + ratio * 7)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_title = get_font(32, bold=True)
    font_sub = get_font(17, bold=False)
    font_h2 = get_font(21, bold=True)
    font_body = get_font(15, bold=False)
    font_bold = get_font(15, bold=True)
    font_code = get_font(13, bold=False)
    font_code_bold = get_font(13, bold=True)
    font_small = get_font(12, bold=False)
    font_badge = get_font(13, bold=True)

    # 1. Top Header Bar
    draw.rectangle([(0, 0), (W, 90)], fill='#04140e', outline='#c5a880', width=1)
    
    emblem_path = os.path.join(ROOT, 'assets', 'branding', 'coresync-emblem-8k.png')
    if os.path.exists(emblem_path):
        try:
            emb = Image.open(emblem_path).resize((62, 62), Image.Resampling.LANCZOS)
            img.paste(emb, (35, 14), emb if emb.mode == 'RGBA' else None)
        except Exception:
            pass

    draw.text((115, 16), "S&R CoreSync For Intelligent Solutions | Sovereign ERP & CRM Invoicing", fill='#f3dfba', font=font_title)
    draw.text((115, 56), "Live Operations Dashboard • B2B Client Ledger • PSD2 & iDEAL Settlements • Dutch BTW (21%) & EU Tax Engine", fill='#94a3b8', font=font_sub)

    # Top Status Badges
    badge_x = 1380
    draw.rounded_rectangle([(badge_x, 22), (badge_x + 500, 68)], radius=22, fill='#072c1e', outline='#10b981', width=2)
    draw.ellipse([(badge_x + 18, 40), (badge_x + 30, 52)], fill='#10b981')
    draw.text((badge_x + 40, 34), "Ledger Node: Active (AMS-01) | PSD2: Online", fill='#34d399', font=font_badge)

    # 2. Main 4 Financial KPI Cards (y: 105 to 215)
    metrics = [
        ("SETTLED TREASURY (MTD)", "€148,650.00", "+28.4% MoM • 100% Reconciled", '#f3dfba', '#0e3425'),
        ("ACTIVE ENTERPRISE CLIENTS", "42 Companies", "Netherlands, Nordics, GCC & DACH", '#34d399', '#08261a'),
        ("SETTLEMENT EFFICIENCY", "98.6% Instant", "iDEAL, SEPA Instant & Stripe Wire", '#60a5fa', '#0c2238'),
        ("TAX & BTW COMPLIANCE", "21% Dutch / 0% RC", "KvK 96515865 • EU Reverse Charge", '#fbbf24', '#2d2208')
    ]
    box_w = 445
    for i, (title, val, sub, col, bg) in enumerate(metrics):
        bx = 40 + i * (box_w + 20)
        by = 105
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + 105)], radius=16, fill=bg, outline=col, width=1)
        draw.text((bx + 20, by + 14), title, fill='#94a3b8', font=font_small)
        draw.text((bx + 20, by + 40), val, fill=col, font=font_h2)
        draw.text((bx + 20, by + 74), sub, fill='#64748b', font=font_small)

    # 3. Left Section: Enterprise Client Pipeline & Directory (x: 40 to 980, y: 225 to 975)
    left_x1, left_y1 = 40, 225
    left_x2, left_y2 = 980, 975
    draw.rounded_rectangle([(left_x1, left_y1), (left_x2, left_y2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    
    # Left Header
    draw.text((left_x1 + 24, left_y1 + 18), "Enterprise Client Directory & Active Subscriptions", fill='#f3dfba', font=font_h2)
    draw.text((left_x1 + 680, left_y1 + 22), "Filter: All (42) • Live Feed", fill='#94a3b8', font=font_small)
    draw.line([(left_x1 + 24, left_y1 + 52), (left_x2 - 24, left_y1 + 52)], fill='#1e382b', width=1)

    clients = [
        ("Van Dijk Logistics B.V.", "Netherlands (Rotterdam)", "Enterprise Sovereign Tier", "€12,500 / mo", "iDEAL / SEPA", "Active • Paid", '#10b981', '#06281b'),
        ("Nordic CleanTech AB", "Sweden (Stockholm)", "AI Automation Core", "€8,750 / mo", "Stripe Corporate", "Active • Paid", '#10b981', '#06281b'),
        ("Al-Andalus Trading Co.", "Saudi Arabia (Riyadh)", "B2B Omnichannel Suite", "€15,200 / mo", "Direct Wire (SWIFT)", "Active • Paid", '#10b981', '#06281b'),
        ("Bavaria Cyber Systems GmbH", "Germany (Munich)", "Cyber Defense Vault", "€18,900 / mo", "SEPA B2B Mandate", "Active • Paid", '#10b981', '#06281b'),
        ("Le Marais Retail Group", "France (Paris)", "Concierge Luxury Hub", "€9,400 / mo", "Credit Card (3DS)", "Pending Renewal", '#f59e0b', '#261b05'),
        ("Emirates Smart Logistics FZCO", "UAE (Dubai)", "Sovereign Cloud Node", "€22,500 / mo", "Corporate Escrow", "Active • Paid", '#10b981', '#06281b')
    ]

    card_y = left_y1 + 65
    for cname, loc, tier, amt, meth, status, status_col, status_bg in clients:
        draw.rounded_rectangle([(left_x1 + 20, card_y), (left_x2 - 20, card_y + 98)], radius=12, fill='#091f17', outline='#1b3b2c', width=1)
        
        # Company & Location
        draw.text((left_x1 + 36, card_y + 14), cname, fill='#ffffff', font=font_bold)
        draw.text((left_x1 + 36, card_y + 40), f"{loc}  •  {tier}", fill='#94a3b8', font=font_small)
        draw.text((left_x1 + 36, card_y + 66), f"Payment Rail: {meth}", fill='#64748b', font=font_small)

        # Amount & Status Badge
        draw.text((left_x1 + 660, card_y + 16), amt, fill='#f3dfba', font=font_bold)
        
        badge_w = 150
        bx = left_x1 + 760
        by = card_y + 50
        draw.rounded_rectangle([(bx, by), (bx + badge_w, by + 30)], radius=8, fill=status_bg, outline=status_col, width=1)
        draw.text((bx + 18, by + 6), status, fill=status_col, font=font_badge)

        card_y += 112

    # 4. Right Section: Live Interactive Sovereign Invoice Sheet (x: 1005 to 1880, y: 225 to 975)
    right_x1, right_y1 = 1005, 225
    right_x2, right_y2 = 1880, 975
    draw.rounded_rectangle([(right_x1, right_y1), (right_x2, right_y2)], radius=18, fill='#071610', outline='#c5a880', width=1)

    # Right Section Header
    draw.text((right_x1 + 24, right_y1 + 18), "Interactive Sovereign Invoice Sheet (Tax & BTW Compliant)", fill='#f3dfba', font=font_h2)
    draw.text((right_x1 + 640, right_y1 + 22), "INV-2026-08492", fill='#38bdf8', font=font_code_bold)
    draw.line([(right_x1 + 24, right_y1 + 52), (right_x2 - 24, right_y1 + 52)], fill='#1e382b', width=1)

    # Printable Invoice Paper Background
    inv_x1, inv_y1 = right_x1 + 24, right_y1 + 65
    inv_x2, inv_y2 = right_x2 - 24, right_y2 - 20
    draw.rounded_rectangle([(inv_x1, inv_y1), (inv_x2, inv_y2)], radius=14, fill='#05110d', outline='#2d4839', width=1)

    # Invoice Top Header Meta
    draw.text((inv_x1 + 24, inv_y1 + 20), "S&R CoreSync For Intelligent Solutions", fill='#f3dfba', font=font_bold)
    draw.text((inv_x1 + 24, inv_y1 + 44), "Keizersgracht 482, 1016 EG Amsterdam, Netherlands", fill='#94a3b8', font=font_small)
    draw.text((inv_x1 + 24, inv_y1 + 64), "KvK: 96515865  •  BTW/VAT ID: NL867549210B01  •  IBAN: NL91ABNA0418111116", fill='#64748b', font=font_code)

    draw.text((inv_x1 + 560, inv_y1 + 20), "OFFICIAL TAX INVOICE", fill='#34d399', font=font_bold)
    draw.text((inv_x1 + 560, inv_y1 + 44), "Issue Date: 26 Oct 2026", fill='#94a3b8', font=font_small)
    draw.text((inv_x1 + 560, inv_y1 + 64), "Due Date: 09 Nov 2026 (Net 14)", fill='#fbbf24', font=font_small)

    draw.line([(inv_x1 + 24, inv_y1 + 95), (inv_x2 - 24, inv_y1 + 95)], fill='#183325', width=1)

    # Billed To Block
    draw.text((inv_x1 + 24, inv_y1 + 108), "BILLED TO (CLIENT):", fill='#f3dfba', font=font_badge)
    draw.text((inv_x1 + 24, inv_y1 + 132), "Van Dijk Logistics B.V.  |  Attn: Executive Financial Board", fill='#ffffff', font=font_body)
    draw.text((inv_x1 + 24, inv_y1 + 154), "Waalhaven Oostzijde 14, 3087 BM Rotterdam, Netherlands  •  KvK: 64918234  •  BTW: NL854219982B01", fill='#94a3b8', font=font_small)

    # Invoice Items Table
    tbl_y = inv_y1 + 188
    draw.rectangle([(inv_x1 + 24, tbl_y), (inv_x2 - 24, tbl_y + 34)], fill='#0d281c')
    draw.text((inv_x1 + 36, tbl_y + 8), "DESCRIPTION / DELIVERABLES", fill='#cbd5e1', font=font_small)
    draw.text((inv_x1 + 440, tbl_y + 8), "QTY", fill='#cbd5e1', font=font_small)
    draw.text((inv_x1 + 520, tbl_y + 8), "UNIT PRICE", fill='#cbd5e1', font=font_small)
    draw.text((inv_x1 + 660, tbl_y + 8), "TOTAL (EUR)", fill='#cbd5e1', font=font_small)

    items = [
        ("Sovereign Enterprise Core Architecture - AMS Cluster Node", "1 mo", "€ 8,500.00", "€ 8,500.00"),
        ("Real-Time Autonomous Agent Concierge Engine (29 Languages)", "1 mo", "€ 2,500.00", "€ 2,500.00"),
        ("PSD2 / iDEAL Instant Settlement Webhook & Multi-Currency Rail", "1 mo", "€ 1,500.00", "€ 1,500.00")
    ]

    iy = tbl_y + 44
    for desc, qty, uprice, total in items:
        draw.text((inv_x1 + 36, iy), desc, fill='#ffffff', font=font_body)
        draw.text((inv_x1 + 445, iy), qty, fill='#94a3b8', font=font_body)
        draw.text((inv_x1 + 525, iy), uprice, fill='#94a3b8', font=font_body)
        draw.text((inv_x1 + 665, iy), total, fill='#f3dfba', font=font_bold)
        draw.line([(inv_x1 + 24, iy + 30), (inv_x2 - 24, iy + 30)], fill='#142e22', width=1)
        iy += 42

    # Financial Calculation Summary
    sum_x = inv_x1 + 450
    draw.text((sum_x, iy + 10), "Subtotal (Excl. BTW):", fill='#94a3b8', font=font_body)
    draw.text((inv_x1 + 665, iy + 10), "€ 12,500.00", fill='#ffffff', font=font_bold)

    draw.text((sum_x, iy + 38), "Dutch BTW (21.0% Rate):", fill='#94a3b8', font=font_body)
    draw.text((inv_x1 + 665, iy + 38), "€  2,625.00", fill='#fbbf24', font=font_bold)

    draw.line([(sum_x, iy + 68), (inv_x2 - 24, iy + 68)], fill='#c5a880', width=2)
    draw.text((sum_x, iy + 80), "TOTAL DUE (INCL. BTW):", fill='#f3dfba', font=font_h2)
    draw.text((inv_x1 + 665, iy + 80), "€ 15,125.00", fill='#10b981', font=font_h2)

    # Verification & Cryptographic Ledger Signature
    sig_y = iy + 140
    draw.rounded_rectangle([(inv_x1 + 24, sig_y), (inv_x2 - 24, sig_y + 115)], radius=10, fill='#081e15', outline='#16422f', width=1)
    draw.text((inv_x1 + 40, sig_y + 14), "Sovereign Ledger Cryptographic Seal & Verification:", fill='#f3dfba', font=font_code_bold)
    draw.text((inv_x1 + 40, sig_y + 40), "SHA-256 Digest: 8f9b4c02da317822fe901c56b9c97b814a0913824f15d86210f92415125", fill='#38bdf8', font=font_code)
    draw.text((inv_x1 + 40, sig_y + 64), "Compliance: W3C Linked Data • EU Directive 2014/55/EU • Dutch Belastingdienst Approved", fill='#94a3b8', font=font_small)
    draw.text((inv_x1 + 40, sig_y + 88), "Instant Settlement: Available via iDEAL QR, SEPA Instant or Corporate Wire (+31 618111116)", fill='#34d399', font=font_small)

    # 5. Bottom Action Bar (y: 990 to 1060)
    draw.rectangle([(0, 990), (W, 1080)], fill='#030d09', outline='#c5a880', width=1)
    draw.text((40, 1025), "Live Ledger Feed: [22:18:40] Settlement €15,125.00 from Van Dijk Logistics via iDEAL AMS Confirmed.", fill='#34d399', font=font_body)

    # Action Buttons on Bottom Right
    btn1_x = 1180
    draw.rounded_rectangle([(btn1_x, 1010), (btn1_x + 210, 1058)], radius=10, fill='#0d3b28', outline='#10b981', width=1)
    draw.text((btn1_x + 28, 1024), "Print / PDF Invoice", fill='#ffffff', font=font_badge)

    btn2_x = 1410
    draw.rounded_rectangle([(btn2_x, 1010), (btn2_x + 220, 1058)], radius=10, fill='#0c2f48', outline='#38bdf8', width=1)
    draw.text((btn2_x + 25, 1024), "Instant Settle (PSD2)", fill='#38bdf8', font=font_badge)

    btn3_x = 1650
    draw.rounded_rectangle([(btn3_x, 1010), (btn3_x + 230, 1058)], radius=10, fill='#2e2008', outline='#fbbf24', width=1)
    draw.text((btn3_x + 22, 1024), "Send VIP WhatsApp", fill='#fbbf24', font=font_badge)

    # Save to project assets and brain directories
    out_paths = [
        os.path.join(ROOT, 'assets', 'branding', 'live_erp_operations_showcase_snapshot.png'),
        os.path.join(BRAIN_ACTIVE, 'live_erp_operations_showcase_snapshot.png'),
        os.path.join(BRAIN_PREV, 'live_erp_operations_showcase_snapshot.png')
    ]
    
    for p in out_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p, format='PNG', optimize=True)
            print(f"Saved snapshot to: {p}")
        except Exception as e:
            print(f"Failed to save {p}: {e}")

if __name__ == '__main__':
    create_showcase()
