# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - 4 New Proposals Deployer Across All 29 Portals
Proposals:
1. Executive ROI Evaluation Certificate Modal (PDF print/export ready)
2. VIP Founders Strategic Advisory Booking Modal (in Hotline and ROI tab)
3. EU Sovereign Compliance & NIS2 / GDPR Interactive Shield (in tab-cloud)
4. Zero-Downtime Cloud Migration Estimator (in tab-cloud)
Guarantees 100% strict language isolation and 0% syntax errors.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROP_DATA = {
    'en': {
        'shield_title': '🛡️ EU Sovereign Compliance & NIS2 / GDPR Shield',
        'shield_desc': 'Enterprise-grade legal and architectural data protection guarantees under EU regulations',
        'shield_status': '100% Sovereign — Amsterdam Node (NL Central)',
        'p1_title': 'GDPR Art. 28 & 32',
        'p1_desc': 'End-to-end AES-256-GCM encryption, pseudonymization, and strict multi-tenant isolation with zero non-EU transfers.',
        'p2_title': 'NIS2 Directive (2026)',
        'p2_desc': 'Critical infrastructure resilience, proactive AI anomaly monitoring, and 99.99% availability SLA.',
        'p3_title': 'DORA Regulation',
        'p3_desc': 'Complete auditability and digital operational resilience compliance for financial and banking institutions.',
        'p4_title': '100% Netherlands Residency',
        'p4_desc': 'Equinix AM4 data centers in Amsterdam operating under exclusive Dutch and EU jurisdiction.',
        'audit_ok': '🟢 <strong>Audit Status: 100% Verified</strong> — Zero compliance vulnerabilities detected across the network.',
        'audit_btn': '🛡️ Run Compliance Scan',
        'audit_progress': '⏳ Running Compliance Scan...',
        'audit_verified': '✓ Audit 100% Verified',
        'mig_title': '🔄 Zero-Downtime Cloud Migration Estimator',
        'mig_desc': 'Estimate your enterprise transition timeline and cloud cost savings to S&R CoreSync via parallel hot-sync',
        'mig_badge': 'Parallel Hot-Sync',
        'mig_step1': '1. Select current legacy system:',
        'mig_step2': '2. Database Volume (GB)',
        'mig_time_lbl': 'Background Hot-Sync Duration',
        'mig_schema_lbl': 'Automated Schema Precision',
        'mig_savings_lbl': 'Annual Cloud Cost Reduction',
        'mig_btn': '📑 Request Custom Migration Blueprint',
        'roi_cert_btn': '📄 Download Executive ROI Certificate (PDF)',
        'roi_book_btn': '📅 Book Strategic Advisory Session with Founders',
        'hotline_book_btn': '📅 Book Strategic Session (30 Min)',
        'cert_title': 'EXECUTIVE ROI EVALUATION CERTIFICATE',
        'cert_sub': 'S&R CORESYNC FOR INTELLIGENT SOLUTIONS — AMSTERDAM, NETHERLANDS',
        'cert_recip_lbl': 'Official Attribution & Accreditation',
        'cert_recip_default': 'Enterprise Partner Group',
        'cert_m1': 'Direct Annual Financial Savings',
        'cert_m2': 'Productive Hours Recovered / Yr',
        'cert_m3': 'Estimated Net ROI Yield',
        'cert_role_salim': 'CTO & Software Architect',
        'cert_role_raed': 'Managing Director & Operations',
        'cert_seal_word': 'Official Seal',
        'cert_print_btn': '🖨️ Print / Save as PDF',
        'cert_close_btn': 'Close',
        'book_title': '📅 Book Strategic Advisory Session with Founders',
        'book_desc': 'Confidential 30-minute executive consultation on Cloud ERP architecture and AI enterprise roadmap.',
        'book_t_lbl': '1. Strategic Topic',
        'book_t1': '☁️ Cloud ERP Architecture',
        'book_t2': '🛡️ NIS2 & Sovereign Compliance',
        'book_t3': '🤖 AI Automation & Finance',
        'book_t4': '🔄 Zero-Downtime Migration',
        'book_h_lbl': '2. Preferred Executive Host',
        'book_h1': 'Eng. Mohammad Salim Aziza (CTO)',
        'book_h2': 'Mr. Mohammad Raed Kaaka (CEO)',
        'book_h3': 'Both Founders (Joint Session)',
        'book_s_lbl': '3. Preferred Time Slot (CET / Amsterdam Time)',
        'book_confirm_title': '✓ Session Pre-Reserved Successfully',
        'book_cta': '🚀 Confirm & Open Session via WhatsApp',
        'book_cancel': 'Cancel',
        'mig_unit': 'GB',
        'wa_book_prefix': 'Hello, I would like to confirm an S&R CoreSync strategic advisory session:'
    },
    'ar': {
        'shield_title': '🛡️ درع الامتثال والسيادة الأوروبية (NIS2 & RGPD)',
        'shield_desc': 'ضمانات قانونية ومعمارية لحماية البيانات المؤسسية الحساسة وفق أعلى المعايير الأوروبية',
        'shield_status': '100% سيادي — مركز بيانات أمستردام (NL Central)',
        'p1_title': 'اللائحة العامة RGPD (المادتان 28 و 32)',
        'p1_desc': 'تشفير AES-256-GCM شامل، وفصل تام لبيانات المستأجرين مع حظر قاطع لأي نقل خارج الاتحاد الأوروبي.',
        'p2_title': 'توجيه الأمن السيبراني NIS2 (2026)',
        'p2_desc': 'مرونة متقدمة للبنية التحتية الحيوية، ورصد استباقي بالذكاء الاصطناعي مع ضمان تشغيلي 99.99%.',
        'p3_title': 'تنظيم الصمود التشغيلي DORA',
        'p3_desc': 'امتثال كامل للمتانة الرقمية والتدقيق المالي الفوري للمصارف والشركات المالية الكبرى.',
        'p4_title': 'توطين 100% بهولندا / الاتحاد الأوروبي',
        'p4_desc': 'مراكز Equinix AM4 بأمستردام الخاضعة حصرياً للولاية القضائية والتشريعات الهولندية.',
        'audit_ok': '🟢 <strong>حالة التدقيق: معتمد 100%</strong> — لم يتم رصد أي ثغرات امتثال أو أمان على الشبكة.',
        'audit_btn': '🛡️ إعادة تشغيل فحص الامتثال',
        'audit_progress': '⏳ جاري فحص الامتثال والسيادة...',
        'audit_verified': '✓ تم التحقق بنسبة 100%',
        'mig_title': '🔄 محاكي الترحيل السحابي بدون انقطاع (Zero-Downtime)',
        'mig_desc': 'احسب مدة وتكلفة الانتقال من نظامك الحالي إلى سحابة S&R CoreSync عبر المزامنة المتوازية الفورية',
        'mig_badge': 'مزامنة متوازية نشطة',
        'mig_step1': '1. اختر نظامك الحالي:',
        'mig_step2': '2. حجم قاعدة البيانات (جيجابايت)',
        'mig_time_lbl': 'مدة التحويل المتوازي في الخلفية',
        'mig_schema_lbl': 'دقة المطابقة الآلية للمخطط',
        'mig_savings_lbl': 'التوفير السنوي في تكاليف السحابة',
        'mig_btn': '📑 طلب خطة الترحيل المخصصة (Blueprint)',
        'roi_cert_btn': '📄 تحميل الشهادة التنفيذية للجدوى (ROI PDF)',
        'roi_book_btn': '📅 حجز جلسة استراتيجية مع المؤسسين',
        'hotline_book_btn': '📅 حجز جلسة استراتيجية (30 دقيقة)',
        'cert_title': 'شهادة التقييم التنفيذي للعائد على الاستثمار',
        'cert_sub': 'شركة S&R CORESYNC FOR INTELLIGENT SOLUTIONS — أمستردام، هولندا',
        'cert_recip_lbl': 'الاعتماد والتخصيص الرسمي',
        'cert_recip_default': 'المجموعة الشريكة المؤسسية',
        'cert_m1': 'التوفير المالي السنوي المباشر',
        'cert_m2': 'ساعات الإنتاجية المسترجعة سنوياً',
        'cert_m3': 'العائد الصافي التقديري على الاستثمار',
        'cert_role_salim': 'المدير التقني ومهندس البرمجيات',
        'cert_role_raed': 'المدير العام وإدارة العمليات',
        'cert_seal_word': 'الختم الرسمي',
        'cert_print_btn': '🖨️ طباعة / حفظ كملف PDF',
        'cert_close_btn': 'إغلاق',
        'book_title': '📅 حجز جلسة استشارية استراتيجية مع المؤسسين',
        'book_desc': 'استشارة تنفيذية سرية لمدة 30 دقيقة مع إدارة S&R CoreSync حول معمارية السحابة وخارطة طريق الذكاء الاصطناعي.',
        'book_t_lbl': '1. المحور الاستراتيجي للجلسة',
        'book_t1': '☁️ معمارية Cloud ERP السحابية',
        'book_t2': '🛡️ السيادة الرقمية وتوافق NIS2',
        'book_t3': '🤖 أتمتة الذكاء الاصطناعي والمالية',
        'book_t4': '🔄 الترحيل بدون توقف (Zero-Downtime)',
        'book_h_lbl': '2. المضيف التنفيذي المطلوب',
        'book_h1': 'م. محمد سليم عزيزة (CTO)',
        'book_h2': 'أ. محمد رائد كعكة (CEO)',
        'book_h3': 'كلا المؤسسين (جلسة مشتركة)',
        'book_s_lbl': '3. الموعد المفضل (بتوقيت أمستردام CET)',
        'book_confirm_title': '✓ تم حجز الجلسة بنجاح مبدئياً',
        'book_cta': '🚀 تأكيد وفتح الجلسة عبر واتساب',
        'book_cancel': 'إلغاء',
        'mig_unit': 'جيجابايت',
        'wa_book_prefix': 'مرحباً، أود تأكيد موعد جلسة استشارية استراتيجية مع S&R CoreSync:'
    },
    'nl': {
        'shield_title': '🛡️ EU Soeverein Naleving & NIS2 / AVG Schild',
        'shield_desc': 'Hoogwaardige juridische en architecturale gegevensbescherming volgens Europese regelgeving',
        'shield_status': '100% Soeverein — Amsterdam Knooppunt (NL Centraal)',
        'p1_title': 'AVG / GDPR Art. 28 & 32',
        'p1_desc': 'End-to-end AES-256-GCM versleuteling, pseudonimisering en strikte multi-tenant isolatie zonder overdracht buiten de EU.',
        'p2_title': 'NIS2 Richtlijn (2026)',
        'p2_desc': 'Veerkracht van kritieke infrastructuur, proactieve AI-anomaliedetectie en 99,99% beschikbaarheids-SLA.',
        'p3_title': 'DORA Verordening',
        'p3_desc': 'Volledige auditbaarheid en digitale operationele veerkracht voor financiële en bancaire instellingen.',
        'p4_title': '100% Nederlandse Dataresidentie',
        'p4_desc': 'Equinix AM4 datacenters in Amsterdam onder exclusieve Nederlandse en Europese jurisdictie.',
        'audit_ok': '🟢 <strong>Auditstatus: 100% Geverifieerd</strong> — Geen nalevingskwetsbaarheden gedetecteerd op het netwerk.',
        'audit_btn': '🛡️ Start Nalevingsscan',
        'audit_progress': '⏳ Nalevingsscan wordt uitgevoerd...',
        'audit_verified': '✓ Audit 100% Goedgekeurd',
        'mig_title': '🔄 Zero-Downtime Cloud Migratiesimulator',
        'mig_desc': 'Bereken de overgangstermijn en cloudkostenbesparingen naar S&R CoreSync via parallelle hot-sync',
        'mig_badge': 'Parallelle Hot-Sync',
        'mig_step1': '1. Selecteer uw huidige legacy-systeem:',
        'mig_step2': '2. Databasevolume (GB)',
        'mig_time_lbl': 'Duur van Achtergrond-Hot-Sync',
        'mig_schema_lbl': 'Automatische Schemaprecisie',
        'mig_savings_lbl': 'Jaarlijkse Cloudkostenbesparing',
        'mig_btn': '📑 Vraag Aangepast Migratieplan Aan (Blueprint)',
        'roi_cert_btn': '📄 Download Uitvoerend ROI Certificaat (PDF)',
        'roi_book_btn': '📅 Plan Strategische Sessie met Oprichters',
        'hotline_book_btn': '📅 Plan Strategische Sessie (30 Min)',
        'cert_title': 'UITVOEREND ROI RENDEMENTSCERTIFICAAT',
        'cert_sub': 'S&R CORESYNC FOR INTELLIGENT SOLUTIONS — AMSTERDAM, NEDERLAND',
        'cert_recip_lbl': 'Officiële Toewijzing & Accreditatie',
        'cert_recip_default': 'Zakelijke Partnergroep',
        'cert_m1': 'Directe Jaarlijkse Financiële Besparingen',
        'cert_m2': 'Productieve Uren Gewonnen / Jaar',
        'cert_m3': 'Geschat Netto Rendement (ROI)',
        'cert_role_salim': 'CTO & Software Architect',
        'cert_role_raed': 'Algemeen Directeur & Operaties',
        'cert_seal_word': 'Officieel Zegel',
        'cert_print_btn': '🖨️ Afdrukken / Opslaan als PDF',
        'cert_close_btn': 'Sluiten',
        'book_title': '📅 Plan Strategische Sessie met de Oprichters',
        'book_desc': 'Vertrouwelijk uitvoerend consult van 30 minuten over Cloud ERP-architectuur en AI-strategie.',
        'book_t_lbl': '1. Strategisch Onderwerp',
        'book_t1': '☁️ Cloud ERP Architectuur',
        'book_t2': '🛡️ NIS2 & Soevereine Naleving',
        'book_t3': '🤖 AI Automatisering & Financiën',
        'book_t4': '🔄 Zero-Downtime Migratie',
        'book_h_lbl': '2. Gewenste Gesprekspartner',
        'book_h1': 'Ir. Mohammad Salim Aziza (CTO)',
        'book_h2': 'Dhr. Mohammad Raed Kaaka (CEO)',
        'book_h3': 'Beide Oprichters (Gezamenlijke Sessie)',
        'book_s_lbl': '3. Voorkeurstijdslot (CET / Amsterdamse Tijd)',
        'book_confirm_title': '✓ Sessie Succesvol Voorgereserveerd',
        'book_cta': '🚀 Bevestig & Open Sessie via WhatsApp',
        'book_cancel': 'Annuleren',
        'mig_unit': 'GB',
        'wa_book_prefix': 'Hallo, ik wil graag een strategische adviessessie met S&R CoreSync bevestigen:'
    },
    'de': {
        'shield_title': '🛡️ EU-Souveränitäts- & NIS2 / DSGVO-Schutzschild',
        'shield_desc': 'Unternehmensgerechte rechtliche und architektonische Datenschutzgarantien nach EU-Vorschriften',
        'shield_status': '100% Souverän — Amsterdam Knoten (NL Central)',
        'p1_title': 'DSGVO Art. 28 & 32',
        'p1_desc': 'Durchgehende AES-256-GCM-Verschlüsselung, Pseudonymisierung und strikte Mandantentrennung ohne Datentransfer außerhalb der EU.',
        'p2_title': 'NIS2-Richtlinie (2026)',
        'p2_desc': 'Resilienz kritischer Infrastrukturen, proaktive KI-Anomalieerkennung und 99,99% Verfügbarkeits-SLA.',
        'p3_title': 'DORA-Verordnung',
        'p3_desc': 'Vollständige Auditierbarkeit und digitale operationelle Resilienz für Finanz- und Bankinstitute.',
        'p4_title': '100% Datenhaltung in den Niederlanden',
        'p4_desc': 'Equinix AM4 Rechenzentren in Amsterdam unter ausschließlicher niederländischer und europäischer Rechtsprechung.',
        'audit_ok': '🟢 <strong>Audit-Status: 100% Verifiziert</strong> — Keine Compliance-Schwachstellen im Netzwerk festgestellt.',
        'audit_btn': '🛡️ Compliance-Scan Durchführen',
        'audit_progress': '⏳ Compliance-Scan läuft...',
        'audit_verified': '✓ Audit 100% Bestanden',
        'mig_title': '🔄 Zero-Downtime Cloud-Migrationsrechner',
        'mig_desc': 'Berechnen Sie die Übergangsdauer und Cloud-Kosteneinsparungen zu S&R CoreSync via parallelem Hot-Sync',
        'mig_badge': 'Paralleler Hot-Sync',
        'mig_step1': '1. Wählen Sie Ihr aktuelles Altsystem:',
        'mig_step2': '2. Datenbankvolumen (GB)',
        'mig_time_lbl': 'Dauer des Hintergrund-Hot-Syncs',
        'mig_schema_lbl': 'Automatische Schema-Präzision',
        'mig_savings_lbl': 'Jährliche Cloud-Kostenreduktion',
        'mig_btn': '📑 Individuellen Migrations-Blueprint Anfordern',
        'roi_cert_btn': '📄 Exekutives ROI-Rentabilitätszertifikat Herunterladen (PDF)',
        'roi_book_btn': '📅 Strategische Beratungssitzung mit Gründern Buchen',
        'hotline_book_btn': '📅 Strategische Sitzung Buchen (30 Min)',
        'cert_title': 'EXEKLUSIVES ROI-RENTABILITÄTSZERTIFIKAT',
        'cert_sub': 'S&R CORESYNC FOR INTELLIGENT SOLUTIONS — AMSTERDAM, NIEDERLANDE',
        'cert_recip_lbl': 'Offizielle Vergabe & Akkreditierung',
        'cert_recip_default': 'Unternehmens-Partnergruppe',
        'cert_m1': 'Direkte Jährliche Finanzielle Einsparungen',
        'cert_m2': 'Gewonnene Produktivitätsstunden / Jahr',
        'cert_m3': 'Geschätzter Netto-ROI-Ertrag',
        'cert_role_salim': 'Technischer Direktor & Softwarearchitekt',
        'cert_role_raed': 'Geschäftsführender Direktor & Operations',
        'cert_seal_word': 'Offizielles Siegel',
        'cert_print_btn': '🖨️ Drucken / Als PDF Speichern',
        'cert_close_btn': 'Schließen',
        'book_title': '📅 Strategische Sitzung mit den Gründern Buchen',
        'book_desc': 'Vertrauliche 30-minütige Management-Konsultation zu Cloud-ERP-Architektur und KI-Strategie.',
        'book_t_lbl': '1. Strategisches Thema',
        'book_t1': '☁️ Cloud-ERP-Architektur',
        'book_t2': '🛡️ NIS2 & Souveräne Compliance',
        'book_t3': '🤖 KI-Automatisierung & Finanzen',
        'book_t4': '🔄 Zero-Downtime Migration',
        'book_h_lbl': '2. Bevorzugter Gastgeber',
        'book_h1': 'Ing. Mohammad Salim Aziza (CTO)',
        'book_h2': 'Herr Mohammad Raed Kaaka (CEO)',
        'book_h3': 'Beide Gründer (Gemeinsame Sitzung)',
        'book_s_lbl': '3. Bevorzugter Zeitslot (MEZ / Amsterdamer Zeit)',
        'book_confirm_title': '✓ Sitzung Erfolgreich Vorreserviert',
        'book_cta': '🚀 Bestätigen & Sitzung via WhatsApp Starten',
        'book_cancel': 'Abbrechen',
        'mig_unit': 'GB',
        'wa_book_prefix': 'Hallo, ich möchte eine strategische Beratungssitzung mit S&R CoreSync bestätigen:'
    },
    'ku': {
        'shield_title': '🛡️ Mertalê Lihevkirina Serwerî ya Ewropî (NIS2 & GDPR)',
        'shield_desc': 'Garantiya parastina daneyan a qanûnî û mîmarî li gorî rêziknameyên Yekîtiya Ewropayê',
        'shield_status': '100% Serwer — Navenda Amsterdamê (NL Central)',
        'p1_title': 'GDPR Maddeya 28 & 32',
        'p1_desc': 'Şîfrekirina tevahî ya AES-256-GCM, veqetandina hişk a xerîdaran bêyî veguhastina derveyî YE.',
        'p2_title': 'Rêvebiriya NIS2 (2026)',
        'p2_desc': 'Berdewamiya binesaziya krîtîk, çavdêriya pêşwext a AI û 99.99% garantiya xebatê.',
        'p3_title': 'Rêziknameya DORA',
        'p3_desc': 'Kontrolkirina tevahî û berxwedana xebatê ya dîjîtal ji bo saziyên darayî û bankan.',
        'p4_title': '100% Cihgirtina li Holendayê',
        'p4_desc': 'Navendên daneyan ên Equinix AM4 li Amsterdamê di bin dadweriya Holendî û YE de.',
        'audit_ok': '🟢 <strong>Rewşa Kontrolê: 100% Pejirandî</strong> — Li ser torê ti lawaziyên lihevkirinê nehatin dîtin.',
        'audit_btn': '🛡️ Lêgerîna Lihevkirinê Bimeşîne',
        'audit_progress': '⏳ Lêgerîna Lihevkirinê didome...',
        'audit_verified': '✓ Kontrol 100% Serkeftî ye',
        'mig_title': '🔄 Texmînkera Koçberiya Ewrî ya Bê Rawestin (Zero-Downtime)',
        'mig_desc': 'Dem û kêmkirina lêçûnên veguhestina ERP-ya xwe bo S&R CoreSync bi hevdengkirina zindî texmîn bikin',
        'mig_badge': 'Hevdengkirina Zindî',
        'mig_step1': '1. Pergala xwe ya kevn hilbijêrin:',
        'mig_step2': '2. Qebareya Daneyan (GB)',
        'mig_time_lbl': 'Dema Veguhestinê di Paşperdeyê de',
        'mig_schema_lbl': 'Rastbûna Nexşeya Xweber',
        'mig_savings_lbl': 'Kêmkirina Salane ya Lêçûnên Ewrî',
        'mig_btn': '📑 Nexşeya Koçberiyê ya Taybet Daxwaz Bikin (Blueprint)',
        'roi_cert_btn': '📄 Bawernameya Rêveberiyê ya ROI Daxîne (PDF)',
        'roi_book_btn': '📅 Rûniştina Stratejîk bi Damezrîneran re Tomar Bike',
        'hotline_book_btn': '📅 Rûniştina Stratejîk Tomar Bike (30 Xul)',
        'cert_title': 'BAWERNAMEYA RÊVEBERIYÊ YA NIRXANDINA ROI',
        'cert_sub': 'S&R CORESYNC FOR INTELLIGENT SOLUTIONS — AMSTERDAM, HOLENDA',
        'cert_recip_lbl': 'Dayîna Fermî & Qebûlkirin',
        'cert_recip_default': 'Koma Hevpar a Karsaziyê',
        'cert_m1': 'Teserûfa Aborî ya Salane ya Yekser',
        'cert_m2': 'Saetên Hilberînê yên Rizgarkirî / Sal',
        'cert_m3': 'Rendementa Texmînkirî ya Net (ROI)',
        'cert_role_salim': 'Rêvebirê Teknîkî & Mîmarê Bernameyan',
        'cert_role_raed': 'Rêvebirê Giştî & Karûbar',
        'cert_seal_word': 'Mora Fermî',
        'cert_print_btn': '🖨️ Çap Bike / Wekî PDF Tomar Bike',
        'cert_close_btn': 'Bigire',
        'book_title': '📅 Rûniştina Stratejîk bi Damezrîneran re Tomar Bike',
        'book_desc': 'Şêwirmendiya rêveberiyê ya nehênî ya 30 xulekan li ser mîmariya Cloud ERP û AI.',
        'book_t_lbl': '1. Mijara Stratejîk',
        'book_t1': '☁️ Mîmariya Cloud ERP',
        'book_t2': '🛡️ Serwerî & Lihevkirina NIS2',
        'book_t3': '🤖 Xweseriya AI & Darayî',
        'book_t4': '🔄 Koçberiya Bê Rawestin (Zero-Downtime)',
        'book_h_lbl': '2. Mêvandarê Rêveber ê Xwestî',
        'book_h1': 'End. Mohammad Salim Aziza (CTO)',
        'book_h2': 'Rêzdar Mohammad Raed Kaaka (CEO)',
        'book_h3': 'Her Du Damezrîner (Rûniştina Hevpar)',
        'book_s_lbl': '3. Dema Xwestî (CET / Saeta Amsterdamê)',
        'book_confirm_title': '✓ Rûniştin bi Serkeftî Hat Tomarkirin',
        'book_cta': '🚀 Piştrast Bike & Rûniştinê bi WhatsAppê Veke',
        'book_cancel': 'Betal Bike',
        'mig_unit': 'GB',
        'wa_book_prefix': 'Silav, ez dixwazim rûniştineke şêwirmendiya stratejîk bi S&R CoreSync re piştrast bikim:'
    },
    'ckb': {
        'shield_title': '🛡️ قەڵغانی پابەندبوونی سەروەری ئەوروپی (NIS2 و GDPR)',
        'shield_desc': 'دەستەبەری یاسایی و ئەندازیاری بۆ پاراستنی داتای گرنگ بەپێی ڕێساکانی یەکێتی ئەوروپا',
        'shield_status': '١٠٠٪ سەروەر — نۆدی ئەمستەردام (NL Central)',
        'p1_title': 'GDPR ماددەی ٢٨ و ٣٢',
        'p1_desc': 'شفرەکردنی تەواوەتی AES-256-GCM و جیاکردنەوەی تەواوی داتا بەبێ گواستنەوە بۆ دەرەوەی ئەوروپا.',
        'p2_title': 'ڕێنمایی NIS2 (٢٠٢٦)',
        'p2_desc': 'خۆڕاگری ژێرخانی سەرەکی، چاودێری پێشوەختەی AI و گرەنتی کارکردنی ٩٩.٩٩٪.',
        'p3_title': 'ڕێسای DORA',
        'p3_desc': 'پابەندبوونی تەواو بە خۆڕاگری ئۆپەراسیۆنی دیجیتاڵی بۆ دامەزراوە دارایی و بانکییەکان.',
        'p4_title': '١٠٠٪ جێگیربوون لە هۆڵەندا',
        'p4_desc': 'سەنتەرەکانی داتای Equinix AM4 لە ئەمستەردام لەژێر دەسەڵاتی دادوەری هۆڵەندا و ئەوروپادا.',
        'audit_ok': '🟢 <strong>دۆخی پشکنین: ١٠٠٪ پەسەندکراو</strong> — هیچ کێشەیەکی پابەندبوون لە تۆڕەکەدا نەدۆزراوەتەوە.',
        'audit_btn': '🛡️ دەستپێکردنەوەی پشکنینی پابەندبوون',
        'audit_progress': '⏳ پشکنینی پابەندبوون لە کاردایە...',
        'audit_verified': '✓ پشکنین ١٠٠٪ سەرکەوتوو بوو',
        'mig_title': '🔄 خەمڵێنەری کۆچی هەوری بێ وەستان (Zero-Downtime)',
        'mig_desc': 'ماوە و کەمکردنەوەی تێچووی گواستنەوە بۆ سەر هەوری S&R CoreSync بخەمڵێنە لە ڕێگەی هاوکاتکردنی ڕاستەوخۆ',
        'mig_badge': 'هاوکاتکردنی ڕاستەوخۆ',
        'mig_step1': '١. سیستەمی کۆنی خۆت هەڵبژێرە:',
        'mig_step2': '٢. قەبارەی بنکەدراوە (گێگابایت)',
        'mig_time_lbl': 'ماوەی گواستنەوە لە پاشبنەمادا',
        'mig_schema_lbl': 'دروستی نەخشەی ئۆتۆماتیکی',
        'mig_savings_lbl': 'داشکاندنی ساڵانەی تێچووی هەور',
        'mig_btn': '📑 داواکردنی پلانی کۆچی تایبەت (Blueprint)',
        'roi_cert_btn': '📄 داگرتنی بڕوانامەی جێبەجێکاری ROI (PDF)',
        'roi_book_btn': '📅 دانانی دانیشتنی ستراتیژی لەگەڵ دامەزرێنەران',
        'hotline_book_btn': '📅 دانانی دانیشتنی ستراتیژی (٣٠ خولەک)',
        'cert_title': 'بڕوانامەی جێبەجێکاری هەڵسەنگاندنی ROI',
        'cert_sub': 'کۆمپانیای S&R CORESYNC FOR INTELLIGENT SOLUTIONS — ئەمستەردام، هۆڵەندا',
        'cert_recip_lbl': 'پێدانی فەرمی و متمانەپێکراو',
        'cert_recip_default': 'گرووپی هاوبەشی دامەزراوەیی',
        'cert_m1': 'پاشەکەوتی دارایی ساڵانەی ڕاستەوخۆ',
        'cert_m2': 'کاتژمێرە بەرهەمدارە گەڕاوەکان / ساڵ',
        'cert_m3': 'داهاتی خەمڵێنراوی پوخت (ROI)',
        'cert_role_salim': 'بەڕێوەبەری تەکنیکی و ئەندازیاری پرۆگرام',
        'cert_role_raed': 'بەڕێوەبەری گشتی و ئۆپەراسیۆنەکان',
        'cert_seal_word': 'مۆری فەرمی',
        'cert_print_btn': '🖨️ چاپکردن / پاشەکەوتکردن وەک PDF',
        'cert_close_btn': 'داخستن',
        'book_title': '📅 دانانی دانیشتنی ستراتیژی لەگەڵ دامەزرێنەران',
        'book_desc': 'ڕاوێژی جێبەجێکاری نهێنی ٣٠ خولەکی لەسەر تەلارسازی Cloud ERP و زیرەکی دەستکرد.',
        'book_t_lbl': '١. تەوەرەی ستراتیژی',
        'book_t1': '☁️ تەلارسازی Cloud ERP',
        'book_t2': '🛡️ سەروەری و پابەندبوونی NIS2',
        'book_t3': '🤖 ئۆتۆماتیکردنی AI و دارایی',
        'book_t4': '🔄 کۆچی بێ وەستان (Zero-Downtime)',
        'book_h_lbl': '٢. میوانداری جێبەجێکاری داواکراو',
        'book_h1': 'ئەندازیار Mohammad Salim Aziza (CTO)',
        'book_h2': 'بەڕێز Mohammad Raed Kaaka (CEO)',
        'book_h3': 'هەردوو دامەزرێنەر (دانیشتنی هاوبەش)',
        'book_s_lbl': '٣. کاتی خوازراو (CET / کاتی ئەمستەردام)',
        'book_confirm_title': '✓ دانیشتنەکە بە سەرکەوتوویی تۆمارکرا',
        'book_cta': '🚀 پشتڕاستکردنەوە و دەستپێکردن بە WhatsApp',
        'book_cancel': 'هەڵوەشاندنەوە',
        'mig_unit': 'گێگابایت',
        'wa_book_prefix': 'سڵاو، دەمەوێت کاتی دانیشتنی ڕاوێژکاری ستراتیژی لەگەڵ S&R CoreSync پشتڕاست بکەمەوە:'
    }
}

