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
S&R CoreSync Solutions - 100% Strict Language Isolation Cleaner
Replaces all remaining Arabic comments, toasts, and UI labels in non-Arabic language directories.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

REPLACEMENTS = [
    # Table & Totals
    ('<th>VAT / BTW المحتسبة</th>', '<th>Calculated VAT / Tax</th>'),
    ('<span>Grand Total المستحق والمقيد بالدفاتر:</span>', '<span>Grand Total Due & Recorded in Ledger:</span>'),
    ('Synchronized فوراً', 'Synchronized Instantly'),
    ('مدفوعة عبر', 'Paid via'),
    ('ترخيص معتمد', 'Certified License'),
    ('ترخيص رقمي مشفر مع دعم التحديثات', 'Encrypted Digital License with Live Updates'),
    ('ربط مباشر عبر بوابات الدفع والفواتير', 'Direct Gateway & Automated Invoicing Integration'),
    ('محاكي واجهة برمجيات سطح المكتب التفاعلي (Desktop OS Simulator JS)', 'Desktop Software Interactive OS Simulator'),
    ('مجموعة الشريك التجاري المستهدف', 'Valued Enterprise Partner Group'),
    ('معفى من VAT / BTW (0%)', 'Zero-Rated VAT / Tax Exempt (0%)'),
    ('📦 ERP & Lagerlogistik الذكية', '📦 Smart Cloud ERP & Warehouse Logistics'),

    # Toasts & Alerts
    ('تمت إضافة المعاملة بنجاح وتحديث قيود الـ ERP والرسوم البيانية لحظياً!', 'Transaction added successfully. ERP ledger and analytics updated!'),
    ('✨ تم حفظ وتطبيق هوية [${name}] على نظام الـ ERP بنجاح!', '✨ Brand identity for [${name}] successfully saved and applied!'),
    ('🔑 تم Kopieren Key: ${key}', '🔑 License key copied: ${key}'),
    ('🔑 تم Kopieren Key التجريبي: ${key}', '🔑 Trial license key copied: ${key}'),
    ('🔑 تم Kopieren Key: ${key}', '🔑 License key copied: ${key}'),
    ('🏛️ تم تطبيق Steuermodell: ${vatText}', '🏛️ Tax model updated: ${vatText}'),
    ('⚡ بدأ Download Package لـ [${title}] بنجاح!', '⚡ Downloading official quick-start package for [${title}]...'),
    ('🛡️ اكتمل تدقيق الامتثال الضريبي بنجاح: متوافق بنسبة 100%!', '🛡️ Tax compliance audit completed: 100% Compliant!'),
    ('⚡ تم توليد وتشفير ملف Digipoort XML بنجاح!', '⚡ Digipoort XML audit payload generated and signed successfully!'),
    ('🎉 تم إتمام الدفع بنجاح وإصدار الفاتورة [${invNum}] وActivate الترخيص!', '🎉 Payment settled successfully. Invoice [${invNum}] issued and license activated!'),
    ('🎉 تم إتمام الدفع بنجاح وإصدار الفاتورة [${invNum}] وتفعيل الترخيص!', '🎉 Payment settled successfully. Invoice [${invNum}] issued and license activated!'),
    ('تم نسخ مفتاح الترخيص!', 'License key copied to clipboard!'),
    ('بدأ تنزيل حزمة التثبيت لـ', 'Downloading setup package for'),

    # Dynamic UI assignments
    ("badge.innerText = 'ترخيص تجريبي 14 يوماً';", "badge.innerText = '14-Day Free Trial';"),
    ("badge.innerText = 'ترخيص تجاري كامل (Pro)';", "badge.innerText = 'Commercial Enterprise (Pro)';"),
    ("btnBuy.innerText = `ترقية للنسخة الكاملة (€ ${sw.price})`;", "btnBuy.innerText = `Upgrade to Full Suite (€ ${sw.price})`;"),
    ("btnBuy.innerText = `إتمام الشراء والفوترة (€ ${sw.price})`;", "btnBuy.innerText = `Checkout & License (€ ${sw.price})`;"),

    # AI chatbot mock response
    ('توجد 1 invoice معلقة بقيمة €35,000 لعميل في الرياض due within 14 d', 'There is 1 pending invoice of €35,000 due within 14 days.')
]

# Process non-Arabic language dirs
langs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d)) and os.path.exists(os.path.join(BASE_DIR, d, 'demo.html'))]
target_langs = [d for d in langs if d not in ['ckb']]

print(f"Cleaning language isolation across {len(target_langs)} portals...")

for lang in target_langs:
    p = os.path.join(BASE_DIR, lang, 'demo.html')
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply all string replacements
    for src, dst in REPLACEMENTS:
        content = content.replace(src, dst)

    # Clean any JS line comments with Arabic letters: // ...
    def clean_comment(m):
        comment_text = m.group(0)
        # If comment contains arabic
        if re.search(r'[\u0600-\u06FF]', comment_text):
            return '// Enterprise CoreSync Engine Logic'
        return comment_text

    content = re.sub(r'//[^\n\r]*[\u0600-\u06FF][^\n\r]*', clean_comment, content)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print("Language isolation cleaning completed!")
