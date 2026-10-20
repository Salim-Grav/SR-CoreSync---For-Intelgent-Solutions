# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - 100% Comprehensive Multilingual Demo Portal Generator (v2)
Translates EVERY single Arabic string in demo.html to high-end corporate English and Dutch.
Establishes full language isolation and LTR ergonomics with ZERO leftover Arabic text.
"""

import os
import re

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(PROJECT_DIR, 'demo.html')
DEMO_EN_PATH = os.path.join(PROJECT_DIR, 'en', 'demo.html')
DEMO_NL_PATH = os.path.join(PROJECT_DIR, 'nl', 'demo.html')

with open(DEMO_AR_PATH, 'r', encoding='utf-8') as f:
    ar_master = f.read()

# Exhaustive translations
DICT = {
    # Head & Meta
    "S&R CoreSync | المنصة السحابية التجريبية (Live Interactive Demo Portal)": (
        "S&R CoreSync | Live Interactive Cloud ERP Portal (Demo)",
        "S&R CoreSync | Live Interactieve Cloud ERP Portal (Demo)"
    ),
    "النظام السحابي متصل (EU Node)": (
        "Cloud Node Online (EU Central)",
        "Cloud Node Online (EU Centraal)"
    ),
    "بدء جولة إرشادية خطواتية توضح مزايا المنصة للزبون": (
        "Start step-by-step interactive guided tour of the ERP architecture",
        "Start interactieve stapsgewijze rondleiding langs de ERP-architectuur"
    ),
    "🚀 ابدأ الجولة": (
        "🚀 Start Tour",
        "🚀 Start Rondleiding"
    ),
    "تصدير بطاقة العرض التنفيذي إلى ملف PDF أنيق للعميل": (
        "Export executive proposal brief to an elegant client PDF",
        "Exporteer zakelijk voorsteloverzicht naar een elegante PDF"
    ),
    "ملخص العرض (PDF)": (
        "Proposal Brief (PDF)",
        "Offerte Overzicht (PDF)"
    ),
    "وضع العرض التقديمي للزبائن (شاشة كاملة وتجربة تنفيذية)": (
        "Client presentation mode (Full screen executive walkthrough)",
        "Klantpresentatiemodus (Volledig scherm en executive ervaring)"
    ),
    "عرض الزبائن [P]": (
        "Client View [P]",
        "Klantpresentatie [P]"
    ),
    "نقل تفضيلات الجلسة وحجز موعد استشاري": (
        "Transfer session telemetry & book founders consultation",
        "Draag sessie-instellingen over en plan oprichtersconsult"
    ),
    "حجز استشارة بهذا النظام": (
        "Book Session with this Architecture",
        "Plan Consult met dit Systeem"
    ),
    "استوديو ومحرر الشعار": (
        "Emblem & Brand Identity Studio",
        "Embleem & Merkidentiteit Studio"
    ),
    "استوديو الشعار": (
        "Emblem Studio",
        "Embleem Studio"
    ),
    "العودة للصفحة الرئيسية - S&R CoreSync Solutions": (
        "Return to Homepage - S&R CoreSync Solutions",
        "Terug naar Homepage - S&R CoreSync Solutions"
    ),
    "العودة للموقع": (
        "Return to Website",
        "Terug naar Website"
    ),
    "تبديل لغة المنصة": (
        "Portal Language",
        "Platformtaal"
    ),

    # Sidebar Navigation
    "لوحة القيادة المالية": (
        "Executive Dashboard",
        "Executive Dashboard"
    ),
    "إدارة الـ ERP والمخازن": (
        "ERP & Inventory Ops",
        "ERP & Voorraadbeheer"
    ),
    "الفواتير والتدفقات النقدية": (
        "E-Invoicing & VAT",
        "E-Facturatie & BTW"
    ),
    "سوق البرمجيات (Software Hub)": (
        "Software Hub & Store",
        "Software Hub & Marktplaats"
    ),
    "المساعد المالي الذكي (AI)": (
        "AI Financial Copilot",
        "AI Financiële Copilot"
    ),
    "حالة الخوادم السحابية": (
        "Cloud Server Status",
        "Cloud Serverstatus"
    ),
    "تخصيص الهوية (White-Label)": (
        "White-Label Branding",
        "White-Label Personalisatie"
    ),
    "تكامل مع الإدارة": (
        "Enterprise Consulting",
        "Zakelijk Consult"
    ),
    "طلب تفعيل لشركتك": (
        "Request Company Activation",
        "Vraag Bedrijfsactivatie Aan"
    ),
    "انقل تفاصيل الجلسة والسيناريوهات المجرّبة مباشرة لاستشارة المؤسسين.": (
        "Transfer session configurations and tested scenarios directly to the founders consultation.",
        "Draag sessie-inzichten en geteste scenario's direct over naar het oprichtersconsult."
    ),
    "حجز استشارة مخصصة": (
        "Book Custom Consultation",
        "Plan Maatwerk Consult"
    ),
    "جلسة معاينة تفاعلية": (
        "Interactive Preview Session",
        "Interactieve Previewsessie"
    ),

    # Simulator Bar
    "محاكي العملات والضرائب الحي (Live Currency & VAT Simulator):": (
        "Live Currency & VAT Simulator:",
        "Live Valuta & BTW Simulator:"
    ),
    "العملة:": (
        "Currency:",
        "Valuta:"
    ),
    "النظام الضريبي:": (
        "Tax Regime:",
        "Belastingstelsel:"
    ),
    "اختيار النظام الضريبي المالي": (
        "Select financial tax regime",
        "Selecteer belastingstelsel"
    ),
    "🇳🇱 BTW هولندي (21%)": (
        "🇳🇱 Dutch BTW (21%)",
        "🇳🇱 Nederlandse BTW (21%)"
    ),
    "🇳🇱 BTW مخفض (9%)": (
        "🇳🇱 Reduced BTW (9%)",
        "🇳🇱 Verlaagd BTW-tarief (9%)"
    ),
    "🇸🇦 ضريبة خليجية (15%)": (
        "🇸🇦 GCC VAT (15%)",
        "🇸🇦 GCC Btw (15%)"
    ),
    "🌐 معفى ضريبياً (0%)": (
        "🌐 Tax Exempt (0%)",
        "🌐 Vrijgesteld van belasting (0%)"
    ),
    "الضريبة المحتسبة:": (
        "Calculated Tax:",
        "Berekende Belasting:"
    ),

    # Section 1: Overview & Financial KPIs
    "لوحة القيادة والتدفق المالي اللحظي": (
        "Real-Time Financial Dashboard & Cash Flow Telemetry",
        "Realtime Financieel Dashboard & Cashflow Telemetrie"
    ),
    "نظام محاكاة حي لحركات الحسابات والإيرادات والمصروفات السحابية المؤتمتة": (
        "Live simulation engine for automated enterprise revenue, cloud expenses, and cash telemetry",
        "Live simulatiesysteem voor geautomatiseerde bedrijfsinkomsten, clouduitgaven en cashflow"
    ),
    "تسجيل معاملة تجريبية": (
        "Record Test Transaction",
        "Registreer Testtransactie"
    ),
    "إجمالي الإيرادات السنوية": (
        "Annual Gross Revenue",
        "Totale Jaaromzet"
    ),
    "مقارنة بالربع السابق": (
        "vs previous quarter",
        "t.o.v. vorig kwartaal"
    ),
    "التدفقات النقدية الصافية": (
        "Net Operating Cash Flow",
        "Netto Operationele Cashflow"
    ),
    "هامش ربحية تشغيلية": (
        "operating profit margin",
        "operationele winstmarge"
    ),
    "طلبات الـ ERP المنجزة": (
        "Completed ERP Orders",
        "Voltooide ERP Orders"
    ),
    "نسبة الامتثال والدقة": (
        "compliance & accuracy rate",
        "nalevings- en nauwkeurigheidsgraad"
    ),
    "عمليات الأتمتة الموفرة": (
        "Automated Work Hours Saved",
        "Bespaarde Automatiseringsuren"
    ),
    "وفر شهري مباشر في وقت الفريق": (
        "Direct monthly time saved for your team",
        "Directe maandelijkse tijdsbesparing voor uw team"
    ),
    "480 ساعة": (
        "480 hours",
        "480 uur"
    ),
    "حركة الإيرادات والتدفق النقدي الشهري (€)": (
        "Monthly Revenue & Cash Flow Trajectory (€)",
        "Maandelijkse Omzet & Cashflow Traject (€)"
    ),
    "توزيع العمليات حسب القطاع": (
        "Operational Breakdown by Sector",
        "Operationele Verdeling per Sector"
    ),
    "سجل العمليات والربط المحاسبي المباشر": (
        "Live Ledger Transactions & Accounting Bridge",
        "Live Grootboektransacties & Boekhoudkoppeling"
    ),
    "مزامنة سحابية لحظية": (
        "Real-time cloud synchronization",
        "Realtime cloudsynchronisatie"
    ),
    "رقم المعاملة": (
        "Tx ID",
        "Transactie-ID"
    ),
    "الجهة / العميل": (
        "Client / Entity",
        "Klant / Entiteit"
    ),
    "التاريخ": (
        "Date",
        "Datum"
    ),
    "النوع / القسم": (
        "Category / Module",
        "Categorie / Module"
    ),
    "المبلغ": (
        "Amount",
        "Bedrag"
    ),
    "الحالة والامتثال": (
        "Status & Compliance",
        "Status & Naleving"
    ),
    "نوع العملية": (
        "Operation Type",
        "Transactietype"
    ),
    "مجموعة الخدمات اللوجستية (هولندا)": (
        "Dutch Logistics Services BV (NL)",
        "Nederlandse Logistieke Diensten BV (NL)"
    ),
    "تكامل مخازن ERP": (
        "ERP Warehouse Sync",
        "ERP Magazijnkoppeling"
    ),
    "تمت المزامنة": (
        "Synchronized",
        "Gesynchroniseerd"
    ),
    "حوكمة دفاتر الحسابات": (
        "General Ledger Audit",
        "Grootboekcontrole"
    ),
    "مجموعة التوزيع التجاري (الرياض)": (
        "Riyadh Commercial Distribution (GCC)",
        "Riyad Handelsdistributie (GCC)"
    ),
    "تطبيق مالي سحابي": (
        "Cloud Financial App",
        "Cloud Financiële App"
    ),
    "قيد التدقيق الآلي": (
        "Automated Audit",
        "Automatische Controle"
    ),
    "ربط نقاط البيع POS": (
        "POS Cashier Integration",
        "Kassa / POS Koppeling"
    ),
    "مكتملة (SEPA)": (
        "Completed (SEPA)",
        "Voltooid (SEPA)"
    ),
    "تمت التسوية (iDEAL)": (
        "Settled (iDEAL)",
        "Verrekend (iDEAL)"
    ),
    "قيد المعالجة السحابية": (
        "Processing (Cloud)",
        "In verwerking (Cloud)"
    ),

    # Section 2: ERP & Inventory
    "منظومة الـ ERP وإدارة سلاسل الإمداد": (
        "Enterprise ERP & Supply Chain Operations",
        "Enterprise ERP & Supply Chain Beheer"
    ),
    "نظام إدارة الموارد المؤسسية (ERP) والمخازن الذكية": (
        "Enterprise Resource Planning (ERP) & Smart Warehouse Ops",
        "Enterprise Resource Planning (ERP) & Slim Voorraadbeheer"
    ),
    "إدارة المخزون متعدد الفروع، تتبع سلاسل التوريد، والتنبؤ التلقائي بالنواقص": (
        "Multi-branch warehouse management, supply chain telemetry, and automated reorder triggers",
        "Voorraadbeheer voor meerdere vestigingen, supply chain telemetrie en automatische herbestellingen"
    ),
    "تكامل مركزي للمخازن، المشتريات، وتتبع الأصول بين المستودعات الأوروبية والخليجية": (
        "Centralized integration for warehouses, procurement, and asset tracking between European and GCC hubs",
        "Centrale integratie voor magazijnen, inkoop en voorraadtracking tussen Europese en GCC hubs"
    ),
    "المستودعات المرتبطة": (
        "Connected Fulfillment Hubs",
        "Gekoppelde Fulfilment Hubs"
    ),
    "6 مراكز": (
        "6 Hubs",
        "6 Hubs"
    ),
    "إجمالي الأصناف النشطة": (
        "Total Active SKUs",
        "Totaal Actieve Artikelen"
    ),
    "18,450 وحدة": (
        "18,450 units",
        "18.450 stuks"
    ),
    "تتبع تلقائي بالباركود وRFID": (
        "Automated barcode & RFID tracking",
        "Automatische barcode- & RFID-tracking"
    ),
    "أوامر التوريد الجارية": (
        "Ongoing Supply Orders",
        "Lopende Leveringsorders"
    ),
    "34 أمر توريد": (
        "34 Purchase Orders",
        "34 Inkooporders"
    ),
    "مؤتمتة مع الموردين المعتمدين": (
        "Automated with verified vendors",
        "Geautomatiseerd met goedgekeurde leveranciers"
    ),
    "خريطة تدفق السلع والطلبات التلقائية": (
        "Automated Goods Flow & Reorder Map",
        "Geautomatiseerde Goederenstroom & Herbestelkaart"
    ),
    "يقوم محرك S&R CoreSync ERP بتحديث مستويات المخزون تلقائيًا فور صدور أي فاتورة مبيعات، وإطلاق طلبات إعادة التوريد الذكية عند بلوغ حد الأمان، مما يمنع انقطاع البضائع ويخفض تكاليف التخزين بنسبة 25%.": (
        "The S&R CoreSync ERP engine updates inventory levels in real time the moment a sales invoice is created, triggering smart replenishment orders at safety thresholds to eliminate stockouts and reduce storage holding costs by 25%.",
        "De S&R CoreSync ERP-engine werkt voorraadniveaus direct bij zodra een verkoopfactuur wordt uitgegeven, en triggert automatische herbestellingen bij veiligheidsdrempels om tekorten te voorkomen en opslagkosten met 25% te verlagen."
    ),
    "إضافة منتج للمخزون": (
        "Add Inventory Item",
        "Artikel Toevoegen"
    ),
    "إجمالي عناصر المخزون": (
        "Total Active Inventory Items",
        "Totaal Actieve Artikelen"
    ),
    "منتج مسجل عبر الفروع": (
        "registered across branches",
        "geregistreerd over vestigingen"
    ),
    "مستودعات نشطة": (
        "Connected Fulfillment Hubs",
        "Gekoppelde Fulfilment Hubs"
    ),
    "أمستردام، روتردام، الرياض، دبي": (
        "Amsterdam, Rotterdam, Riyadh, Dubai",
        "Amsterdam, Rotterdam, Riyad, Dubai"
    ),
    "قيمة البضاعة المخزنة": (
        "Total Valuation of Stock",
        "Totale Voorraadwaarde"
    ),
    "جاهزية التوزيع السريع": (
        "Express fulfillment readiness",
        "Snelle leveringsgereedheid"
    ),
    "تنبيهات نقص المخزون": (
        "Low Stock Critical Alerts",
        "Kritieke Voorraadwaarschuwingen"
    ),
    "أوامر شراء مؤتمتة جاهزة": (
        "Automated POs ready for approval",
        "Automatische inkooporders gereed"
    ),
    "جدول المخزون والمواد اللحظي": (
        "Live Warehouse Inventory Ledger",
        "Live Magazijnvoorraad Grootboek"
    ),
    "تحديث حي لكميات الفروع": (
        "Live sync across regional hubs",
        "Live synchronisatie over regionale hubs"
    ),
    "رمز المنتج (SKU)": (
        "SKU Code",
        "Artikelcode (SKU)"
    ),
    "اسم المنتج": (
        "Item Name",
        "Artikelomschrijving"
    ),
    "المستودع": (
        "Warehouse Location",
        "Magazijnlocatie"
    ),
    "الكمية المتوفرة": (
        "Quantity on Hand",
        "Beschikbare Voorraad"
    ),
    "سعر الوحدة": (
        "Unit Price",
        "Eenheidsprijs"
    ),
    "حالة التوريد": (
        "Inventory Status",
        "Voorraadstatus"
    ),
    "متوفر بكثرة": (
        "In Stock",
        "Ruim op voorraad"
    ),
    "حد الأمان (مطلوب توريد)": (
        "Low Stock (Reorder)",
        "Veiligheidsdrempel (Herbestellen)"
    ),
    "مكتمل التوزيع": (
        "Optimal Stock",
        "Optimale voorraad"
    ),

    # Section 3: Invoicing & Compliance
    "الفواتير الإلكترونية والامتثال الضريبي الذكي": (
        "E-Invoicing & Intelligent Tax Compliance",
        "E-Facturatie & Intelligente Belastingnaleving"
    ),
    "مطابقة معايير الفوترة الإلكترونية المعتمدة في هولندا والاتحاد الأوروبي (UBL / PEPPOL) وهيئة الزكاة والضريبة (ZATCA)": (
        "Fully compliant with European e-invoicing standards (UBL / PEPPOL BIS 3.0), Dutch Belastingdienst (AWR), and GCC ZATCA Phase 2",
        "Volledig conform Europese e-facturatiestandaarden (UBL / PEPPOL BIS 3.0), Nederlandse Belastingdienst (AWR) en GCC ZATCA Fase 2"
    ),
    "إنشاء فاتورة سحابية متوافقة مع أنظمة الضرائب في هولندا (BTW 21%) والخليج": (
        "Generate compliant cloud e-invoices with Dutch BTW (21%), EU Reverse Charge, and GCC VAT",
        "Genereer conforme cloud e-facturen met Nederlandse BTW (21%), EU Verlegging en GCC Btw"
    ),
    "معتمدة رقمياً ومطابقة للمعيار الأوروبي EN 16931": (
        "Digitally certified and compliant with European Standard EN 16931",
        "Digitaal gecertificeerd en conform Europese norm EN 16931"
    ),
    "توليد فاتورة إلكترونية تجريبية": (
        "Generate Sample E-Invoice",
        "Voorbeeldfactuur Genereren"
    ),
    "محاكاة دفع فوري عبر iDEAL": (
        "Simulate Instant iDEAL Settlement",
        "Directe iDEAL Betaling Simuleren"
    ),
    "إنشاء فاتورة جديدة": (
        "Create New Invoice",
        "Nieuwe Factuur Aanmaken"
    ),
    "فحص الامتثال المحاسبي AWR": (
        "Run AWR Tax Audit",
        "AWR Boekhoudcontrole Uitvoeren"
    ),
    "تصدير Digipoort XML": (
        "Export Digipoort XML",
        "Digipoort XML Exporteren"
    ),
    "الفواتير الصادرة هذا الشهر": (
        "Invoices Issued This Month",
        "Uitgaande Facturen Deze Maand"
    ),
    "الفواتير المحصلة هذا الشهر": (
        "Invoices Collected This Month",
        "Geïncasseerde Facturen Deze Maand"
    ),
    "فواتير مسجلة": (
        "invoices logged",
        "facturen geregistreerd"
    ),
    "الفواتير المحصلة بنجاح": (
        "Successfully Collected",
        "Succesvol Geïncasseerd"
    ),
    "عبر SEPA وiDEAL": (
        "via SEPA & iDEAL",
        "via SEPA & iDEAL"
    ),
    "المبالغ قيد التحصيل": (
        "Pending Receivables",
        "Openstaande Vorderingen"
    ),
    "الفواتير قيد الاستحقاق": (
        "Invoices Maturing Soon",
        "Binnenkort Vervallende Facturen"
    ),
    "فاتورة واحدة": (
        "1 invoice",
        "1 factuur"
    ),
    "قابلة للمحاكاة الفورية": (
        "ready for live simulation",
        "gereed voor live simulatie"
    ),
    "معدل التحصيل التلقائي": (
        "Automated Settlement Rate",
        "Automatisch Incassopercentage"
    ),
    "تسوية via SEPA & iDEAL بدون تدخل بشري": (
        "Reconciliation via SEPA & iDEAL without manual input",
        "Afstemming via SEPA & iDEAL zonder handmatige tussenkomst"
    ),
    "سداد فوري بالربط البنكي المباشر": (
        "Instant direct banking settlement",
        "Directe bankoverschrijving & verrekening"
    ),
    "تستحق خلال 14 يوماً": (
        "due within 14 days",
        "vervalt binnen 14 dagen"
    ),
    "تستحق خلال 14 يوم": (
        "Due in 14 days",
        "Vervalt binnen 14 dagen"
    ),
    "سجل الفواتير الصادرة والواردة": (
        "Inbound & Outbound Invoices Ledger",
        "Overzicht Inkomende & Uitgaande Facturen"
    ),
    "توليد فوري بتنسيق UBL وXML معتمد": (
        "Instant generation in certified UBL & XML formats",
        "Directe aanmaak in gecertificeerd UBL- & XML-formaat"
    ),
    "توليد لحظي وتوافق كامل مع المعايير المحاسبية": (
        "Real-time generation and 100% accounting standard compliance",
        "Directe aanmaak en 100% conform boekhoudstandaarden"
    ),
    "الكل (5)": (
        "All (5)",
        "Alle (5)"
    ),
    "المدفوعة (3)": (
        "Paid (3)",
        "Betaald (3)"
    ),
    "قيد الانتظار (2)": (
        "Pending (2)",
        "Openstaand (2)"
    ),
    "رقم الفاتورة": (
        "Invoice No.",
        "Factuurnummer"
    ),
    "العميل / الجهة": (
        "Client / Debtor",
        "Klant / Debiteur"
    ),
    "العميل والجهة": (
        "Client / Debtor",
        "Klant / Debiteur"
    ),
    "المبلغ الصافي": (
        "Net Amount",
        "Netto Bedrag"
    ),
    "الضريبة": (
        "VAT / BTW",
        "BTW"
    ),
    "الإجمالي": (
        "Grand Total",
        "Totaalbedrag"
    ),
    "الحالة": (
        "Status",
        "Status"
    ),
    "حالة السداد والربط": (
        "Settlement Status",
        "Betalingsstatus"
    ),
    "طريقة الدفع / الامتثال": (
        "Payment Rail / Compliance",
        "Betaalmethode / Naleving"
    ),
    "الإجراءات": (
        "Actions",
        "Acties"
    ),
    "Actionات التفاعلية": (
        "Interactive Actions",
        "Interactieve Acties"
    ),
    "Actions التفاعلية": (
        "Interactive Actions",
        "Interactieve Acties"
    ),
    "مدفوعة عبر iDEAL ✓": (
        "Paid via iDEAL ✓",
        "Betaald via iDEAL ✓"
    ),
    "مدفوعة بتحويل SEPA Instant ✓": (
        "Paid via SEPA Instant ✓",
        "Betaald via SEPA Instant ✓"
    ),
    "قيد الانتظار": (
        "Pending",
        "Openstaand"
    ),
    "جديدة - تستحق السداد": (
        "New - Due",
        "Nieuw - Te betalen"
    ),
    "معاينة الفاتورة": (
        "Preview Invoice",
        "Factuur Bekijken"
    ),
    "Preview الفاتورة": (
        "Preview Invoice",
        "Factuur Bekijken"
    ),
    "محاكاة سداد iDEAL": (
        "Simulate iDEAL",
        "Simuleer iDEAL"
    ),
    "تحويل بنكي مباشر": (
        "Direct Bank Transfer",
        "Directe Bankoverschrijving"
    ),

    # Section 4: Software Hub & Store
    "سوق البرمجيات والحلول الحصرية (S&R Software Hub & Store)": (
        "Software Ecosystem & Store (S&R Software Hub)",
        "Software Ecosysteem & Marktplaats (S&R Software Hub)"
    ),
    "تطبيقات سطح المكتب للكمبيوتر، تطبيقات الهاتف، وأدوات الربط المطورة حصرياً بعوائد وتراخيص رقمية": (
        "Desktop enterprise apps, mobile scanner clients, and developer SDKs with instant encrypted licensing",
        "Desktop software, mobiele scan-apps en developer SDKs met directe versleutelde licenties"
    ),
    "نشر وتوزيع برنامج جديد عبر المنصة": (
        "Publish & Distribute Enterprise App",
        "Publiceer & Distribueer Zakelijke App"
    ),
    "بصفتك مطوراً ومهندساً للبرمجيات، يمكنك إضافة حلولك وتطبيقاتك الحصرية للبيع والتوزيع:": (
        "As an enterprise software engineer, you can publish exclusive commercial solutions for sale and distribution:",
        "Als enterprise software-engineer kunt u exclusieve commerciële oplossingen publiceren voor verkoop en distributie:"
    ),
    "نشر برنامج جديد (Publish)": (
        "Publish New App",
        "Nieuwe Software Publiceren"
    ),
    "الكل (4)": (
        "All (4)",
        "Alle (4)"
    ),
    "برامج الكمبيوتر PC/Mac (2)": (
        "Desktop PC/Mac (2)",
        "Desktop PC/Mac (2)"
    ),
    "تطبيقات الموبايل (1)": (
        "Mobile Apps (1)",
        "Mobiele Apps (1)"
    ),
    "أدوات المطورين SDK (1)": (
        "Developer SDKs (1)",
        "Developer SDKs (1)"
    ),
    "نقاط البيع POS (1)": (
        "POS Agents (1)",
        "Kassa/POS Agents (1)"
    ),
    "برنامج سطح مكتب محاسبي وضريبي مستقل يعمل بدون إنترنت (Offline-First) لحساب ضريبة القيمة المضافة BTW/VAT 21% وتوليد إقرارات XML لمصلحة الضرائب الهولندية والخليجية.": (
        "Standalone desktop accounting & tax engine (Offline-First) calculating 21% Dutch BTW and generating validated XML filings for the Belastingdienst and GCC tax authorities.",
        "Zelfstandige desktop boekhoud- en belastingengine (Offline-First) voor het berekenen van 21% BTW en het genereren van gevalideerde XML-aangiftes voor de Belastingdienst en GCC autoriteiten."
    ),
    "برنامج سطح مكتب مستقل يعمل بدون إنترنت (Offline-First) لحساب ضريبة القيمة المضافة BTW/VAT 21% وتوليد إقرارات XML لمصلحة الضرائب الهولندية والخليجية.": (
        "Standalone desktop application (Offline-First) calculating 21% Dutch BTW and generating validated XML filings for the Belastingdienst and GCC tax authorities.",
        "Zelfstandige desktopapplicatie (Offline-First) voor het berekenen van 21% BTW en het genereren van gevalideerde XML-aangiftes voor de Belastingdienst en GCC autoriteiten."
    ),
    "برنامج سطح مكتب محاسبي وضريبي متكامل يعمل بدون اتصال بالإنترنت.": (
        "Fully integrated offline-first accounting and tax desktop software.",
        "Volledig geïntegreerde offline-first desktopsoftware voor boekhouding en belastingen."
    ),
    "تطبيق هاتف ذكي للمسح الضوئي الذكي للإيصالات والفواتير الورقية بالكاميرا واستخراج بيانات الضريبة والمبالغ آلياً وترحيلها لحظياً للـ ERP.": (
        "Enterprise smartphone app for high-precision OCR scanning of paper receipts and invoices, extracting tax telemetry and syncing in real time with CoreSync ERP.",
        "Zakelijke smartphone-app voor zeer nauwkeurige OCR-scanning van papieren bonnen en facturen, directe gegevensextractie en realtime synchronisatie met CoreSync ERP."
    ),
    "مكتبة برمجية للمطورين والشركات البرمجية لدمج خوارزميات الذكاء الاصطناعي المالي والفوترة والامتثال المحاسبي في تطبيقاتهم الخاصة بسهولة عبر REST APIs.": (
        "Developer SDK for software engineers to embed financial AI algorithms, e-invoicing, and accounting compliance directly into custom applications via REST APIs.",
        "Developer SDK voor softwareontwikkelaars om financiële AI-algoritmen, e-facturatie en fiscale compliance direct in maatwerkapplicaties te integreren via REST APIs."
    ),
    "وسيط برمجي خفيف يعمل في خلفية أجهزة الكاشير القديمة لربطها فورياً بنظام الـ ERP السحابي لمزامنة حركة المخازن والسيولة دون تغيير الأجهزة.": (
        "Lightweight bridge daemon running in the background of legacy POS terminals, synchronizing store sales and cash registers with CoreSync Cloud ERP without replacing hardware.",
        "Lichtgewicht achtergronddaemon voor bestaande POS-kassasystemen, die winkelverkopen en kassa's realtime koppelt aan CoreSync Cloud ERP zonder hardwarevervanging."
    ),
    "برمجية تشفير وحماية النسخ الاحتياطية لقواعد البيانات والمستندات الحساسة بمعيار AES-256 العسكري مع تخزين متوافق 100% مع قانون GDPR الأوروبي.": (
        "Enterprise backup encryption software securing sensitive financial ledgers with military-grade AES-256 encryption and 100% GDPR-compliant immutable storage.",
        "Encryptiesoftware voor back-ups van financiële grootboeken met militaire AES-256 versleuteling en 100% AVG/GDPR-conforme onveranderlijke opslag."
    ),
    "تراخيص رقمية فورية وتنزيل مباشر": (
        "Instant digital licenses & direct installer packages",
        "Directe digitale licenties & installatiebestanden"
    ),
    "تشفير البيانات محلياً على جهازك دون اتصال": (
        "Local on-device data encryption with zero cloud leakage",
        "Lokale apparaatversleuteling zonder cloudlekken"
    ),
    "تصدير آلي لتقارير BTW والمحاسبة بضغطة زر": (
        "Automated 1-click export of BTW and accounting reports",
        "1-klik export van BTW- en boekhoudrapportages"
    ),
    "طباعة فواتير رسمية وتوافق مع EN 16931": (
        "Official invoice printing fully compliant with EN 16931",
        "Officiële facturen conform EN 16931 afdrukken"
    ),
    "اختيار نسبة VAT / BTW للحاسبة السريعة": (
        "Select VAT / BTW rate for quick calculator",
        "Selecteer BTW-tarief voor snelle calculator"
    ),
    "BTW هولندي 21%": (
        "Dutch BTW 21%",
        "Nederlandse BTW 21%"
    ),
    "BTW مخفض 9%": (
        "Reduced BTW 9%",
        "Verlaagde BTW 9%"
    ),
    "ضريبة خليجية 15%": (
        "GCC VAT 15%",
        "GCC Btw 15%"
    ),
    "📋 نسخ": (
        "📋 Copy",
        "📋 Kopiëren"
    ),
    "ترخيص سنوي / جهاز": (
        "Annual license / workstation",
        "Jaarlicentie / werkstation"
    ),
    "محاكي حي ⚡": (
        "Live Sandbox ⚡",
        "Live Sandbox ⚡"
    ),
    "محاكاة حية فورية داخل المتصفح": (
        "Live in-browser simulation sandbox",
        "Interactieve sandbox in browser"
    ),
    "تجربة 14 يوماً": (
        "14-Day Trial",
        "14-Dagen Proefversie"
    ),
    "نشط 14 يوماً": (
        "Active 14 Days",
        "14 Dagen Actief"
    ),
    "التوافق: Windows 11/10 (64-bit), macOS 13+": (
        "Compatibility: Windows 11/10 (64-bit), macOS 13+",
        "Compatibiliteit: Windows 11/10 (64-bit), macOS 13+"
    ),
    "توقيع رقمي: SHA-256 Validated": (
        "Digital Signature: SHA-256 Validated",
        "Digitale Handtekening: SHA-256 Validated"
    ),
    "شراء الترخيص الآن (€ 189 / سنة)": (
        "Purchase Commercial License Now (€ 189 / yr)",
        "Commerciële Licentie Nu Aanschaffen (€ 189 / jaar)"
    ),
    "ترخيص تجاري مؤسسي سنوي • Commercial B2B": (
        "Annual Corporate License • Commercial B2B",
        "Jaarlijkse Bedrijfslicentie • Zakelijk B2B"
    ),
    "هولندا وأوروبا": (
        "Netherlands & EU",
        "Nederland & EU"
    ),
    "اختر البنك الهولندي (Kies uw bank):": (
        "Select your Dutch Bank (Kies uw bank):",
        "Kies uw Nederlandse Bank:"
    ),
    "رقم البطاقة الائتمانية": (
        "Card Number",
        "Kaartnummer"
    ),
    "تاريخ الانتهاء:": (
        "Expiry Date:",
        "Vervaldatum:"
    ),
    "رمز الأمان CVC": (
        "CVC Security Code",
        "CVC Beveiligingscode"
    ),
    "رقم الآيبان للشركة (IBAN)": (
        "Business IBAN",
        "Zakelijk IBAN"
    ),
    "رقم الآيبان للشركة": (
        "Business IBAN",
        "Zakelijk IBAN"
    ),
    "اسم الحساب التجاري": (
        "Business Account Name",
        "Zakelijke Rekeningnaam"
    ),
    "اسم الشركة": (
        "Company Name",
        "Bedrijfsnaam"
    ),
    "تم نسخ مفتاح الترخيص!": (
        "License key copied!",
        "Licentiesleutel gekopieerd!"
    ),
    "Close الجولة": (
        "Close Tour",
        "Rondleiding Sluiten"
    ),
    "ذكاء اصطناعي OCR": (
        "AI OCR Engine",
        "AI OCR Engine"
    ),
    "معالجة OCR فائقة السرعة بدقة 99.4%": (
        "Ultra-fast OCR processing with 99.4% precision",
        "Ultrasnelle OCR-verwerking met 99,4% precisie"
    ),
    "فرز تلقائي لمصاريف الوقود، الضيافة، والتشغيل": (
        "Automated categorization of operational & overhead costs",
        "Automatische categorisering van operationele kosten"
    ),
    "مزامنة فورية سحابية مع لوحة تحكم الشركة": (
        "Real-time cloud sync with corporate executive dashboard",
        "Realtime cloudsynchronisatie met executive dashboard"
    ),
    "شهرياً / مستخدم": (
        "monthly / user",
        "per maand / gebruiker"
    ),
    "تجربة مجانية": (
        "Free Trial",
        "Gratis Proefversie"
    ),
    "اشتراك": (
        "Subscribe",
        "Abonneren"
    ),
    "ربط نقاط البيع POS": (
        "POS Cashier Bridge",
        "Kassa / POS Koppeling"
    ),
    "تكامل فوري مع أجهزة طابعات الفواتير والباركود": (
        "Instant integration with thermal receipt printers & scanners",
        "Directe integratie met bonprinters en barcodescanners"
    ),
    "مزامنة مبيعات أوفلاين عند انقطاع الإنترنت": (
        "Offline-resilient sales caching during network outages",
        "Offline-bestendige verkoopcaching bij netwerkuitval"
    ),
    "حماية وأمان معزول للأرصدة النقدية": (
        "Isolated ledger protection for cash registers",
        "Beveiligde grootboekbescherming voor kassa's"
    ),
    "شهرياً / نقطة بيع": (
        "monthly / terminal",
        "per maand / kassa"
    ),
    "تفعيل": (
        "Activate",
        "Activeren"
    ),
    "حماية ونسخ احتياطي": (
        "Encrypted Backup Vault",
        "Versleutelde Back-upkluis"
    ),
    "تخزين معزول في خوادم أمستردام المشفرة": (
        "Isolated encrypted storage in Amsterdam Tier-4 nodes",
        "Geïsoleerde versleutelde opslag in Amsterdamse Tier-4 datacenters"
    ),
    "استعادة كاملة لقواعد بيانات الـ ERP في ثوانٍ": (
        "Sub-second zero-loss recovery of ERP databases",
        "Herstel van complete ERP-databases binnen seconden"
    ),
    "تقارير امتثال وجاهزية للتدقيق القانوني": (
        "Audit-ready compliance and chain-of-custody logs",
        "Audit-ready nalevingsrapportages en forensische logs"
    ),
    "شهرياً (1TB Encrypted)": (
        "monthly (1TB Encrypted)",
        "per maand (1TB Versleuteld)"
    ),
    "للمطورين والشركات": (
        "Developer SDK & API",
        "Developer SDK & API"
    ),
    "توثيق تفاعلي كامل وكود تشغيل جاهز": (
        "Comprehensive interactive docs with production-ready snippets",
        "Complete interactieve documentatie en kant-en-klare code"
    ),
    "توليد فوري لمفاتيح الـ API مع Rate Limiting": (
        "Instant API key provisioning with enterprise rate limiting",
        "Directe API-sleutelaanmaak met enterprise rate limiting"
    ),
    "تحديثات دورية متوافقة مع القوانين المالية": (
        "Automated regulatory updates aligned with tax directives",
        "Regelmatige updates conform actuele belastingwetgeving"
    ),
    "شهرياً (50k Calls)": (
        "monthly (50k calls)",
        "per maand (50k calls)"
    ),
    "تحميل الـ SDK": (
        "Download SDK",
        "SDK Downloaden"
    ),
    "طلب الترخيص": (
        "Request License",
        "Licentie Aanvragen"
    ),
    "الأكثر طلباً للمحاسبين ★": (
        "Accountants' Top Pick ★",
        "Meest Gekozen door Boekhouders ★"
    ),
    "جديد مُضاف بواسطة المؤسس ★": (
        "New Founder Release ★",
        "Nieuwe Oprichtersrelease ★"
    ),
    "تجربة الربط": (
        "Test Integration",
        "Integratie Testen"
    ),
    "تنزيل حزمة التثبيت": (
        "Download Package",
        "Installatiepakket Downloaden"
    ),
    "شراء الترخيص": (
        "Purchase License",
        "Licentie Aanschaffen"
    ),
    "Purchase License": (
        "Purchase License",
        "Licentie Aanschaffen"
    ),
    "Purchase License وإصدار فاتورة": (
        "Purchase License & Issue Invoice",
        "Licentie Aanschaffen & Factuur Ontvangen"
    ),
    "ترقية للنسخة الكاملة (€ 189)": (
        "Upgrade to Full License (€ 189)",
        "Upgrade naar Volledige Licentie (€ 189)"
    ),
    "تنزيل حزمة التثبيت المباشرة (Installer .zip)": (
        "Download Verified Installer (.zip)",
        "Geverifieerde Installer Downloaden (.zip)"
    ),
    "تأكيد الدفع الآمن وإصدار الفاتورة (€ 228.69)": (
        "Confirm Secure Checkout & Issue Invoice (€ 228.69)",
        "Bevestig Veilige Betaling & Facturatie (€ 228.69)"
    ),
    "حاسبة ضريبة فورية:": (
        "Quick Tax Calculator:",
        "Snelle BTW Calculator:"
    ),
    "أدخل المبلغ الصافي": (
        "Enter net amount",
        "Voer nettobedrag in"
    ),
    "قيمة الضريبة:": (
        "Tax Amount:",
        "BTW Bedrag:"
    ),
    "الإجمالي مع الضريبة:": (
        "Total with Tax:",
        "Totaal incl. BTW:"
    ),
    "مفتاح تجريبي فوري (14 يوماً):": (
        "Instant 14-Day Trial Key:",
        "Directe 14-Dagen Proeflicentie:"
    ),
    "توليد مفتاح جديد": (
        "Generate New Key",
        "Nieuwe Sleutel Genereren"
    ),
    "نسخ المفتاح": (
        "Copy Key",
        "Sleutel Kopiëren"
    ),
    "هل ترغب في برمجة ونشر برنامجك التجاري الخاص عبر المنصة؟": (
        "Looking to engineer and distribute your proprietary software on our platform?",
        "Wilt u uw eigen commerciële software ontwikkelen en distribueren via ons platform?"
    ),
    "توفر شركة S&R CoreSync Solutions بنية متكاملة للمطورين لتوزيع البرمجيات مع نظام التراخيص الرقمية المشفرة وبوابات الدفع الهولندية والأوروبية والخليجية.": (
        "S&R CoreSync Solutions offers an enterprise distribution rail featuring encrypted license keys, multi-currency payment gateways, and automated revenue share.",
        "S&R CoreSync Solutions biedt een complete distributie-infrastructuur met versleutelde licenties, Europese en GCC betaalkoppelingen en geautomatiseerde facturatie."
    ),
    "إضافة برنامج جديد الآن": (
        "Publish Enterprise Software Now",
        "Zakelijke Software Nu Publiceren"
    ),

    # Section 5: AI Financial Copilot
    "المساعد المالي والتحليلي بالذكاء الاصطناعي": (
        "Autonomous AI Financial Copilot & Strategic Advisor",
        "Autonome AI Financiële Copilot & Strategisch Adviseur"
    ),
    "توليد تقارير مالية وتنبؤات استراتيجية فورية مبنية على بيانات مؤسستك الحية": (
        "Generates instant financial telemetry, automated audit insights, and cash flow forecasting from live corporate ledgers",
        "Genereert directe financiële telemetrie, geautomatiseerde auditinzichten en cashflowprognoses uit live bedrijfsgegevens"
    ),
    "مرحباً بك! أنا المساعد المالي الذكي لنظام S&R CoreSync. قمت للتو بمراجعة كافة حركات التدفق النقدي ومطابقة فواتير الشهر الحالي. كيف يمكنني مساعدتك اليوم؟": (
        "Welcome! I am your S&R CoreSync Autonomous Financial Copilot. I have just completed real-time ledger reconciliation and verified this month's cash flow against EU tax standards. How can I assist your operations today?",
        "Welkom! Ik ben uw S&R CoreSync Autonome Financiële Copilot. Ik heb zojuist de grootboekafstemming voltooid en de cashflow gecontroleerd conform de Europese belastingnormen. Hoe kan ik uw organisatie vandaag ondersteunen?"
    ),
    "مدرب على المعايير المحاسبية الدولية IFRS": (
        "Trained on International Financial Reporting Standards (IFRS)",
        "Getraind op International Financial Reporting Standards (IFRS)"
    ),
    "حلل التدفق المالي لشهر أكتوبر وأخبرني بهامش الأرباح المتوقع": (
        "Analyze October cash flow and projected profit margin",
        "Analyseer de cashflow van oktober en de verwachte winstmarge"
    ),
    "ما هي الفواتير المعلقة التي تتجاوز مدتها 15 يوماً؟": (
        "Which pending invoices are nearing maturity?",
        "Welke openstaande facturen naderen de vervaldatum?"
    ),
    "قدم لي نصيحة لتحسين كفاءة إدارة المخزون وفق بيانات الأسبوع الماضي": (
        "Provide recommendations to optimize inventory holding costs based on last week's telemetry",
        "Geef advies om de voorraadkosten te optimaliseren op basis van recente gegevens"
    ),
    "📊 تحليل التدفق المالي لشهر أكتوبر": (
        "📊 October Cash Flow Telemetry Analysis",
        "📊 Cashflow- en Liquiditeitsanalyse Oktober"
    ),
    "⏳ الفواتير المتأخرة والتحصيل": (
        "⏳ Overdue Invoices & Collection Strategy",
        "⏳ Openstaande Facturen & Incassostrategie"
    ),
    "⏳ الفواتير المتأخرة": (
        "⏳ Overdue Invoices",
        "⏳ Openstaande Facturen"
    ),
    "💡 تحسين تكاليف التخزين": (
        "💡 Warehouse Holding Cost Optimization",
        "💡 Magazijn- en Opslagkosten Optimalisatie"
    ),
    "اكتب استفسارك المالي أو التقني هنا...": (
        "Type your financial or operational inquiry here...",
        "Typ hier uw financiële of operationele vraag..."
    ),
    "إرسال للاستفسار": (
        "Submit Inquiry",
        "Verstuur Vraag"
    ),
    "إرسال": (
        "Send",
        "Versturen"
    ),

    # Section 6: Cloud Infrastructure
    "حالة البنية التحتية السحابية (Cloud Nodes)": (
        "Cloud Infrastructure & Distributed Nodes Telemetry",
        "Cloud Infrastructuur & Gedistribueerde Nodes Telemetrie"
    ),
    "مراقبة لحظية للخوادم الموزعة في أمستردام وفرانكفورت والرياض مع نسخ احتياطي فوري": (
        "Live monitoring across high-availability clusters in Amsterdam (Primary NL), Frankfurt (Backup DE), and Riyadh (GCC Hub)",
        "Live monitoring van clusters met hoge beschikbaarheid in Amsterdam (Primair NL), Frankfurt (Back-up DE) en Riyad (GCC Hub)"
    ),
    "عقدة أمستردام الرئيسية (NL)": (
        "Amsterdam Primary Node (NL Central)",
        "Amsterdam Primaire Node (NL Centraal)"
    ),
    "خوادم الإنتاج والفوترة الأوروبية": (
        "Production & European E-Invoicing Rails",
        "Productie & Europese E-Facturatie Knooppunt"
    ),
    "زمن الاستجابة: 12ms (فائق السرعة)": (
        "Latency: 12ms (Ultra-Low Latency)",
        "Responstijd: 12ms (Ultra-Laag)"
    ),
    "عقدة فرانكفورت الاحتياطية (DE)": (
        "Frankfurt Redundancy Node (DE Core)",
        "Frankfurt Redundantie Node (DE Kern)"
    ),
    "النسخ الاحتياطي السحابي المشفر": (
        "Encrypted Failover & Disaster Recovery",
        "Versleutelde Failover & Herstelcluster"
    ),
    "بوابة الشرق الأوسط السحابية (KSA)": (
        "Middle East Gateway Node (KSA Riyadh)",
        "Midden-Oosten Gateway Node (KSA Riyad)"
    ),
    "مطابقة أنظمة هيئة الزكاة والضريبة": (
        "GCC Low-Latency Hub & ZATCA Gateway",
        "GCC Low-Latency Hub & ZATCA Gateway"
    ),
    "تعتمد منصة S&R CoreSync على بنية تحتية سحابية هجينة تضمن عزل بيانات كل عميل في قواعد بيانات مشفرة مستقلة، مع شهادات التوافق مع اللائحة العامة لحماية البيانات في الاتحاد الأوروبي (GDPR) وأنظمة الأمن السيبراني المصرفية.": (
        "S&R CoreSync operates on a dedicated hybrid architecture guaranteeing tenant isolation with independent AES-256 encrypted databases, certified compliance with EU GDPR, and Tier-4 banking-grade cybersecurity.",
        "S&R CoreSync opereert op een dedicated hybride architectuur die strikte tenantisolatie garandeert met onafhankelijke AES-256 versleutelde databases, gecertificeerde naleving van de AVG/GDPR en bancaire Tier-4 beveiliging."
    ),
    "نسخ متزامن ومشفّر AES-256": (
        "Synchronous AES-256 encrypted replication",
        "Synchrone AES-256 versleutelde replicatie"
    ),
    "تكامل محلي سريع مع البنوك": (
        "Low-latency local bank rails",
        "Snelle lokale bankkoppelingen"
    ),
    "معايير الأمان والحماية المؤسسية": (
        "Enterprise Security & Compliance Standards",
        "Enterprise Beveiligings- & Compliancestandaarden"
    ),

    # Section 7: White-Label Studio
    "محرك العلامة البيضاء وتخصيص هوية العميل (White-Label Studio)": (
        "White-Label Customization Engine & Identity Studio",
        "White-Label Personalisatie & Merkidentiteit Studio"
    ),
    "شاهد كيف تتحول لوحة تحكم الـ ERP السحابية فورياً لتلائم هوية شركتك وشعارك وألوانك المؤسسية": (
        "Experience instantaneous re-branding of the entire Cloud ERP portal to match your corporate brand, logo, and luxury palette",
        "Ervaar directe herpositionering van het complete Cloud ERP-portaal naar uw eigen huisstijl, logo en zakelijke kleurenpalet"
    ),
    "1. اختيار السمة اللونية الفاخرة (Theme Presets)": (
        "1. Executive Theme Presets",
        "1. Executive Kleurenthema's"
    ),
    "انقر على أي سمة لمشاهدة تحول ألوان الأزرار والمخططات والإضاءات فوراً:": (
        "Click any theme preset to see dynamic UI accents, charts, and lighting transform instantly:",
        "Klik op een thema om UI-accenten, grafieken en sfeerverlichting direct te transformeren:"
    ),
    "الذهب الملكي (Royal Gold)": (
        "Royal Gold (Default Prestige)",
        "Koninklijk Goud (Prestige)"
    ),
    "التيتانيوم السيبراني (Titanium Cyan)": (
        "Titanium Cyan (Tech Innovation)",
        "Titanium Cyaan (Tech Innovatie)"
    ),
    "الزمرد المالي (Fintech Emerald)": (
        "Fintech Emerald (Banking & Trust)",
        "Fintech Smaragd (Financiële Zekerheid)"
    ),
    "الياقوت الإمبراطوري (Imperial Violet)": (
        "Imperial Violet (Luxury Enterprise)",
        "Keizerlijk Violet (Luxe Onderneming)"
    ),
    "الهوية الرسمية المعتمدة لـ S&R CoreSync": (
        "Official default identity of S&R CoreSync",
        "Officiële standaardidentiteit van S&R CoreSync"
    ),
    "لشركات التقنية السحابية وهندسة البيانات": (
        "For cloud software & data engineering firms",
        "Voor cloudsoftware- & databedrijven"
    ),
    "للبنوك والمؤسسات المالية وحلول الامتثال": (
        "For fintechs, banking, and compliance firms",
        "Voor fintech, banken en compliancebedrijven"
    ),
    "لشركات الذكاء الاصطناعي والابتكار الرقمي": (
        "For enterprise AI & digital scale-ups",
        "Voor enterprise AI & digitale innovators"
    ),
    "● محفوظ في المتصفح": (
        "● Saved in browser",
        "● Opgeslagen in browser"
    ),
    "2. تطبيق اسم وشعار شركتك (Client Custom Brand)": (
        "2. Client Custom Enterprise Branding & Emblem",
        "2. Klantspecifieke Bedrijfsidentiteit & Logo"
    ),
    "أدخل اسم مؤسستك أو ارفع شعارك لمعاينة نظام الـ ERP باسمك:": (
        "Enter your enterprise name or upload your emblem to preview the ERP system under your custom brand:",
        "Voer uw bedrijfsnaam in of upload uw logo om het ERP-systeem onder uw eigen merk te testen:"
    ),
    "اسم شركتك أو مؤسستك:": (
        "Enterprise Legal Name:",
        "Officiële Bedrijfsnaam:"
    ),
    "اسم شركتك": (
        "Your Company Name",
        "Uw Bedrijfsnaam"
    ),
    "اسم الشركة": (
        "Company Name",
        "Bedrijfsnaam"
    ),
    "أدخل اسم شركة العميل...": (
        "Enter client enterprise name...",
        "Voer bedrijfsnaam in..."
    ),
    "شعار الشركة (اختياري - PNG / SVG / JPG):": (
        "Company Emblem (PNG / SVG / JPG):",
        "Bedrijfslogo (PNG / SVG / JPG):"
    ),
    "تطبيق الهوية فوراً على المنصة بالكامل": (
        "Apply Custom Brand to Platform",
        "Huisstijl Direct Toepassen op Portaal"
    ),
    "استعادة هوية S&R الأصلية": (
        "Restore Default S&R Identity",
        "Standaard S&R Huisstijl Herstellen"
    ),
    "أو اختر نموذجاً جاهزاً سريعاً:": (
        "Or choose a pre-configured enterprise profile:",
        "Of kies een voorgeconfigureerd bedrijfsprofiel:"
    ),
    "مجموعة الرياض للخدمات اللوجستية": (
        "Riyadh Logistics Group BV",
        "Riyadh Logistics Group BV"
    ),
    "مجموعة الرياض 🇸🇦": (
        "Riyadh Group 🇸🇦",
        "Riyad Groep 🇸🇦"
    ),
    "بنك التقنية الحديثة": (
        "Modern Tech Bank BV",
        "Moderne Tech Bank BV"
    ),
    "بنك التقنية 🏦": (
        "Tech Bank 🏦",
        "Tech Bank 🏦"
    ),
    "سلسلة مطاعم راقية (أمستردام)": (
        "Amsterdam Fine Dining Hospitality Group",
        "Amsterdam Fine Dining Hospitality Group"
    ),
    "شركة الاستشارات المالية (فرانكفورت)": (
        "Frankfurt Capital Financial Advisory",
        "Frankfurt Capital Financial Advisory"
    ),
    "توليد ومعاينة فاتورة تجريبية رسمية بهوية شركتك (Branded Invoice PDF)": (
        "Preview Official Branded Invoice with Your Enterprise Emblem",
        "Officiële Factuur met Uw Bedrijfsidentiteit Bekijken"
    ),
    "يمكن لشركة S&R CoreSync Solutions تخصيص نظام الـ ERP ونظام الفوترة والمحاسبة الذكية بالكامل تحت علامتك التجارية (White-Label Deployment) على نطاقك الخاص (yourcompany.com) مع خوادم معزولة بالكامل.": (
        "S&R CoreSync Solutions delivers turnkey white-label enterprise deployments on your custom domain (e.g. portal.yourcompany.com) with dedicated sovereign database clusters and complete brand isolation.",
        "S&R CoreSync Solutions levert kant-en-klare white-label implementaties op uw eigen domein (bijv. portaal.uwbedrijf.nl) met dedicated soevereine databases en volledige merkisolatie."
    ),
    "جاهز لإطلاق نسختك الخاصة من النظام؟": (
        "Ready to deploy your sovereign enterprise ERP instance?",
        "Klaar om uw eigen soevereine ERP-omgeving te lanceren?"
    ),
    "طلب عرض سعر لنظام White-Label مخصص": (
        "Request White-Label Proposal",
        "Offerte voor White-Label Aanvragen"
    ),

    # Modals & Interactions
    "Record Test Transaction في الـ ERP": (
        "Record Test Transaction in ERP",
        "Registreer Testtransactie in ERP"
    ),
    "تسجيل معاملة تجريبية في الـ ERP": (
        "Record Test Transaction in ERP",
        "Registreer Testtransactie in ERP"
    ),
    "تسجيل معاملة تجريبية جديدة": (
        "Record New Ledger Transaction",
        "Nieuwe Grootboektransactie Registreren"
    ),
    "أدخل بيانات المعاملة لاختبار المزامنة اللحظية في الرسم البياني والجدول": (
        "Enter transaction details to simulate real-time ledger synchronization across charts and tables",
        "Voer transactiegegevens in om realtime synchronisatie in grafieken en tabellen te testen"
    ),
    "اسم الجهة أو العميل:": (
        "Client / Counterparty Name:",
        "Klant- / Tegenpartijnaam:"
    ),
    "اسم الجهة أو العميل": (
        "Client / Counterparty Name",
        "Klant- / Tegenpartijnaam"
    ),
    "شركة تجارية هولندية جديدة": (
        "Dutch Commercial Enterprise BV",
        "Nederlandse Handelsonderneming BV"
    ),
    "المبلغ باليورو (€):": (
        "Amount in EUR (€):",
        "Bedrag in EUR (€):"
    ),
    "Amount باليورو (€)": (
        "Amount in EUR (€)",
        "Bedrag in EUR (€)"
    ),
    "Amount باليورو": (
        "Amount in EUR",
        "Bedrag in EUR"
    ),
    "المبلغ باليورو": (
        "Amount in EUR",
        "Bedrag in EUR"
    ),
    "المبلغ (€):": (
        "Amount (€):",
        "Bedrag (€):"
    ),
    "نوع المعاملة:": (
        "Transaction Type:",
        "Transactietype:"
    ),
    "نوع الخدمة": (
        "Service Category",
        "Dienstencategorie"
    ),
    "ربط وتكامل ERP": (
        "ERP Integration & Architecture",
        "ERP Integratie & Architectuur"
    ),
    "تطوير برمجيات سحابية": (
        "Cloud Software Engineering",
        "Cloudsoftware Ontwikkeling"
    ),
    "استشارات مالية وحوكمة": (
        "Financial Advisory & Governance",
        "Financieel Advies & Governance"
    ),
    "إيراد مبيعات برمجيات": (
        "Software License Revenue",
        "Softwarelicentie Omzet"
    ),
    "خدمات استشارية وحوكمة": (
        "Consulting & Governance Services",
        "Consultancy & Governance Diensten"
    ),
    "اشتراك سحابي ERP": (
        "Cloud ERP SaaS Subscription",
        "Cloud ERP SaaS Abonnement"
    ),
    "حفظ ومزامنة فورية": (
        "Save & Instant Sync",
        "Opslaan & Direct Synchroniseren"
    ),
    "حفظ وإدراج في السجلات": (
        "Save & Post to Ledger",
        "Opslaan & Boeken in Grootboek"
    ),
    "إلغاء": (
        "Cancel",
        "Annuleren"
    ),

    # Invoice Generator Modal
    "إنشاء وتوليد فاتورة إلكترونية": (
        "Generate Compliant E-Invoice",
        "Conforme E-Factuur Aanmaken"
    ),
    "توليد فاتورة إلكترونية معتمدة": (
        "Generate Certified E-Invoice",
        "Gecertificeerde E-Factuur Aanmaken"
    ),
    "أدخل بيانات الفاتورة لتوليدها وتشفيرها بنظام UBL 2.1 الأوروبي المعتمد": (
        "Enter invoice telemetry to generate certified, encrypted European UBL 2.1 XML documents",
        "Voer factuurgegevens in om gecertificeerde, versleutelde Europese UBL 2.1 XML-documenten te genereren"
    ),
    "اسم العميل أو المؤسسة:": (
        "Client / Enterprise Name:",
        "Klant- of Bedrijfsnaam:"
    ),
    "اسم العميل / الشركة": (
        "Client / Enterprise Name",
        "Klant- of Bedrijfsnaam"
    ),
    "اسم العميل": (
        "Client Name",
        "Klantnaam"
    ),
    "المبلغ الصافي (€):": (
        "Net Amount (€):",
        "Nettobedrag (€):"
    ),
    "Amount الصافي (€)": (
        "Net Amount (€)",
        "Nettobedrag (€)"
    ),
    "Amount الصافي": (
        "Net Amount",
        "Nettobedrag"
    ),
    "المبلغ الصافي (€)": (
        "Net Amount (€)",
        "Nettobedrag (€)"
    ),
    "المبلغ الصافي": (
        "Net Amount",
        "Nettobedrag"
    ),
    "نسبة الضريبة (BTW / VAT):": (
        "VAT Rate (BTW / Belasting):",
        "BTW-tarief (BTW / Belasting):"
    ),
    "النظام الضريبي والامتثال": (
        "Tax Regime & Compliance",
        "Belastingstelsel & Naleving"
    ),
    "النظام الضريبي": (
        "Tax Regime",
        "Belastingstelsel"
    ),
    "ضريبة القيمة المضافة بهولندا (BTW 21%)": (
        "Netherlands Standard VAT (BTW 21%)",
        "Nederlandse Omzetbelasting (BTW 21%)"
    ),
    "إعفاء ضريبي أوروبي (Reverse Charge 0%)": (
        "EU Reverse Charge (Intra-Community 0%)",
        "BTW Verlegd (Intra-Communautair 0%)"
    ),
    "ضريبة القيمة المضافة السعودية (ZATCA 15%)": (
        "Saudi Arabia VAT (ZATCA 15%)",
        "Saoedische Btw (ZATCA 15%)"
    ),
    "BTW 21% (هولندي قياسي)": (
        "BTW 21% (Standard Dutch)",
        "BTW 21% (Standaard Nederlands)"
    ),
    "BTW 9% (هولندي مخفض)": (
        "BTW 9% (Reduced Dutch)",
        "BTW 9% (Verlaagd Nederlands)"
    ),
    "Reverse Charge 0% (أوروبي معفى)": (
        "Reverse Charge 0% (Intra-Community EU)",
        "BTW Verlegd 0% (Intra-Communautair EU)"
    ),
    "ZATCA 15% (ضريبة سعودية)": (
        "ZATCA 15% (GCC Saudi VAT)",
        "ZATCA 15% (GCC Saoedische Btw)"
    ),
    "وصف الخدمة أو المنتجات:": (
        "Line Item Description:",
        "Omschrijving Dienst of Goederen:"
    ),
    "إصدار الفاتورة وتوليد QR": (
        "Issue Invoice & Generate QR",
        "Factuur Uitgeven & QR Genereren"
    ),

    # iDEAL Simulator Modal
    "محاكي بوابات الدفع iDEAL": (
        "iDEAL Instant Payment Simulator",
        "iDEAL Directe Betaalsimulator"
    ),
    "محاكي الدفع الفوري iDEAL الهولندي": (
        "Dutch iDEAL Instant Payment Simulator",
        "Nederlandse iDEAL Directe Betaalsimulator"
    ),
    "الفاتورة المستهدفة:": (
        "Target Invoice No:",
        "Doelfactuurnummer:"
    ),
    "الجهة المسددة:": (
        "Payer Account:",
        "Betalende Partij:"
    ),
    "Amount Grand Total المطلوب:": (
        "Total Amount Due:",
        "Totaal Te Betalen Bedrag:"
    ),
    "Total Amount المطلوب:": (
        "Total Amount Due:",
        "Totaal Te Betalen Bedrag:"
    ),
    "المبلغ الإجمالي المطلوب:": (
        "Total Amount Due:",
        "Totaal Te Betalen Bedrag:"
    ),
    "الإجمالي المستحق للسداد:": (
        "Total Amount Due:",
        "Totaal Te Betalen:"
    ),
    "جاهز لتنفيذ أمر التحويل الفوري": (
        "Ready to execute instant transfer via SEPA Instant",
        "Gereed voor directe overboeking via SEPA Instant"
    ),
    "تأكيد السداد التجريبي اللحظي": (
        "Confirm Instant Demo Settlement",
        "Bevestig Directe Testbetaling"
    ),
    "اختر البنك الهولندي (Dutch Banking Partner):": (
        "Select Dutch Banking Partner (iDEAL 2.0):",
        "Kies uw Nederlandse Bank (iDEAL 2.0):"
    ),
    "اختر البنك الهولندي لمحاكاة تسوية الفاتورة اللحظية في حساب الشركة": (
        "Select your preferred Dutch bank to simulate instantaneous ledger reconciliation in your corporate account",
        "Selecteer uw Nederlandse bank om directe factuurafstemming op uw zakelijke rekening te simuleren"
    ),
    "اختر البنك واضغط على تأكيد السداد الفوري": (
        "Select your bank and click Confirm Instant Payment",
        "Kies uw bank en klik op Bevestig Directe Betaling"
    ),
    "تأكيد السداد الفوري": (
        "Confirm Instant Payment",
        "Bevestig Directe Betaling"
    ),
    "جاري المعالجة البنكية...": (
        "Processing bank transaction...",
        "Banktransactie wordt verwerkt..."
    ),
    "الاتصال الآمن ببروتوكول iDEAL 2.0 وSEPA Instant...": (
        "Secure handshake via iDEAL 2.0 and SEPA Instant rails...",
        "Beveiligde verbinding via iDEAL 2.0 en SEPA Instant..."
    ),
    "تمت تسوية المبلغ وتحويله لحساب المؤسسة بنجاح!": (
        "Amount successfully settled and deposited into the corporate bank account!",
        "Bedrag succesvol verrekend en bijgeschreven op de zakelijke rekening!"
    ),
    "إغلاق النافذة": (
        "Close Window",
        "Venster Sluiten"
    ),

    # Invoice Document Preview Modal
    "فاتورة إلكترونية رسمية (e-Invoice)": (
        "Official E-Invoice (e-Factuur)",
        "Officiële E-Factuur (e-Factuur)"
    ),
    "إلى السيد/الشركة:": (
        "Bill To / Debtor:",
        "Factuur Aan / Debiteur:"
    ),
    "تاريخ الإصدار:": (
        "Issue Date:",
        "Factuurdatum:"
    ),
    "حالة السداد:": (
        "Payment Status:",
        "Betalingsstatus:"
    ),
    "الوصف": (
        "Description",
        "Omschrijving"
    ),
    "VAT / BTW المحتسبة": (
        "VAT / BTW Calculated",
        "Berekende BTW"
    ),
    "تكامل منظومة CoreSync Cloud ERP وحوكمة العمليات المالية": (
        "CoreSync Cloud ERP Deployment & Financial Governance Architecture",
        "CoreSync Cloud ERP Implementatie & Financiële Governance"
    ),
    "Grand Total المستحق والمقيد بالدفاتر:": (
        "Total Ledger Balance Due:",
        "Totaal Openstaand Saldo:"
    ),
    "طباعة الفاتورة": (
        "Print Invoice",
        "Factuur Afdrukken"
    ),
    "تم الإطلاع": (
        "Acknowledged",
        "Gelezen & Begrepen"
    ),
    "هوية مخصصة:": (
        "Custom Brand:",
        "Aangepast Merk:"
    ),
    "فاتورة معتمدة - جاهزة للتحصيل ✓": (
        "Certified Invoice - Ready for Collection ✓",
        "Gecertificeerde Factuur - Gereed voor Incasso ✓"
    ),

    # Presentation Bar & Tour
    "الخروج من العرض": (
        "Exit Presentation",
        "Presentatie Sluiten"
    ),
    "وضع Client View [P]": (
        "Client View [P]",
        "Klantpresentatie [P]"
    ),
    "لوحة القيادة والتدفق المالي": (
        "Executive Financial Dashboard",
        "Executive Financieel Dashboard"
    ),
    "هنا يظهر الأداء المالي اللحظي للشركة مع مؤشرات الإيرادات ونسب النمو بدقة متناهية.": (
        "Live corporate financial performance displayed with precision revenue metrics and growth indicators.",
        "Live bedrijfsprestaties weergegeven met nauwkeurige omzetstatistieken en groei-indicatoren."
    ),
    "تم تفعيل اختصارات لوحة المفاتيح لوضع العرض التقديمي": (
        "Keyboard shortcuts enabled: [P] Toggle Mode • [Esc] Exit",
        "Sneltoetsen actief: [P] Presentatiemodus • [Esc] Sluiten"
    ),
    "الخروج من وضع العرض [Esc]": (
        "Exit Presentation Mode [Esc]",
        "Presentatiemodus Verlaten [Esc]"
    ),

    # PDF Modal
    "ملخص العرض التنفيذي والجاهزية المؤسسية": (
        "Executive Enterprise Proposal & Architecture Dossier",
        "Executive Bedrijfsvoorstel & Architectuuroverzicht"
    ),
    "إعداد وتخصيص الملف التنفيذي إلى (Presented To):": (
        "Configure & Personalize Dossier For (Presented To):",
        "Configureer & Personaliseer Dossier Voor (Gepresenteerd Aan):"
    ),
    "اسم الجهة أو الشريك التجاري...": (
        "Enterprise or Partner Name...",
        "Bedrijfs- of Partnernaam..."
    ),
    "تحديث الاسم في التقرير": (
        "Update Name in Brief",
        "Naam Bijwerken in Document"
    ),
    "طباعة وتصدير كـ PDF": (
        "Print & Export PDF",
        "Afdrukken & Exporteren als PDF"
    ),
    "مخصص لشركة (Client Enterprise):": (
        "Prepared For (Client Enterprise):",
        "Voorbereid Voor (Klantonderneming):"
    ),
    "مجموعة الشريك التجاري المستهدف": (
        "Enterprise Client Partner Group",
        "Enterprise Partnerorganisatie"
    ),
    "التاريخ المرجعي للجلسة:": (
        "Session Reference Date:",
        "Referentiedatum Sessie:"
    ),
    "نظام الضريبة المطبق في الجلسة:": (
        "Applied Tax Regime:",
        "Toegepast Belastingstelsel:"
    ),
    "نظام VAT / BTW المطبق في الجلسة": (
        "Applied Tax Regime in Session",
        "Toegepast Belastingstelsel in Sessie"
    ),
    "نظام الضريبة المطبق في الجلسة": (
        "Applied Tax Regime in Session",
        "Toegepast Belastingstelsel in Sessie"
    ),
    "إجمالي الإيرادات السنوية التقديرية:": (
        "Estimated Annual Gross Revenue:",
        "Geschatte Bruto Jaaromzet:"
    ),
    "إجمالي الإيرادات السنوية التقديرية": (
        "Estimated Annual Gross Revenue",
        "Geschatte Bruto Jaaromzet"
    ),
    "Annual Gross Revenue التقديرية": (
        "Estimated Annual Gross Revenue",
        "Geschatte Bruto Jaaromzet"
    ),
    "التدفقات النقدية الصافية المحققة:": (
        "Realized Net Operating Cash Flow:",
        "Gerealiseerde Netto Cashflow:"
    ),
    "التدفقات النقدية الصافية المحققة": (
        "Realized Net Operating Cash Flow",
        "Gerealiseerde Netto Cashflow"
    ),
    "Net Operating Cash Flow المحققة": (
        "Realized Net Operating Cash Flow",
        "Gerealiseerde Netto Cashflow"
    ),
    "الضريبة المقدرة المحتسبة:": (
        "Estimated Tax Liability:",
        "Berekende Belastingverplichting:"
    ),
    "الضريبة المقدرة المحتسبة": (
        "Estimated Tax Liability",
        "Berekende Belastingverplichting"
    ),
    "VAT / BTW المقدرة المحتسبة": (
        "Estimated Tax Liability",
        "Berekende Belastingverplichting"
    ),
    "معايير الأمان والحماية المؤسسية:": (
        "Enterprise Security & Governance Standards:",
        "Beveiligings- & Governancestandaarden:"
    ),
    "تشفير AES-256 لقواعد البيانات وعزل تام لكل عميل": (
        "AES-256 encryption with full tenant database isolation",
        "AES-256 encryptie met volledige tenantisolatie"
    ),
    "توافق كامل مع اللائحة العامة لحماية البيانات في أوروبا (GDPR)": (
        "100% compliance with EU General Data Protection Regulation (GDPR)",
        "100% naleving van de Algemene Verordening Gegevensbescherming (AVG/GDPR)"
    ),
    "ربط محاسبي معتمد مع مصلحة الضرائب الهولندية (Digipoort SBR)": (
        "Certified accounting bridge to Dutch Tax Administration (Digipoort SBR)",
        "Gecertificeerde boekhoudkoppeling met de Belastingdienst (Digipoort SBR)"
    ),
    "حوكمة استشارية مباشرة بإشراف مؤسسي S&R CoreSync Solutions": (
        "Executive governance guided directly by the founders of S&R CoreSync Solutions",
        "Directe executive begeleiding onder toezicht van de oprichters van S&R CoreSync Solutions"
    ),
    "ينعكس الاسم المخصص تلقائياً على الوثيقة المطبوعة": (
        "Customized name reflects automatically across exported documents",
        "Aangepaste bedrijfsnaam wordt automatisch doorgevoerd op afdrukken"
    ),
    "عرض استشاري مخصص (Bespoke Enterprise Dossier)": (
        "Bespoke Enterprise Consulting Dossier",
        "Op Maat Gemaakt Zakelijk Consultdossier"
    ),
    "🌟 نظرة عامة على حلول S&R CoreSync": (
        "🌟 Overview of S&R CoreSync Solutions",
        "🌟 Overzicht van S&R CoreSync Oplossingen"
    ),
    "منظومة سحابية أوروبية موحدة تجمع بين معايير هندسة البرمجيات الهولندية (Compliant with Dutch Tax Administration AWR & EU GDPR) وسرعة البنية التحتية التوزيعية، متوافقة كلياً مع الفوترة الإلكترونية EN 16931 والربط المصرفي المباشر.": (
        "A unified European cloud ecosystem combining Dutch software engineering standards (Compliant with Dutch Tax Administration AWR & EU GDPR) with ultra-fast distributed infrastructure, fully aligned with EN 16931 e-invoicing and direct banking rails.",
        "Een uniform Europees cloud-ecosysteem dat Nederlandse software engineering normen (conform Belastingdienst AWR & EU AVG/GDPR) combineert met snelle infrastructuur, volledig conform EN 16931 e-facturatie en directe bankkoppelingen."
    ),
    "📊 ملخص المؤشرات المالية والضريبية المختارة (Live Simulation Snapshot):": (
        "📊 Selected Financial & Tax Indicators Summary (Live Simulation):",
        "📊 Samenvatting Geselecteerde Financiële & Fiscale Indicatoren (Live Simulatie):"
    ),
    "البند المالي": (
        "Financial Metric",
        "Financiële Post"
    ),
    "القيمة المعتمدة": (
        "Verified Telemetry",
        "Geverifieerde Waarde"
    ),
    "متحقق سحابياً (+18.4%)": (
        "Cloud Verified (+18.4%)",
        "Cloud Geverifieerd (+18,4%)"
    ),
    "هامش ربحية 9.2%": (
        "Operating Margin 9.2%",
        "Operationele Marge 9,2%"
    ),
    "متوافق مع AWR Art. 52": (
        "Compliant with AWR Art. 52",
        "Conform AWR Art. 52"
    ),
    "Digipoort XML جاهز": (
        "Digipoort XML Ready",
        "Digipoort XML Gereed"
    ),
    "📈 مخطط مسار الإيرادات والسيولة المتوقعة (2026 Trend Simulation):": (
        "📈 Revenue & Cash Flow Projection Trajectory (2026 Trend):",
        "📈 Geprojecteerd Omzet- & Liquiditeitstraject (Trend 2026):"
    ),
    "إجمالي الإيرادات (Gross Revenue)": (
        "Gross Revenue",
        "Bruto Omzet"
    ),
    "التدفق النقدي الصافي (Net Cash Flow)": (
        "Net Cash Flow",
        "Netto Cashflow"
    ),
    "تطبيق سطح مكتب مستقل (Offline-First) لحساب BTW وتوليد ملفات إقرارات الضرائب المشفرة.": (
        "Standalone offline-first desktop app calculating BTW and producing encrypted tax return files.",
        "Zelfstandige offline-first desktopapplicatie voor BTW-berekening en versleutelde belastingaangiftes."
    ),
    "محرك تحليل ذكاء اصطناعي محلي مع معالجة مستندات الفواتير بدقة 99.4%.": (
        "On-premise AI document processing engine extracting invoices with 99.4% precision.",
        "Lokale AI-documentanalyse met factuurextractie met 99,4% precisie."
    ),
    "تم تطبيق الإعدادات بنجاح": (
        "Settings applied successfully",
        "Instellingen succesvol toegepast"
    ),

    # Desktop Simulator Window
    "تصغير": (
        "Minimize",
        "Minimaliseren"
    ),
    "تكبير": (
        "Maximize",
        "Maximaliseren"
    ),
    "🖥️ تشغيل المحاكي التفاعلي داخل المتصفح (Live Desktop Sandbox)": (
        "🖥️ Launch In-Browser Desktop Sandbox Simulator",
        "🖥️ Interactieve Desktop Sandbox in Browser Starten"
    ),
    "محاكي واجهة البرنامج الحية (Live OS Sandbox)": (
        "Live OS Desktop Sandbox",
        "Live Desktop OS Sandbox"
    ),
    "بطاقة المواصفات والمعمارية (Architecture & Specs)": (
        "Architecture Specifications & Technical Brief",
        "Architectuurspecificaties & Technische Brief"
    ),
    "📁 ملف (Bestand)": (
        "📁 File (Bestand)",
        "📁 Bestand"
    ),
    "📊 مبيعات وضرائب (Omzet & BTW)": (
        "📊 Sales & Taxes (Omzet & BTW)",
        "📊 Omzet & BTW"
    ),
    "🛡️ فحص الامتثال AWR (Audit)": (
        "🛡️ AWR Audit Check",
        "🛡️ AWR Boekhoudcontrole"
    ),
    "⚙️ إعدادات الأمان (AES-256)": (
        "⚙️ Security Settings (AES-256)",
        "⚙️ Beveiligingsinstellingen (AES-256)"
    ),
    "إقرار BTW والضرائب": (
        "BTW & Tax Filing",
        "BTW-Aangifte & Belastingen"
    ),
    "تدقيق الذكاء الاصطناعي": (
        "AI Autonomous Audit",
        "AI Autonome Controle"
    ),
    "محرك الحسابات:": (
        "Ledger Engine:",
        "Grootboekengine:"
    ),
    "وضع العمل: Offline 100%": (
        "Operating Mode: 100% Offline",
        "Bedrijfsmodus: 100% Offline"
    ),
    "نموذج حساب ضريبة القيمة المضافة (Aangifte Omzetbelasting Q3 2026)": (
        "VAT Filing Return Calculator (Aangifte Omzetbelasting Q3 2026)",
        "BTW-Aangifte Calculator (Aangifte Omzetbelasting Q3 2026)"
    ),
    "جرب إدخال الأرقام أدناه لمشاهدة الاحتساب الآلي وتوليد الإقرار الهولندي والخليجي فورياً": (
        "Enter values below to test automated real-time calculation and generate official XML filings",
        "Vul hieronder bedragen in om automatische realtime berekening en officiële XML-aangiftes te testen"
    ),
    "جاهز للاحتساب ✓": (
        "Ready for Calculation ✓",
        "Gereed voor Berekening ✓"
    ),
    "المبيعات بنسبة 21% BTW (Omzet Hoog):": (
        "Standard 21% BTW Sales (Omzet Hoog):",
        "Omzet Hoog (21% BTW):"
    ),
    "المبيعات بنسبة 9% BTW (Omzet Laag):": (
        "Reduced 9% BTW Sales (Omzet Laag):",
        "Omzet Laag (9% BTW):"
    ),
    "ضريبة المدخلات القابلة للخصم (Voorbelasting):": (
        "Deductible Input VAT (Voorbelasting):",
        "Voorbelasting (Aftrekbare BTW):"
    ),
    "ضريبة 21% (Hoog)": (
        "21% VAT (Hoog)",
        "21% BTW (Hoog)"
    ),
    "ضريبة 9% (Laag)": (
        "9% VAT (Laag)",
        "9% BTW (Laag)"
    ),
    "الخصم المسموح (Voorb.)": (
        "Deductible (Voorb.)",
        "Aftrekbaar (Voorb.)"
    ),
    "صافي VAT / BTW الواجبة السداد": (
        "Net VAT Payable / (Refund)",
        "Netto te Betalen / (Terug te Vragen) BTW"
    ),
    "صافي الضريبة الواجبة السداد": (
        "Net VAT Payable / (Refund)",
        "Netto te Betalen / (Terug te Vragen) BTW"
    ),
    "📄 توليد ملف Digipoort XML": (
        "📄 Generate Digipoort XML",
        "📄 Genereer Digipoort XML"
    ),
    "تقرير تدقيق الامتثال:": (
        "Compliance Audit Report:",
        "Compliance Auditrapport:"
    ),
    "تنزيل ملف .xml": (
        "Download .xml File",
        "Download .xml Bestand"
    ),
    "معمارية الخصوصية والأمان (Zero-Cloud Privacy)": (
        "Zero-Cloud Privacy & Local Security Architecture",
        "Zero-Cloud Privacy & Lokale Beveiligingsarchitectuur"
    ),
    "تم تصميم البرنامج ليعمل بمعمارية محلية بحتة (Offline-First Engine)، حيث تُخزن قواعد البيانات محلياً عبر محرك SQLite مشفر بخوارزمية AES-256 بت، مما يضمن سرية البيانات المحاسبية بنسبة 100% دون أي تسريب سحابي.": (
        "The software is engineered with a strict Offline-First architecture where ledgers reside in local SQLite databases encrypted with military-grade AES-256, guaranteeing 100% confidentiality without cloud exposure.",
        "De software is ontworpen met een strikte Offline-First architectuur waarbij databases lokaal worden opgeslagen via SQLite versleuteld met militaire AES-256, wat 100% vertrouwelijkheid garandeert zonder cloudlekken."
    ),
    "توافق كامل مع المادة 52 من قانون الضرائب الهولندي (AWR)": (
        "100% compliance with Article 52 of Dutch State Taxes Act (AWR)",
        "100% conform Artikel 52 van de Algemene wet inzake rijksbelastingen (AWR)"
    ),
    "حماية البيانات بموجب اللائحة الأوروبية العامة لحماية البيانات (GDPR)": (
        "Data protection certified under EU General Data Protection Regulation (GDPR)",
        "Gegevensbescherming conform de Algemene Verordening Gegevensbescherming (AVG/GDPR)"
    ),
    "توليد مفاتيح تشفير رقمية مرتبطة بالعتاد (Hardware ID Locking)": (
        "Hardware-locked cryptographic license generation (Hardware ID Binding)",
        "Hardware-gebonden cryptografische licentiesleutels (Hardware ID Binding)"
    ),
    "التوافق والتكامل (Digipoort & PEPPOL)": (
        "Compliance & Gateway Bridges (Digipoort & PEPPOL)",
        "Compliance & Gatewaykoppelingen (Digipoort & PEPPOL)"
    ),
    "يدعم الربط المباشر مع بوابة مصلحة الضرائب الهولندية (Digipoort SBR) وبروتوكول الفوترة الأوروبية الموحدة PEPPOL BIS 3.0.": (
        "Direct integration with Dutch Tax Administration gateway (Digipoort SBR) and Pan-European PEPPOL BIS 3.0 e-invoicing rail.",
        "Directe koppeling met de Belastingdienst (Digipoort SBR) en Europese PEPPOL BIS 3.0 e-facturatienetwerken."
    ),
    "برنامج سطح مكتب للكمبيوتر (Desktop PC/Mac)": (
        "Desktop Application (PC / Mac)",
        "Desktop Applicatie (PC / Mac)"
    ),
    "تطبيق هاتف ذكي (iOS / Android)": (
        "Mobile Application (iOS / Android)",
        "Mobiele Applicatie (iOS / Android)"
    ),
    "حلول ونقاط بيع (POS Agent)": (
        "Point of Sale (POS Terminal Agent)",
        "Kassasysteem (POS Terminal Agent)"
    ),
    "مكتبة أو حزمة مطورين (SDK / API)": (
        "Developer Library (SDK / REST API)",
        "Developer Bibliotheek (SDK / REST API)"
    ),
    "مثال: S&R InventorySync Pro": (
        "e.g. S&R InventorySync Pro",
        "bijv. S&R InventorySync Pro"
    ),
    "التصنيف": (
        "Category",
        "Categorie"
    ),
    "الوصف": (
        "Description",
        "Omschrijving"
    ),
    "سعر الترخيص": (
        "License Price",
        "Licentieprijs"
    ),
    "رقم الإصدار": (
        "Version",
        "Versie"
    ),
    "اسم البرنامج": (
        "Software Name",
        "Softwarenaam"
    ),

    # Publish Software Modal
    "نشر وتوزيع برنامج جديد": (
        "Publish & Distribute Enterprise Application",
        "Nieuwe Software Publiceren & Distribueren"
    ),
    "اسم البرنامج أو التطبيق:": (
        "Application / Software Name:",
        "Software- of Applicatienaam:"
    ),
    "اسم البرنامج أو التطبيق": (
        "Application / Software Name",
        "Software- of Applicatienaam"
    ),
    "التصنيف والمنصة:": (
        "Category & Architecture:",
        "Categorie & Architectuur:"
    ),
    "التصنيف والمنصة": (
        "Category & Architecture",
        "Categorie & Architectuur"
    ),
    "برنامج كمبيوتر (Windows / Mac)": (
        "Desktop Application (Windows / Mac)",
        "Desktop Applicatie (Windows / Mac)"
    ),
    "تطبيق هاتف (iOS / Android)": (
        "Mobile App (iOS / Android)",
        "Mobiele App (iOS / Android)"
    ),
    "مكتبة برمجية (SDK / API)": (
        "Developer SDK / REST API",
        "Developer SDK / REST API"
    ),
    "أداة كاشير ونقاط بيع (POS Agent)": (
        "POS Cashier Daemon",
        "Kassa / POS Daemon"
    ),
    "رقم الإصدار:": (
        "Version Number:",
        "Versienummer:"
    ),
    "سعر الترخيص باليورو (€):": (
        "License Price in EUR (€):",
        "Licentieprijs in EUR (€):"
    ),
    "سعر الترخيص باليورو (€)": (
        "License Price in EUR (€)",
        "Licentieprijs in EUR (€)"
    ),
    "وصف موجز ومميزات البرنامج:": (
        "Itemized Description & Features:",
        "Omschrijving & Kernfuncties:"
    ),
    "وصف موجز ومميزات البرنامج": (
        "Itemized Description & Features",
        "Omschrijving & Kernfuncties"
    ),
    "اكتب وصفاً موجزاً لما يقوم به البرنامج وكيف يساعد العملاء...": (
        "Briefly describe what this software accomplishes and how it creates value for clients...",
        "Beschrijf kort wat deze software doet en welke waarde het toevoegt voor zakelijke klanten..."
    ),
    "نشر البرنامج فورياً في المتجر 🚀": (
        "Publish App to Store 🚀",
        "Publiceer Software in Store 🚀"
    ),

    # Checkout Modal Details
    "تأكيد الدفع والترخيص التجاري": (
        "Commercial License Checkout",
        "Commerciële Licentie Afrekenen"
    ),
    "بوابة الدفع والتراخيص الدولية (Stripe / Mollie iDEAL Checkout JS)": (
        "International Payment Gateway & Digital Licensing (Mollie iDEAL & Stripe)",
        "Internationale Betaalgateway & Digitale Licenties (Mollie iDEAL & Stripe)"
    ),
    "اختر طريقة الدفع المعتمدة:": (
        "Select Verified Payment Method:",
        "Selecteer Geverifieerde Betaalmethode:"
    ),
    "بطاقة ائتمانية": (
        "Credit / Debit Card",
        "Creditcard / Debitkaart"
    ),
    "تحويل SEPA": (
        "SEPA Bank Wire",
        "SEPA Overschrijving"
    ),
    "اسم الحساب التجاري (Bedrijfsnaam):": (
        "Registered Business Name (Bedrijfsnaam):",
        "Geregistreerde Bedrijfsnaam:"
    ),
    "رقم الآيبان للشركة (Business IBAN):": (
        "Business IBAN (NL..):",
        "Zakelijk IBAN (NL..):"
    ),
    "رقم البطاقة الائتمانية:": (
        "Card Number:",
        "Kaartnummer:"
    ),
    "تاريخ انتهاء البطاقة MM/YY:": (
        "Expiry Date MM/YY:",
        "Vervaldatum MM/YY:"
    ),
    "تاريخ انتهاء البطاقة MM/YY": (
        "Expiry Date MM/YY",
        "Vervaldatum MM/YY"
    ),
    "تاريخ انتهاء البطاقة": (
        "Expiry Date",
        "Vervaldatum"
    ),
    "رمز الأمان CVC:": (
        "Security Code CVC:",
        "Beveiligingscode CVC:"
    ),
    "قيمة الترخيص البرمجي الصافي (Net Price):": (
        "Software Net License Price:",
        "Software Licentie Nettoprijs:"
    ),
    "ضريبة القيمة المضافة الهولندية (BTW 21%):": (
        "Dutch Value Added Tax (BTW 21%):",
        "Nederlandse Omzetbelasting (BTW 21%):"
    ),
    "الإجمالي المستحق للسداد (Total Incl. BTW):": (
        "Total Amount Due (Incl. BTW):",
        "Totaal Te Betalen (Incl. BTW):"
    ),
    "🔒 سيتم تحويلك بشكل آمن عبر بروتوكول التشفير المباشر Mollie Connect.": (
        "🔒 Encrypted end-to-end transmission via certified Mollie Connect banking protocol.",
        "🔒 Beveiligde end-to-end versleuteling via gecertificeerd Mollie Connect bankprotocol."
    ),
    "تم إتمام عملية الدفع بنجاح!": (
        "Payment Processed Successfully!",
        "Betaling Succesvol Verwerkt!"
    ),
    "تم تفعيل الترخيص التجاري وإصدار الفاتورة الضريبية الرسمية": (
        "Commercial license activated and official tax invoice issued.",
        "Commerciële licentie geactiveerd en officiële factuur verstrekt."
    ),
    "مفتاح الترخيص الرقمي (Digital License Key):": (
        "Digital License Key:",
        "Digitale Licentiesleutel:"
    ),
    "ختم الاعتماد الرقمي (Verified SHA-256)": (
        "Digital Authenticity Stamp (Verified SHA-256)",
        "Digitale Authenticiteitsstempel (Geverifieerd SHA-256)"
    ),
    "تنزيل حزمة التثبيت الرسمية": (
        "Download Official Package",
        "Officieel Pakket Downloaden"
    ),
    "معاينة الفاتورة الضريبية الصادرة": (
        "Preview Official Tax Invoice",
        "Officiële BTW-Factuur Bekijken"
    ),

    # Chart Months & Labels
    "'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر'": (
        "'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'",
        "'Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt'"
    ),
    "الإيرادات الفعلية (€)": (
        "Gross Revenue (€)",
        "Bruto Omzet (€)"
    ),
    "التدفق النقدي الصافي (€)": (
        "Net Cash Flow (€)",
        "Netto Cashflow (€)"
    ),
    "حلول ERP والربط المالي": (
        "ERP & Financial Bridges",
        "ERP & Financiële Koppelingen"
    ),
    "برمجيات سحابية وتطبيقات": (
        "Cloud Software & Mobile",
        "Cloudsoftware & Mobiel"
    ),
    "أتمتة الذكاء الاصطناعي": (
        "AI & Autonomous Automation",
        "AI & Autonome Automatisering"
    ),
    "استشارات وحوكمة": (
        "Governance & Consulting",
        "Governance & Consultancy"
    )
}

def clean_and_build(target_lang):
    c = ar_master

    # 1. HTML tag attributes
    c = c.replace('<html lang="ar" dir="rtl">', f'<html lang="{target_lang}" dir="ltr" data-page-language="{target_lang}">')

    # 2. Update Asset and Script paths for child folder en/ or nl/
    c = c.replace('href="assets/', 'href="../assets/')
    c = c.replace('src="assets/', 'src="../assets/')
    c = c.replace('href="./assets/', 'href="../assets/')
    c = c.replace('src="./assets/', 'src="../assets/')
    c = c.replace('href="css/', 'href="../css/')
    c = c.replace('src="js/', 'src="../js/')

    # 3. Update Return Links
    c = c.replace('href="logo-studio.html"', 'href="../logo-studio.html"')

    # 4. Remove auto-redirect query param script
    c = re.sub(r'<!-- Language Auto-Redirect from Query Param.*?-->\s*<script>.*?</script>', '', c, flags=re.DOTALL)

    # 5. Remove all Arabic comments
    c = re.sub(r'<!--.*?[\u0600-\u06FF].*?-->', '', c, flags=re.DOTALL)

    # 6. Inject Localized Language Switcher
    if target_lang == 'en':
        switcher_html = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Language">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="demo.html" class="portal-lang-btn active" title="English">🇬🇧 EN</a>
                <a href="../nl/demo.html" class="portal-lang-btn" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
    else:
        switcher_html = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Taal">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="../en/demo.html" class="portal-lang-btn" title="English">🇬🇧 EN</a>
                <a href="demo.html" class="portal-lang-btn active" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
    if 'portal-lang-switcher' in c:
        c = re.sub(r'<div class="portal-lang-switcher".*?</div>', switcher_html.strip(), c, flags=re.DOTALL)
    else:
        c = re.sub(r'(<a href="\.\./logo-studio\.html"[^>]*>)', switcher_html + '\n            \\1', c, count=1)

    # 7. Apply dictionary replacements (longest first)
    sorted_dict = sorted(DICT.items(), key=lambda x: len(x[0]), reverse=True)
    idx = 0 if target_lang == 'en' else 1
    for ar_str, trans_pair in sorted_dict:
        target_trans = trans_pair[idx]
        c = c.replace(ar_str, target_trans)

    # 8. Script Replacements: Guided Tour
    if target_lang == 'en':
        c = c.replace("title: '⚡ محاكي العملات والضرائب اللحظي (Simulator Bar)'", "title: '⚡ Live Currency & Tax Simulator Bar'")
        c = c.replace("desc: 'يتيح للزبون التبديل اللحظي بين اليورو والدولار والريال السعودي مع احتساب مباشر لضريبة القيمة المضافة BTW 21% والخليجية 15% وتحديث الأرقام فورياً.'", "desc: 'Enables real-time switching between EUR, USD, and SAR with dynamic 21% Dutch BTW and 15% GCC VAT recalculation across all widgets.'")
        c = c.replace("title: '📊 لوحة القيادة والتدفق المالي (Financial KPIs)'", "title: '📊 Executive Financial KPI Dashboard'")
        c = c.replace("desc: 'مؤشرات مالية دقيقة للإيرادات السنوية، التدفقات النقدية الصافية، ونسبة الامتثال والأتمتة الموفرة لساعات العمل.'", "desc: 'Accurate metrics tracking annual gross revenue, net operational cash flow, compliance rates, and automated work hours saved.'")
        c = c.replace("title: '📦 إدارة الـ ERP والمخازن الذكية'", "title: '📦 Enterprise ERP & Warehouse Telemetry'")
        c = c.replace("desc: 'وحدة الـ ERP الموزعة لإدارة الفروع المتعددة، تتبع سلاسل التوريد، والتنبؤ بالطلب بدقة عالية.'", "desc: 'Distributed multi-branch inventory tracking, real-time dispatch monitoring, and AI reorder predictions.'")
        c = c.replace("title: '🧾 الفواتير الإلكترونية والامتثال الضريبي الأوروبي'", "title: '🧾 E-Invoicing & European Tax Compliance'")
        c = c.replace("desc: 'إنشاء الفواتير المشفرة بنظام EN 16931 الأوروبي وتوافق كامل مع بوابات الدفع iDEAL والتحويل المصرفي SEPA.'", "desc: 'Encrypted invoices compliant with EU EN 16931 standards, integrated with iDEAL and SEPA instant bank rails.'")
        c = c.replace("title: '💻 سوق البرمجيات وحاسبة S&R TaxSync'", "title: '💻 Software Marketplace & S&R TaxSync Vault'")
        c = c.replace("desc: 'تراخيص رقمية فورية، حاسبة ضريبة BTW مدمجة، ومولد مفاتيح تجريبية (14 يوماً) يعمل بضغطة زر مع تنزيل فوري.'", "desc: 'Instant trial key generation, automated 14-day licenses, and verified Windows desktop installers.'")
        c = c.replace("showPortalToast('🚀 مرحباً بك في الجولة الإرشادية التفاعلية!');", "showPortalToast('🚀 Welcome to the Interactive Guided Tour!');")
        c = c.replace("showPortalToast('🎉 اكتملت الجولة الإرشادية بنجاح!');", "showPortalToast('🎉 Guided tour completed successfully!');")
        c = c.replace("`خطوة ${currentTourStep + 1} من ${tourSteps.length}`", "`Step ${currentTourStep + 1} of ${tourSteps.length}`")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Finish Tour ✓' : 'Next ➡️';")

        # White Label & JS Strings
        c = c.replace("showPortalToast(`✨ تم تطبيق وحفظ هوية [${name}] على نظام الـ ERP بنجاح!`);", "showPortalToast(`✨ Successfully applied and saved custom brand identity [${name}] on ERP platform!`);")
        c = c.replace("showPortalToast('تمت استعادة هوية S&R CoreSync الأصلية ومسح التخصيص المحفوظ.');", "showPortalToast('Restored original S&R CoreSync identity and cleared custom configuration.');")
        c = c.replace("showPortalToast('تم تحميل ملف الشعار بنجاح! انقر على زر تطبيق الهوية لحفظه.');", "showPortalToast('Emblem uploaded successfully! Click Apply Custom Brand to activate.');")
        c = c.replace("showPortalToast(`تم تطبيق وحفظ سمة [${themeName.toUpperCase()}] في المتصفح!`);", "showPortalToast(`Applied and saved [${themeName.toUpperCase()}] theme in browser!`);")
        c = c.replace("showPortalToast(`💱 تم التبديل إلى عملة: ${currencyConfig[cur].label}`);", "showPortalToast(`💱 Switched currency to: ${currencyConfig[cur].label}`);")
        c = c.replace("showPortalToast(`🏛️ تم تطبيق النظام الضريبي: ${vatText}`);", "showPortalToast(`🏛️ Applied tax regime: ${vatText}`);")
        c = c.replace("showPortalToast(`⚡ تم توليد وتشفير ملف Digipoort XML بنجاح!`);", "showPortalToast('⚡ Digipoort SBR XML generated and validated successfully!');")
        c = c.replace("showPortalToast('📁 تم تنزيل ملف Digipoort XML الرسمي على جهازك!');", "showPortalToast('📁 Official Digipoort XML file downloaded to your device!');")
        c = c.replace("showPortalToast(`✨ تم توليد مفتاح تجريبي جديد: ${newKey}`);", "showPortalToast(`✨ Generated new trial license key: ${newKey}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ المفتاح التجريبي: ${key}`);", "showPortalToast(`🔑 Copied trial key: ${key}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ مفتاح الترخيص: ${key}`);", "showPortalToast(`🔑 Copied license key: ${key}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ المفتاح: ${key}`);", "showPortalToast(`🔑 Copied key: ${key}`);")
        c = c.replace("showPortalToast(`⚡ بدأ تنزيل حزمة التثبيت لـ [${title}] بنجاح!`);", "showPortalToast(`⚡ Starting installer download for [${title}] successfully!`);")
        c = c.replace("showPortalToast(`💻 تم تشغيل المحاكي التفاعلي لـ [${sw.title}] بنجاح!`);", "showPortalToast(`💻 Interactive sandbox launched for [${sw.title}]!`);")
        c = c.replace("showPortalToast(`🚀 تم نشر برنامج [${title}] بنجاح في متجر المنصة!`);", "showPortalToast(`🚀 Successfully published [${title}] to the Software Hub!`);")
        c = c.replace("showPortalToast(`🛡️ اكتمل تدقيق الامتثال الضريبي بنجاح: متوافق بنسبة 100%!`);", "showPortalToast('🛡️ Tax compliance audit completed: 100% Compliant!');")
        c = c.replace("showPortalToast(`✨ تم توليد فاتورة تجريبية رسمية بهوية [${currentName}] جاهزة للمعاينة والطباعة!`);", "showPortalToast(`✨ Generated official branded invoice for [${currentName}] ready for print & preview!`);")
        c = c.replace("showPortalToast(`🎉 تم إتمام الدفع بنجاح وإصدار الفاتورة [${invNum}] وتفعيل الترخيص!`);", "showPortalToast(`🎉 Payment confirmed, invoice [${invNum}] issued, and license activated!`);")
        c = c.replace("showPortalToast('تم نسخ مفتاح الترخيص!');", "showPortalToast('License key copied to clipboard!');")
        c = c.replace("statusText.innerHTML = '<span class=\"ideal-success-msg\">✓ تمت تسوية المبلغ وتحويله لحساب المؤسسة بنجاح!</span>';", "statusText.innerHTML = '<span class=\"ideal-success-msg\">✓ Settlement completed and deposited into corporate account!</span>';")
        c = c.replace("btn.innerText = 'تأكيد السداد التجريبي اللحظي';", "btn.innerText = 'Confirm Instant Demo Settlement';")
        c = c.replace("btn.innerText = 'جاري المعالجة البنكية...';", "btn.innerText = 'Processing Bank Handshake...';")
        c = c.replace("statusText.innerText = 'الاتصال الآمن ببروتوكول iDEAL 2.0 وSEPA Instant...';", "statusText.innerText = 'Secure handshake via iDEAL 2.0 & SEPA Instant rails...';")
        c = c.replace("statusText.innerText = 'اختر البنك واضغط على تأكيد السداد الفوري';", "statusText.innerText = 'Select bank and click Confirm Instant Payment';")
        c = c.replace("badge.textContent = `● مخصص (${hasCustomBrand || hasCustomTheme}) ومحفوظ محلياً`;", "badge.textContent = `● Custom (${hasCustomBrand || hasCustomTheme}) Saved Locally`;")
        c = c.replace("wlBadge.innerText = `هوية مخصصة: ${effectiveIssuer}`;", "wlBadge.innerText = `Custom Brand: ${effectiveIssuer}`;")
        c = c.replace("btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M4 14h6m0 0v6m0-6L3 21m17-7h-6m0 0v6m0-6l7 7M14 4h6m-6 0v6m0-6l7-7M4 10h6m0 0V4m0 6L3 3\"></path></svg> <span>الخروج من العرض</span>`;", "btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M4 14h6m0 0v6m0-6L3 21m17-7h-6m0 0v6m0-6l7 7M14 4h6m-6 0v6m0-6l7-7M4 10h6m0 0V4m0 6L3 3\"></path></svg> <span>Exit Client View</span>`;")
        c = c.replace("btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3\"></path></svg> <span>وضع Client View [P]</span>`;", "btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3\"></path></svg> <span>Client View [P]</span>`;")
        c = c.replace("const note = encodeURIComponent(`طلب استشارة بناءً على المعاينة التجريبية: القسم المستهدف (${activeTab})، وحجم العمليات المقدر في الجلسة: ${revText}`);", "const note = encodeURIComponent(`Consultation request from Interactive Demo: Target Module (${activeTab}), Estimated Volume: ${revText}`);")
        c = c.replace("'فاتورة معتمدة - جاهزة للتحصيل ✓'", "'Certified Invoice - Ready for Collection ✓'")
        c = c.replace("'قيد الانتظار'", "'Pending'")
        c = c.replace("`مدفوعة عبر ${gwLabel}`", "`Paid via ${gwLabel}`")
        c = c.replace("label: 'يورو (EUR)'", "label: 'Euro (EUR)'")
        c = c.replace("label: 'دولار أمريكي (USD)'", "label: 'US Dollar (USD)'")
        c = c.replace("label: 'ريال سعودي (SAR)'", "label: 'Saudi Riyal (SAR)'")
        c = c.replace("'BTW هولندي (21%)'", "'Dutch BTW (21%)'")
        c = c.replace("'BTW مخفض (9%)'", "'Reduced BTW (9%)'")
        c = c.replace("'ضريبة خليجية (15%)'", "'GCC VAT (15%)'")
        c = c.replace("'معفى (0%)'", "'Exempt (0%)'")
        c = c.replace("'معفى من الضريبة (0%)'", "'Tax Exempt (0%)'")
        c = c.replace("titleEl.innerText = '🛡️ تقرير الفحص والامتثال الضريبي الذكي (AWR Audit Report):';", "titleEl.innerText = '🛡️ Smart Tax Compliance Audit Report (AWR Art. 52):';")
        c = c.replace("titleEl.innerText = '📄 ملف الإقرار الضريبي الرسمي المولد (Digipoort SBR XML):';", "titleEl.innerText = '📄 Official Tax Return File (Digipoort SBR XML):';")
        c = c.replace("document.getElementById('chkAppLicenseType').innerText = `ترخيص تجاري كامل (${sw.version}) • شامل الفاتورة الضريبية`;", "document.getElementById('chkAppLicenseType').innerText = `Full Commercial License (${sw.version}) • Includes Official VAT Invoice`;")
        c = c.replace("document.getElementById('chkBtnText').innerText = `تأكيد الدفع الآمن وإصدار الفاتورة (€ ${total.toFixed(2)})`;", "document.getElementById('chkBtnText').innerText = `Confirm Secure Payment & Issue Invoice (€ ${total.toFixed(2)})`;")
        c = c.replace("text.innerText = 'جاري الاتصال الآمن مع بوابة الدفع وتوثيق الترخيص...';", "text.innerText = 'Connecting securely to payment gateway and authenticating license...';")

        # AI Copilot in JS
        c = c.replace("query.includes('أكتوبر') || query.includes('التدفق')", "query.toLowerCase().includes('october') || query.toLowerCase().includes('cash') || query.includes('أكتوبر') || query.includes('التدفق')")
        c = c.replace("query.includes('فواتير') || query.includes('المتأخرة')", "query.toLowerCase().includes('invoice') || query.toLowerCase().includes('overdue') || query.includes('فواتير') || query.includes('المتأخرة')")
        c = re.sub(r'aiResponse = "بناءً على مطابقة دفاتر المحاسبة.*?;', 'aiResponse = "Based on October general ledgers and Cloud ERP records:\\n- Gross Realized Revenue: €144,500 (+18% record quarterly growth).\\n- Operating Margin: 27.4%, outperforming Dutch benchmarks.\\n- Recommendation: Accelerate €42,000 receivable collection due October 10 to boost liquidity.";', c)
        c = re.sub(r'aiResponse = "توجد فاتورة واحدة معلقة.*?;', 'aiResponse = "There is currently 1 pending invoice (€35,000) for a corporate client maturing within 14 days with validated Reverse Charge. Zero overdue receivables exceed 30 days due to automated notifications.";', c)
        c = re.sub(r'aiResponse = "تم تحليل استفسارك عبر خوارزمية.*?;', 'aiResponse = "Your inquiry was analyzed by the S&R CoreSync Financial Engine. Accounting and operations are synchronized. RPA automation is projected to save 35 work hours next month via instant document archiving.";', c)

    else: # Dutch (NL)
        c = c.replace("title: '⚡ محاكي العملات والضرائب اللحظي (Simulator Bar)'", "title: '⚡ Live Valuta & BTW Simulator Bar'")
        c = c.replace("desc: 'يتيح للزبون التبديل اللحظي بين اليورو والدولار والريال السعودي مع احتساب مباشر لضريبة القيمة المضافة BTW 21% والخليجية 15% وتحديث الأرقام فورياً.'", "desc: 'Maakt realtime wisselen tussen EUR, USD en SAR mogelijk met directe herberekening van 21% BTW en 15% GCC belasting over alle widgets.'")
        c = c.replace("title: '📊 لوحة القيادة والتدفق المالي (Financial KPIs)'", "title: '📊 Zakelijk Financieel KPI Dashboard'")
        c = c.replace("desc: 'مؤشرات مالية دقيقة للإيرادات السنوية، التدفقات النقدية الصافية، ونسبة الامتثال والأتمتة الموفرة لساعات العمل.'", "desc: 'Nauwkeurige KPI-indicatoren voor jaaromzet, netto operationele cashflow, nalevingspercentages en bespaarde werkuren.'")
        c = c.replace("title: '📦 إدارة الـ ERP والمخازن الذكية'", "title: '📦 Enterprise ERP & Magazijntelemetrie'")
        c = c.replace("desc: 'وحدة الـ ERP الموزعة لإدارة الفروع المتعددة، تتبع سلاسل التوريد، والتنبؤ بالطلب بدقة عالية.'", "desc: 'Gedistribueerd voorraadbeheer over meerdere vestigingen, realtime tracking en automatische herbestellingen.'")
        c = c.replace("title: '🧾 الفواتير الإلكترونية والامتثال الضريبي الأوروبي'", "title: '🧾 E-Facturatie & BTW Naleving'")
        c = c.replace("desc: 'إنشاء الفواتير المشفرة بنظام EN 16931 الأوروبي وتوافق كامل مع بوابات الدفع iDEAL والتحويل المصرفي SEPA.'", "desc: 'Versleutelde facturen conform Europese norm EN 16931, geïntegreerd met iDEAL en SEPA-overschrijvingen.'")
        c = c.replace("title: '💻 سوق البرمجيات وحاسبة S&R TaxSync'", "title: '💻 Softwaremarktplaats & S&R TaxSync Kluis'")
        c = c.replace("desc: 'تراخيص رقمية فورية، حاسبة ضريبة BTW مدمجة، ومولد مفاتيح تجريبية (14 يوماً) يعمل بضغطة زر مع تنزيل فوري.'", "desc: 'Directe licentiesleutels, ingebouwde BTW-calculator en geverifieerde 14-dagen proeflicentie met één klik.'")
        c = c.replace("showPortalToast('🚀 مرحباً بك في الجولة الإرشادية التفاعلية!');", "showPortalToast('🚀 Welkom bij de interactieve rondleiding!');")
        c = c.replace("showPortalToast('🎉 اكتملت الجولة الإرشادية بنجاح!');", "showPortalToast('🎉 Rondleiding succesvol voltooid!');")
        c = c.replace("`خطوة ${currentTourStep + 1} من ${tourSteps.length}`", "`Stap ${currentTourStep + 1} van ${tourSteps.length}`")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Rondleiding Afronden ✓' : 'Volgende ➡️';")

        # White Label & JS Strings
        c = c.replace("showPortalToast(`✨ تم تطبيق وحفظ هوية [${name}] على نظام الـ ERP بنجاح!`);", "showPortalToast(`✨ Bedrijfsidentiteit [${name}] succesvol toegepast op ERP-platform!`);")
        c = c.replace("showPortalToast('تمت استعادة هوية S&R CoreSync الأصلية ومسح التخصيص المحفوظ.');", "showPortalToast('Standaard S&R CoreSync identiteit hersteld en instellingen gewist.');")
        c = c.replace("showPortalToast('تم تحميل ملف الشعار بنجاح! انقر على زر تطبيق الهوية لحفظه.');", "showPortalToast('Logo succesvol geüpload! Klik op Huisstijl Toepassen om te activeren.');")
        c = c.replace("showPortalToast(`تم تطبيق وحفظ سمة [${themeName.toUpperCase()}] في المتصفح!`);", "showPortalToast(`Thema [${themeName.toUpperCase()}] toegepast en opgeslagen in browser!`);")
        c = c.replace("showPortalToast(`💱 تم التبديل إلى عملة: ${currencyConfig[cur].label}`);", "showPortalToast(`💱 Valuta gewijzigd naar: ${currencyConfig[cur].label}`);")
        c = c.replace("showPortalToast(`🏛️ تم تطبيق النظام الضريبي: ${vatText}`);", "showPortalToast(`🏛️ Belastingstelsel toegepast: ${vatText}`);")
        c = c.replace("showPortalToast(`⚡ تم توليد وتشفير ملف Digipoort XML بنجاح!`);", "showPortalToast('⚡ Digipoort SBR XML succesvol gegenereerd en gevalideerd!');")
        c = c.replace("showPortalToast('📁 تم تنزيل ملف Digipoort XML الرسمي على جهازك!');", "showPortalToast('📁 Officieel Digipoort XML-bestand gedownload naar uw apparaat!');")
        c = c.replace("showPortalToast(`✨ تم توليد مفتاح تجريبي جديد: ${newKey}`);", "showPortalToast(`✨ Nieuwe proeflicentiesleutel gegenereerd: ${newKey}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ المفتاح التجريبي: ${key}`);", "showPortalToast(`🔑 Proeflicentiesleutel gekopieerd: ${key}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ مفتاح الترخيص: ${key}`);", "showPortalToast(`🔑 Licentiesleutel gekopieerd: ${key}`);")
        c = c.replace("showPortalToast(`🔑 تم نسخ المفتاح: ${key}`);", "showPortalToast(`🔑 Sleutel gekopieerd: ${key}`);")
        c = c.replace("showPortalToast(`⚡ بدأ تنزيل حزمة التثبيت لـ [${title}] بنجاح!`);", "showPortalToast(`⚡ Installatiepakket downloaden voor [${title}] gestart!`);")
        c = c.replace("showPortalToast(`💻 تم تشغيل المحاكي التفاعلي لـ [${sw.title}] بنجاح!`);", "showPortalToast(`💻 Interactieve sandbox gestart voor [${sw.title}]!`);")
        c = c.replace("showPortalToast(`🚀 تم نشر برنامج [${title}] بنجاح في متجر المنصة!`);", "showPortalToast(`🚀 Software [${title}] succesvol gepubliceerd in de Software Hub!`);")
        c = c.replace("showPortalToast(`🛡️ اكتمل تدقيق الامتثال الضريبي بنجاح: متوافق بنسبة 100%!`);", "showPortalToast('🛡️ AWR compliance audit voltooid: 100% Fiscaal Conform!');")
        c = c.replace("showPortalToast(`✨ تم توليد فاتورة تجريبية رسمية بهوية [${currentName}] جاهزة للمعاينة والطباعة!`);", "showPortalToast(`✨ Officiële factuur voor [${currentName}] gereed voor weergave en afdrukken!`);")
        c = c.replace("showPortalToast(`🎉 تم إتمام الدفع بنجاح وإصدار الفاتورة [${invNum}] وتفعيل الترخيص!`);", "showPortalToast(`🎉 Betaling voltooid, factuur [${invNum}] uitgegeven en licentie actief!`);")
        c = c.replace("showPortalToast('تم نسخ مفتاح الترخيص!');", "showPortalToast('Licentiesleutel gekopieerd naar klembord!');")
        c = c.replace("statusText.innerHTML = '<span class=\"ideal-success-msg\">✓ تمت تسوية المبلغ وتحويله لحساب المؤسسة بنجاح!</span>';", "statusText.innerHTML = '<span class=\"ideal-success-msg\">✓ Betaling succesvol verrekend en bijgeschreven op zakelijke rekening!</span>';")
        c = c.replace("btn.innerText = 'تأكيد السداد التجريبي اللحظي';", "btn.innerText = 'Bevestig Directe Testbetaling';")
        c = c.replace("btn.innerText = 'جاري المعالجة البنكية...';", "btn.innerText = 'Banktransactie wordt verwerkt...';")
        c = c.replace("statusText.innerText = 'الاتصال الآمن ببروتوكول iDEAL 2.0 وSEPA Instant...';", "statusText.innerText = 'Beveiligde verbinding via iDEAL 2.0 en SEPA Instant...';")
        c = c.replace("statusText.innerText = 'اختر البنك واضغط على تأكيد السداد الفوري';", "statusText.innerText = 'Kies uw bank en klik op Bevestig Directe Betaling';")
        c = c.replace("badge.textContent = `● مخصص (${hasCustomBrand || hasCustomTheme}) ومحفوظ محلياً`;", "badge.textContent = `● Aangepast (${hasCustomBrand || hasCustomTheme}) Lokaal Opgeslagen`;")
        c = c.replace("wlBadge.innerText = `هوية مخصصة: ${effectiveIssuer}`;", "wlBadge.innerText = `Aangepast Merk: ${effectiveIssuer}`;")
        c = c.replace("btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M4 14h6m0 0v6m0-6L3 21m17-7h-6m0 0v6m0-6l7 7M14 4h6m-6 0v6m0-6l7-7M4 10h6m0 0V4m0 6L3 3\"></path></svg> <span>الخروج من العرض</span>`;", "btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M4 14h6m0 0v6m0-6L3 21m17-7h-6m0 0v6m0-6l7 7M14 4h6m-6 0v6m0-6l7-7M4 10h6m0 0V4m0 6L3 3\"></path></svg> <span>Presentatie Sluiten</span>`;")
        c = c.replace("btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3\"></path></svg> <span>وضع Client View [P]</span>`;", "btn.innerHTML = `<svg viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3\"></path></svg> <span>Klantpresentatie [P]</span>`;")
        c = c.replace("const note = encodeURIComponent(`طلب استشارة بناءً على المعاينة التجريبية: القسم المستهدف (${activeTab})، وحجم العمليات المقدر في الجلسة: ${revText}`);", "const note = encodeURIComponent(`Consultaanvraag vanuit Demosessie: Doelmodule (${activeTab}), Geschat Transactievolume: ${revText}`);")
        c = c.replace("'فاتورة معتمدة - جاهزة للتحصيل ✓'", "'Gecertificeerde Factuur - Gereed voor Incasso ✓'")
        c = c.replace("'قيد الانتظار'", "'Openstaand'")
        c = c.replace("`مدفوعة عبر ${gwLabel}`", "`Betaald via ${gwLabel}`")
        c = c.replace("label: 'يورو (EUR)'", "label: 'Euro (EUR)'")
        c = c.replace("label: 'دولار أمريكي (USD)'", "label: 'Amerikaanse Dollar (USD)'")
        c = c.replace("label: 'ريال سعودي (SAR)'", "label: 'Saoedische Riyal (SAR)'")
        c = c.replace("'BTW هولندي (21%)'", "'Nederlandse BTW (21%)'")
        c = c.replace("'BTW مخفض (9%)'", "'Verlaagd BTW-tarief (9%)'")
        c = c.replace("'ضريبة خليجية (15%)'", "'GCC Btw (15%)'")
        c = c.replace("'معفى (0%)'", "'Vrijgesteld (0%)'")
        c = c.replace("'معفى من الضريبة (0%)'", "'Vrijgesteld van Belasting (0%)'")
        c = c.replace("titleEl.innerText = '🛡️ تقرير الفحص والامتثال الضريبي الذكي (AWR Audit Report):';", "titleEl.innerText = '🛡️ Fiscaal Nalevingsrapport (AWR Art. 52):';")
        c = c.replace("titleEl.innerText = '📄 ملف الإقرار الضريبي الرسمي المولد (Digipoort SBR XML):';", "titleEl.innerText = '📄 Gegenereerd Belastingaangiftebestand (Digipoort SBR XML):';")
        c = c.replace("document.getElementById('chkAppLicenseType').innerText = `ترخيص تجاري كامل (${sw.version}) • شامل الفاتورة الضريبية`;", "document.getElementById('chkAppLicenseType').innerText = `Volledige Commerciële Licentie (${sw.version}) • Inclusief BTW-Factuur`;")
        c = c.replace("document.getElementById('chkBtnText').innerText = `تأكيد الدفع الآمن وإصدار الفاتورة (€ ${total.toFixed(2)})`;", "document.getElementById('chkBtnText').innerText = `Bevestig Veilige Betaling & Facturatie (€ ${total.toFixed(2)})`;")
        c = c.replace("text.innerText = 'جاري الاتصال الآمن مع بوابة الدفع وتوثيق الترخيص...';", "text.innerText = 'Beveiligde verbinding met betaalgateway en licentie-authenticatie...';")

        # AI Copilot in JS
        c = c.replace("query.includes('أكتوبر') || query.includes('التدفق')", "query.toLowerCase().includes('oktober') || query.toLowerCase().includes('cash') || query.includes('أكتوبر') || query.includes('التدفق')")
        c = c.replace("query.includes('فواتير') || query.includes('المتأخرة')", "query.toLowerCase().includes('factuur') || query.toLowerCase().includes('vervallen') || query.includes('فواتير') || query.includes('المتأخرة')")
        c = re.sub(r'aiResponse = "بناءً على مطابقة دفاتر المحاسبة.*?;', 'aiResponse = "Op basis van het grootboek en het ERP-systeem voor oktober:\\n- Gerealiseerde Bruto Omzet: €144.500 (+18% record kwartaalgroei).\\n- Operationele Marge: 27,4%, boven Nederlands sectorgemiddelde.\\n- Advies: Versnel incasso van openstaande vordering van €42.000 om liquiditeit te versterken.";', c)
        c = re.sub(r'aiResponse = "توجد فاتورة واحدة معلقة.*?;', 'aiResponse = "Er is 1 openstaande factuur van €35.000 voor een zakelijke cliënt met correcte BTW-verlegging. Er zijn nul achterstallige posten ouder dan 30 dagen dankzij geautomatiseerde herinneringen.";', c)
        c = re.sub(r'aiResponse = "تم تحليل استفسارك عبر خوارزمية.*?;', 'aiResponse = "Uw vraag is geanalyseerd door de S&R CoreSync Financiële Engine. Boekhouding en operatie zijn gesynchroniseerd. RPA-automatisering bespaart komende maand circa 35 declarabele uren.";', c)

    # General replacements for any leftover phrases in JS/HTML
    if target_lang == 'en':
        c = c.replace("'مجموعة الرياض للخدمات اللوجستية'", "'Riyadh Logistics Group BV'")
        c = c.replace("'مجموعة الشريك التجاري المستهدف'", "'Enterprise Partner Organization'")
        c = c.replace("'جلسة معاينة تفاعلية'", "'Interactive Demo Session'")
        c = c.replace("<td><span class=\"status-badge status-completed\">تمت المزامنة فوراً</span></td>", "<td><span class=\"status-badge status-completed\">Instantly Synchronized</span></td>")
        c = c.replace("'مدفوعة عبر ", "'Paid via ")
        c = c.replace("'قيد الانتظار'", "'Pending'")
        c = c.replace("استرداد: €", "Refund: €")
        c = c.replace('تسوية via SEPA & iDEAL بدون تدخل بشري', 'Reconciliation via SEPA & iDEAL without manual input')
        c = c.replace('الكل (<span id="count-all">3</span>)', 'All (<span id="count-all">3</span>)')
        c = c.replace('المدفوعة (<span id="count-paid">2</span>)', 'Paid (<span id="count-paid">2</span>)')
        c = c.replace('المستحقة (<span id="count-pending">1</span>)', 'Pending (<span id="count-pending">1</span>)')
        c = c.replace('Actions التفاعلية', 'Actions')
        c = c.replace('اختيار نسبة VAT / BTW للحاسبة السريعة', 'Select VAT rate for quick calculation')
        c = c.replace('Purchase License وإصدار فاتورة', 'Purchase License & Issue Invoice')
        c = c.replace('Purchase License التجاري الآن (€ 189 / سنة)', 'Purchase Commercial License Now (€ 189 / yr)')
        c = c.replace('📄 Preview Invoice الصادرة', '📄 Preview Issued Invoice')
        c = c.replace('خطوة 1 من 5', 'Step 1 of 5')
        c = c.replace('title="إغلاق الجولة"', 'title="Close Tour"')
        c = c.replace('⬅️ السابق', '⬅️ Previous')
        c = c.replace('التالي ➡️', 'Next ➡️')
        c = c.replace('🖨️ طباعة / حفظ كـ PDF', '🖨️ Print / Save as PDF')
        c = c.replace('إغلاق ✕', 'Close ✕')
        c = c.replace('>إغلاق<', '>Close<')
        c = c.replace('title="إغلاق"', 'title="Close"')
        c = c.replace('>نسخ<', '>Copy<')
        c = c.replace('id="pdfVatScheme">BTW هولندي (21%)</td>', 'id="pdfVatScheme">Dutch BTW (21%)</td>')
    else:
        c = c.replace("'مجموعة الرياض للخدمات اللوجستية'", "'Riyadh Logistics Group BV'")
        c = c.replace("'مجموعة الشريك التجاري المستهدف'", "'Enterprise Partner Organisatie'")
        c = c.replace("'جلسة معاينة تفاعلية'", "'Interactieve Demosessie'")
        c = c.replace("<td><span class=\"status-badge status-completed\">تمت المزامنة فوراً</span></td>", "<td><span class=\"status-badge status-completed\">Direct Gesynchroniseerd</span></td>")
        c = c.replace("'مدفوعة عبر ", "'Betaald via ")
        c = c.replace("'قيد الانتظار'", "'Openstaand'")
        c = c.replace("استرداد: €", "Teruggave: €")
        c = c.replace('تسوية via SEPA & iDEAL بدون تدخل بشري', 'Afstemming via SEPA & iDEAL zonder handmatige tussenkomst')
        c = c.replace('الكل (<span id="count-all">3</span>)', 'Alle (<span id="count-all">3</span>)')
        c = c.replace('المدفوعة (<span id="count-paid">2</span>)', 'Betaald (<span id="count-paid">2</span>)')
        c = c.replace('المستحقة (<span id="count-pending">1</span>)', 'Openstaand (<span id="count-pending">1</span>)')
        c = c.replace('Actions التفاعلية', 'Acties')
        c = c.replace('<th>Acties التفاعلية</th>', '<th>Interactieve Acties</th>')
        c = c.replace('اختيار نسبة VAT / BTW للحاسبة السريعة', 'Selecteer BTW-tarief voor snelle berekening')
        c = c.replace('اختيار نسبة BTW للحاسبة السريعة', 'Selecteer BTW-tarief voor snelle berekening')
        c = c.replace('Purchase License وإصدار فاتورة', 'Licentie Aanschaffen & Factuur Ontvangen')
        c = c.replace('Licentie Aanschaffen وإصدار فاتورة', 'Licentie Aanschaffen & Factuur Ontvangen')
        c = c.replace('Purchase License التجاري الآن (€ 189 / سنة)', 'Commerciële Licentie Nu Aanschaffen (€ 189 / jaar)')
        c = c.replace('Licentie Aanschaffen التجاري الآن (€ 189 / سنة)', 'Commerciële Licentie Nu Aanschaffen (€ 189 / jaar)')
        c = c.replace('📄 Preview Invoice الصادرة', '📄 Gegenereerde Factuur Bekijken')
        c = c.replace('📄 Factuur Bekijken الصادرة', '📄 Gegenereerde Factuur Bekijken')
        c = c.replace('خطوة 1 من 5', 'Stap 1 van 5')
        c = c.replace('title="إغلاق الجولة"', 'title="Rondleiding Sluiten"')
        c = c.replace('⬅️ السابق', '⬅️ Vorige')
        c = c.replace('التالي ➡️', 'Volgende ➡️')
        c = c.replace('🖨️ طباعة / حفظ كـ PDF', '🖨️ Afdrukken / Opslaan als PDF')
        c = c.replace('إغلاق ✕', 'Sluiten ✕')
        c = c.replace('>إغلاق<', '>Sluiten<')
        c = c.replace('title="إغلاق"', 'title="Sluiten"')
        c = c.replace('>نسخ<', '>Kopiëren<')
        c = c.replace('id="pdfVatScheme">BTW هولندي (21%)</td>', 'id="pdfVatScheme">Nederlandse BTW (21%)</td>')

    return c

print("Building English demo...")
en_clean = clean_and_build('en')
with open(DEMO_EN_PATH, 'w', encoding='utf-8') as f:
    f.write(en_clean)
print("English demo built successfully!")

print("Building Dutch demo...")
nl_clean = clean_and_build('nl')
with open(DEMO_NL_PATH, 'w', encoding='utf-8') as f:
    f.write(nl_clean)
print("Dutch demo built successfully!")