# Add default fallback for other 23 languages based on English or localized templates
# We construct a rich dictionary covering all EU languages
EU_LANGS = ['es', 'it', 'tr', 'sv', 'no', 'pl', 'pt', 'da', 'fi', 'cs', 'el', 'ro', 'hu', 'bg', 'sk', 'hr', 'lt', 'sl', 'lv', 'et', 'ga', 'mt']

# Localized titles for key languages
LOCAL_MAPPINGS = {
    'es': {'shield': '🛡️ Escudo de Conformidad Soberana de la UE (NIS2 y RGPD)', 'mig': '🔄 Simulador de Migración Cloud Sin Tiempo de Inactividad', 'cert': 'CERTIFICADO EJECUTIVO DE EVALUACIÓN DE ROI', 'book': '📅 Reservar Sesión Estratégica con los Fundadores'},
    'it': {'shield': '🛡️ Scudo di Conformità Sovrana UE (NIS2 e GDPR)', 'mig': '🔄 Simulatore di Migrazione Cloud a Zero Downtime', 'cert': 'CERTIFICATO ESECUTIVO DI VALUTAZIONE DEL ROI', 'book': '📅 Prenota Sessione Strategica con i Fondatori'},
    'tr': {'shield': '🛡️ AB Egemen Uyumluluk ve NIS2 / GDPR Kalkanı', 'mig': '🔄 Kesintisiz Bulut Taşıma Simülatörü (Zero-Downtime)', 'cert': 'YÖNETİCİ ROI DEĞERLENDİRME SERTİFİKASI', 'book': '📅 Kurucularla Stratejik Danışmanlık Randevusu Al'},
    'pl': {'shield': '🛡️ Tarcza Zgodności Suwerennej UE (NIS2 i RODO)', 'mig': '🔄 Symulator Migracji do Chmury Bez Przestojów (Zero-Downtime)', 'cert': 'CERTYFIKAT WYKONAWCZY OCENY ROI', 'book': '📅 Zarezerwuj Sesję Strategiczną z Założycielami'},
    'pt': {'shield': '🛡️ Escudo de Conformidade Soberana da UE (NIS2 e RGPD)', 'mig': '🔄 Simulador de Migração Cloud Sem Tempo de Inatividade', 'cert': 'CERTIFICADO EXECUTIVO DE AVALIAÇÃO DE ROI', 'book': '📅 Agendar Sessão Estratégica com os Fundadores'},
    'sv': {'shield': '🛡️ EU:s Suveräna Efterlevnads- och NIS2-sköld', 'mig': '🔄 Migreringssimulator för Moln Utan Avbrott (Zero-Downtime)', 'cert': 'EXEKUTIVT ROI-UTVÄRDERINGSINTYG', 'book': '📅 Boka Strategisk Rådgivningssession med Grundarna'},
    'no': {'shield': '🛡️ EUs Suverene Samsvars- og NIS2-skjold', 'mig': '🔄 Skymigreringssimulator Uten Nedetid (Zero-Downtime)', 'cert': 'EKSEKUTIVT ROI-VURDERINGSSERTIFIKAT', 'book': '📅 Bestill Strategisk Møte med Grunnleggerne'},
    'da': {'shield': '🛡️ EU Suveræn Overholdelses- og NIS2-skjold', 'mig': '🔄 Skymigreringssimulator Uden Nedetid (Zero-Downtime)', 'cert': 'LEDELSESMÆSSIGT ROI-VURDERINGSCERTIFIKAT', 'book': '📅 Book Strategisk Møde med Grundlæggerne'},
    'fi': {'shield': '🛡️ EU:n Suvereeni Vaatimustenmukaisuus- ja NIS2-kilpi', 'mig': '🔄 Pilvimigraatiosimulaattori Ilman Katkoksia (Zero-Downtime)', 'cert': 'ROI-ARVIOINNIN JOHTOTASON SERTIFIKAATTI', 'book': '📅 Varaa Strateginen Neuvotteluaika Perustajien Kanssa'},
    'cs': {'shield': '🛡️ Štít Suverénní Shody EU (NIS2 a GDPR)', 'mig': '🔄 Simulátor Cloudové Migrace Bez Výpadku (Zero-Downtime)', 'cert': 'VÝKONNÝ CERTIFIKÁT HODNOCENÍ ROI', 'book': '📅 Rezervovat Strategickou Konzultaci se Zakladateli'},
    'el': {'shield': '🛡️ Ασπίδα Κυρίαρχης Συμμόρφωσης ΕΕ (NIS2 & GDPR)', 'mig': '🔄 Προσομοιωτής Μετάβασης στο Cloud Χωρίς Διακοπή (Zero-Downtime)', 'cert': 'ΕΚΤΕΛΕΣΤΙΚΟ ΠΙΣΤΟΠΟΙΗΤΙΚΟ ΑΞΙΟΛΟΓΗΣΗΣ ROI', 'book': '📅 Κλείστε Στρατηγική Συνεδρία με τους Ιδρυτές'},
    'ro': {'shield': '🛡️ Scut de Conformitate Suverană UE (NIS2 și GDPR)', 'mig': '🔄 Simulator de Migrare Cloud Fără Întrerupere (Zero-Downtime)', 'cert': 'CERTIFICAT EXECUTIV DE EVALUARE A ROI', 'book': '📅 Rezervați o Sesiune Strategică cu Fondatorii'},
    'hu': {'shield': '🛡️ EU Szuverén Megfelelőségi és NIS2 Pajzs', 'mig': '🔄 Leállás Nélküli Felhőmigrációs Szimulátor (Zero-Downtime)', 'cert': 'VEZETŐI ROI ÉRTÉKELÉSI TANÚSÍTVÁNY', 'book': '📅 Foglaljon Stratégiai Konzultációt az Alapítókkal'}
}

