#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_ckb_alt_texts.py — Fix all Arabic image alt text in ckb/index.html"""

import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE = r'i:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project'
CKB = os.path.join(BASE, 'ckb', 'index.html')

with open(CKB, 'r', encoding='utf-8') as f:
    content = f.read()

# Count Arabic img alt texts before
before_imgs = len(re.findall(r'alt="[^"]*[\u0600-\u06FF][^"]*"', content))
print(f"Arabic alt attrs BEFORE: {before_imgs}")

def translate_alt(alt_text):
    """Translate Arabic alt text to Kurdish Sorani / English."""
    t = alt_text

    # Names - keep as-is (proper nouns)
    # Service icons
    t = t.replace('تصميم الهوية البصرية', 'Brand Identity Design')
    t = t.replace('تصميم الهوية', 'Brand Identity Design')
    t = t.replace('تطوير المواقع الإلكترونية', 'Web Development')
    t = t.replace('تطوير الويب', 'Web Development')
    t = t.replace('التجارة الإلكترونية', 'E-Commerce')
    t = t.replace('برمجيات سحابية', 'Cloud Software')
    t = t.replace('تطبيقات الجوال', 'Mobile Apps')
    t = t.replace('أنظمة ERP والمالية', 'ERP & Financial Systems')
    t = t.replace('الذكاء الاصطناعي والأتمتة', 'AI & Automation')
    t = t.replace('الذكاء الاصطناعي', 'AI Automation')
    t = t.replace('الاستشارات المالية', 'Financial Advisory')
    t = t.replace('الأمن السيبراني', 'Cybersecurity')

    # Emblem/logo
    t = t.replace('الشعار الذهبي الفاخر', 'Official Gold Luxury Emblem')
    t = t.replace('الشعار الرسمي', 'Official Emblem')
    t = t.replace('الشعار الذهبي الرسمي 4K Ultra-DPI', 'Official Gold Emblem 4K Ultra-DPI')
    t = t.replace('الشعار الرسمي الرسمي 2026', 'Official Emblem 2026')
    t = t.replace('الشعار', 'Emblem')

    # Founder titles
    t = t.replace('المدير التنفيذي ورئيس مجلس الإدارة', 'CEO & Chairman')
    t = t.replace('المدير التقني والشريك المؤسس', 'CTO & Co-Founder')
    t = t.replace('قائد تنفيذي', 'Executive Leader')
    t = t.replace('خبير تقني', 'Technical Expert')
    t = t.replace('الرئيس التنفيذي للتقنية', 'Chief Technology Officer')
    t = t.replace('المؤسس', 'Founder')

    # Platform descriptions
    t = t.replace('منصة الجاليات والمنظمات', 'Community & Organizations Platform')
    t = t.replace('منصة الرعاية الصحية', 'Healthcare Platform')
    t = t.replace('نظام ERP المخابز', 'ERP System for Bakeries')
    t = t.replace('منصة', 'Platform')
    t = t.replace('نظام', 'System')

    # Background / other
    t = t.replace('خلفية الجبل', 'Mountain Background')
    t = t.replace('خلفية الشبكة', 'Grid Background')
    t = t.replace('خلفية متدرجة', 'Gradient Background')
    t = t.replace('خلفية ذهبية', 'Gold Background')
    t = t.replace('خلفية', 'Background')

    # Work / career
    t = t.replace('صورة العمل', 'Work Image')
    t = t.replace('صورة', 'Image')

    # Leadership
    t = t.replace('القيادة التنفيذية والمؤسسون', 'Executive Leadership & Founders')
    t = t.replace('القيادة التنفيذية', 'Executive Leadership')
    t = t.replace('والمؤسسون', '& Founders')

    # Signature
    t = t.replace('توقيع محمد سليم', 'Mohammad Salim Signature')
    t = t.replace('توقيع', 'Signature')

    # People names
    t = t.replace('م. محمد سليم عزيزة', 'Eng. Mohammad Salim Aziza')
    t = t.replace('م. محمد سليم', 'Eng. Mohammad Salim Aziza')
    t = t.replace('أ. محمد رائد كعكة', 'Mr. Mohammad Raed Kaakeh')
    t = t.replace('أ. محمد رائد', 'Mr. Mohammad Raed Kaakeh')
    t = t.replace('محمد سليم', 'Mohammad Salim')
    t = t.replace('محمد رائد', 'Mohammad Raed')

    # Roles
    t = t.replace('قائد تنفيذي ورئيس مجلس الإدارة', 'CEO & Chairman')

    # Abbreviated names
    t = re.sub(r'^م\.\s+', 'Eng. ', t)
    t = re.sub(r'^أ\.\s+', 'Mr. ', t)

    # Generic remaining Arabic
    t = re.sub(r'[\u0600-\u06FF\s]+$', '', t).strip()

    return t

def replace_img_alt(match):
    full_tag = match.group(0)
    alt_match = re.search(r'alt="([^"]*)"', full_tag)
    if not alt_match:
        return full_tag
    old_alt = alt_match.group(1)
    if not re.search(r'[\u0600-\u06FF]', old_alt):
        return full_tag
    new_alt = translate_alt(old_alt)
    return full_tag.replace(f'alt="{old_alt}"', f'alt="{new_alt}"')

content = re.sub(r'<img[^>]*/?>',  replace_img_alt, content, flags=re.DOTALL)

# Also fix the title tag
content = re.sub(
    r'<title>(S&amp;R CoreSync For Intelligent Solutions|S&R CoreSync For Intelligent Solutions)\s*\|[^<]+</title>',
    '<title>S&amp;R CoreSync For Intelligent Solutions | Advanced Software, ERP Solutions &amp; Intelligent Financial Advisory</title>',
    content
)

