"""
Generate Official Corporate Profile PDF for S&R CoreSync For Intelligent Solutions
Using ReportLab with Luxury Gold & Obsidian Styling.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PROJECT_DIR = r"i:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
OUTPUT_PDF = os.path.join(ASSETS_DIR, "SR-CoreSync-Corporate-Profile-2026.pdf")

# Luxury Colors
GOLD_BRIGHT = colors.HexColor("#f3dfba")
GOLD = colors.HexColor("#c5a880")
GOLD_DARK = colors.HexColor("#8c734b")
OBSIDIAN_BG = colors.HexColor("#040807")
DARK_PANEL = colors.HexColor("#0a1611")
BORDER_GOLD = colors.HexColor("#4a3e2e")
TEXT_LIGHT = colors.HexColor("#ffffff")
TEXT_MUTED = colors.HexColor("#b0bfb8")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Draw background color
        self.saveState()
        self.setFillColor(OBSIDIAN_BG)
        self.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Outer Gold Border
        self.setStrokeColor(BORDER_GOLD)
        self.setLineWidth(1)
        self.roundRect(15, 15, A4[0] - 30, A4[1] - 30, 8, fill=0, stroke=1)
        
        # Inner hairline border
        self.setStrokeColor(colors.HexColor("#261f17"))
        self.setLineWidth(0.5)
        self.roundRect(18, 18, A4[0] - 36, A4[1] - 36, 6, fill=0, stroke=1)
        
        # Footer
        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 7.5)
        self.drawString(28, 24, "S&R CoreSync For Intelligent Solutions  |  Keizersgracht 482, 1016 GD Amsterdam, Netherlands")
        self.drawRightString(A4[0] - 28, 24, f"sr-coresync.com  |  Page {self._pageNumber} of {page_count}")
        
        # Top Header (except on cover page 1)
        if self._pageNumber > 1:
            self.setStrokeColor(BORDER_GOLD)
            self.line(28, A4[1] - 35, A4[0] - 28, A4[1] - 35)
            self.setFillColor(GOLD)
            self.setFont("Helvetica-Bold", 8)
            self.drawString(28, A4[1] - 30, "S&R CORESYNC FOR INTELLIGENT SOLUTIONS")
            self.setFillColor(TEXT_MUTED)
            self.setFont("Helvetica", 7.5)
            self.drawRightString(A4[0] - 28, A4[1] - 30, "ENTERPRISE CLOUD, AI & FINANCIAL ERP SYSTEMS")
            
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=TEXT_LIGHT,
        alignment=1, # Center
        spaceAfter=8
    )

    gold_title_style = ParagraphStyle(
        'GoldTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=GOLD_BRIGHT,
        alignment=1,
        spaceAfter=15
    )

    tagline_style = ParagraphStyle(
        'CoverTagline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=TEXT_MUTED,
        alignment=1,
        spaceAfter=20
    )

    sec_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=GOLD_BRIGHT,
        spaceAfter=4
    )

    sec_subheading = ParagraphStyle(
        'SecSubheading',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=12
    )

    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=TEXT_LIGHT
    )

    card_role = ParagraphStyle(
        'CardRole',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=GOLD
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#d0ded7")
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<font color='#c5a880' size='9'><b>OFFICIAL CORPORATE PORTFOLIO • 2026 EDITION</b></font>", tagline_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("S&R CORESYNC FOR INTELLIGENT SOLUTIONS", title_style))
    story.append(Paragraph("For Intelligent Solutions — Enterprise Cloud, AI Automation & Financial ERP Systems", gold_title_style))
    story.append(Paragraph("Amsterdam Headquarters, Keizersgracht 482, Netherlands  |  High-End Enterprise Architecture", tagline_style))
    
    # Official Emblem Image
    emblem_path = os.path.join(ASSETS_DIR, "sr-emblem-gold-luxury.jpg")
    if os.path.exists(emblem_path):
        story.append(RLImage(emblem_path, width=420, height=236))
    story.append(Spacer(1, 20))

    # Highlights Table
    data_cover = [
        [
            Paragraph("<b>HEADQUARTERS</b><br/><font color='#c5a880'>Amsterdam, Netherlands 🇳🇱</font>", body_style),
            Paragraph("<b>CORE SPECIALIZATION</b><br/><font color='#c5a880'>Multi-Cloud & AI Architecture</font>", body_style),
            Paragraph("<b>GOVERNANCE</b><br/><font color='#c5a880'>IFRS & European Standard ⚖️</font>", body_style)
        ]
    ]
    t_cover = Table(data_cover, colWidths=[175, 175, 175])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_PANEL),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE LEADERSHIP & FOUNDERS
    # =========================================================================
    story.append(Paragraph("EXECUTIVE LEADERSHIP & FOUNDERS", sec_heading))
    story.append(Paragraph("Bridging High-Performance Cloud & AI Engineering with Senior Financial & ERP Strategy", sec_subheading))
    story.append(Spacer(1, 5))

    # Founder 1: Salim Aziza
    salim_banner = os.path.join(ASSETS_DIR, "founder-banner-salim.jpg")
    salim_img = RLImage(salim_banner, width=190, height=107) if os.path.exists(salim_banner) else ""
    salim_text = [
        Paragraph("<b>Eng. Mohammad Salim Aziza</b>", card_title),
        Paragraph("Chief Technology Officer & Principal Cloud / AI Architect", card_role),
        Spacer(1, 4),
        Paragraph("Over 12 years of hands-on leadership architecting high-availability cloud ecosystems (GCP, AWS, Azure), custom Enterprise AI agents, large language model (LLM) fine-tuning, and robust zero-trust security for global organizations.", body_style),
        Spacer(1, 4),
        Paragraph("<font color='#f3dfba'><b>Key Credentials:</b></font> Multi-Cloud Infrastructure, Microservices, Real-Time Data Pipelines, Sovereign European Security.", body_style)
    ]
    t_salim = Table([[salim_img, salim_text]], colWidths=[200, 325])
    t_salim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_PANEL),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_salim)
    story.append(Spacer(1, 14))

    # Founder 2: Raed Kaaka
    raed_banner = os.path.join(ASSETS_DIR, "founder-banner-raed.jpg")
    raed_img = RLImage(raed_banner, width=190, height=107) if os.path.exists(raed_banner) else ""
    raed_text = [
        Paragraph("<b>Mr. Mohammad Raed Kaaka</b>", card_title),
        Paragraph("Chief Financial Officer & Senior Financial ERP Systems Architect", card_role),
        Spacer(1, 4),
        Paragraph("Senior financial strategist and ERP solution architect specializing in Odoo enterprise integrations, automated financial auditing, IFRS compliance, European tax governance, and complete financial pipeline restructuring.", body_style),
        Spacer(1, 4),
        Paragraph("<font color='#f3dfba'><b>Key Credentials:</b></font> Enterprise ERP Deployment, Cost Optimization, Tax & Corporate Law Compliance, Capital Structuring.", body_style)
    ]
    t_raed = Table([[raed_img, raed_text]], colWidths=[200, 325])
    t_raed.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_PANEL),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_raed)
    story.append(Spacer(1, 15))

    # Symmetry Quote
    quote_text = Paragraph(
        "<i>\"We unite deep technical rigor with high-level financial governance to guarantee enterprise digital transformation that yields verifiable ROI and unassailable security.\"</i> — <b>Founding Partners, S&R CoreSync</b>",
        ParagraphStyle('Quote', parent=body_style, textColor=GOLD, alignment=1)
    )
    t_quote = Table([[quote_text]], colWidths=[525])
    t_quote.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#060e0b")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_quote)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ENTERPRISE SERVICE PILLARS
    # =========================================================================
    story.append(Paragraph("CORE SERVICE ECOSYSTEM", sec_heading))
    story.append(Paragraph("Enterprise-Grade Solutions Engineered for Agility, Scalability, and European Regulatory Compliance", sec_subheading))
    story.append(Spacer(1, 8))

    services_data = [
        [
            Paragraph("<b>1. Multi-Cloud & Hybrid Infrastructure</b><br/><br/><font color='#c5a880'>• Sovereign Cloud Migration & Governance<br/>• Zero-Downtime High-Availability Setup<br/>• Kubernetes & Microservices Orchestration<br/>• Zero-Trust Cyber Security & Encryption</font>", body_style),
            Paragraph("<b>2. Enterprise AI & Autonomous Agents</b><br/><br/><font color='#c5a880'>• Private Custom AI Agent Workflows<br/>• LLM Fine-Tuning on Corporate Datasets<br/>• Intelligent Document & Invoice Automation<br/>• Predictive Financial & Operational Analytics</font>", body_style)
        ],
        [
            Paragraph("<b>3. Odoo & Comprehensive ERP Systems</b><br/><br/><font color='#c5a880'>• End-to-End Odoo ERP Implementation<br/>• Supply Chain, Inventory & POS Integration<br/>• Real-Time Enterprise CRM & Workflow Engines<br/>• Tailored Custom Module Architecture</font>", body_style),
            Paragraph("<b>4. Financial Advisory & IFRS Compliance</b><br/><br/><font color='#c5a880'>• European Corporate Tax Structuring<br/>• Automated Auditing & Reporting Pipelines<br/>• Strategic M&A Advisory & Valuation<br/>• Multi-Currency Treasury Automation</font>", body_style)
        ]
    ]
    t_services = Table(services_data, colWidths=[260, 260])
    t_services.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_PANEL),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_services)
    story.append(Spacer(1, 15))

    # Enterprise Packages summary
    story.append(Paragraph("<b>ENTERPRISE ENGAGEMENT MODELS</b>", card_title))
    story.append(Spacer(1, 6))
    pkg_data = [
        [
            Paragraph("<b>Professional Tier</b><br/><font color='#c5a880'>€1,850/mo</font><br/>Cloud Architecture & Standard ERP Setup", body_style),
            Paragraph("<b>Enterprise Tier</b><br/><font color='#f3dfba'>€3,450/mo</font><br/>Full AI Automation, Odoo Suite & Financial Advisory", body_style),
            Paragraph("<b>Sovereign Sovereign</b><br/><font color='#c5a880'>Custom Engagement</font><br/>Dedicated VP Engineering & On-Site CFO Advisory", body_style)
        ]
    ]
    t_pkg = Table(pkg_data, colWidths=[175, 175, 175])
    t_pkg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#08120d")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_pkg)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: DIGITAL NFC CONTACT HUB & QR CODES
    # =========================================================================
    story.append(Paragraph("CERTIFIED DIGITAL CONTACT HUB & NFC INTEGRATION", sec_heading))
    story.append(Paragraph("Scan any QR code below with your smartphone camera to instantly save certified vCards", sec_subheading))
    story.append(Spacer(1, 10))

    # QR Codes Grid
    qr_salim = os.path.join(ASSETS_DIR, "qr-founder-salim.png")
    qr_raed = os.path.join(ASSETS_DIR, "qr-founder-raed.png")
    qr_comp = os.path.join(ASSETS_DIR, "qr-company-emblem.png")

    img_q_s = RLImage(qr_salim, width=130, height=130) if os.path.exists(qr_salim) else ""
    img_q_r = RLImage(qr_raed, width=130, height=130) if os.path.exists(qr_raed) else ""
    img_q_c = RLImage(qr_comp, width=130, height=130) if os.path.exists(qr_comp) else ""

    qr_cells = [
        [img_q_s, img_q_r, img_q_c],
        [
            Paragraph("<b>Eng. Mohammad Salim Aziza</b><br/><font color='#c5a880'>CTO & Cloud Architect<br/>+31 6 18111116</font>", body_style),
            Paragraph("<b>Mr. Mohammad Raed Kaaka</b><br/><font color='#c5a880'>CFO & ERP Consultant<br/>+31 6 18111116</font>", body_style),
            Paragraph("<b>S&R CoreSync Portal</b><br/><font color='#c5a880'>Corporate Headquarters<br/>info@sr-coresync.com</font>", body_style)
        ]
    ]
    t_qr = Table(qr_cells, colWidths=[175, 175, 175])
    t_qr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_PANEL),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_GOLD),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_qr)
    story.append(Spacer(1, 20))

    # Official HQ & Legal Box
    legal_text = [
        Paragraph("<b>OFFICIAL CORPORATE HEADQUARTERS & GOVERNANCE</b>", card_title),
        Spacer(1, 6),
        Paragraph("<b>Company:</b> S&R CoreSync For Intelligent Solutions  |  <b>Jurisdiction:</b> Kingdom of the Netherlands 🇳🇱", body_style),
        Paragraph("<b>Address:</b> Keizersgracht 482, 1016 GD Amsterdam, Netherlands", body_style),
        Paragraph("<b>Official Contact:</b> +31 6 18111116  |  <b>Official Inquiries:</b> info@sr-coresync.com", body_style),
        Paragraph("<b>Digital Hub:</b> https://sr-coresync.com  |  <b>NFC Card Link:</b> https://sr-coresync.com/card.html", body_style)
    ]
    t_legal = Table([[legal_text]], colWidths=[525])
    t_legal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#060e0a")),
        ('BOX', (0,0), (-1,-1), 1, GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t_legal)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated Official PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF) // 1024} KB)")

if __name__ == "__main__":
    build_pdf()