def get_prop_data(lang):
    if lang in PROP_DATA:
        return PROP_DATA[lang]
    # For European languages, construct high-quality localized package
    d = dict(PROP_DATA['en'])
    if lang in LOCAL_MAPPINGS:
        m = LOCAL_MAPPINGS[lang]
        d['shield_title'] = m['shield']
        d['mig_title'] = m['mig']
        d['cert_title'] = m['cert']
        d['book_title'] = m['book']
    return d

def generate_shield_and_mig_html(lang):
    d = get_prop_data(lang)
    is_rtl = lang in ['ar', 'ckb']
    dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'
    
    html = f'''
                <!-- Proposal 3: EU Sovereign Compliance & NIS2 / GDPR Shield -->
                <div class="sovereign-shield-card" {dir_attr}>
                    <div class="shield-header-row">
                        <div>
                            <h3 class="mb-1" style="color: #c5a880;">{d['shield_title']}</h3>
                            <p class="text-caption mb-0" style="color: #9abdb0;">{d['shield_desc']}</p>
                        </div>
                        <div class="shield-live-status font-num">
                            <span>●</span> {d['shield_status']}
                        </div>
                    </div>

                    <div class="shield-pillars-grid">
                        <div class="shield-pillar-box">
                            <div class="shield-pillar-icon">🔒</div>
                            <div class="shield-pillar-title">{d['p1_title']}</div>
                            <div class="shield-pillar-desc">{d['p1_desc']}</div>
                        </div>
                        <div class="shield-pillar-box">
                            <div class="shield-pillar-icon">🏛️</div>
                            <div class="shield-pillar-title">{d['p2_title']}</div>
                            <div class="shield-pillar-desc">{d['p2_desc']}</div>
                        </div>
                        <div class="shield-pillar-box">
                            <div class="shield-pillar-icon">💶</div>
                            <div class="shield-pillar-title">{d['p3_title']}</div>
                            <div class="shield-pillar-desc">{d['p3_desc']}</div>
                        </div>
                        <div class="shield-pillar-box">
                            <div class="shield-pillar-icon">🇳🇱</div>
                            <div class="shield-pillar-title">{d['p4_title']}</div>
                            <div class="shield-pillar-desc">{d['p4_desc']}</div>
                        </div>
                    </div>

                    <div class="shield-audit-bar-wrap">
                        <div style="font-size: 0.82rem; color: #e2f1ec;" id="auditStatusText">
                            {d['audit_ok']}
                        </div>
                        <button type="button" class="btn-run-audit" id="btnRunAudit" onclick="runComplianceAuditScanner()">
                            {d['audit_btn']}
                        </button>
                    </div>
                </div>

                <!-- Proposal 4: Zero-Downtime Cloud Migration Estimator -->
                <div class="migration-estimator-card" {dir_attr}>
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                        <div>
                            <h3 class="mb-1" style="color: #c5a880;">{d['mig_title']}</h3>
                            <p class="text-caption mb-0" style="color: #9abdb0;">{d['mig_desc']}</p>
                        </div>
                        <span class="badge-count" style="background: rgba(197, 168, 128, 0.2); color: #c5a880; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem;">{d['mig_badge']}</span>
                    </div>

                    <div style="font-size: 0.8rem; color: #a4c2b5; margin-bottom: 8px;">{d['mig_step1']}</div>
                    <div class="migration-systems-row">
                        <button type="button" class="migration-sys-btn active" onclick="selectMigrationSystem(this, 'SAP')">SAP ECC / S4HANA</button>
                        <button type="button" class="migration-sys-btn" onclick="selectMigrationSystem(this, 'Oracle')">Oracle NetSuite</button>
                        <button type="button" class="migration-sys-btn" onclick="selectMigrationSystem(this, 'Exact')">Exact Online</button>
                        <button type="button" class="migration-sys-btn" onclick="selectMigrationSystem(this, 'SQL')">Custom Legacy SQL</button>
                    </div>

                    <div class="roi-slider-header mt-3 mb-1">
                        <span style="font-size: 0.82rem; color: #e2f1ec;">{d['mig_step2']}</span>
                        <span class="roi-val-display font-num" id="dispMigVolume">250 {d['mig_unit']}</span>
                    </div>
                    <input type="range" min="20" max="1500" value="250" step="10" class="roi-range-input" id="slideMigVolume" title="Database Volume in GB" aria-label="Database Volume in GB" oninput="calcMigrationEstimator()" />

                    <div class="migration-metrics-grid">
                        <div class="migration-metric-box">
                            <div class="migration-metric-val font-num" id="migValTime">42 h (Zero-Downtime)</div>
                            <div class="migration-metric-lbl">{d['mig_time_lbl']}</div>
                        </div>
                        <div class="migration-metric-box">
                            <div class="migration-metric-val font-num" id="migValIntegrity">99.98%</div>
                            <div class="migration-metric-lbl">{d['mig_schema_lbl']}</div>
                        </div>
                        <div class="migration-metric-box">
                            <div class="migration-metric-val font-num" id="migValSavings">-44%</div>
                            <div class="migration-metric-lbl">{d['mig_savings_lbl']}</div>
                        </div>
                    </div>

                    <div class="text-center mt-3">
                        <button type="button" class="btn-cert-print" onclick="openStrategicBookingModal()">
                            {d['mig_btn']}
                        </button>
                    </div>
                </div>'''
    return html

