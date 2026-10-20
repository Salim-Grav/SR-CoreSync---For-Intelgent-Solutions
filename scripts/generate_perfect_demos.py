# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - 100% Comprehensive Multilingual Demo Portal Generator
Translates every Arabic string in demo.html to high-end corporate English and Dutch.
Establishes full language isolation and LTR ergonomics.
"""

import os
import re

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(PROJECT_DIR, 'demo.html')
DEMO_EN_PATH = os.path.join(PROJECT_DIR, 'en', 'demo.html')
DEMO_NL_PATH = os.path.join(PROJECT_DIR, 'nl', 'demo.html')

with open(DEMO_AR_PATH, 'r', encoding='utf-8') as f:
    ar_master = f.read()

# Base Dictionary for English and Dutch
# Format: 'Arabic String': ('English Translation', 'Dutch Translation')
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
    "تستحق خلال 14 يوماً": (
        "due within 14 days",
        "vervalt binnen 14 dagen"
    ),
    "سجل الفواتير الصادرة والواردة": (
        "Inbound & Outbound Invoices Ledger",
        "Overzicht Inkomende & Uitgaande Facturen"
    ),
    "توليد فوري بتنسيق UBL وXML معتمد": (
        "Instant generation in certified UBL & XML formats",
        "Directe aanmaak in gecertificeerd UBL- & XML-formaat"
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
    "طريقة الدفع / الامتثال": (
        "Payment Rail / Compliance",
        "Betaalmethode / Naleving"
    ),
    "الإجراءات": (
        "Actions",
        "Acties"
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
    "📊 تحليل التدفق المالي لشهر أكتوبر": (
        "📊 October Cash Flow Telemetry Analysis",
        "📊 Cashflow- en Liquiditeitsanalyse Oktober"
    ),
    "⏳ الفواتير المتأخرة والتحصيل": (
        "⏳ Overdue Invoices & Collection Strategy",
        "⏳ Openstaande Facturen & Incassostrategie"
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
    "طلب عرض سعر لنظام White-Label مخصص": (
        "Request White-Label Proposal",
        "Offerte voor White-Label Aanvragen"
    ),

    # Modals & Interactions
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
    "معاينة الفاتورة الصادرة": (
        "Invoice Document Preview",
        "Factuurdocument Bekijken"
    ),
    "طباعة / حفظ كـ PDF": (
        "Print / Save as PDF",
        "Afdrukken / Opslaan als PDF"
    ),
    "إغلاق": (
        "Close",
        "Sluiten"
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
    "المبلغ باليورو (€):": (
        "Amount in EUR (€):",
        "Bedrag in EUR (€):"
    ),
    "نوع المعاملة:": (
        "Transaction Type:",
        "Transactietype:"
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
    "حفظ وإدراج في السجلات": (
        "Save & Post to Ledger",
        "Opslaan & Boeken in Grootboek"
    ),
    "إلغاء": (
        "Cancel",
        "Annuleren"
    ),
    "إنشاء وتوليد فاتورة إلكترونية": (
        "Generate Compliant E-Invoice",
        "Conforme E-Factuur Aanmaken"
    ),
    "أدخل بيانات الفاتورة لتوليدها وتشفيرها بنظام UBL 2.1 الأوروبي المعتمد": (
        "Enter invoice telemetry to generate certified, encrypted European UBL 2.1 XML documents",
        "Voer factuurgegevens in om gecertificeerde, versleutelde Europese UBL 2.1 XML-documenten te genereren"
    ),
    "اسم العميل أو المؤسسة:": (
        "Client / Enterprise Name:",
        "Klant- of Bedrijfsnaam:"
    ),
    "المبلغ الصافي (€):": (
        "Net Amount (€):",
        "Nettobedrag (€):"
    ),
    "نسبة الضريبة (BTW / VAT):": (
        "VAT Rate (BTW / Belasting):",
        "BTW-tarief (BTW / Belasting):"
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
    "إجمالي الإيرادات السنوية التقديرية:": (
        "Estimated Annual Gross Revenue:",
        "Geschatte Bruto Jaaromzet:"
    ),
    "التدفقات النقدية الصافية المحققة:": (
        "Realized Net Operating Cash Flow:",
        "Gerealiseerde Netto Cashflow:"
    ),
    "الضريبة المقدرة المحتسبة:": (
        "Estimated Tax Liability:",
        "Berekende Belastingverplichting:"
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

    # Presentation Bar
    "وضع العرض التقديمي للزبائن (Presentation Mode)": (
        "Client Presentation Mode (Executive Walkthrough)",
        "Klantpresentatiemodus (Executive Ervaring)"
    ),
    "تم تفعيل اختصارات لوحة المفاتيح لوضع العرض التقديمي": (
        "Keyboard shortcuts enabled: [P] Toggle Mode • [Esc] Exit",
        "Sneltoetsen actief: [P] Presentatiemodus • [Esc] Sluiten"
    ),
    "الخروج من وضع العرض [Esc]": (
        "Exit Presentation Mode [Esc]",
        "Presentatiemodus Verlaten [Esc]"
    ),

    # Quick Add & Software Publish Modals
    "نشر وتوزيع برنامج جديد": (
        "Publish & Distribute Enterprise Application",
        "Nieuwe Software Publiceren & Distribueren"
    ),
    "اسم البرنامج أو التطبيق:": (
        "Application / Software Name:",
        "Software- of Applicatienaam:"
    ),
    "التصنيف والمنصة:": (
        "Category & Architecture:",
        "Categorie & Architectuur:"
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
    "وصف موجز ومميزات البرنامج:": (
        "Itemized Description & Features:",
        "Omschrijving & Kernfuncties:"
    ),
    "اكتب وصفاً موجزاً لما يقوم به البرنامج وكيف يساعد العملاء...": (
        "Briefly describe what this software accomplishes and how it creates value for clients...",
        "Beschrijf kort wat deze software doet en welke waarde het toevoegt voor zakelijke klanten..."
    ),
    "نشر البرنامج فورياً في المتجر 🚀": (
        "Publish App to Store 🚀",
        "Publiceer Software in Store 🚀"
    ),

    # Toast notifications and feedback
    "تم حفظ وتطبيق هوية": (
        "Successfully applied and saved custom brand identity",
        "Bedrijfsidentiteit succesvol toegepast en opgeslagen"
    ),
    "تمت استعادة هوية S&R CoreSync الأصلية ومسح التخصيص المحفوظ.": (
        "Restored default S&R CoreSync corporate identity and cleared custom cache.",
        "Standaard S&R CoreSync huisstijl hersteld en opgeslagen instellingen gewist."
    ),
    "تم تحميل ملف الشعار بنجاح! انقر على زر تطبيق الهوية لحفظه.": (
        "Emblem uploaded successfully! Click Apply Custom Brand to activate.",
        "Logo succesvol geüpload! Klik op Huisstijl Toepassen om te activeren."
    ),
    "تم توليد مفتاح تجريبي جديد:": (
        "Generated new trial license key:",
        "Nieuwe proeflicentiesleutel gegenereerd:"
    ),
    "تم نسخ المفتاح التجريبي:": (
        "Copied trial key to clipboard:",
        "Proeflicentiesleutel gekopieerd naar klembord:"
    ),
    "تم نسخ مفتاح الترخيص:": (
        "Copied license key to clipboard:",
        "Licentiesleutel gekopieerd naar klembord:"
    ),
    "تم نسخ المفتاح:": (
        "Copied key:",
        "Sleutel gekopieerd:"
    ),
    "تم التبديل إلى عملة:": (
        "Switched currency to:",
        "Valuta gewijzigd naar:"
    ),
    "تم تطبيق النظام الضريبي:": (
        "Applied tax regime:",
        "Belastingstelsel toegepast:"
    ),
    "مرحباً بك في الجولة الإرشادية التفاعلية!": (
        "Welcome to the Interactive Guided Tour!",
        "Welkom bij de interactieve rondleiding!"
    ),
    "اكتملت الجولة الإرشادية بنجاح!": (
        "Guided tour completed successfully!",
        "Rondleiding succesvol voltooid!"
    ),
    "خطوة 1 من 5": (
        "Step 1 of 5",
        "Stap 1 van 5"
    ),
    "إنهاء الجولة ✓": (
        "Finish Tour ✓",
        "Rondleiding Afronden ✓"
    ),
    "التالي ➡️": (
        "Next ➡️",
        "Volgende ➡️"
    ),
    "⬅️ السابق": (
        "⬅️ Previous",
        "⬅️ Vorige"
    ),
    "تمت إضافة المعاملة بنجاح وتحديث قيود الـ ERP والرسوم البيانية لحظياً!": (
        "Transaction posted successfully! Ledgers and KPI charts updated in real time.",
        "Transactie succesvol geregistreerd! Grootboeken en KPI-grafieken realtime bijgewerkt."
    ),
    "تم توليد وتشفير ملف Digipoort XML بنجاح!": (
        "Digipoort SBR XML generated and validated successfully!",
        "Digipoort SBR XML succesvol gegenereerd en gevalideerd!"
    ),
    "تم تنزيل ملف Digipoort XML الرسمي على جهازك!": (
        "Official Digipoort SBR XML file downloaded to your device!",
        "Officieel Digipoort SBR XML-bestand gedownload naar uw apparaat!"
    ),
    "بدأ تنزيل حزمة التثبيت لـ": (
        "Starting installation download for",
        "Installatiepakket downloaden voor"
    ),
    "تم نشر برنامج": (
        "Successfully published application",
        "Software succesvol gepubliceerd"
    ),
    "بنجاح في متجر المنصة!": (
        "to the Enterprise Software Hub!",
        "in de Enterprise Software Hub!"
    ),
    "اكتمل تدقيق الامتثال الضريبي بنجاح: متوافق بنسبة 100%!": (
        "AWR compliance audit completed: 100% Tax Compliant!",
        "AWR compliance audit voltooid: 100% Fiscaal Conform!"
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

# Guided Tour Steps Texts
TOUR_STEPS = {
    'en': {
        "title_sim": "⚡ Live Currency & Tax Simulator Bar",
        "desc_sim": "Allows clients to switch dynamically between EUR, USD, and SAR with instantaneous recalculation of 21% Dutch BTW and 15% GCC VAT across all metrics.",
        "title_kpi": "📊 Executive Financial KPI Dashboard",
        "desc_kpi": "Accurate metrics tracking annual gross revenue, net operational cash flow, compliance rates, and automated work hours saved.",
        "title_erp": "📦 Enterprise ERP & Warehouse Telemetry",
        "desc_erp": "Distributed multi-branch inventory tracking, real-time dispatch monitoring, and AI-driven reorder predictions.",
        "title_inv": "🧾 E-Invoicing & European Tax Compliance",
        "desc_inv": "Generates encrypted invoices compliant with EU EN 16931 standards, integrated with iDEAL and SEPA instant bank rails.",
        "title_sw": "💻 Software Marketplace & S&R TaxSync Vault",
        "desc_sw": "Instant digital licenses, integrated BTW calculator, and 14-day trial key generator operating at the click of a button."
    },
    'nl': {
        "title_sim": "⚡ Live Valuta & BTW Simulator Bar",
        "desc_sim": "Maakt realtime wisselen tussen EUR, USD en SAR mogelijk met directe herberekening van 21% BTW en 15% GCC belasting over alle widgets.",
        "title_kpi": "📊 Zakelijk Financieel KPI Dashboard",
        "desc_kpi": "Nauwkeurige KPI-indicatoren voor jaaromzet, netto operationele cashflow, nalevingspercentages en bespaarde werkuren.",
        "title_erp": "📦 Enterprise ERP & Magazijntelemetrie",
        "desc_erp": "Gedistribueerd voorraadbeheer over meerdere vestigingen, realtime tracking en automatische herbestellingen.",
        "title_inv": "🧾 E-Facturatie & BTW Naleving",
        "desc_inv": "Versleutelde facturen conform Europese norm EN 16931, geïntegreerd met iDEAL en SEPA-overschrijvingen.",
        "title_sw": "💻 Softwaremarktplaats & S&R TaxSync Kluis",
        "desc_sw": "Directe licentiesleutels, ingebouwde BTW-calculator en geverifieerde 14-dagen proeflicentie met één klik."
    }
}

# AI Copilot Dynamic Responses
AI_RESPONSES = {
    'en': {
        'october': "Based on the reconciliation of October general ledgers and Cloud ERP records:\\n- Gross Realized Revenue: €144,500 (+18% record quarterly growth).\\n- Operating Profit Margin: 27.4%, outperforming Dutch sector averages.\\n- Strategic Recommendation: Accelerate collection of an outstanding €42,000 receivable due October 10 to maximize reinvestment capital in distributed cloud nodes.",
        'invoices': "There is currently 1 pending invoice (€35,000) for a corporate client in Riyadh maturing within 14 days under a verified Reverse Charge clause. Zero delinquent receivables exceed 30 days due to automated multi-channel reminders.",
        'general': "Your inquiry was processed by the S&R CoreSync Financial Engine. Financial and operational ledgers are in full synchronization. RPA automated workflows are projected to save your enterprise team 35 billable hours next month via instant document archiving."
    },
    'nl': {
        'october': "Op basis van de afstemming van de grootboeken en het Cloud ERP-systeem voor oktober:\\n- Gerealiseerde Bruto Omzet: €144.500 (+18% record kwartaalgroei).\\n- Operationele Winstmarge: 27,4%, ruim boven het Nederlandse sectorgemiddelde.\\n- Strategisch Advies: Versnel incasso van openstaande vordering van €42.000 (vervalt 10 oktober) ter versterking van liquiditeit voor cloudinvesteringen.",
        'invoices': "Er is momenteel 1 openstaande factuur van €35.000 voor een zakelijke cliënt in Riyad, vervallend binnen 14 dagen met correcte BTW-verlegging. Er zijn nul achterstallige posten ouder dan 30 dagen dankzij automatische herinneringen.",
        'general': "Uw vraag is geanalyseerd door de S&R CoreSync Financiële Engine. Alle systemen werken naadloos samen tussen boekhouding en operatie. RPA-automatisering bespaart uw team komende maand circa 35 declarabele uren via directe documentarchivering."
    }
}

def build_portal(lang):
    c = ar_master

    # 1. HTML tag attributes
    c = c.replace('<html lang="ar" dir="rtl">', f'<html lang="{lang}" dir="ltr" data-page-language="{lang}">')

    # 2. Update Asset and Script paths for child folder en/ or nl/
    c = c.replace('href="assets/', 'href="../assets/')
    c = c.replace('src="assets/', 'src="../assets/')
    c = c.replace('href="./assets/', 'href="../assets/')
    c = c.replace('src="./assets/', 'src="../assets/')
    c = c.replace('href="css/', 'href="../css/')
    c = c.replace('src="js/', 'src="../js/')

    # 3. Update Return Links
    # href="index.html" stays "index.html" because it lands in the localized homepage!
    c = c.replace('href="logo-studio.html"', 'href="../logo-studio.html"')

    # 4. Remove auto-redirect query param script from localized pages
    c = re.sub(r'<!-- Language Auto-Redirect from Query Param.*?-->\s*<script>.*?</script>', '', c, flags=re.DOTALL)

    # 5. Inject Proper Language Switcher
    if lang == 'en':
        switcher_html = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Language">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="demo.html" class="portal-lang-btn active" title="English">🇬🇧 EN</a>
                <a href="../nl/demo.html" class="portal-lang-btn" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
    else: # nl
        switcher_html = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Taal">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="../en/demo.html" class="portal-lang-btn" title="English">🇬🇧 EN</a>
                <a href="demo.html" class="portal-lang-btn active" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
    # Replace existing language switcher if present, or inject before return button
    if 'portal-lang-switcher' in c:
        c = re.sub(r'<div class="portal-lang-switcher".*?</div>', switcher_html.strip(), c, flags=re.DOTALL)
    else:
        c = re.sub(r'(<a href="\.\./logo-studio\.html"[^>]*>)', switcher_html + '\n            \\1', c, count=1)

    # 6. Apply Dictionary Replacements (Sorted by length descending)
    sorted_dict = sorted(DICT.items(), key=lambda x: len(x[0]), reverse=True)
    idx = 0 if lang == 'en' else 1
    for ar_str, trans_pair in sorted_dict:
        target_trans = trans_pair[idx]
        c = c.replace(ar_str, target_trans)

    # 7. Guided Tour Replacement in JS
    ts = TOUR_STEPS[lang]
    c = c.replace("title: '⚡ محاكي العملات والضرائب اللحظي (Simulator Bar)'", f"title: '{ts['title_sim']}'")
    c = c.replace("desc: 'يتيح للزبون التبديل اللحظي بين اليورو والدولار والريال السعودي مع احتساب مباشر لضريبة القيمة المضافة BTW 21% والخليجية 15% وتحديث الأرقام فورياً.'", f"desc: '{ts['desc_sim']}'")
    c = c.replace("title: '📊 لوحة القيادة والتدفق المالي (Financial KPIs)'", f"title: '{ts['title_kpi']}'")
    c = c.replace("desc: 'مؤشرات مالية دقيقة للإيرادات السنوية، التدفقات النقدية الصافية، ونسبة الامتثال والأتمتة الموفرة لساعات العمل.'", f"desc: '{ts['desc_kpi']}'")
    c = c.replace("title: '📦 إدارة الـ ERP والمخازن الذكية'", f"title: '{ts['title_erp']}'")
    c = c.replace("desc: 'وحدة الـ ERP الموزعة لإدارة الفروع المتعددة، تتبع سلاسل التوريد، والتنبؤ بالطلب بدقة عالية.'", f"desc: '{ts['desc_erp']}'")
    c = c.replace("title: '🧾 الفواتير الإلكترونية والامتثال الضريبي الأوروبي'", f"title: '{ts['title_inv']}'")
    c = c.replace("desc: 'إنشاء الفواتير المشفرة بنظام EN 16931 الأوروبي وتوافق كامل مع بوابات الدفع iDEAL والتحويل المصرفي SEPA.'", f"desc: '{ts['desc_inv']}'")
    c = c.replace("title: '💻 سوق البرمجيات وحاسبة S&R TaxSync'", f"title: '{ts['title_sw']}'")
    c = c.replace("desc: 'تراخيص رقمية فورية، حاسبة ضريبة BTW مدمجة، ومولد مفاتيح تجريبية (14 يوماً) يعمل بضغطة زر مع تنزيل فوري.'", f"desc: '{ts['desc_sw']}'")

    # 8. Tour Steps Navigation Strings in JS
    if lang == 'en':
        c = c.replace("`خطوة ${currentTourStep + 1} من ${tourSteps.length}`", "`Step ${currentTourStep + 1} of ${tourSteps.length}`")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Finish Tour ✓' : 'Next ➡️';")
        c = c.replace("showPortalToast('🚀 مرحباً بك في الجولة الإرشادية التفاعلية!');", "showPortalToast('🚀 Welcome to the Interactive Guided Tour!');")
        c = c.replace("showPortalToast('🎉 اكتملت الجولة الإرشادية بنجاح!');", "showPortalToast('🎉 Guided Tour Completed Successfully!');")
    else:
        c = c.replace("`خطوة ${currentTourStep + 1} من ${tourSteps.length}`", "`Stap ${currentTourStep + 1} van ${tourSteps.length}`")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Rondleiding Afronden ✓' : 'Volgende ➡️';")
        c = c.replace("showPortalToast('🚀 مرحباً بك في الجولة الإرشادية التفاعلية!');", "showPortalToast('🚀 Welkom bij de interactieve rondleiding!');")
        c = c.replace("showPortalToast('🎉 اكتملت الجولة الإرشادية بنجاح!');", "showPortalToast('🎉 Rondleiding succesvol voltooid!');")

    # 9. AI Copilot Script Strings
    ai = AI_RESPONSES[lang]
    # Replace October response
    c = re.sub(
        r'aiResponse = "بناءً على مطابقة دفاتر المحاسبة.*?;',
        f'aiResponse = "{ai["october"]}";',
        c
    )
    # Replace Invoices response
    c = re.sub(
        r'aiResponse = "توجد فاتورة واحدة معلقة.*?;',
        f'aiResponse = "{ai["invoices"]}";',
        c
    )
    # Replace General response
    c = re.sub(
        r'aiResponse = "تم تحليل استفسارك عبر خوارزمية.*?;',
        f'aiResponse = "{ai["general"]}";',
        c
    )

    # 10. Default Client Names in White-Label Logic
    if lang == 'en':
        c = c.replace("'مجموعة الرياض للخدمات اللوجستية'", "'Riyadh Logistics Group BV'")
        c = c.replace("'مجموعة الشريك التجاري المستهدف'", "'Enterprise Partner Organization'")
        c = c.replace("'جلسة معاينة تفاعلية'", "'Interactive Demo Session'")
    else:
        c = c.replace("'مجموعة الرياض للخدمات اللوجستية'", "'Riyadh Logistics Group BV'")
        c = c.replace("'مجموعة الشريك التجاري المستهدف'", "'Enterprise Partner Organisatie'")
        c = c.replace("'جلسة معاينة تفاعلية'", "'Interactieve Demosessie'")

    return c

print("Building 100% localized English portal...")
en_output = build_portal('en')
with open(DEMO_EN_PATH, 'w', encoding='utf-8') as f:
    f.write(en_output)
print(f"Generated {DEMO_EN_PATH} ({len(en_output)} bytes)")

print("Building 100% localized Dutch portal...")
nl_output = build_portal('nl')
with open(DEMO_NL_PATH, 'w', encoding='utf-8') as f:
    f.write(nl_output)
print(f"Generated {DEMO_NL_PATH} ({len(nl_output)} bytes)")

print("Done generating localized portals!")
