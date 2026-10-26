# -*- coding: utf-8 -*-
"""
S&R CoreSync - Showcase Generator for Milestones 72, 73 & 74
===========================================================
1. Milestone 72: Sovereign Stress & Penetration Testing Engine (1920x1080)
2. Milestone 73: ISO 27001 & Compliance Assurance Center (1920x1080)
3. Milestone 74: B2B White-Label Partner & Reseller Portal (1920x1080)
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

def generate_stress_showcase():
    W, H = 1920, 1080
    img = Image.new('RGB', (W, H), '#020705')
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / float(H)
        r = int(2 + ratio * 3)
        g = int(8 + ratio * 8)
        b = int(6 + ratio * 6)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_title = get_font(30, bold=True)
    font_sub = get_font(16, bold=False)
    font_h2 = get_font(20, bold=True)
    font_body = get_font(15, bold=False)
    font_code = get_font(13, bold=False)
    font_small = get_font(12, bold=False)
    font_badge = get_font(13, bold=True)

    # Header
    draw.rectangle([(0, 0), (W, 90)], fill='#04140e', outline='#c5a880', width=1)
    emblem_path = os.path.join(ROOT, 'assets', 'branding', 'coresync-emblem-8k.png')
    if os.path.exists(emblem_path):
        try:
            emb = Image.open(emblem_path).resize((62, 62), Image.Resampling.LANCZOS)
            img.paste(emb, (35, 14), emb if emb.mode == 'RGBA' else None)
        except Exception:
            pass

    draw.text((115, 16), "S&R CoreSync | Sovereign Stress & Penetration Testing Engine", fill='#f3dfba', font=font_title)
    draw.text((115, 56), "Milestone 72 • 100K RPS Synthetic Flood • BGP Anycast DDoS Shield (2.4 Tbps) • Amsterdam AMS-01", fill='#94a3b8', font=font_sub)

    badge_x = 1380
    draw.rounded_rectangle([(badge_x, 22), (badge_x + 500, 68)], radius=22, fill='#072c1e', outline='#10b981', width=2)
    draw.ellipse([(badge_x + 18, 40), (badge_x + 30, 52)], fill='#10b981')
    draw.text((badge_x + 40, 34), "DEFENSE SHIELD: 100% SCRUBBING ACTIVE", fill='#34d399', font=font_badge)

    # 4 Telemetry KPIs
    metrics = [
        ("THROUGHPUT CAPACITY", "100,000 RPS", "Peak Anycast Handling • 0% Loss", '#f3dfba', '#0e3425'),
        ("SCRUBBING RATIO", "100.00%", "Malicious SYN/L7 Packets Blocked", '#34d399', '#08261a'),
        ("CORE LATENCY", "1.18 ms", "Amsterdam Fiber Loop Latency", '#38bdf8', '#0c2238'),
        ("ERROR RATE", "0.00%", "Zero Unhandled Exceptions or 5xx", '#f87171', '#2d1414')
    ]
    box_w = 445
    for i, (title, val, sub, col, bg) in enumerate(metrics):
        bx = 40 + i * (box_w + 20)
        by = 105
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + 105)], radius=16, fill=bg, outline=col, width=1)
        draw.text((bx + 20, by + 14), title, fill='#94a3b8', font=font_small)
        draw.text((bx + 20, by + 40), val, fill=col, font=font_h2)
        draw.text((bx + 20, by + 74), sub, fill='#64748b', font=font_small)

    # Left Section: Vector Setup & Controls
    left_x1, left_y1 = 40, 225
    left_x2, left_y2 = 820, 975
    draw.rounded_rectangle([(left_x1, left_y1), (left_x2, left_y2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    draw.text((left_x1 + 24, left_y1 + 18), "Attack Vectors & Stress Controls (Synthetic)", fill='#f3dfba', font=font_h2)
    draw.line([(left_x1 + 24, left_y1 + 52), (left_x2 - 24, left_y1 + 52)], fill='#1e382b', width=1)

    vectors = [
        ("Layer-7 HTTPS Flood", "50,000 concurrent API queries against /api/v1/erp endpoints", "ACTIVE", '#10b981'),
        ("TLS Handshake Exhaustion", "Rapid ephemeral ECDHE negotiation stress testing", "ARMED", '#38bdf8'),
        ("WAF Malicious Injection", "OWASP Top-10 SQLi, XSS, and Header Smuggling vectors", "TESTED", '#fbbf24'),
        ("Distributed Bot Swarm", "12,000 multi-region IP botnet simulation against login", "MITIGATED", '#ef4444')
    ]
    for j, (name, dsc, st, cl) in enumerate(vectors):
        vy = left_y1 + 70 + j * 125
        draw.rounded_rectangle([(left_x1 + 20, vy), (left_x2 - 20, vy + 105)], radius=12, fill='#040e0a', outline='#183327', width=1)
        draw.text((left_x1 + 35, vy + 14), name, fill='#ffffff', font=font_body)
        draw.rounded_rectangle([(left_x2 - 130, vy + 12), (left_x2 - 35, vy + 38)], radius=6, fill='#0f281e', outline=cl, width=1)
        draw.text((left_x2 - 118, vy + 16), st, fill=cl, font=font_small)
        draw.text((left_x1 + 35, vy + 45), dsc, fill='#94a3b8', font=font_code)
        draw.text((left_x1 + 35, vy + 75), "Target: Amsterdam Primary Cluster AMS-01 • Zero Cloud Act Reach", fill='#64748b', font=font_small)

    # Right Section: Live Telemetry Graph & Log
    right_x1, right_y1 = 850, 225
    right_x2, right_y2 = 1880, 975
    draw.rounded_rectangle([(right_x1, right_y1), (right_x2, right_y2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    draw.text((right_x1 + 24, right_y1 + 18), "Live Throughput Absorption & Edge Scrubbing Engine", fill='#f3dfba', font=font_h2)
    draw.line([(right_x1 + 24, right_y1 + 52), (right_x2 - 24, right_y1 + 52)], fill='#1e382b', width=1)

    # Simulated Sparkline Chart Box
    chart_y = right_y1 + 70
    draw.rounded_rectangle([(right_x1 + 20, chart_y), (right_x2 - 20, chart_y + 260)], radius=12, fill='#020704', outline='#183327', width=1)
    draw.text((right_x1 + 35, chart_y + 15), "Real-Time Ingestion (Requests / Sec) — Peak Handling Verified", fill='#94a3b8', font=font_small)

    # Points for chart
    pts = [
        (right_x1 + 40, chart_y + 210),
        (right_x1 + 200, chart_y + 180),
        (right_x1 + 360, chart_y + 120),
        (right_x1 + 520, chart_y + 150),
        (right_x1 + 680, chart_y + 80),
        (right_x1 + 840, chart_y + 60),
        (right_x2 - 40, chart_y + 50)
    ]
    for k in range(len(pts) - 1):
        draw.line([pts[k], pts[k+1]], fill='#10b981', width=3)
        draw.ellipse([(pts[k][0]-4, pts[k][1]-4), (pts[k][0]+4, pts[k][1]+4)], fill='#34d399')
    draw.ellipse([(pts[-1][0]-4, pts[-1][1]-4), (pts[-1][0]+4, pts[-1][1]+4)], fill='#34d399')

    # Security Log Stream
    log_y = chart_y + 280
    draw.rounded_rectangle([(right_x1 + 20, log_y), (right_x2 - 20, right_y2 - 20)], radius=12, fill='#020604', outline='#183327', width=1)
    logs = [
        ("[23:15:01.042] [BGP] Anycast announced across Equinix AM3, AM4, and Interxion Frankfurt.", '#38bdf8'),
        ("[23:15:02.115] [WAF] Scrubbed 142 malicious SQLi payload attempts on /api/v1/auth.", '#34d399'),
        ("[23:15:03.882] [STRESS] Concurrency set to 50,000 Req/s. Cluster CPU remaining below 34%.", '#f3dfba'),
        ("[23:15:05.109] [MITIGATE] 10,000 bot SYN packets scrubbed at Edge Layer without passing to origin.", '#34d399'),
        ("[23:15:06.440] [AUDIT] Zero unencrypted bytes detected in transit. All requests TLS 1.3 enforced.", '#fbbf24')
    ]
    for m, (txt, col) in enumerate(logs):
        draw.text((right_x1 + 35, log_y + 16 + m * 30), txt, fill=col, font=font_code)

    # Save to targets
    out_paths = [
        os.path.join(ROOT, 'assets', 'branding', 'live_stress_testing_showcase_snapshot.png'),
        os.path.join(BRAIN_ACTIVE, 'live_stress_testing_showcase_snapshot.png'),
        os.path.join(BRAIN_PREV, 'live_stress_testing_showcase_snapshot.png')
    ]
    for p in out_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p, format='PNG', optimize=True)
            print(f"Saved Stress Testing snapshot to: {p}")
        except Exception as e:
            print(f"Failed to save {p}: {e}")

def generate_compliance_showcase():
    W, H = 1920, 1080
    img = Image.new('RGB', (W, H), '#020705')
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / float(H)
        r = int(2 + ratio * 3)
        g = int(8 + ratio * 8)
        b = int(6 + ratio * 6)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_title = get_font(30, bold=True)
    font_sub = get_font(16, bold=False)
    font_h2 = get_font(20, bold=True)
    font_body = get_font(15, bold=False)
    font_code = get_font(13, bold=False)
    font_small = get_font(12, bold=False)
    font_badge = get_font(13, bold=True)

    # Header
    draw.rectangle([(0, 0), (W, 90)], fill='#04140e', outline='#c5a880', width=1)
    emblem_path = os.path.join(ROOT, 'assets', 'branding', 'coresync-emblem-8k.png')
    if os.path.exists(emblem_path):
        try:
            emb = Image.open(emblem_path).resize((62, 62), Image.Resampling.LANCZOS)
            img.paste(emb, (35, 14), emb if emb.mode == 'RGBA' else None)
        except Exception:
            pass

    draw.text((115, 16), "S&R CoreSync | ISO 27001 & Global Regulatory Assurance Center", fill='#f3dfba', font=font_title)
    draw.text((115, 56), "Milestone 73 • ISO/IEC 27001:2022 • SOC 2 Type II • GDPR Article 32 EU Residency • NCSC-NL Level 4", fill='#94a3b8', font=font_sub)

    badge_x = 1380
    draw.rounded_rectangle([(badge_x, 22), (badge_x + 500, 68)], radius=22, fill='#072c1e', outline='#10b981', width=2)
    draw.ellipse([(badge_x + 18, 40), (badge_x + 30, 52)], fill='#10b981')
    draw.text((badge_x + 40, 34), "AUDIT STATUS: 100% UNQUALIFIED COMPLIANT", fill='#34d399', font=font_badge)

    # 4 Key Pillars
    pillars = [
        ("ISO/IEC 27001:2022", "93 Controls 100%", "Certified ISMS • Amsterdam Vaults", '#f3dfba', '#0e3425'),
        ("SOC 2 TYPE II", "Unqualified Opinion", "Security, Confidentiality & Availability", '#34d399', '#08261a'),
        ("GDPR & DUTCH AVG", "EU Sovereign Residency", "Article 32 BYOK • Zero US Cloud Exposure", '#38bdf8', '#0c2238'),
        ("DUTCH NCSC LEVEL 4", "Critical Grade", "Cyber Security Framework Aligned", '#fbbf24', '#2d2208')
    ]
    box_w = 445
    for i, (title, val, sub, col, bg) in enumerate(pillars):
        bx = 40 + i * (box_w + 20)
        by = 105
        draw.rounded_rectangle([(bx, by), (bx + box_w, by + 105)], radius=16, fill=bg, outline=col, width=1)
        draw.text((bx + 20, by + 14), title, fill='#94a3b8', font=font_small)
        draw.text((bx + 20, by + 40), val, fill=col, font=font_h2)
        draw.text((bx + 20, by + 74), sub, fill='#64748b', font=font_small)

    # Table Section: 5 Detailed Controls
    tx1, ty1 = 40, 225
    tx2, ty2 = 1880, 975
    draw.rounded_rectangle([(tx1, ty1), (tx2, ty2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    draw.text((tx1 + 24, ty1 + 18), "Cryptographically Verified Compliance Controls Matrix (Zero-Knowledge Attestation)", fill='#f3dfba', font=font_h2)
    draw.line([(tx1 + 24, ty1 + 52), (tx2 - 24, ty1 + 52)], fill='#1e382b', width=1)

    headers = [("DOMAIN & OBJECTIVE", 40), ("REGULATORY STANDARD", 420), ("IMPLEMENTATION SCOPE", 800), ("DIGITAL EVIDENCE DIGEST (SHA-256)", 1320), ("STATUS", 1700)]
    for hname, hx in headers:
        draw.text((tx1 + hx, ty1 + 65), hname, fill='#94a3b8', font=font_small)
    draw.line([(tx1 + 24, ty1 + 90), (tx2 - 24, ty1 + 90)], fill='#1e382b', width=1)

    rows = [
        ("Sovereign Data Isolation", "GDPR Art. 32 / ISO A.8.24", "Single-tenant dedicated databases in Amsterdam AMS-01", "8f4c9b2018a...4b02e1a9", "✓ VERIFIED"),
        ("Hardware KMS & Envelope Encryption", "FIPS 140-3 Level 4 / ISO A.8.20", "Physical HSM modules with ChaCha20-Poly1305 and Ed25519", "3a710dec889...9911c420", "✓ VERIFIED"),
        ("Disaster Recovery & WORM Storage", "ISO A.8.14 / SOC 2 A1.2", "Frankfurt WORM node with RTO < 2.4 min and zero RPO", "99b5e320aa1...2284f881", "✓ VERIFIED"),
        ("External Penetration & Code Audit", "NCSC-NL / OWASP Top 10", "Quarterly automated stress testing with zero critical flaws", "6d148aa9012...8833072b", "✓ VERIFIED"),
        ("PSD2 Banking & Tax Compliance", "EU PSD2 / Dutch BTW 21%", "Real-time European VAT calculation and immutable receipts", "12ef90c4411...661155d8", "✓ VERIFIED")
    ]
    for r_idx, (d1, d2, d3, d4, d5) in enumerate(rows):
        ry = ty1 + 105 + r_idx * 120
        draw.rounded_rectangle([(tx1 + 20, ry), (tx2 - 20, ry + 100)], radius=12, fill='#040e0a', outline='#183327', width=1)
        draw.text((tx1 + 40, ry + 20), d1, fill='#ffffff', font=font_body)
        draw.text((tx1 + 40, ry + 55), "Annual third-party audit signed by Lead ISO Auditor", fill='#64748b', font=font_small)

        draw.text((tx1 + 420, ry + 20), d2, fill='#c5a880', font=font_body)
        draw.text((tx1 + 800, ry + 20), d3, fill='#94a3b8', font=font_body)
        draw.text((tx1 + 1320, ry + 22), d4, fill='#38bdf8', font=font_code)

        draw.rounded_rectangle([(tx1 + 1680, ry + 22), (tx1 + 1820, ry + 60)], radius=8, fill='#072c1e', outline='#10b981', width=1)
        draw.text((tx1 + 1695, ry + 30), d5, fill='#34d399', font=font_badge)

    # Save to targets
    out_paths = [
        os.path.join(ROOT, 'assets', 'branding', 'live_compliance_center_showcase_snapshot.png'),
        os.path.join(BRAIN_ACTIVE, 'live_compliance_center_showcase_snapshot.png'),
        os.path.join(BRAIN_PREV, 'live_compliance_center_showcase_snapshot.png')
    ]
    for p in out_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p, format='PNG', optimize=True)
            print(f"Saved Compliance snapshot to: {p}")
        except Exception as e:
            print(f"Failed to save {p}: {e}")

def generate_reseller_showcase():
    W, H = 1920, 1080
    img = Image.new('RGB', (W, H), '#020705')
    draw = ImageDraw.Draw(img)

    for y in range(H):
        ratio = y / float(H)
        r = int(2 + ratio * 3)
        g = int(8 + ratio * 8)
        b = int(6 + ratio * 6)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    font_title = get_font(30, bold=True)
    font_sub = get_font(16, bold=False)
    font_h2 = get_font(20, bold=True)
    font_body = get_font(15, bold=False)
    font_code = get_font(13, bold=False)
    font_small = get_font(12, bold=False)
    font_badge = get_font(13, bold=True)

    # Header
    draw.rectangle([(0, 0), (W, 90)], fill='#04140e', outline='#c5a880', width=1)
    emblem_path = os.path.join(ROOT, 'assets', 'branding', 'coresync-emblem-8k.png')
    if os.path.exists(emblem_path):
        try:
            emb = Image.open(emblem_path).resize((62, 62), Image.Resampling.LANCZOS)
            img.paste(emb, (35, 14), emb if emb.mode == 'RGBA' else None)
        except Exception:
            pass

    draw.text((115, 16), "S&R CoreSync | Enterprise B2B White-Label & Reseller Portal", fill='#f3dfba', font=font_title)
    draw.text((115, 56), "Milestone 74 • 100% Brand Customization • PSD2 Instant Commission Payouts • Multi-Tenant Sovereign Cloud", fill='#94a3b8', font=font_sub)

    badge_x = 1380
    draw.rounded_rectangle([(badge_x, 22), (badge_x + 500, 68)], radius=22, fill='#072c1e', outline='#10b981', width=2)
    draw.ellipse([(badge_x + 18, 40), (badge_x + 30, 52)], fill='#10b981')
    draw.text((badge_x + 40, 34), "PARTNER ECOSYSTEM: 28 EUROPEAN RESELLERS", fill='#34d399', font=font_badge)

    # 3 Reseller Tiers Cards
    tiers = [
        ("GOLD PARTNER", "18% Margin", "Co-Branded • SEPA Monthly • L2 Support", '#94a3b8', '#071510', 40),
        ("PLATINUM SOVEREIGN", "28% Margin", "100% White-Label • Custom Domains • HSM Key", '#c5a880', '#0a2218', 655),
        ("ENTERPRISE MASTER", "38% Margin", "Unlimited Tenant Provisioning • 24/7 Exec Manager", '#38bdf8', '#081a28', 1270)
    ]
    for t_name, t_margin, t_desc, t_col, t_bg, t_x in tiers:
        draw.rounded_rectangle([(t_x, 105), (t_x + 600, 310)], radius=16, fill=t_bg, outline=t_col, width=2)
        draw.text((t_x + 24, 125), t_name, fill='#ffffff', font=font_h2)
        draw.text((t_x + 420, 122), t_margin, fill=t_col, font=font_h2)
        draw.line([(t_x + 24, 165), (t_x + 576, 165)], fill='#1e382b', width=1)
        draw.text((t_x + 24, 185), "• " + t_desc, fill='#cbd5e1', font=font_body)
        draw.text((t_x + 24, 220), "• Full PSD2 Instant Automated Ledger Settlements", fill='#94a3b8', font=font_small)
        draw.text((t_x + 24, 255), "• Dedicated Amsterdam Vault & Dutch Tax Invoice Engine", fill='#64748b', font=font_small)

    # Lower Left: ARR Calculator
    lx1, ly1 = 40, 335
    lx2, ly2 = 930, 975
    draw.rounded_rectangle([(lx1, ly1), (lx2, ly2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    draw.text((lx1 + 24, ly1 + 18), "Interactive Reseller Profit Calculator (ARR Projection)", fill='#f3dfba', font=font_h2)
    draw.line([(lx1 + 24, ly1 + 52), (lx2 - 24, ly1 + 52)], fill='#1e382b', width=1)

    calc_boxes = [
        ("SUBSCRIBED ENTERPRISE CLIENTS", "25 Clients", "Average Package: €890 / month", '#38bdf8', '#0c2238'),
        ("GROSS RECURRING MONTHLY VOLUME", "€22,250 / mo", "Client base gross platform billing", '#f3dfba', '#1a2c1f'),
        ("PARTNER COMMISSION RATE", "28.00%", "Platinum Sovereign Tier Standard", '#34d399', '#08261a'),
        ("NET PARTNER ANNUAL ARR", "€74,760 / yr", "Automated PSD2 Payout to IBAN", '#fbbf24', '#2d2208')
    ]
    for c_i, (c_tit, c_val, c_sub, c_col, c_bg) in enumerate(calc_boxes):
        cy = ly1 + 75 + c_i * 135
        draw.rounded_rectangle([(lx1 + 20, cy), (lx2 - 20, cy + 115)], radius=12, fill=c_bg, outline=c_col, width=1)
        draw.text((lx1 + 35, cy + 15), c_tit, fill='#94a3b8', font=font_small)
        draw.text((lx1 + 35, cy + 42), c_val, fill=c_col, font=font_h2)
        draw.text((lx1 + 35, cy + 80), c_sub, fill='#64748b', font=font_small)

    # Lower Right: Instant White-Label Simulator
    rx1, ry1 = 960, 335
    rx2, ry2 = 1880, 975
    draw.rounded_rectangle([(rx1, ry1), (rx2, ry2)], radius=18, fill='#061611', outline='#c5a880', width=1)
    draw.text((rx1 + 24, ry1 + 18), "White-Label Tenant Provisioning Simulator & Live Ledger", fill='#f3dfba', font=font_h2)
    draw.line([(rx1 + 24, ry1 + 52), (rx2 - 24, ry1 + 52)], fill='#1e382b', width=1)

    # Partner Tenant Mock
    mock_y = ry1 + 75
    draw.rounded_rectangle([(rx1 + 20, mock_y), (rx2 - 20, mock_y + 190)], radius=12, fill='#020704', outline='#38bdf8', width=1)
    draw.text((rx1 + 35, mock_y + 18), "PROVISIONED WHITE-LABEL ENVIRONMENT: ACTIVE", fill='#38bdf8', font=font_body)
    draw.text((rx1 + 35, mock_y + 55), "Partner Entity: Nordic Cloud Solutions B.V. (Amsterdam)", fill='#ffffff', font=font_body)
    draw.text((rx1 + 35, mock_y + 88), "Custom Subdomain: portal.nordiccloud.eu • SSL: TLS 1.3 Active", fill='#cbd5e1', font=font_code)
    draw.text((rx1 + 35, mock_y + 120), "Primary Brand Color: Obsidian Navy & Cyan • Dedicated HSM Vault: Armed", fill='#94a3b8', font=font_small)
    draw.text((rx1 + 35, mock_y + 150), "Tenant Cryptographic Digest: 78fe902a...11ef8842 (Immutable Sign-off)", fill='#64748b', font=font_code)

    # Ledger Payout Rows
    ledger_y = mock_y + 210
    draw.text((rx1 + 24, ledger_y), "Recent PSD2 Partner Payout Ledger (SEPA Instant)", fill='#f3dfba', font=font_body)
    payouts = [
        ("Nordic Cloud Solutions B.V.", "€6,230.00", "NL88ABNA01...8892", "PAID & SETTLED (PSD2)", '#34d399'),
        ("Apex Digital Consulting GmbH", "€14,880.00", "DE02DB00...4410", "PAID & SETTLED (PSD2)", '#34d399'),
        ("Benelux AI Innovations B.V.", "€8,410.00", "NL91INGB00...7721", "PAID & SETTLED (PSD2)", '#34d399')
    ]
    for p_idx, (p_name, p_amt, p_iban, p_stat, p_col) in enumerate(payouts):
        py = ledger_y + 35 + p_idx * 75
        draw.rounded_rectangle([(rx1 + 20, py), (rx2 - 20, py + 65)], radius=10, fill='#040e0a', outline='#183327', width=1)
        draw.text((rx1 + 35, py + 12), p_name, fill='#ffffff', font=font_body)
        draw.text((rx1 + 35, py + 38), p_iban, fill='#64748b', font=font_code)
        draw.text((rx2 - 220, py + 12), p_amt, fill='#fbbf24', font=font_body)
        draw.text((rx2 - 220, py + 38), p_stat, fill=p_col, font=font_small)

    # Save to targets
    out_paths = [
        os.path.join(ROOT, 'assets', 'branding', 'live_reseller_portal_showcase_snapshot.png'),
        os.path.join(BRAIN_ACTIVE, 'live_reseller_portal_showcase_snapshot.png'),
        os.path.join(BRAIN_PREV, 'live_reseller_portal_showcase_snapshot.png')
    ]
    for p in out_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p, format='PNG', optimize=True)
            print(f"Saved Reseller snapshot to: {p}")
        except Exception as e:
            print(f"Failed to save {p}: {e}")

if __name__ == '__main__':
    generate_stress_showcase()
    generate_compliance_showcase()
    generate_reseller_showcase()