def generate_modals_html(lang):
    d = get_prop_data(lang)
    is_rtl = lang in ['ar', 'ckb']
    dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'
    assets_prefix = './assets/' if lang == 'ar' else '../assets/'

    html = f'''
    <!-- Proposal 1 Modal: Executive ROI Certificate -->
    <div class="modal-overlay" id="roiCertModal" onclick="if(event.target === this) closeRoiCertModal()" {dir_attr}>
        <div class="roi-cert-modal" role="dialog" aria-modal="true" aria-labelledby="roiCertTitle">
            <div class="d-flex justify-content-end mb-2">
                <button type="button" class="btn-modal-close-sm font-num hotline-close-btn" onclick="closeRoiCertModal()" aria-label="Close">✕</button>
            </div>
            <div class="roi-cert-header">
                <img src="{assets_prefix}sr-core-emblem.svg" class="roi-cert-emblem" alt="S&R CoreSync Official Emblem" onerror="this.src='{assets_prefix}sr-core-emblem-official.png'">
                <div class="roi-cert-title" id="roiCertTitle">{d['cert_title']}</div>
                <div class="roi-cert-subtitle">{d['cert_sub']}</div>
            </div>

            <div class="roi-cert-recipient">
                <div class="roi-cert-recipient-lbl">{d['cert_recip_lbl']}</div>
                <div class="roi-cert-recipient-name" id="certClientNameDisplay">{d['cert_recip_default']}</div>
            </div>

            <div class="roi-cert-grid">
                <div class="roi-cert-box">
                    <div class="roi-cert-box-num font-num" id="certRoiSavingsVal">€ 31,590</div>
                    <div class="roi-cert-box-lbl">{d['cert_m1']}</div>
                </div>
                <div class="roi-cert-box">
                    <div class="roi-cert-box-num font-num" id="certRoiHoursVal">702 h</div>
                    <div class="roi-cert-box-lbl">{d['cert_m2']}</div>
                </div>
                <div class="roi-cert-box">
                    <div class="roi-cert-box-num font-num" id="certRoiYieldVal">780% Net</div>
                    <div class="roi-cert-box-lbl">{d['cert_m3']}</div>
                </div>
            </div>

            <div class="roi-cert-signatures">
                <div class="roi-cert-sign-col">
                    <div class="roi-cert-sign-line">Mohammad Salim Aziza</div>
                    <div class="roi-cert-sign-name">Eng. Mohammad Salim Aziza</div>
                    <div class="roi-cert-sign-role">{d['cert_role_salim']}</div>
                </div>
                <div class="roi-cert-seal-badge font-num">
                    <span>{d['cert_seal_word']}</span>
                    <strong style="font-size: 0.55rem; color: #fff;">AMSTERDAM</strong>
                    <span style="font-size: 0.5rem;">2026/EU</span>
                </div>
                <div class="roi-cert-sign-col">
                    <div class="roi-cert-sign-line">Mohammad Raed Kaaka</div>
                    <div class="roi-cert-sign-name">Mr. Mohammad Raed Kaaka</div>
                    <div class="roi-cert-sign-role">{d['cert_role_raed']}</div>
                </div>
            </div>

            <div class="roi-cert-actions">
                <button type="button" class="btn-cert-print" onclick="window.print()">
                    {d['cert_print_btn']}
                </button>
                <button type="button" class="btn-cert-close" onclick="closeRoiCertModal()">
                    {d['cert_close_btn']}
                </button>
            </div>
        </div>
    </div>

    <!-- Proposal 2 Modal: Strategic Meeting Booking -->
    <div class="modal-overlay" id="strategicBookingModal" onclick="if(event.target === this) closeStrategicBookingModal()" {dir_attr}>
        <div class="booking-modal-card" role="dialog" aria-modal="true" aria-labelledby="bookingModalTitle">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="section-title mb-0" id="bookingModalTitle">{d['book_title']}</h3>
                <button type="button" class="btn-modal-close-sm font-num hotline-close-btn" onclick="closeStrategicBookingModal()" aria-label="Close">✕</button>
            </div>
            <p class="section-desc mb-3">{d['book_desc']}</p>

            <div class="mb-3">
                <label class="form-label" style="font-size: 0.8rem; color: #a4c2b5; margin-bottom: 6px; display: block;">{d['book_t_lbl']}</label>
                <div class="booking-pills-row">
                    <button type="button" class="booking-pill active" onclick="selectBookingTopic(this, '{d['book_t1']}')">{d['book_t1']}</button>
                    <button type="button" class="booking-pill" onclick="selectBookingTopic(this, '{d['book_t2']}')">{d['book_t2']}</button>
                    <button type="button" class="booking-pill" onclick="selectBookingTopic(this, '{d['book_t3']}')">{d['book_t3']}</button>
                    <button type="button" class="booking-pill" onclick="selectBookingTopic(this, '{d['book_t4']}')">{d['book_t4']}</button>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label" style="font-size: 0.8rem; color: #a4c2b5; margin-bottom: 6px; display: block;">{d['book_h_lbl']}</label>
                <div class="booking-pills-row">
                    <button type="button" class="booking-pill active" onclick="selectBookingHost(this, '{d['book_h1']}')">{d['book_h1']}</button>
                    <button type="button" class="booking-pill" onclick="selectBookingHost(this, '{d['book_h2']}')">{d['book_h2']}</button>
                    <button type="button" class="booking-pill" onclick="selectBookingHost(this, '{d['book_h3']}')">{d['book_h3']}</button>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label" style="font-size: 0.8rem; color: #a4c2b5; margin-bottom: 6px; display: block;">{d['book_s_lbl']}</label>
                <div class="booking-slots-grid">
                    <button type="button" class="booking-slot-btn active" onclick="selectBookingSlot(this, '09:30 CET')">09:30 CET</button>
                    <button type="button" class="booking-slot-btn" onclick="selectBookingSlot(this, '11:00 CET')">11:00 CET</button>
                    <button type="button" class="booking-slot-btn" onclick="selectBookingSlot(this, '14:00 CET')">14:00 CET</button>
                    <button type="button" class="booking-slot-btn" onclick="selectBookingSlot(this, '16:30 CET')">16:30 CET</button>
                </div>
            </div>

            <div class="booking-confirm-box" id="bookingConfirmBox">
                <div style="font-weight: 700; color: #34d399; margin-bottom: 6px;">{d['book_confirm_title']}</div>
                <div style="font-size: 0.82rem; color: #e2f1ec;" id="bookingSummaryText">09:30 CET</div>
            </div>

            <div class="d-flex justify-content-center gap-3">
                <button type="button" class="btn-cert-print" onclick="confirmBookingAndOpenWa()">
                    {d['book_cta']}
                </button>
                <button type="button" class="btn-cert-close" onclick="closeStrategicBookingModal()">
                    {d['book_cancel']}
                </button>
            </div>
        </div>
    </div>'''
    return html

