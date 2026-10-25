# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - Multilingual Demo Generator
Generates full, culturally-accurate, production-ready EN and NL localized versions of demo.html
and injects the language switcher into AR demo.html.
"""

import os
import re

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(PROJECT_DIR, 'demo.html')
DEMO_EN_PATH = os.path.join(PROJECT_DIR, 'en', 'demo.html')
DEMO_NL_PATH = os.path.join(PROJECT_DIR, 'nl', 'demo.html')

with open(DEMO_AR_PATH, 'r', encoding='utf-8') as f:
    ar_content = f.read()

# 1. Update Arabic demo.html with Language Switcher and Redirect Helper if not present
ar_redirect_script = """
    <!-- Language Auto-Redirect from Query Param (?lang=en / ?lang=nl) -->
    <script>
    (function() {
        var params = new URLSearchParams(window.location.search);
        var l = (params.get('lang') || '').toLowerCase();
        if (l === 'en') {
            window.location.replace('en/demo.html' + (window.location.hash || ''));
        } else if (l === 'nl') {
            window.location.replace('nl/demo.html' + (window.location.hash || ''));
        }
    })();
    </script>
"""

ar_lang_switcher = """
            <!-- محول اللغة السحابي المتكامل -->
            <div class="portal-lang-switcher" aria-label="تبديل لغة المنصة">
                <a href="demo.html" class="portal-lang-btn active" title="العربية">🇸🇦 AR</a>
                <a href="en/demo.html" class="portal-lang-btn" title="English">🇬🇧 EN</a>
                <a href="nl/demo.html" class="portal-lang-btn" title="Nederlands">🇳🇱 NL</a>
            </div>
