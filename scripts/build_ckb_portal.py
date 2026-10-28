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
S&R CoreSync For Intelligent Solutions - Sorani Kurdish (ckb) Portal Generator
Generates full RTL Kurdish Sorani portal based on Arabic RTL master.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(BASE_DIR, 'demo.html')
INDEX_AR_PATH = os.path.join(BASE_DIR, 'index.html')

from deploy_sovereign_multilingual import build_dropdown_html, build_dropdown_js, build_apple_dock_html

CKB_DIR = os.path.join(BASE_DIR, 'ckb')
os.makedirs(CKB_DIR, exist_ok=True)

CKB_DEMO_PATH = os.path.join(CKB_DIR, 'demo.html')
CKB_INDEX_PATH = os.path.join(CKB_DIR, 'index.html')

with open(DEMO_AR_PATH, 'r', encoding='utf-8') as f:
    ar_demo = f.read()

with open(INDEX_AR_PATH, 'r', encoding='utf-8') as f:
    ar_index = f.read()

# Exhaustive Sorani Kurdish Replacements from Arabic Master
CKB_REPLACEMENTS = {
    "النظام السحابي متصل (EU Node)": "ڕاژەی هەورەیی چالاکە (EU Node)",
    "ابدأ الجولة 🚀": "دەستپێکردنی گەشت 🚀",
    "ملخص العرض (PDF)": "کورتەی پێشنیار (PDF)",
    "عرض الزبائن [P]": "نمایشی کڕیاران [P]",
    "حجز استشارة بهذا النظام": "تۆمارکردنی راوێژکاری بەم سیستەمە",
    "استوديو الشعار": "ستۆدیۆی لۆگۆ",
    "العودة للموقع": "گەڕانەوە بۆ ماڵپەڕ",
    "لوحة القيادة المالية": "داشبۆردی سەرکردایەتی دارایی",
    "إدارة الـ ERP والمخازن": "بەڕێوەبردنی ERP و کۆگاکان",
    "الفواتير والتدفقات النقدية": "فەتوورەی ئەلەکترۆنی و نەختینە",
    "المساعد المالي الذكي (AI)": "هاوکاری زیرەکی دارایی (AI)",
    "حالة الخوادم السحابية": "ڕەوشی ڕاژەکارە هەورەییەکان",
    "تخصيص الهوية (White-Label)": "تایبەتمەندکردنی براند (White-Label)",
    "سوق البرمجيات (Software Hub)": "کۆگای نەرمەکاڵاکان (Software Hub)",
    "استشارة مؤسسية": "راوێژکاری دامەزراوەیی",
    "طلب تفعيل للنظام بالكامل": "داواکاری چالاککردنی تەواوی سیستەم",
    "حجز استشارة خاصة": "تۆمارکردنی راوێژکاری تایبەت",
    "جلسة تفاعلية تجريبية": "دانیشتنی تاقیکاری کارلێککارانە",
    "عرض تنفيذي S&R": "نمایشی جێبەجێکاری S&R",
    "محاكي العملات والضرائب الحي": "هاوشێوەکەری دراو و باج لە کاتی ڕاستەقینەدا",
    "الضريبة المحتسبة:": "باجی ئەژمارکراو:",
    "النظام الضريبي:": "مۆدێلی باج:",
    "العملة:": "دراو:",
    "لوحة القيادة والتدفق المالي اللحظي": "داشبۆردی سەرکردایەتی و جوڵەی نەختینەی دارایی",
    "نظام محاكاة حي لحركات الحسابات والإيرادات والمصروفات السحابية المؤتمتة": "سیستەمی هاوشێوەکاری ڕاستەوخۆ بۆ جوڵەی هەژمارەکان، داهات و خەرجییە هەورەییە ئۆتۆماتیکەکان",
    "تسجيل معاملة تجريبية": "تۆمارکردنی مامەڵەی تاقیکاری",
    "إجمالي الإيرادات السنوية": "کۆی داهاتی ساڵانە",
    "التدفقات النقدية الصافية": "نەختینەی ئۆپەراسیۆنی خاوێن",
    "طلبات الـ ERP المنجزة": "داواکارییە تەواوکراوەکانی ERP",
    "عمليات الأتمتة الموفرة": "کاتژمێری پاشەکەوتکراوی ئۆتۆماتیک",
    "مقارنة بالربع السابق": "بەراورد بە چارەکی پێشوو",
    "هامش ربحية تشغيلية": "ڕێژەی قازانجی کارگێڕی",
    "نسبة الامتثال والدقة": "ڕێژەی پابەندبوون و دروستی",
    "وفر شهري مباشر في وقت الفريق": "پاشەکەوتی ڕاستەوخۆی مانگانە لە کاتی تیمدا",
    "حركة الإيرادات والتدفق النقدي الشهري (€)": "جوڵەی داهات و نەختینەی مانگانە (€)",
    "توزيع العمليات حسب القطاع": "دابەشکردنی کارەکان بەپێی کەرتەکان",
    "سجل المعاملات والفواتير الحية": "تۆماری مامەڵەکان و فەتوورە زیندووەکان",
    "إصدار فاتورة جديدة": "دەرکردنی فەتوورەی نوێ",
    "تصدير CSV": "هەناردەکردنی CSV",
    "العميل / المنشأة": "کڕیار / دامەزراوە",
    "التاريخ": "مێژوو",
    "المبلغ": "بڕی پارە",
    "حالة الفاتورة": "ڕەوشی فەتوورە",
    "إجراءات تفاعلية": "کردارە کارلێککارەکان",
    "حالة المزامنة": "ڕەوشی هاوکاتکردن",
    "الكل": "هەموو",
    "مدفوعة": "دراوە",
    "معلقة": "هەڵپەسێردراو",
    "تمت المزامنة فوراً": "دەستبەجێ هاوکات کرا",
    "معاينة الفاتورة": "بینینی فەتوورە",
    "تحميل PDF": "داگرتنی PDF",
    "حساب سريع": "ئەژمارکردنی خێرا",
    "اختر معدل الضريبة": "ڕێژەی باج هەڵبژێرە",
    "إغلاق": "داخستن",
    "نسخ": "کۆپیکردن",
    "طباعة / حفظ كـ PDF": "چاپکردن / پاشەکەوتکردن وەک PDF",
    "S&R CoreSync | بوابة النظام السحابي التفاعلية (Live Interactive Demo Portal)": "S&R CoreSync | دەروازەی سیستەمی هەورەیی کارلێککارانە (Demo)",
}