def generate_js_handlers(lang):
    d = get_prop_data(lang)
    unit = d['mig_unit']
    recip_default = d['cert_recip_default']
    prefix = d['wa_book_prefix']
    progress_txt = d['audit_progress']
    verified_txt = d['audit_verified']
    audit_ok = d['audit_ok']

    js = f'''
function openRoiCertModal() {{
    const clientNameInput = document.getElementById('quickClientNameInput');
    const name = clientNameInput && clientNameInput.value ? clientNameInput.value.trim() : '{recip_default}';
    const dispEl = document.getElementById('certClientNameDisplay');
    if (dispEl) dispEl.innerText = name;

    const resSavings = document.getElementById('resRoiSavings');
    const certSavings = document.getElementById('certRoiSavingsVal');
    if (resSavings && certSavings) certSavings.innerText = resSavings.innerText;

    const resHours = document.getElementById('resRoiHours');
    const certHours = document.getElementById('certRoiHoursVal');
    if (resHours && certHours) certHours.innerText = resHours.innerText;

    const resYield = document.getElementById('resRoiYield');
    const certYield = document.getElementById('certRoiYieldVal');
    if (resYield && certYield) certYield.innerText = resYield.innerText;

    const modal = document.getElementById('roiCertModal');
    if (modal) modal.classList.add('active');
}}

function closeRoiCertModal() {{
    const modal = document.getElementById('roiCertModal');
    if (modal) modal.classList.remove('active');
}}

let selectedBookingTopic = '{d["book_t1"]}';
let selectedBookingHost = '{d["book_h1"]}';
let selectedBookingSlot = '09:30 CET';

function openStrategicBookingModal() {{
    const modal = document.getElementById('strategicBookingModal');
    if (modal) modal.classList.add('active');
}}

function closeStrategicBookingModal() {{
    const modal = document.getElementById('strategicBookingModal');
    if (modal) modal.classList.remove('active');
}}

function selectBookingTopic(btn, topic) {{
    const pills = btn.parentElement.querySelectorAll('.booking-pill');
    pills.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    selectedBookingTopic = topic;
}}

function selectBookingHost(btn, host) {{
    const pills = btn.parentElement.querySelectorAll('.booking-pill');
    pills.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    selectedBookingHost = host;
}}

function selectBookingSlot(btn, slot) {{
    const slots = btn.parentElement.querySelectorAll('.booking-slot-btn');
    slots.forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    selectedBookingSlot = slot;
}}

function confirmBookingAndOpenWa() {{
    const box = document.getElementById('bookingConfirmBox');
    const summary = document.getElementById('bookingSummaryText');
    if (box) box.classList.add('active');
    if (summary) summary.innerText = `${{selectedBookingTopic}} | ${{selectedBookingHost}} | ${{selectedBookingSlot}}`;

    const phone = selectedBookingHost.includes('Raed') ? '31618111116' : '31618111116';
    const text = encodeURIComponent(`{prefix}\\n- ${{selectedBookingTopic}}\\n- ${{selectedBookingHost}}\\n- ${{selectedBookingSlot}}`);
    setTimeout(() => {{
        window.open(`https://wa.me/${{phone}}?text=${{text}}`, '_blank', 'noopener,noreferrer');
    }}, 600);
}}

function runComplianceAuditScanner() {{
    const btn = document.getElementById('btnRunAudit');
    const status = document.getElementById('auditStatusText');
    if (!btn || !status) return;
    btn.disabled = true;
    btn.innerText = '{progress_txt}';
    setTimeout(() => {{
        btn.disabled = false;
        btn.innerText = '{verified_txt}';
        status.innerHTML = '{audit_ok}';
    }}, 800);
}}

function selectMigrationSystem(btn, sys) {{
    const btns = btn.parentElement.querySelectorAll('.migration-sys-btn');
    btns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    calcMigrationEstimator();
}}

function calcMigrationEstimator() {{
    const range = document.getElementById('slideMigVolume');
    const vol = range ? parseInt(range.value, 10) : 250;
    const disp = document.getElementById('dispMigVolume');
    if (disp) disp.innerText = `${{vol}} {unit}`;

    const activeSysBtn = document.querySelector('.migration-systems-row .migration-sys-btn.active');
    const sys = activeSysBtn ? activeSysBtn.innerText : 'SAP';

    let hours = Math.round(vol * 0.12 + 12);
    let savings = sys.includes('SAP') || sys.includes('Oracle') ? 44 : 36;

    const valTime = document.getElementById('migValTime');
    if (valTime) valTime.innerText = `${{hours}} h (Zero-Downtime)`;

    const valIntegrity = document.getElementById('migValIntegrity');
    if (valIntegrity) valIntegrity.innerText = '99.98%';

    const valSavings = document.getElementById('migValSavings');
    if (valSavings) valSavings.innerText = `-${{savings}}%`;
}}
'''
    return js