"""

updated_ar = ar_content
if 'Language Auto-Redirect' not in updated_ar:
    updated_ar = updated_ar.replace('</head>', ar_redirect_script + '\n</head>', 1)

if 'portal-lang-switcher' not in updated_ar:
    # insert switcher before btn-return-main
    updated_ar = re.sub(r'(<a href="logo-studio\.html"[^>]*>)', ar_lang_switcher + '\n            \\1', updated_ar, count=1)

with open(DEMO_AR_PATH, 'w', encoding='utf-8') as f:
    f.write(updated_ar)
print("Updated AR demo.html with language switcher & redirect helper!")

# Build comprehensive translation dictionary
TRANSLATIONS = {
    # Head & Meta
    'S&R CoreSync | المنصة السحابية التجريبية (Live Interactive Demo Portal)': {
        'en': 'S&R CoreSync | Live Interactive Cloud ERP Portal (Demo)',
        'nl': 'S&R CoreSync | Live Interactieve Cloud ERP Portal (Demo)'
    },
    'النظام السحابي متصل (EU Node)': {
        'en': 'Cloud System Online (EU Node)',
        'nl': 'Cloud Systeem Online (EU Node)'
    },
    'بدء جولة إرشادية خطواتية توضح مزايا المنصة للزبون': {
        'en': 'Start interactive step-by-step guided tour of platform features',
        'nl': 'Start interactieve stapsgewijze rondleiding langs platformfuncties'
    },
    '🚀 ابدأ الجولة': {
        'en': '🚀 Start Tour',
        'nl': '🚀 Start Rondleiding'
    },
    'تصدير بطاقة العرض التنفيذي إلى ملف PDF أنيق للعميل': {
        'en': 'Export executive proposal brief to an elegant client PDF',
        'nl': 'Exporteer zakelijk voorsteloverzicht naar een elegante PDF'
    },
    'ملخص العرض (PDF)': {
        'en': 'Brief Summary (PDF)',
        'nl': 'Offerte Overzicht (PDF)'
    },
    'وضع العرض التقديمي للزبائن (شاشة كاملة وتجربة تنفيذية)': {
        'en': 'Client presentation mode (Full screen & executive walkthrough)',
        'nl': 'Klantpresentatiemodus (Volledig scherm en executive ervaring)'
    },
    'عرض الزبائن [P]': {
        'en': 'Client View [P]',
        'nl': 'Klantpresentatie [P]'
    },
    'نقل تفضيلات الجلسة وحجز موعد استشاري': {
        'en': 'Transfer session settings and book an executive consultation',
        'nl': 'Draag sessie-instellingen over en plan een zakelijk consult'
    },
    'حجز استشارة بهذا النظام': {
        'en': 'Book Session with this Architecture',
        'nl': 'Plan Consult met dit Systeem'
    },
    'استوديو ومحرر الشعار': {
        'en': 'Emblem & Brand Identity Studio',
        'nl': 'Embleem & Merkidentiteit Studio'
    },
    'استوديو الشعار': {
        'en': 'Emblem Studio',
        'nl': 'Embleem Studio'
    },
    'العودة للصفحة الرئيسية - S&R CoreSync For Intelligent Solutions': {
        'en': 'Return to Homepage - S&R CoreSync For Intelligent Solutions',
        'nl': 'Terug naar Homepage - S&R CoreSync For Intelligent Solutions'
    },
    'العودة للموقع': {
        'en': 'Return to Website',
        'nl': 'Terug naar Website'
    },
    # Sidebar
    'لوحة القيادة المالية': {
        'en': 'Financial KPI Dashboard',
        'nl': 'Financieel KPI Dashboard'
    },
    'إدارة الـ ERP والمخازن': {
        'en': 'ERP & Inventory Ops',
        'nl': 'ERP & Voorraadbeheer'
    },
    'الفواتير والتدفقات النقدية': {
        'en': 'Invoicing & Cash Flow',
        'nl': 'Facturen & Cashflow'
    },
    'المساعد المالي الذكي (AI)': {
        'en': 'AI Financial Copilot',
        'nl': 'AI Financiële Copilot'
    },
    'حالة الخوادم السحابية': {
        'en': 'Cloud Server Status',
        'nl': 'Cloud Serverstatus'
    },
    'تخصيص الهوية (White-Label)': {
        'en': 'White-Label Branding',
        'nl': 'White-Label Personalisatie'
    },
    'سوق البرمجيات (Software Hub)': {
        'en': 'Software Hub',
        'nl': 'Software Hub'
    },
    'تكامل مع الإدارة': {
        'en': 'Enterprise Integration',
        'nl': 'Zakelijke Integratie'
    },
    'طلب تفعيل لشركتك': {
        'en': 'Request Company Activation',
        'nl': 'Vraag Bedrijfsactivatie Aan'
    },
    'انقل تفاصيل الجلسة والسيناريوهات المجرّبة مباشرة لاستشارة المؤسسين.': {
        'en': 'Transfer session configurations and tested scenarios directly to the founders consultation.',
        'nl': "Draag sessie-inzichten en geteste scenario's direct over naar het oprichtersconsult."
    },
    'حجز استشارة مخصصة': {
        'en': 'Book Custom Consultation',
        'nl': 'Plan Maatwerk Consult'
    },
    'جلسة معاينة تفاعلية': {
        'en': 'Interactive Preview Session',
        'nl': 'Interactieve Previewsessie'
    },
    # Tab 1: Overview & VAT Simulator
    'محاكي العملات والضرائب الحي (Live Currency & VAT Simulator):': {
        'en': 'Live Currency & VAT Simulator:',
        'nl': 'Live Valuta & BTW Simulator:'
    },
    'العملة:': {
        'en': 'Currency:',
        'nl': 'Valuta:'
    },
    'النظام الضريبي:': {
        'en': 'Tax Regime:',
        'nl': 'Belastingstelsel:'
    },
    'اختيار النظام الضريبي المالي': {
        'en': 'Select financial tax regime',
        'nl': 'Selecteer belastingstelsel'
    },
    '🇳🇱 BTW هولندي (21%)': {
        'en': '🇳🇱 Dutch BTW (21%)',
        'nl': '🇳🇱 Nederlandse BTW (21%)'
    },
    '🇳🇱 BTW مخفض (9%)': {
        'en': '🇳🇱 Reduced BTW (9%)',
        'nl': '🇳🇱 Verlaagd BTW-tarief (9%)'
    },
    '🇸🇦 ضريبة خليجية (15%)': {
        'en': '🇸🇦 GCC VAT (15%)',
        'nl': '🇸🇦 GCC Btw (15%)'
    },
    '🌐 معفى ضريبياً (0%)': {
        'en': '🌐 Tax Exempt (0%)',
        'nl': '🌐 Vrijgesteld van belasting (0%)'
    },
    'الضريبة المحتسبة:': {
        'en': 'Estimated Tax:',
        'nl': 'Berekende Belasting:'
    },
    'لوحة القيادة والتدفق المالي اللحظي': {
        'en': 'Real-Time Financial Dashboard & Cash Flow Telemetry',
        'nl': 'Realtime Financieel Dashboard & Cashflow Telemetrie'
    },
    'نظام محاكاة حي لحركات الحسابات والإيرادات والمصروفات السحابية المؤتمتة': {
        'en': 'Live simulation engine for automated enterprise revenue, cloud expenses, and cash telemetry',
        'nl': 'Live simulatiesysteem voor geautomatiseerde bedrijfsinkomsten, clouduitgaven en cashflow'
    },
    'تسجيل معاملة تجريبية': {
        'en': 'Record Test Transaction',
        'nl': 'Registreer Testtransactie'
    },
    'إجمالي الإيرادات السنوية': {
        'en': 'Annual Gross Revenue',
        'nl': 'Totale Jaaromzet'
    },
    'مقارنة بالربع السابق': {
        'en': 'vs previous quarter',
        'nl': 't.o.v. vorig kwartaal'
    },
    'التدفقات النقدية الصافية': {
        'en': 'Net Operating Cash Flow',
        'nl': 'Netto Operationele Cashflow'
    },
    'هامش ربحية تشغيلية': {
        'en': 'operating profit margin',
        'nl': 'operationele winstmarge'
    },
    'طلبات الـ ERP المنجزة': {
        'en': 'Completed ERP Orders',
        'nl': 'Voltooide ERP Orders'
    },
    'نسبة الامتثال والدقة': {
        'en': 'compliance and accuracy rate',
        'nl': 'nalevings- en nauwkeurigheidsgraad'
    },
    'عمليات الأتمتة الموفرة': {
        'en': 'Automated Work Hours Saved',
        'nl': 'Bespaarde Automatiseringsuren'
    },
    'وفر شهري مباشر في وقت الفريق': {
        'en': 'Direct monthly time saved for your team',
        'nl': 'Directe maandelijkse tijdsbesparing voor uw team'
    },
    'ساعة': {
        'en': 'hours',
        'nl': 'uur'
    },
    'حركة الإيرادات والتدفق النقدي الشهري (€)': {
        'en': 'Monthly Revenue & Cash Flow Trajectory (€)',
        'nl': 'Maandelijkse Omzet & Cashflow Traject (€)'
    },
    'توزيع العمليات حسب القطاع': {
        'en': 'Operational Breakdown by Sector',
        'nl': 'Operationele Verdeling per Sector'
    },
    'سجل العمليات والربط المحاسبي المباشر': {
        'en': 'Live Ledger Transactions & Accounting Bridge',
        'nl': 'Live Grootboektransacties & Boekhoudkoppeling'
    },
    'مزامنة سحابية لحظية': {
        'en': 'Real-time cloud synchronization',
        'nl': 'Realtime cloudsynchronisatie'
    },
    'رقم المعاملة': {
        'en': 'Tx ID',
        'nl': 'Transactie-ID'
    },
    'الجهة / العميل': {
        'en': 'Client / Entity',
        'nl': 'Klant / Entiteit'
    },
    'التاريخ': {
        'en': 'Date',
        'nl': 'Datum'
    },
    'النوع / القسم': {
        'en': 'Category / Module',
        'nl': 'Categorie / Module'
    },
    'المبلغ': {
        'en': 'Amount',
        'nl': 'Bedrag'
    },
    'الحالة والامتثال': {
        'en': 'Status & Compliance',
        'nl': 'Status & Naleving'
    },
    'مكتملة (SEPA)': {
        'en': 'Completed (SEPA)',
        'nl': 'Voltooid (SEPA)'
    },
    'تمت التسوية (iDEAL)': {
        'en': 'Settled (iDEAL)',
        'nl': 'Verrekend (iDEAL)'
    },
    'قيد المعالجة السحابية': {
        'en': 'Processing (Cloud)',
        'nl': 'In verwerking (Cloud)'
    },
    # Tab 2: ERP & Inventory
    'نظام إدارة الموارد المؤسسية (ERP) والمخازن الذكية': {
        'en': 'Enterprise Resource Planning (ERP) & Smart Warehouse Ops',
        'nl': 'Enterprise Resource Planning (ERP) & Slim Voorraadbeheer'
    },
    'إدارة المخزون متعدد الفروع، تتبع سلاسل التوريد، والتنبؤ التلقائي بالنواقص': {
        'en': 'Multi-branch warehouse management, supply chain telemetry, and automated reorder triggers',
        'nl': 'Voorraadbeheer voor meerdere vestigingen, supply chain telemetrie en automatische herbestellingen'
    },
    'إضافة منتج للمخزون': {
        'en': 'Add Inventory Item',
        'nl': 'Artikel Toevoegen'
    },
    'إجمالي عناصر المخزون': {
        'en': 'Total Active Inventory Items',
        'nl': 'Totaal Actieve Artikelen'
    },
    'منتج مسجل عبر الفروع': {
        'en': 'registered across branches',
        'nl': 'geregistreerd over vestigingen'
    },
    'مستودعات نشطة': {
        'en': 'Connected Fulfillment Hubs',
        'nl': 'Gekoppelde Fulfilment Hubs'
    },
    'أمستردام، روتردام، الرياض، دبي': {
        'en': 'Amsterdam, Rotterdam, Riyadh, Dubai',
        'nl': 'Amsterdam, Rotterdam, Riyad, Dubai'
    },
    'قيمة البضاعة المخزنة': {
        'en': 'Total Valuation of Stock',
        'nl': 'Totale Voorraadwaarde'
    },
    'جاهزية التوزيع السريع': {
        'en': 'Express fulfillment readiness',
        'nl': 'Snelle leveringsgereedheid'
    },
    'تنبيهات نقص المخزون': {
        'en': 'Low Stock Critical Alerts',
        'nl': 'Kritieke Voorraadwaarschuwingen'
    },
    'أوامر شراء مؤتمتة جاهزة': {
        'en': 'Automated POs ready for approval',
        'nl': 'Automatische inkooporders gereed'
    },
    'جدول المخزون والمواد اللحظي': {
        'en': 'Live Warehouse Inventory Ledger',
        'nl': 'Live Magazijnvoorraad Grootboek'
    },
    'تحديث حي لكميات الفروع': {
        'en': 'Real-time multi-branch stock telemetry',
        'nl': 'Realtime voorraadtelemetrie over vestigingen'
    },
    'رمز SKU': {
        'en': 'SKU Code',
        'nl': 'SKU-code'
    },
    'اسم المادة / المنتج': {
        'en': 'Product / Item Name',
        'nl': 'Product- / Artikelnaam'
    },
    'المستودع الرئيسي': {
        'en': 'Assigned Warehouse Hub',
        'nl': 'Toegewezen Magazijnhub'
    },
    'الكمية المتوفرة': {
        'en': 'Available Qty',
        'nl': 'Beschikbare Aantal'
    },
    'سعر الوحدة': {
        'en': 'Unit Price',
        'nl': 'Eenheidsprijs'
    },
    'حالة التوفر': {
        'en': 'Stock Status',
        'nl': 'Voorraadstatus'
    },
    'الإجراء': {
        'en': 'Action',
        'nl': 'Actie'
    },
    'متوفر بكثرة': {
        'en': 'In Stock (Optimal)',
        'nl': 'Op voorraad (Optimaal)'
    },
    'مستوى آمن': {
        'en': 'In Stock (Safe)',
        'nl': 'Op voorraad (Veilig)'
    },
    'نقص حرج ⚠️': {
        'en': 'Low Stock Critical ⚠️',
        'nl': 'Kritieke Lage Voorraad ⚠️'
    },
    'طلب فوري': {
        'en': 'Order Now',
        'nl': 'Bestel Nu'
    },
    'تفاصيل': {
        'en': 'Details',
        'nl': 'Details'
    },
    # Tab 3: Invoices & Cashflow
    'منظومة الفواتير الإلكترونية والتدفق النقدي الأوروبي': {
        'en': 'Enterprise E-Invoicing & European Cash Flow Architecture',
        'nl': 'Zakelijke E-Facturatie & Europese Cashflow Architectuur'
    },
    'إصدار فواتير مشفرة متوافقة مع معايير الاتحاد الأوروبي (EN 16931) والربط المباشر مع iDEAL وSEPA': {
        'en': 'Issue encrypted invoices compliant with European EN 16931 standards with direct iDEAL and SEPA integration',
        'nl': 'Genereer versleutelde facturen conform Europese EN 16931-normen met directe iDEAL- en SEPA-integratie'
    },
    'إصدار فاتورة جديدة': {
        'en': 'Create New Invoice',
        'nl': 'Nieuwe Factuur Maken'
    },
    'سجل الفواتير الضريبية المعتمدة': {
        'en': 'Certified Tax Invoice Ledger',
        'nl': 'Gecertificeerd Belastingfactuuroverzicht'
    },
    'أرشيف رقمي فوري غير قابل للتلاعب': {
        'en': 'Immutable real-time digital archive',
        'nl': 'Onveranderlijk digitaal realtime archief'
    },
    'رقم الفاتورة': {
        'en': 'Invoice No.',
        'nl': 'Factuurnummer'
    },
    'العميل / المؤسسة': {
        'en': 'Client / Enterprise',
        'nl': 'Klant / Onderneming'
    },
    'تاريخ الإصدار': {
        'en': 'Issue Date',
        'nl': 'Factuurdatum'
    },
    'المبلغ الإجمالي': {
        'en': 'Total Amount',
        'nl': 'Totaalbedrag'
    },
    'ضريبة BTW': {
        'en': 'BTW Tax',
        'nl': 'BTW Bedrag'
    },
    'حالة الدفع': {
        'en': 'Payment Status',
        'nl': 'Betaalstatus'
    },
    'معاينة': {
        'en': 'Preview',
        'nl': 'Bekijken'
    },
    'مدفوعة (iDEAL)': {
        'en': 'Paid (iDEAL)',
        'nl': 'Betaald (iDEAL)'
    },
    'مدفوعة (SEPA)': {
        'en': 'Paid (SEPA)',
        'nl': 'Betaald (SEPA)'
    },
    'بانتظار السداد': {
        'en': 'Pending Payment',
        'nl': 'In afwachting'
    },
    # Tab 4: AI Financial Copilot
    'المساعد المالي والتشغيلي الذكي (S&R Autonomous AI Copilot)': {
        'en': 'S&R Autonomous AI Financial & Operational Copilot',
        'nl': 'S&R Autonome Financiële & Operationele AI Copilot'
    },
    'اسأل خوارزميات الذكاء الاصطناعي لتحليل البيانات، توقع الأرباح، واكتشاف الأخطاء المحاسبية': {
        'en': 'Consult proprietary AI models for telemetry analysis, cash flow forecasting, and tax audit anomaly detection',
        'nl': 'Raadpleeg AI-modellen voor telemetrie-analyse, cashflowvoorspellingen en BTW-audit anomaliedetectie'
    },
    'تحليل التدفق النقدي للربع الرابع': {
        'en': 'Analyze Q4 cash flow forecast',
        'nl': 'Analyseer cashflowvoorspelling Q4'
    },
    'فحص إقرارات ضريبة القيمة المضافة BTW': {
        'en': 'Audit BTW tax return compliance',
        'nl': 'Controleer BTW-aangiftenaleving'
    },
    'توقع المخزون الناقص للشهر القادم': {
        'en': 'Forecast stockout risks for next month',
        'nl': 'Voorspel voorraadtekorten voor volgende maand'
    },
    'مرحبا! أنا مساعد S&R الذكي. تم تدريبي على دفاتر حساباتك السحابية ومعايير التدقيق المالي الأوروبية. كيف يمكنني مساعدتك اليوم؟': {
        'en': 'Welcome! I am the S&R Autonomous Copilot, trained on your cloud ledgers and European audit standards. How can I assist you today?',
        'nl': 'Welkom! Ik ben de S&R Autonome Copilot, getraind op uw cloudgrootboeken en Europese auditnormen. Hoe kan ik u vandaag helpen?'
    },
    'اكتب سؤالك المالي أو الإداري هنا...': {
        'en': 'Type your financial or operational query here...',
        'nl': 'Typ hier uw financiële of operationele vraag...'
    },
    'إرسال': {
        'en': 'Send',
        'nl': 'Versturen'
    },
    # Tab 5: Cloud Status
    'حالة البنية التحتية السحابية (Enterprise Cloud Telemetry)': {
        'en': 'Enterprise Cloud Infrastructure & Node Telemetry',
        'nl': 'Enterprise Cloudinfrastructuur & Servertelemetrie'
    },
    'مراقبة فورية لأداء الخوادم، زمن الاستجابة، ونسب الجاهزية التشغيلية (99.99%)': {
        'en': 'Real-time telemetry for multi-region server clusters, latency metrics, and 99.99% SLA uptime',
        'nl': 'Realtime telemetrie voor multi-regio serverclusters, latency metrics en 99.99% SLA uptime'
    },
    'العقدة السحابية': {
        'en': 'Cloud Node',
        'nl': 'Cloudnode'
    },
    'الموقع الجغرافي': {
        'en': 'Geographic Region',
        'nl': 'Geografische Regio'
    },
    'الحمل التشغيلي': {
        'en': 'CPU Load',
        'nl': 'CPU Belasting'
    },
    'زمن الاستجابة': {
        'en': 'Latency',
        'nl': 'Responstijd'
    },
    'الجاهزية': {
        'en': 'Uptime SLA',
        'nl': 'Uptime SLA'
    },
    'أمستردام (Node 01)': {
        'en': 'Amsterdam (Node 01)',
        'nl': 'Amsterdam (Node 01)'
    },
    'فرانكفورت (Node 02)': {
        'en': 'Frankfurt (Node 02)',
        'nl': 'Frankfurt (Node 02)'
    },
    'لندن (Node 03)': {
        'en': 'London (Node 03)',
        'nl': 'Londen (Node 03)'
    },
    'الرياض (Node 04)': {
        'en': 'Riyadh (Node 04)',
        'nl': 'Riyad (Node 04)'
    },
    'ممتازة': {
        'en': 'Optimal',
        'nl': 'Optimaal'
    },
    'نشط ومستقر': {
        'en': 'Active & Resilient',
        'nl': 'Actief & Stabiel'
    },
    # Tab 6: White-Label
    'استوديو تخصيص الهوية (White-Label Architecture)': {
        'en': 'White-Label Architecture & Brand Customizer',
        'nl': 'White-Label Architectuur & Merkpersonalisatie'
    },
    'أعد تخصيص ألوان المنصة، الشعار، والترويسة لتلائم الهوية البصرية لمؤسستك بضغطة زر': {
        'en': 'Tailor platform accent colors, corporate emblem, and branding to match your corporate identity instantly',
        'nl': 'Pas platformkleuren, het bedrijfslogo en de huisstijl direct aan op uw eigen bedrijfsidentiteit'
    },
    'اسم المؤسسة المعروض': {
        'en': 'Organization Display Name',
        'nl': 'Weergavenaam Organisatie'
    },
    'اللون الأساسي للواجهة': {
        'en': 'Primary Theme Hue',
        'nl': 'Primaire Interfacekleur'
    },
    'رفع شعار مخصص': {
        'en': 'Upload Custom Logo',
        'nl': 'Upload Aangepast Logo'
    },
    'تطبيق التغييرات حياً': {
        'en': 'Apply Live Changes',
        'nl': 'Wijzigingen Live Toepassen'
    },
    'إعادة تعيين للأصل': {
        'en': 'Reset to Sovereign Default',
        'nl': 'Herstel naar Standaard'
    },
    # Tab 7: Software Hub
    'سوق البرمجيات والتراخيص الرقمية (Software Hub)': {
        'en': 'Enterprise Software Hub & License Vault',
        'nl': 'Zakelijke Software Hub & Licentiekluis'
    },
    'استكشف البرمجيات المعتمدة، فعّل المفاتيح التجريبية الفورية (14 يوماً)، وحمّل النسخ الأصلية': {
        'en': 'Explore certified enterprise software, activate 14-day trial keys, and download desktop installers',
        'nl': 'Ontdek gecertificeerde software, activeer 14-dagen proeflicenties en download desktop installers'
    },
    'حاسبة الضرائب الهولندية والأوروبية الذكية لسطح المكتب': {
        'en': 'Desktop Smart Dutch BTW & EU Tax Compliance Calculator',
        'nl': 'Desktop Slimme Nederlandse BTW & EU Belastingcalculator'
    },
    'برنامج سطح مكتب متقدم لمحاسبي الشركات وأصحاب الأعمال لحساب وإقرار ضرائب BTW 21% و 9% وإصدار التقارير المعتمدة.': {
        'en': 'Advanced desktop software for corporate accountants and business owners to calculate and file 21% and 9% BTW with official audit reports.',
        'nl': 'Geavanceerde desktopsoftware voor bedrijfsaccountants en ondernemers om 21% en 9% BTW te berekenen en officiële rapporten te genereren.'
    },
    'توليد مفتاح تجريبي (14 يوماً)': {
        'en': 'Generate 14-Day Trial Key',
        'nl': 'Genereer 14-Dagen Proefsleutel'
    },
    'تحميل البرنامج (Windows)': {
        'en': 'Download Setup (Windows)',
        'nl': 'Download Installer (Windows)'
    },
    'شراء ترخيص تجاري': {
        'en': 'Buy Commercial License',
        'nl': 'Koop Zakelijke Licentie'
    },
    'تشغيل المحاكي السحابي': {
        'en': 'Launch Cloud Simulator',
        'nl': 'Start Cloud Simulator'
    },
    # Modals
    'تسجيل معاملة مالية جديدة': {
        'en': 'Record New Financial Transaction',
        'nl': 'Nieuwe Financiële Transactie Registreren'
    },
    'إصدار فاتورة إلكترونية معتمدة': {
        'en': 'Issue Certified Electronic Invoice',
        'nl': 'Gecertificeerde E-Factuur Maken'
    },
    'بوابة الدفع الإلكتروني (iDEAL)': {
        'en': 'iDEAL Secure Payment Gateway',
        'nl': 'iDEAL Veilige Betaalomgeving'
    },
    'معاينة الفاتورة الضريبية الرسمية': {
        'en': 'Official Certified Tax Invoice Preview',
        'nl': 'Officiële Belastingfactuur Bekijken'
    },
    'تفاصيل وترخيص البرنامج': {
        'en': 'Software Licensing & Technical Details',
        'nl': 'Softwarelicentie & Technische Details'
    },
    'محاكي برمجيات سطح المكتب السحابي': {
        'en': 'Virtual Desktop Software Cloud Sandbox',
        'nl': 'Virtuele Desktop Software Cloud Sandbox'
    },
    'شراء الترخيص التجاري الرقمي': {
        'en': 'Purchase Digital Commercial License',
        'nl': 'Koop Digitale Zakelijke Licentie'
    },
    'ملخص العرض التنفيذي وبطاقة التسعير': {
        'en': 'Executive Proposal Brief & Investment Summary',
        'nl': 'Zakelijk Voorsteloverzicht & Investeringsoverzicht'
    },
    'إلغاء': {
        'en': 'Cancel',
        'nl': 'Annuleren'
    },
    'حفظ المعاملة': {
        'en': 'Save Transaction',
        'nl': 'Transactie Opslaan'
    },
    'إصدار وتشفير': {
        'en': 'Issue & Encrypt',
        'nl': 'Aanmaken & Versleutelen'
    },
    'تأكيد الدفع التجريبي': {
        'en': 'Confirm Test Payment',
        'nl': 'Bevestig Testbetaling'
    },
    'طباعة الفاتورة': {
        'en': 'Print Invoice',
        'nl': 'Factuur Afdrukken'
    },
    'تحميل PDF': {
        'en': 'Download PDF',
        'nl': 'Download PDF'
    },
    'إغلاق': {
        'en': 'Close',
        'nl': 'Sluiten'
    },
    'طباعة الملخص': {
        'en': 'Print Brief',
        'nl': 'Overzicht Afdrukken'
    },
    'تنزيل وثيقة العرض': {
        'en': 'Download Proposal Document',
        'nl': 'Download Voorstel'
    }
}

def generate_localized_demo(target_lang):
    c = ar_content

    # 1. Update HTML tag and lang
    if target_lang == 'en':
        c = re.sub(r'<html[^>]*>', '<html lang="en" dir="ltr" data-page-language="en">', c, count=1)
    elif target_lang == 'nl':
        c = re.sub(r'<html[^>]*>', '<html lang="nl" dir="ltr" data-page-language="nl">', c, count=1)

    # 2. Fix asset relative paths (prepend ../ to relative paths since we are in a subfolder)
    c = re.sub(r'href="\./assets/', 'href="../assets/', c)
    c = re.sub(r'src="\./assets/', 'src="../assets/', c)
    c = re.sub(r'href="\./css/', 'href="../css/', c)
    c = re.sub(r'src="\./js/', 'src="../js/', c)
    c = re.sub(r'href="css/', 'href="../css/', c)
    c = re.sub(r'src="js/', 'src="../js/', c)
    c = re.sub(r'href="assets/', 'href="../assets/', c)
    c = re.sub(r'src="assets/', 'src="../assets/', c)

    # 3. Update return to homepage links
    c = c.replace('href="index.html"', 'href="index.html"') # in en/ or nl/, index.html points to local index!
    c = c.replace('href="logo-studio.html"', 'href="../logo-studio.html"')

    # 4. Inject Localized Language Switcher
    if target_lang == 'en':
        en_lang_switcher = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Language">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="demo.html" class="portal-lang-btn active" title="English">🇬🇧 EN</a>
                <a href="../nl/demo.html" class="portal-lang-btn" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
        c = re.sub(r'(<a href="\.\./logo-studio\.html"[^>]*>)', en_lang_switcher + '\n            \\1', c, count=1)

    elif target_lang == 'nl':
        nl_lang_switcher = """
            <!-- Multi-Language Portal Switcher -->
            <div class="portal-lang-switcher" aria-label="Portal Taal">
                <a href="../demo.html" class="portal-lang-btn" title="العربية">🇸🇦 AR</a>
                <a href="../en/demo.html" class="portal-lang-btn" title="English">🇬🇧 EN</a>
                <a href="demo.html" class="portal-lang-btn active" title="Nederlands">🇳🇱 NL</a>
            </div>