# 1. Generate ckb/demo.html
c_demo = ar_demo
c_demo = re.sub(r'<html lang="[^"]*" dir="[^"]*"', '<html lang="ckb" dir="rtl"', c_demo)

# Apply Sorani replacements
for ar_txt, ckb_txt in CKB_REPLACEMENTS.items():
    c_demo = c_demo.replace(ar_txt, ckb_txt)

def fix_subfolder_links(html, page_type="index"):
    root_pages = [
        "status.html", "verify.html", "whitelabel-calculator.html", "contract-of2026-pdf.html",
        "card.html", "3d-mockup.html", "software.html", "estimator.html", "logo-studio.html",
        "manifest.json"
    ]
    for p in root_pages:
        html = html.replace(f'href="./{p}"', f'href="../{p}"')
        html = html.replace(f'href="{p}"', f'href="../{p}"')
    
    for folder in ["assets", "css", "js", "downloads"]:
        html = html.replace(f'href="./{folder}/', f'href="../{folder}/')
        html = html.replace(f'href="{folder}/', f'href="../{folder}/')
        html = html.replace(f'src="./{folder}/', f'src="../{folder}/')
        html = html.replace(f'src="{folder}/', f'src="../{folder}/')
    
    langs = ["de", "fr", "en", "nl", "es", "it", "sv", "no", "tr", "ku", "da", "fi", "cs", "el", "ro", "hu", "bg", "sk", "hr", "lt", "sl", "lv", "et", "ga", "mt", "pl", "pt"]
    for l in langs:
        html = html.replace(f'href="./{l}/', f'href="../{l}/')
        html = html.replace(f'href="{l}/', f'href="../{l}/')
        
    return html

def inject_apple_dock(html, code="ckb", page_type="index"):
    dock_html = build_apple_dock_html(code, page_type=page_type, is_subfolder=True)
    pattern_dock = r'<!-- Apple macOS Sovereign Language & Flags Dock -->[\s\S]*?</aside>'
    if re.search(pattern_dock, html):
        return re.sub(pattern_dock, dock_html, html, count=1)
    return html.replace('</body>', dock_html + '\n</body>', 1)

# Relative links update for ckb subfolder
c_demo = fix_subfolder_links(c_demo, page_type="demo")

# Inject dropdown for ckb
ckb_dropdown_demo = build_dropdown_html("ckb", page_type="demo", is_subfolder=True)

# Replace existing dropdown in demo
pattern_hub = r'(?:<!-- Sovereign Global Multilingual Hub[^\n]*\n\s*)?<div class="sovereign-lang-hub-wrap"[\s\S]*?</div>\s*</div>\s*</div>'
pattern_drop = r'(?:<!-- Sovereign Global Multilingual Hub[^\n]*\n\s*)?<div class="sovereign-lang-dropdown"[\s\S]*?</div>\s*</div>'
if re.search(pattern_hub, c_demo):
    c_demo = re.sub(pattern_hub, ckb_dropdown_demo, c_demo, count=1)
elif re.search(pattern_drop, c_demo):
    c_demo = re.sub(pattern_drop, ckb_dropdown_demo, c_demo, count=1)

c_demo = inject_apple_dock(c_demo, code="ckb", page_type="demo")
if 'Sovereign Global Multilingual Hub Controller' not in c_demo:
    c_demo = c_demo.replace('</body>', build_dropdown_js() + '\n</body>', 1)

with open(CKB_DEMO_PATH, 'w', encoding='utf-8') as f:
    f.write(c_demo)
print("Generated Sorani Kurdish Portal: ckb/demo.html [RTL]")

# 2. Generate ckb/index.html
c_index = ar_index
c_index = re.sub(r'<html lang="[^"]*" dir="[^"]*"', '<html lang="ckb" dir="rtl"', c_index)

for ar_txt, ckb_txt in CKB_REPLACEMENTS.items():
    c_index = c_index.replace(ar_txt, ckb_txt)

c_index = fix_subfolder_links(c_index, page_type="index")
ckb_dropdown_index = build_dropdown_html("ckb", page_type="index", is_subfolder=True)

if re.search(pattern_hub, c_index):
    c_index = re.sub(pattern_hub, ckb_dropdown_index, c_index, count=1)
elif re.search(pattern_drop, c_index):
    c_index = re.sub(pattern_drop, ckb_dropdown_index, c_index, count=1)

c_index = inject_apple_dock(c_index, code="ckb", page_type="index")
if 'Sovereign Global Multilingual Hub Controller' not in c_index:
    c_index = c_index.replace('</body>', build_dropdown_js() + '\n</body>', 1)

with open(CKB_INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(c_index)
print("Generated Sorani Kurdish Landing Page: ckb/index.html [RTL]")