# Fix meta description
content = re.sub(
    r'(<meta name="description" content="S&amp;R CoreSync For Intelligent Solutions - )[^"]+(")',
    r'\1Pioneer in custom cloud software development, mobile apps, ERP & accounting system integration, and AI automation in Netherlands, Europe &amp; Middle East.\2',
    content
)
content = re.sub(
    r'(<meta name="description" content="S&R CoreSync For Intelligent Solutions - )[^"]+(")',
    r'\1Pioneer in custom cloud software development, mobile apps, ERP & accounting system integration, and AI automation in Netherlands, Europe & Middle East.\2',
    content
)

# Fix og:title
content = re.sub(
    r'(og:title" content="S&amp;R CoreSync For Intelligent Solutions \| )[^"]+(")',
    r'\1Executive Leadership &amp; Cloud Software Engineering and Advanced ERP Systems\2',
    content
)

# Fix og:description
content = re.sub(
    r'(og:description" content=")[^"]*[\u0600-\u06FF][^"]+(")',
    r'\1Enterprise cloud software solutions, AI engineering and financial ERP system integration, led by Eng. Mohammad Salim Aziza and Mr. Mohammad Raed Kaakeh.\2',
    content
)

# Fix og:image:alt
content = re.sub(
    r'(og:image:alt" content=")[^"]*[\u0600-\u06FF][^"]+(")',
    r'\1S&amp;R CoreSync For Intelligent Solutions - Executive Leadership &amp; Founders\2',
    content
)

# Fix twitter:title
content = re.sub(
    r'(twitter:title" content="S&amp;R CoreSync For Intelligent Solutions \| )[^"]+(")',
    r'\1Executive Leadership &amp; Cloud Software Engineering and Advanced ERP Systems\2',
    content
)
content = re.sub(
    r'(twitter:title" content="S&R CoreSync For Intelligent Solutions \| )[^"]+(")',
    r'\1Executive Leadership & Cloud Software Engineering and Advanced ERP Systems\2',
    content
)

# Fix twitter:description
content = re.sub(
    r'(twitter:description" content=")[^"]*[\u0600-\u06FF][^"]+(")',
    r'\1Enterprise cloud software solutions, AI engineering and financial ERP system integration.\2',
    content
)

# Fix twitter:image:alt
content = re.sub(
    r'(twitter:image:alt" content=")[^"]*[\u0600-\u06FF][^"]+(")',
    r'\1S&amp;R CoreSync For Intelligent Solutions - Executive Leadership &amp; Founders\2',
    content
)

# Fix vCard title
content = content.replace(
    'S&amp;R CoreSync Solutions - بطاقة التواصل (vCard)',
    'S&amp;R CoreSync Solutions - Business Contact Card (vCard)'
)
content = content.replace(
    'S&R CoreSync Solutions - بطاقة التواصل (vCard)',
    'S&R CoreSync Solutions - Business Contact Card (vCard)'
)

# Fix og:locale
content = content.replace('content="ar_AR"', 'content="ckb_IQ"')
content = content.replace("content='ar_AR'", "content='ckb_IQ'")

# Fix data-page-language
content = content.replace('data-page-language="ar"', 'data-page-language="ckb"')

# Fix canonical URL
content = re.sub(
    r'<link rel="canonical" href="https://sr-coresync\.com/"',
    '<link rel="canonical" href="https://sr-coresync.com/ckb/"',
    content, count=1
)

# Fix hero section visible texts
hero_fixes = [
    ('يُقدِّم', 'PRESENTS'),
    ('يقدم', 'PRESENTS'),
    ('متاح لمشاريع مؤسسية جديدة 2026', 'Available for New Enterprise Projects 2026'),
    ('متاح لاستقبال مشاريع مؤسسية جديدة 2026', 'Available for New Enterprise Projects 2026'),
    ('تجربة صوتية محيطية (انقر للتشغيل)', 'Ambient Audio Experience (Click to Play)'),
    ('النموذج الرائد: الجالية السورية في هولندا', 'Pilot: Syrian Community in Netherlands'),
    ('جميع الحقوق محفوظة', 'All Rights Reserved'),
]
for ar, en in hero_fixes:
    content = content.replace(ar, en)

# Fix visible heading service cards (dana-card-title and similar)
heading_fixes = [
    ('>تصميم الهوية البصرية<', '>Brand Identity Design<'),
    ('>تصميم الهوية<', '>Brand Identity<'),
    ('>تطوير المواقع<', '>Web Development<'),
    ('>تطوير الويب<', '>Web Development<'),
    ('>التجارة الإلكترونية<', '>E-Commerce<'),
    ('>أنظمة مؤسسية<', '>Enterprise Systems<'),
    ('>برمجيات سحابية<', '>Cloud Software<'),
    ('>تطبيقات الجوال<', '>Mobile Apps<'),
    ('>الذكاء الاصطناعي<', '>AI & Automation<'),
    ('>الاستشارات المالية<', '>Financial Advisory<'),
    ('>الأمن السيبراني<', '>Cybersecurity<'),
]
for ar, en in heading_fixes:
    content = content.replace(ar, en)

# Count after
after_imgs = len(re.findall(r'alt="[^"]*[\u0600-\u06FF][^"]*"', content))
print(f"Arabic alt attrs AFTER: {after_imgs}")
print(f"Fixed: {before_imgs - after_imgs} image alt attributes")

with open(CKB, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Saved: {CKB}")