"""
        c = re.sub(r'(<a href="\.\./logo-studio\.html"[^>]*>)', nl_lang_switcher + '\n            \\1', c, count=1)

    # 5. Apply Exact Text Replacements
    for ar_text, trans_map in TRANSLATIONS.items():
        if target_lang in trans_map:
            trans_text = trans_map[target_lang]
            c = c.replace(ar_text, trans_text)

    # 6. Translate Guided Tour Steps in Script
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
        c = c.replace("document.getElementById('tourStepBadge').innerText = `خطوة ${currentTourStep + 1} من ${tourSteps.length}`;", "document.getElementById('tourStepBadge').innerText = `Step ${currentTourStep + 1} of ${tourSteps.length}`;")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Finish Tour ✓' : 'Next ➡️';")
        c = c.replace("'السابق'", "'Previous'")
        c = c.replace("'التالي'", "'Next'")
        c = c.replace("'إنهاء'", "'Finish'")

    elif target_lang == 'nl':
        c = c.replace("title: '⚡ محاكي العملات والضرائب اللحظي (Simulator Bar)'", "title: '⚡ Live Valuta & BTW Simulator Bar'")
        c = c.replace("desc: 'يتيح للزبون التبديل اللحظي بين اليورو والدولار والريال السعودي مع احتساب مباشر لضريبة القيمة المضافة BTW 21% والخليجية 15% وتحديث الأرقام فورياً.'", "desc: 'Maakt realtime wisselen tussen EUR, USD en SAR mogelijk met directe herberekening van 21% BTW en 15% GCC belasting over alle widgets.'")
        c = c.replace("title: '📊 لوحة القيادة والتدفق المالي (Financial KPIs)'", "title: '📊 Zakelijk Financieel KPI Dashboard'")
        c = c.replace("desc: 'مؤشرات مالية دقيقة للإيرادات السنوية، التدفقات النقدية الصافية، ونسبة الامتثال والأتمتة الموفرة لساعات العمل.'", "desc: 'Nauwkeurige KPI-indicatoren voor jaaromzet, netto operationele cashflow, nalevingspercentages en bespaarde werkuren.'")
        c = c.replace("title: '📦 إدارة الـ ERP والمخازن الذكية'", "title: '📦 Enterprise ERP & Magazijntelemetrie'")
        c = c.replace("desc: 'وحدة الـ ERP الموزعة لإدارة الفروع المتعددة، تتبع سلاسل التوريد، والتنبؤ بالطلب بدقة عالية.'", "desc: 'Gedistribueerd voorraadbeheer over meerdere vestigingen, realtime tracking en automatische herbestellingen.'")
        c = c.replace("title: '🧾 الفواتير الإلكترونية والامتثال الضريبي الأوروبي'", "title: '🧾 E-Facturatie & BTW Naleving'")
        c = c.replace("desc: 'إنشاء الفواتير المشفرة بنظام EN 16931 الأوروبي وتوافق كامل مع بوابات الدفع iDEAL والتحويل المصرفي SEPA.'", "desc: 'Versleutelde facturen conform Europese norm EN 16931, geïntegreerd met iDEAL en SEPA-overschrijvingen.'")
        c = c.replace("title: '💻 سوق البرمجيات وحاسبة S&R TaxSync'", "title: '💻 Softwaremarktplaats & S&R TaxSync Kluis'")
        c = c.replace("desc: 'تراخيص رقمية فورية، حاسبة ضريبة BTW مدمجة، ومولد مفاتيح تجريبية (14 يوماً) يعمل بضغطة زر مع تنزيل فوري.'", "desc: 'Directe licentiesleutels, ingebouwde BTW-calculator en geverifieerde Windows installers.'")
        c = c.replace("showPortalToast('🚀 مرحباً بك في الجولة الإرشادية التفاعلية!');", "showPortalToast('🚀 Welkom bij de interactieve rondleiding!');")
        c = c.replace("showPortalToast('🎉 اكتملت الجولة الإرشادية بنجاح!');", "showPortalToast('🎉 Rondleiding succesvol voltooid!');")
        c = c.replace("document.getElementById('tourStepBadge').innerText = `خطوة ${currentTourStep + 1} من ${tourSteps.length}`;", "document.getElementById('tourStepBadge').innerText = `Stap ${currentTourStep + 1} van ${tourSteps.length}`;")
        c = c.replace("nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'إنهاء الجولة ✓' : 'التالي ➡️';", "nextBtn.innerText = currentTourStep === tourSteps.length - 1 ? 'Afronden ✓' : 'Volgende ➡️';")
        c = c.replace("'السابق'", "'Vorige'")
        c = c.replace("'التالي'", "'Volgende'")
        c = c.replace("'إنهاء'", "'Afronden'")

    return c

# Generate and write en/demo.html
en_html = generate_localized_demo('en')
with open(DEMO_EN_PATH, 'w', encoding='utf-8') as f:
    f.write(en_html)
print(f"Generated {DEMO_EN_PATH} ({len(en_html)} bytes)")

# Generate and write nl/demo.html
nl_html = generate_localized_demo('nl')
with open(DEMO_NL_PATH, 'w', encoding='utf-8') as f:
    f.write(nl_html)
print(f"Generated {DEMO_NL_PATH} ({len(nl_html)} bytes)")
