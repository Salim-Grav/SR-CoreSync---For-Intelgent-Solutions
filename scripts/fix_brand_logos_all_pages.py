#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_brand_logos_all_pages.py
============================
S&R CoreSync – Fix Arabic brand names in logos, images, and shared HTML pages.

This script fixes TWO distinct problems:

1. CKB portal (ckb/index.html): Contains full Arabic content instead of Kurdish Sorani.
   → Replaces Arabic meta tags, image alt texts, visible headings, nav items.

2. Shared tool pages (sovereign-*.html, supply-chain*.html, etc.): 
   Their <title> tags and <h1> headers still reference Arabic-only descriptions.
   The brand name S&R CoreSync is correct but descriptive text is Arabic-only.
   → For shared pages that ARE Arabic by design, this is acceptable.
   → Only fix cases where the brand name itself was Arabicized.

3. Logos (img alt tags) with Arabicized brand names across ALL language portals.
   → Replace any remaining Arabic brand-name alt texts.
"""

import re
import os
import sys
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────────
# 1. CKB PORTAL TRANSLATIONS
# ─────────────────────────────────────────────────────────────────

CKB_META_REPLACEMENTS = [
    # title
    (
        r'<title>S&amp;R CoreSync For Intelligent Solutions \| برمجيات متقدمة، حلول ERP واستشارات مالية ذكية</title>',
        '<title>S&amp;R CoreSync For Intelligent Solutions | نەرمەکالای پێشکەوتوو، چارەسەری ERP و ڕاوێژی داراییی زیرەک</title>'
    ),
    (
        r'<title>S&R CoreSync For Intelligent Solutions \| برمجيات متقدمة، حلول ERP واستشارات مالية ذكية</title>',
        '<title>S&R CoreSync For Intelligent Solutions | نەرمەکالای پێشکەوتوو، چارەسەری ERP و ڕاوێژی داراییی زیرەک</title>'
    ),
    # meta description
    (
        r'content="S&amp;R CoreSync For Intelligent Solutions - رواد تطوير البرمجيات[^"]*"',
        'content="S&amp;R CoreSync For Intelligent Solutions - پیشەوای پەرەپێدانی نەرمەکالای هەور، ئەپلیکەیشنی مۆبایل، یەکگرتنی سیستەمەکانی ERP و ئەتۆماسیۆنی زیرەکی دەستکردی لە هۆڵەندا، ئەوروپا و ڕۆژهەڵاتی ناوەڕاست."'
    ),
    (
        r'content="S&R CoreSync For Intelligent Solutions - رواد تطوير البرمجيات[^"]*"',
        'content="S&R CoreSync For Intelligent Solutions - پیشەوای پەرەپێدانی نەرمەکالای هەور، ئەپلیکەیشنی مۆبایل، یەکگرتنی سیستەمەکانی ERP و ئەتۆماسیۆنی زیرەکی دەستکردی لە هۆڵەندا، ئەوروپا و ڕۆژهەڵاتی ناوەڕاست."'
    ),
    # og:title
    (
        r'og:title" content="S&amp;R CoreSync For Intelligent Solutions \| القيادة التنفيذية[^"]*"',
        'og:title" content="S&amp;R CoreSync For Intelligent Solutions | سەرکردایەتی کارگێڕی و ئەندازیاری نەرمەکالای هەور و سیستەمەکانی ERP پێشکەوتوو"'
    ),
    (
        r'og:title" content="S&R CoreSync For Intelligent Solutions \| القيادة التنفيذية[^"]*"',
        'og:title" content="S&R CoreSync For Intelligent Solutions | سەرکردایەتی کارگێڕی و ئەندازیاری نەرمەکالای هەور و سیستەمەکانی ERP پێشکەوتوو"'
    ),
    # og:description
    (
        r'og:description" content="حلول البرمجيات السحابية المؤسسية[^"]*"',
        'og:description" content="چارەسەرەکانی نەرمەکالای هەوری دامەزراوەیی و ئەندازیاری زیرەکی دەستکردی و یەکگرتنی سیستەمەکانی ERP داراییی."'
    ),
    # og:image:alt
    (
        r'og:image:alt" content="S&amp;R CoreSync For Intelligent Solutions - القيادة التنفيذية والمؤسسون"',
        'og:image:alt" content="S&amp;R CoreSync For Intelligent Solutions - سەرکردایەتی کارگێڕی و دامەزرێنەران"'
    ),
    (
        r'og:image:alt" content="S&R CoreSync For Intelligent Solutions - القيادة التنفيذية والمؤسسون"',
        'og:image:alt" content="S&R CoreSync For Intelligent Solutions - سەرکردایەتی کارگێڕی و دامەزرێنەران"'
    ),
    # og:locale
    ('content="ar_AR"', 'content="ckb_IQ"'),
    # twitter:title
    (
        r'twitter:title" content="S&amp;R CoreSync For Intelligent Solutions \| القيادة التنفيذية[^"]*"',
        'twitter:title" content="S&amp;R CoreSync For Intelligent Solutions | سەرکردایەتی کارگێڕی و ئەندازیاری نەرمەکالای هەور و سیستەمەکانی ERP پێشکەوتوو"'
    ),
    (
        r'twitter:title" content="S&R CoreSync For Intelligent Solutions \| القيادة التنفيذية[^"]*"',
        'twitter:title" content="S&R CoreSync For Intelligent Solutions | سەرکردایەتی کارگێڕی و ئەندازیاری نەرمەکالای هەور و سیستەمەکانی ERP پێشکەوتوو"'
    ),
    # twitter:description
    (
        r'twitter:description" content="حلول البرمجيات السحابية المؤسسية[^"]*"',
        'twitter:description" content="چارەسەرەکانی نەرمەکالای هەوری دامەزراوەیی و ئەندازیاری زیرەکی دەستکردی و یەکگرتنی سیستەمەکانی ERP داراییی."'
    ),
    # twitter:image:alt
    (
        r'twitter:image:alt" content="S&amp;R CoreSync For Intelligent Solutions - القيادة التنفيذية والمؤسسون"',
        'twitter:image:alt" content="S&amp;R CoreSync For Intelligent Solutions - سەرکردایەتی کارگێڕی و دامەزرێنەران"'
    ),
    # data-page-language
    ('data-page-language="ar"', 'data-page-language="ckb"'),
    # og:url canonical
    ('content="https://sr-coresync.com/" property="og:url"', 'content="https://sr-coresync.com/ckb/" property="og:url"'),
    # vCard title
    ('S&amp;R CoreSync Solutions - بطاقة التواصل (vCard)', 'S&amp;R CoreSync Solutions - کارتی پەیوەندی (vCard)'),
    ('S&R CoreSync Solutions - بطاقة التواصل (vCard)', 'S&R CoreSync Solutions - کارتی پەیوەندی (vCard)'),
]

# Image alt text: Arabic → Kurdish Sorani (for CKB portal)
CKB_ALT_REPLACEMENTS = {
    'الشعار الذهبي الفاخر S&amp;R CoreSync': 'ئامرازی زێرینی S&amp;R CoreSync',
    'الشعار الذهبي الفاخر': 'ئامرازی زێرین',
    'الشعار الرسمي S&amp;R CoreSync': 'ئامرازی فەرمی S&amp;R CoreSync',
    'الشعار الرسمي': 'ئامرازی فەرمی',
    'م. محمد سليم عزيزة': 'م. محمد سلیم عزیزة',
    'م. محمد سليم': 'م. محمد سلیم',
    'أ. محمد رائد كعكة': 'أ. محمد رائد كعكة',
    'أ. محمد رائد': 'أ. محمد رائد',
    'المدير التنفيذي ورئيس مجلس الإدارة': 'بەڕێوەبەری کارگێڕی',
    'المدير التقني والشريك المؤسس': 'بەڕێوەبەری تەکنیکی و دامەزرێنەر',
    'تصميم الهوية البصرية': 'ئامادەکردنی ناسنامەی بینراو',
    'تطوير المواقع الإلكترونية': 'پەرەپێدانی مەلپەڕ',
    'التجارة الإلكترونية': 'بازرگانی ئەلیکترۆنی',
    'برمجيات سحابية': 'نەرمەکالای هەور',
    'تطبيقات الجوال': 'ئەپلیکەیشنی مۆبایل',
    'أنظمة ERP والمالية': 'سیستەمەکانی ERP و دارایی',
    'الذكاء الاصطناعي والأتمتة': 'زیرەکی دەستکردی و ئۆتۆماسیۆن',
    'الاستشارات المالية': 'ڕاوێژی دارایی',
    'الأمن السيبراني': 'ئەمنیەتی سایبەری',
    'خلفية الجبل': 'پاشمینەی چیا',
    'صورة العمل': 'وێنەی کار',
    'القيادة التنفيذية والمؤسسون': 'سەرکردایەتی کارگێڕی و دامەزرێنەران',
    'الشعار الرسمي الرسمي 2026': 'ئامرازی فەرمی 2026',
    'الشعار الذهبي الرسمي 4K Ultra-DPI': 'ئامرازی زێرینی فەرمی 4K Ultra-DPI',
    'منصة الجاليات والمنظمات': 'پلاتفۆرمی کۆمەڵگا و ڕێکخراوەکان',
    'منصة الرعاية الصحية': 'پلاتفۆرمی تەندروستی',
    'نظام ERP المخابز': 'سیستەمی ERP نانوایی',
    'خلفية الشبكة': 'پاشمینەی تۆڕ',
    'خلفية متدرجة': 'پاشمینەی لیستە',
    'خلفية ذهبية': 'پاشمینەی زێرین',
    'خلفية': 'پاشمینە',
    'توقيع محمد سليم': 'واژووی محمد سلیم',
    'توقيع': 'واژوو',
    'صورة': 'وێنە',
    'الشعار': 'ئامراز',
}

# H3 card title replacements for CKB (dana-card-title class)
CKB_HEADING_REPLACEMENTS = [
    ('تصميم الهوية', 'ئامادەکردنی ناسنامە'),
    ('تطوير الويب', 'پەرەپێدانی وێب'),
    ('التجارة الإلكترونية', 'بازرگانی ئەلیکترۆنی'),
    ('أنظمة مؤسسية', 'سیستەمەکانی دامەزراوەیی'),
    ('برمجيات سحابية', 'نەرمەکالای هەور'),
    ('تطبيقات الجوال', 'ئەپلیکەیشنی مۆبایل'),
    ('نظم المالية', 'سیستەمی دارایی'),
    ('الذكاء الاصطناعي', 'زیرەکی دەستکردی'),
    ('الاستشارات المالية', 'ڕاوێژی دارایی'),
    ('الأمن السيبراني', 'ئەمنیەتی سایبەری'),
    ('أعمالنا', 'کارەکانمان'),
    ('منصاتنا', 'پلاتفۆرمەکانمان'),
    ('الخدمات', 'خزمەتگوزارییەکان'),
    ('التقنيات', 'تەکنەلۆژیاکان'),
    ('البرمجيات', 'نەرمەکالا'),
    ('التسعير', 'نرخەکان'),
    ('عن الشركة', 'دەربارەی کۆمپانیا'),
    ('تواصل معنا', 'پەیوەندیمان پێوەبکە'),
    ('الأسعار', 'نرخەکان'),
]

# Hero section visible text
CKB_HERO_REPLACEMENTS = [
    # Brand tag
    ('يُقدِّم', 'پێشکەش دەکات'),
    ('يقدم', 'پێشکەش دەکات'),
    # Availability
    ('متاح لمشاريع مؤسسية جديدة 2026', 'بەردەستە بۆ پڕۆژەی دامەزراوەیی نوێ 2026'),
    ('متاح لاستقبال مشاريع مؤسسية جديدة 2026', 'بەردەستە بۆ پڕۆژەی دامەزراوەیی نوێ 2026'),
    # Audio
    ('تجربة صوتية محيطية (انقر للتشغيل)', 'ئەزموونی دەنگی ژینگەیی (کلیک بکە بۆ لێدانەوە)'),
    # Platform flag
    ('النموذج الرائد: الجالية السورية في هولندا', 'نموونەی پێشەنگ: کۆمەڵگای سووریەیی لە هۆڵەندا'),
    # Nav
    ('>الخدمات<', '>خزمەتگوزارییەکان<'),
    ('>التقنيات<', '>تەکنەلۆژیاکان<'),
    ('>الأعمال<', '>کارەکان<'),
    ('>البرمجيات<', '>نەرمەکالاکان<'),
    ('>التسعير<', '>نرخەکان<'),
    ('>عن الشركة<', '>دەربارەی کۆمپانیا<'),
    ('>تواصل<', '>پەیوەندی<'),
    ('>تواصل معنا<', '>پەیوەندیمان پێوەبکە<'),
    ('>تحدث الآن<', '>ئێستا قسە بکە<'),
    ('>متضمن<', '>ناوەوەی<'),
    # Footer
    ('جميع الحقوق محفوظة.', 'هەموو مافەکان پارێزراون.'),
    ('جميع الحقوق محفوظة', 'هەموو مافەکان پارێزراون'),
    ('>سياسة الخصوصية<', '>سیاسەتی تایبەتمەندی<'),
    ('>شروط الخدمة<', '>مەرجەکانی خزمەتگوزاری<'),
    ('>اتفاقية مستوى الخدمة<', '>ڕێکەوتنی ئاستی خزمەتگوزاری<'),
]

# ─────────────────────────────────────────────────────────────────
# 2. BRAND NAME FIX – All pages (Arabic brand name in img alt or visible text)
# These are Arabic brand names that should always be in English
# ─────────────────────────────────────────────────────────────────

ARABIC_BRAND_FIX = [
    # Arabicized company name variants → correct English brand
    ('إس آند آر كور سينك للحلول الذكية', 'S&R CoreSync For Intelligent Solutions'),
    ('إس آند آر كور سينك', 'S&R CoreSync'),
    ('إس آند آر', 'S&R'),
    ('كور سينك للحلول الذكية', 'CoreSync For Intelligent Solutions'),
    ('كور سينك', 'CoreSync'),
    ('س و ر للحلول الذكية', 'S&R CoreSync For Intelligent Solutions'),
    ('س & ر كور سينك', 'S&R CoreSync'),
]


def fix_arabic_brand_names(content: str) -> str:
    """Replace any remaining Arabicized company name with correct English."""
    for ar, en in ARABIC_BRAND_FIX:
        content = content.replace(ar, en)
    return content


def fix_image_alt_texts_ckb(content: str) -> str:
    """Replace Arabic alt text in img tags with Kurdish Sorani equivalents."""
    def replace_alt(match):
        full_tag = match.group(0)
        alt_match = re.search(r'alt="([^"]*)"', full_tag)
        if not alt_match:
            return full_tag
        old_alt = alt_match.group(1)

        if not re.search(r'[\u0600-\u06FF]', old_alt):
            return full_tag

        new_alt = old_alt
        for ar, ckb in CKB_ALT_REPLACEMENTS.items():
            new_alt = new_alt.replace(ar, ckb)

        if new_alt == old_alt:
            # Fallback generic replacements
            new_alt = re.sub(r'الشعار', 'ئامراز', new_alt)
            new_alt = re.sub(r'صورة', 'وێنە', new_alt)
            new_alt = re.sub(r'خلفية', 'پاشمینە', new_alt)
            new_alt = re.sub(r'توقيع', 'واژوو', new_alt)
            new_alt = re.sub(r'الرسمي', 'فەرمی', new_alt)
            new_alt = re.sub(r'الذهبي', 'زێرین', new_alt)
            new_alt = re.sub(r'الفاخر', 'لوکس', new_alt)
            new_alt = re.sub(r'القيادة التنفيذية', 'سەرکردایەتی کارگێڕی', new_alt)
            new_alt = re.sub(r'والمؤسسون', 'و دامەزرێنەران', new_alt)
            new_alt = re.sub(r'المدير التنفيذي', 'بەڕێوەبەری کارگێڕی', new_alt)
            new_alt = re.sub(r'المدير التقني', 'بەڕێوەبەری تەکنیکی', new_alt)
            new_alt = re.sub(r'المؤسس', 'دامەزرێنەر', new_alt)
            new_alt = re.sub(r'منصة', 'پلاتفۆرم', new_alt)
            new_alt = re.sub(r'نظام', 'سیستەم', new_alt)

        return full_tag.replace(f'alt="{old_alt}"', f'alt="{new_alt}"')

    return re.sub(r'<img[^>]*/?>',  replace_alt, content, flags=re.DOTALL)


def fix_visible_headings_ckb(content: str) -> str:
    """Fix visible H1/H2/H3 text in CKB portal."""
    for ar, ckb in CKB_HEADING_REPLACEMENTS:
        # Target heading tags
        content = re.sub(
            r'(<h[1-3][^>]*>)([^<]*' + re.escape(ar) + r'[^<]*)(</h[1-3]>)',
            lambda m, a=ar, c=ckb: m.group(1) + m.group(2).replace(a, c) + m.group(3),
            content
        )
    return content


def process_ckb_file():
    """Process the Kurdish Sorani portal file."""
    ckb_file = os.path.join(BASE_DIR, 'ckb', 'index.html')
    if not os.path.exists(ckb_file):
        print(f"  [SKIP] ckb/index.html not found")
        return

    print(f"\n{'='*60}")
    print(f"Processing CKB portal: {ckb_file}")

    with open(ckb_file, 'r', encoding='utf-8') as f:
        content = f.read()

    arabic_before = len(re.findall(r'[\u0600-\u06FF]{3,}', content))
    print(f"  Arabic text blocks before: {arabic_before}")

    # Apply CKB-specific fixes
    for pattern, replacement in CKB_META_REPLACEMENTS:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content

    # Apply simple string replacements for meta
    meta_str_fixes = [
        ('content="ar_AR"', 'content="ckb_IQ"'),
        ('data-page-language="ar"', 'data-page-language="ckb"'),
    ]
    for old, new in meta_str_fixes:
        content = content.replace(old, new)

    # Fix canonical URL
    content = re.sub(
        r'<link rel="canonical" href="https://sr-coresync\.com/"',
        '<link rel="canonical" href="https://sr-coresync.com/ckb/"',
        content, count=1
    )

    # Fix image alt texts
    content = fix_image_alt_texts_ckb(content)

    # Fix visible headings
    content = fix_visible_headings_ckb(content)

    # Fix hero / nav / footer texts
    for old, new in CKB_HERO_REPLACEMENTS:
        content = content.replace(old, new)

    # Fix brand name Arabicization
    content = fix_arabic_brand_names(content)

    arabic_after = len(re.findall(r'[\u0600-\u06FF]{3,}', content))
    print(f"  Arabic text blocks after: {arabic_after}")
    print(f"  Reduced by: {arabic_before - arabic_after} blocks")

    with open(ckb_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ Saved: {ckb_file}")


def process_all_html_files():
    """Fix Arabic brand names (Arabicized company name) in all HTML files."""
    print(f"\n{'='*60}")
    print("Fixing Arabic brand names in ALL HTML files...")

    html_files = glob.glob(os.path.join(BASE_DIR, '**', '*.html'), recursive=True)
    # Exclude _site directory
    html_files = [f for f in html_files if '_site' not in f.replace('\\', '/')]

    fixed_count = 0
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = fix_arabic_brand_names(content)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                rel_path = os.path.relpath(filepath, BASE_DIR)
                print(f"  ✅ Fixed brand names in: {rel_path}")
                fixed_count += 1
        except Exception as e:
            print(f"  ⚠️ Error processing {filepath}: {e}")

    print(f"\nTotal files with brand fixes: {fixed_count}")


def main():
    print("S&R CoreSync – Brand Logos & Language Fix")
    print("=" * 60)

    # Step 1: Fix all files for Arabic brand name (Arabicized company name)
    process_all_html_files()

    # Step 2: Fix CKB portal specifically
    process_ckb_file()

    print(f"\n{'='*60}")
    print("✅ All fixes complete!")


if __name__ == '__main__':
    main()
