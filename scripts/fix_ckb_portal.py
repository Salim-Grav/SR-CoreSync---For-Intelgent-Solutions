#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_ckb_portal.py
=================
S&R CoreSync – Kurdish Sorani (CKB) Portal Full Localization Fix
Fixes ckb/index.html which was a copy of the Arabic page with Arabic content
instead of Kurdish Sorani (ckb) translations.

Targets:
  - <title> tag
  - meta description, og:title, og:description, twitter:title, twitter:description
  - og:locale, og:image:alt, twitter:image:alt
  - vcard title
  - data-page-language attribute
  - alt text on all images (Arabic → Kurdish Sorani)
  - visible H1/H2/H3 headings that contain Arabic
  - hero section key texts (brand tag, hero title, availability text)
  - navigation items
  - footer copyright
"""

import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKB_FILE = os.path.join(BASE_DIR, 'ckb', 'index.html')

# ─────────────────────────────────────────────
# Kurdish Sorani (CKB) Translation Dictionary
# ─────────────────────────────────────────────

CKB_META = {
    # Title
    'S&R CoreSync For Intelligent Solutions | برمجيات متقدمة، حلول ERP واستشارات مالية ذكية':
        'S&R CoreSync For Intelligent Solutions | نەرمەکالای پێشکەوتوو، چارەسەری ERP و ڕاوێژی داراییی زیرەک',

    # meta description
    'S&R CoreSync For Intelligent Solutions - رواد تطوير البرمجيات السحابية المخصصة، تطبيقات الجوال، تكامل أنظمة الـ ERP والمحاسبة، وأتمتة الذكاء الاصطناعي في هولندا وأوروبا والشرق الأوسط.':
        'S&R CoreSync For Intelligent Solutions - پیشەوای پەرەپێدانی نەرمەکالای هەور، ئەپلیکەیشنی مۆبایل، یەکگرتنی سیستەمەکانی ERP و ئەتۆماسیۆنی زیرەکی دەستکردی لە هۆڵەندا، ئەوروپا و ڕۆژهەڵاتی ناوەڕاست.',

    # og:title
    'S&R CoreSync For Intelligent Solutions | القيادة التنفيذية وهندسة البرمجيات السحابية وأنظمة ERP المتقدمة':
        'S&R CoreSync For Intelligent Solutions | سەرکردایەتی کارگێڕی و ئەندازیاری نەرمەکالای هەور و سیستەمەکانی ERP پێشکەوتوو',

    # og:description / twitter:description
    'حلول البرمجيات السحابية المؤسسية وهندسة الذكاء الاصطناعي وتكامل أنظمة الـ ERP المالية بإشراف م. محمد سليم عزيزة و أ. محمد رائد كعكة.':
        'چارەسەرەکانی نەرمەکالای هەوری دامەزراوەیی و ئەندازیاری زیرەکی دەستکردی و یەکگرتنی سیستەمەکانی ERP داراییی بە سەرپەرشتیی م. محمد سلیم عزیزة و أ. محمد رائد كعكة.',

    # og:image:alt / twitter:image:alt
    'S&R CoreSync For Intelligent Solutions - القيادة التنفيذية والمؤسسون':
        'S&R CoreSync For Intelligent Solutions - سەرکردایەتی کارگێڕی و دامەزرێنەران',

    # vcard title
    'S&R CoreSync Solutions - بطاقة التواصل (vCard)':
        'S&R CoreSync Solutions - کارتی پەیوەندی (vCard)',

    # og:locale
    'ar_AR': 'ckb_IQ',
}

# Image alt text replacements: Arabic → Kurdish Sorani
CKB_ALT_MAP = {
    'الشعار الذهبي الفاخر S&amp;R CoreSync': 'ئامراز S&amp;R CoreSync زێرین',
    'الشعار الذهبي الفاخر': 'ئامراز زێرین',
    'الشعار الرسمي S&amp;R CoreSync': 'ئامرازی فەرمی S&amp;R CoreSync',
    'م. محمد سليم عزيزة': 'م. محمد سلیم عزیزة',
    'أ. محمد رائد كعكة': 'أ. محمد رائد كعكة',
    'م. محمد سليم': 'م. محمد سلیم',
    'أ. محمد رائد': 'أ. محمد رائد',
    'تصميم الهوية البصرية - S&R CoreSync': 'ئامادەکردنی ناسنامەی بینراو - S&R CoreSync',
    'تطوير المواقع الإلكترونية - S&R CoreSync': 'پەرەپێدانی مەلپەڕ - S&R CoreSync',
    'التجارة الإلكترونية - S&R CoreSync': 'بازرگانی ئەلیکترۆنی - S&R CoreSync',
    'برمجيات سحابية - S&R CoreSync': 'نەرمەکالای هەور - S&R CoreSync',
    'تطبيقات الجوال - S&R CoreSync': 'ئەپلیکەیشنی مۆبایل - S&R CoreSync',
    'أنظمة ERP والمالية - S&R CoreSync': 'سیستەمەکانی ERP و دارایی - S&R CoreSync',
    'الذكاء الاصطناعي والأتمتة - S&R CoreSync': 'زیرەکی دەستکردی و ئۆتۆماسیۆن - S&R CoreSync',
    'الاستشارات المالية - S&R CoreSync': 'ڕاوێژی دارایی - S&R CoreSync',
    'الأمن السيبراني - S&R CoreSync': 'ئەمنیەتی سایبەری - S&R CoreSync',
    'خلفية الجبل': 'شەقامی چیا',
    'صورة العمل': 'وێنەی کار',
    'المدير التنفيذي ورئيس مجلس الإدارة': 'بەڕێوەبەری کارگێڕی و سەرۆکی ئەنجومەنی کارگێڕی',
    'المدير التقني والشريك المؤسس': 'بەڕێوەبەری تەکنیکی و هاوبەشی دامەزرێنەر',
    'خلفية تقنية': 'پاشمینەی تەکنیکی',
    'خلفية ذهبية': 'پاشمینەی زێرین',
    'S&amp;R CoreSync For Intelligent Solutions - الشعار الرسمي': 'S&amp;R CoreSync For Intelligent Solutions - ئامرازی فەرمی',
    'S&amp;R CoreSync For Intelligent Solutions - الشعار الذهبي الرسمي 4K Ultra-DPI': 'S&amp;R CoreSync For Intelligent Solutions - ئامرازی زێرینی فەرمی 4K Ultra-DPI',
    'م. محمد سليم عزيزة - المدير التنفيذي ورئيس مجلس الإدارة': 'م. محمد سلیم عزیزة - بەڕێوەبەری کارگێڕی و سەرۆکی ئەنجومەن',
    'أ. محمد رائد كعكة - المدير التقني والشريك المؤسس': 'أ. محمد رائد كعكة - بەڕێوەبەری تەکنیکی و دامەزرێنەر',
    'م. محمد سليم عزيزة - قائد تنفيذي': 'م. محمد سلیم عزیزة - بەڕێوەبەری کارگێڕی',
    'أ. محمد رائد كعكة - خبير تقني': 'أ. محمد رائد كعكة - پسپۆڕی تەکنیکی',
    'S&amp;R CivicSync - منصة الجاليات والمنظمات': 'S&amp;R CivicSync - پلاتفۆرمی کۆمەڵگا و ڕێکخراوەکان',
    'S&amp;R HealthBridge - منصة الرعاية الصحية': 'S&amp;R HealthBridge - پلاتفۆرمی تەندروستی',
    'S&amp;R OmniBakery - نظام ERP المخابز': 'S&amp;R OmniBakery - سیستەمی ERP نانوایی',
    'خلفية الشبكة': 'پاشمینەی تۆڕ',
    'خلفية متدرجة': 'پاشمینەی لیستە',
    'توقيع محمد سليم': 'واژووی محمد سلیم',
    'S&amp;R CoreSync For Intelligent Solutions - الشعار الرسمي الرسمي 2026': 'S&amp;R CoreSync For Intelligent Solutions - ئامرازی فەرمی 2026',
    'أ. محمد رائد كعكة - الرئيس التنفيذي للتقنية': 'أ. محمد رائد كعكة - بەڕێوەبەری تەکنیکی',
    'توقيع': 'واژوو',
    'م.': 'م.',
    'أ.': 'أ.',
}

# Hero section key texts
CKB_HERO_TEXTS = {
    # Brand tag / hero tag
    'يُقدِّم': 'پێشکەش دەکات',
    'يقدم': 'پێشکەش دەکات',
    # Availability
    'متاح لمشاريع مؤسسية جديدة 2026': 'بەردەستە بۆ پڕۆژەی دامەزراوەیی نوێ 2026',
    'متاح لاستقبال مشاريع مؤسسية جديدة 2026': 'بەردەستە بۆ پڕۆژەی دامەزراوەیی نوێ 2026',
    # Hero title
    'أنظمة مؤسسية': 'سیستەمەکانی دامەزراوەیی',
    'Enterprise Systems': 'Enterprise Systems',
    # Audio label
    'تجربة صوتية محيطية (انقر للتشغيل)': 'ئەزموونی دەنگی ژینگەیی (کلیک بکە بۆ لێدانەوە)',
    # Nav items
    'الخدمات': 'خزمەتگوزارییەکان',
    'التقنيات': 'تەکنەلۆژیاکان',
    'الأعمال': 'کارەکان',
    'البرمجيات': 'نەرمەکالاکان',
    'التسعير': 'نرخەکان',
    'عن الشركة': 'دەربارەی کۆمپانیا',
    'تواصل معنا': 'پەیوەندیمان پێوەبکە',
    # Footer
    'جميع الحقوق محفوظة': 'هەموو مافەکان پارێزراون',
    'سياسة الخصوصية': 'سیاسەتی تایبەتمەندی',
    'شروط الخدمة': 'مەرجەکانی خزمەتگوزاری',
    'اتفاقية مستوى الخدمة': 'ڕێکەوتنی ئاستی خزمەتگوزاری',
}

# Visible heading text replacements (h1/h2/h3 Arabic → Kurdish Sorani)
CKB_HEADINGS = {
    'تصميم الهوية': 'ئامادەکردنی ناسنامە',
    'تطوير الويب': 'پەرەپێدانی وێب',
    'التجارة الإلكترونية': 'بازرگانی ئەلیکترۆنی',
    'أنظمة مؤسسية': 'سیستەمەکانی دامەزراوەیی',
    'برمجيات سحابية': 'نەرمەکالای هەور',
    'تطبيقات الجوال': 'ئەپلیکەیشنی مۆبایل',
    'نظم المالية': 'سیستەمی دارایی',
    'الذكاء الاصطناعي': 'زیرەکی دەستکردی',
    'الاستشارات المالية': 'ڕاوێژی دارایی',
    'الأمن السيبراني': 'ئەمنیەتی سایبەری',
    'أعمالنا': 'کارەکانمان',
    'منصاتنا': 'پلاتفۆرمەکانمان',
    'فريقنا': 'تیمەکەمان',
    'الخدمات': 'خزمەتگوزارییەکان',
    'التقنيات': 'تەکنەلۆژیاکان',
    'شركاؤنا': 'هاوبەشەکانمان',
    'الأسعار': 'نرخەکان',
    'عن الشركة': 'دەربارەی کۆمپانیا',
    'المنصات البيضاء': 'پلاتفۆرمەکانی سپی',
}


def fix_meta_tags(content: str) -> str:
    """Fix title, meta description, og tags, twitter tags for CKB."""
    for ar, ckb in CKB_META.items():
        content = content.replace(ar, ckb)

    # Fix canonical to point to ckb
    content = re.sub(
        r'<link rel="canonical" href="https://sr-coresync\.com/"',
        '<link rel="canonical" href="https://sr-coresync.com/ckb/"',
        content,
        count=1
    )

    # Fix og:url
    content = re.sub(
        r'<meta property="og:url" content="https://sr-coresync\.com/"',
        '<meta property="og:url" content="https://sr-coresync.com/ckb/"',
        content,
        count=1
    )

    # Fix data-page-language attribute
    content = content.replace('data-page-language="ar"', 'data-page-language="ckb"')

    # Fix the lang attribute (should already be ckb but ensure)
    content = re.sub(r'<html lang="ar"', '<html lang="ckb"', content)

    return content


def fix_image_alt_texts(content: str) -> str:
    """Replace Arabic alt text in img tags with Kurdish Sorani equivalents."""

    def replace_alt(match):
        full_tag = match.group(0)
        alt_match = re.search(r'alt="([^"]*)"', full_tag)
        if not alt_match:
            return full_tag
        old_alt = alt_match.group(1)

        # Check if alt contains Arabic characters
        if not re.search(r'[\u0600-\u06FF]', old_alt):
            return full_tag

        new_alt = old_alt
        # Try exact matches first
        for ar, ckb in CKB_ALT_MAP.items():
            if ar in new_alt:
                new_alt = new_alt.replace(ar, ckb)

        # If still Arabic, do generic substitution
        if re.search(r'[\u0600-\u06FF]', new_alt):
            # Replace common patterns
            new_alt = re.sub(r'م\. محمد سليم عزيزة?', 'م. محمد سلیم عزیزة', new_alt)
            new_alt = re.sub(r'أ\. محمد رائد كعكة?', 'أ. محمد رائد كعكة', new_alt)
            new_alt = re.sub(r'محمد سليم', 'محمد سلیم', new_alt)
            new_alt = re.sub(r'الشعار(.*?)S&amp;R', r'ئامراز\1S&amp;R', new_alt)
            new_alt = re.sub(r'الشعار(.*?)S&R', r'ئامراز\1S&R', new_alt)
            new_alt = re.sub(r'الشعار الرسمي', 'ئامرازی فەرمی', new_alt)
            new_alt = re.sub(r'الشعار الذهبي', 'ئامرازی زێرین', new_alt)
            new_alt = re.sub(r'الشعار', 'ئامراز', new_alt)
            new_alt = re.sub(r'صورة', 'وێنە', new_alt)
            new_alt = re.sub(r'خلفية', 'پاشمینە', new_alt)
            new_alt = re.sub(r'توقيع', 'واژوو', new_alt)
            new_alt = re.sub(r'المؤسس', 'دامەزرێنەر', new_alt)
            new_alt = re.sub(r'المدير التنفيذي', 'بەڕێوەبەری کارگێڕی', new_alt)
            new_alt = re.sub(r'المدير التقني', 'بەڕێوەبەری تەکنیکی', new_alt)
            new_alt = re.sub(r'القيادة التنفيذية', 'سەرکردایەتی کارگێڕی', new_alt)
            new_alt = re.sub(r'والمؤسسون', 'و دامەزرێنەران', new_alt)
            new_alt = re.sub(r'الرسمي', 'فەرمی', new_alt)

        return full_tag.replace(f'alt="{old_alt}"', f'alt="{new_alt}"')

    return re.sub(r'<img[^>]*/?>',  replace_alt, content, flags=re.DOTALL)


def fix_hero_section(content: str) -> str:
    """Fix the hero section key visible texts."""
    for ar, ckb in CKB_HERO_TEXTS.items():
        content = content.replace(ar, ckb)
    return content


def fix_page_title_tag(content: str) -> str:
    """Ensure title tag is in Kurdish Sorani."""
    def replace_title(match):
        title_content = match.group(1)
        if re.search(r'[\u0600-\u06FF]', title_content):
            # Keep brand name, replace Arabic description
            title_content = re.sub(
                r'\|[^<]+$',
                '| نەرمەکالای پێشکەوتوو، چارەسەری ERP و ڕاوێژی داراییی زیرەک',
                title_content
            )
        return f'<title>{title_content}</title>'

    return re.sub(r'<title>(.*?)</title>', replace_title, content, flags=re.DOTALL)


def fix_h3_cards(content: str) -> str:
    """Fix visible h3 card titles that contain Arabic service names."""
    def replace_heading(match):
        tag_open = match.group(1)
        text = match.group(2)
        tag_close = match.group(3)

        if not re.search(r'[\u0600-\u06FF]', text):
            return match.group(0)

        new_text = text
        for ar, ckb in CKB_HEADINGS.items():
            new_text = new_text.replace(ar, ckb)

        # If still Arabic, apply generic fallback
        if re.search(r'[\u0600-\u06FF]', new_text):
            new_text = re.sub(r'تصميم', 'ئامادەکردن', new_text)
            new_text = re.sub(r'تطوير', 'پەرەپێدان', new_text)
            new_text = re.sub(r'الهوية البصرية', 'ناسنامەی بینراو', new_text)
            new_text = re.sub(r'البرمجيات', 'نەرمەکالا', new_text)
            new_text = re.sub(r'الموقع الإلكتروني', 'مەلپەڕ', new_text)
            new_text = re.sub(r'التجارة الإلكترونية', 'بازرگانی ئەلیکترۆنی', new_text)
            new_text = re.sub(r'الجوال', 'مۆبایل', new_text)
            new_text = re.sub(r'السحابية?', 'هەور', new_text)
            new_text = re.sub(r'الذكاء الاصطناعي', 'زیرەکی دەستکردی', new_text)
            new_text = re.sub(r'الأمن السيبراني', 'ئەمنیەتی سایبەری', new_text)
            new_text = re.sub(r'الاستشارات', 'ڕاوێژ', new_text)
            new_text = re.sub(r'المالية?', 'دارایی', new_text)
            new_text = re.sub(r'الأنظمة?', 'سیستەم', new_text)
            new_text = re.sub(r'المؤسسية?', 'دامەزراوەیی', new_text)
            new_text = re.sub(r'المنصات?', 'پلاتفۆرم', new_text)
            new_text = re.sub(r'الفريق', 'تیم', new_text)
            new_text = re.sub(r'الأعمال', 'کار', new_text)
            new_text = re.sub(r'الخدمات?', 'خزمەتگوزاری', new_text)

        return f'{tag_open}{new_text}{tag_close}'

    return re.sub(r'(<h[1-3][^>]*>)(.*?)(</h[1-3]>)', replace_heading, content, flags=re.DOTALL)


def fix_nav_items(content: str) -> str:
    """Fix navigation menu items that are in Arabic."""
    nav_translations = {
        '>الخدمات<': '>خزمەتگوزارییەکان<',
        '>التقنيات<': '>تەکنەلۆژیاکان<',
        '>الأعمال<': '>کارەکان<',
        '>البرمجيات<': '>نەرمەکالاکان<',
        '>التسعير<': '>نرخەکان<',
        '>عن الشركة<': '>دەربارەی کۆمپانیا<',
        '>تواصل<': '>پەیوەندی<',
        '>تواصل معنا<': '>پەیوەندیمان پێوەبکە<',
        '>تحدث الآن<': '>ئێستا قسە بکە<',
        '>احجز مشاورة مجانية<': '>ڕاوێژی خۆڕایی حجز بکە<',
        '>ابدأ مشروعك<': '>پڕۆژەکەت دەست پێبکە<',
        '>عرض الأعمال<': '>نیشاندانی کارەکان<',
        '>خدماتنا<': '>خزمەتگوزارییەکانمان<',
        '>متضمن<': '>ناوەوەی<',
        '>طلب عرض سعر رسمي معتمد 📄<': '>داواکردنی نرخی فەرمی پشتگیریکراو 📄<',
        '>عرض الديمو<': '>نیشاندانی دیمۆ<',
    }
    for ar, ckb in nav_translations.items():
        content = content.replace(ar, ckb)
    return content


def fix_platform_flag(content: str) -> str:
    """Fix the sr-platform-flag span text."""
    content = re.sub(
        r'(<span class="sr-platform-flag">)(النموذج الرائد[^<]*)(</span>)',
        r'\1نموونەی پێشەنگ: کۆمەڵگای سووریەیی لە هۆڵەندا\3',
        content
    )
    return content


def fix_footer(content: str) -> str:
    """Fix footer copyright and links."""
    content = re.sub(
        r'(جميع الحقوق محفوظة\.)',
        'هەموو مافەکان پارێزراون.',
        content
    )
    content = re.sub(
        r'>سياسة الخصوصية<',
        '>سیاسەتی تایبەتمەندی<',
        content
    )
    content = re.sub(
        r'>شروط الخدمة<',
        '>مەرجەکانی خزمەتگوزاری<',
        content
    )
    content = re.sub(
        r'>اتفاقية مستوى الخدمة<',
        '>ڕێکەوتنی ئاستی خزمەتگوزاری<',
        content
    )
    return content


def main():
    if not os.path.exists(CKB_FILE):
        print(f"ERROR: File not found: {CKB_FILE}")
        sys.exit(1)

    print(f"Reading: {CKB_FILE}")
    with open(CKB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    print(f"Original size: {original_len:,} bytes")

    # Count Arabic occurrences before fix
    arabic_count_before = len(re.findall(r'[\u0600-\u06FF]{3,}', content))
    print(f"Arabic text blocks before: {arabic_count_before}")

    # Apply all fixes
    print("Fixing meta tags...")
    content = fix_meta_tags(content)

    print("Fixing page title...")
    content = fix_page_title_tag(content)

    print("Fixing image alt texts...")
    content = fix_image_alt_texts(content)

    print("Fixing hero section...")
    content = fix_hero_section(content)

    print("Fixing H1/H2/H3 headings...")
    content = fix_h3_cards(content)

    print("Fixing navigation items...")
    content = fix_nav_items(content)

    print("Fixing platform flag...")
    content = fix_platform_flag(content)

    print("Fixing footer...")
    content = fix_footer(content)

    # Count Arabic occurrences after fix
    arabic_count_after = len(re.findall(r'[\u0600-\u06FF]{3,}', content))
    print(f"Arabic text blocks after: {arabic_count_after}")
    print(f"Reduced by: {arabic_count_before - arabic_count_after} blocks")

    # Write back
    with open(CKB_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Done! Saved: {CKB_FILE}")
    print(f"   New size: {len(content):,} bytes")


if __name__ == '__main__':
    main()