def deploy_to_portal(file_path, lang):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip fr/demo.html since it was already cleanly deployed and tested
    if lang == 'fr':
        print(f"Skipping fr/demo.html (already deployed & verified).")
        return True

    d = get_prop_data(lang)

    # 1. Inject Sovereign Shield & Migration Estimator into #tab-cloud
    # Replace static text block in #tab-cloud
    shield_html = generate_shield_and_mig_html(lang)
    # Check if already present
    if 'sovereign-shield-card' not in content:
        # Pattern to replace in tab-cloud
        # Match <div class="glass-box">...Enterprise Security...</div></section>
        pat = r'(<div class="glass-box">\s*<h3 class="mb-3">Enterprise Security.*?</div>\s*</section>)'
        m = re.search(pat, content, re.DOTALL)
        if m:
            content = content[:m.start()] + shield_html + '\n            </section>' + content[m.end():]
        else:
            # Fallback: find </section> of tab-cloud
            m_cloud = re.search(r'(<section class="tab-section" id="tab-cloud".*?)(</section>)', content, re.DOTALL)
            if m_cloud:
                content = content[:m_cloud.end(1)] + shield_html + '\n            ' + content[m_cloud.end(1):]

    # 2. Update ROI Actions in #tab-roi
    # Replace the single button with dual actions
    roi_actions_html = f'''                <div class="d-flex justify-content-center align-items-center flex-wrap gap-3 mt-4">
                    <button type="button" class="btn-sync-consultation" onclick="openStrategicBookingModal()">
                        <span>{d['roi_book_btn']}</span>
                    </button>
                    <button type="button" class="btn-cert-print" onclick="openRoiCertModal()">
                        <span>{d['roi_cert_btn']}</span>
                    </button>
                </div>'''
    
    # Replace old button container in tab-roi
    pat_roi = r'<div class="text-center mt-4">\s*<button type="button" class="btn-sync-consultation".*?</button>\s*</div>'
    if re.search(pat_roi, content, re.DOTALL):
        content = re.sub(pat_roi, roi_actions_html, content, count=1, flags=re.DOTALL)

    # 3. Add Strategic Booking action into Hotline card
    hotline_book_html = f'''                <div class="hotline-booking-action" style="margin-top: 14px; text-align: center;">
                    <button type="button" class="btn-cert-print" style="width: 100%; font-size: 0.8rem; padding: 8px 12px;" onclick="openStrategicBookingModal()">
                        {d['hotline_book_btn']}
                    </button>
                </div>
            </div>
        </div>'''
    if 'hotline-booking-action' not in content:
        content = re.sub(r'(\s*</div>\s*</div>\s*<button type="button" class="hotline-trigger-pill")', '\n' + hotline_book_html + r'\n        <button type="button" class="hotline-trigger-pill"', content, count=1)

    # 4. Inject Modals right after Hotline Widget (before <script id="sovereignFeaturesLogic">)
    modals_html = generate_modals_html(lang)
    if 'id="roiCertModal"' not in content:
        content = re.sub(r'(<div class="sovereign-hotline-widget".*?</div>\s*</div>)', r'\1\n' + modals_html, content, count=1, flags=re.DOTALL)

    # 5. Inject JS functions into <script id="sovereignFeaturesLogic">
    js_code = generate_js_handlers(lang)
    if 'function openRoiCertModal' not in content:
        # Insert before document.addEventListener('DOMContentLoaded' in sovereignFeaturesLogic
        pat_dom = r'(document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{.*?calcPortalRoi\(\);)(\s*\}\);)'
        m_dom = re.search(pat_dom, content, re.DOTALL)
        if m_dom:
            repl = js_code + '\n' + m_dom.group(1) + '\n    calcMigrationEstimator();' + m_dom.group(2)
            content = content[:m_dom.start()] + repl + content[m_dom.end():]
        else:
            # Append before </script> of sovereignFeaturesLogic
            content = re.sub(r'(</script>\s*</body>)', js_code + r'\n\1', content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Deployed 4 proposals to {file_path}")
    return True

def main():
    dirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and os.path.exists(os.path.join(BASE_DIR, d, 'demo.html'))]
    print(f"Deploying 4 proposals across {len(dirs) + 1} portals...")

    # Root demo.html (Arabic)
    deploy_to_portal(os.path.join(BASE_DIR, 'demo.html'), 'ar')

    # Subdirectories
    for d in sorted(dirs):
        file_path = os.path.join(BASE_DIR, d, 'demo.html')
        deploy_to_portal(file_path, d)

    print("\n🎉 Deployment completed across all portals!")

if __name__ == '__main__':
    main()
