import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Building English versions of partner-portal and developer-portal...")

# 1. Partner Portal
with open('partner-portal.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Switch HTML language & direction
c = c.replace('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">')

# Asset paths fix for en/ subdirectory
c = re.sub(r'href="\./assets/', 'href="../assets/', c)
c = re.sub(r'src="\./assets/', 'src="../assets/', c)
c = re.sub(r'href="assets/', 'href="../assets/', c)
c = re.sub(r'src="assets/', 'src="../assets/', c)

# Header & Meta Translations
c = c.replace(
    'بوابة شركاء الحلول والوكلاء البيضاء | S&R CoreSync White-Label Partner Portal',
    'S&R CoreSync | White-Label Partner & Solutions Provider Gateway'
)
c = c.replace(
    'البوابة الرسمية لشركاء الحلول والوكلاء ومكاتب المحاسبة الأوروبية - إعادة بيع منظومة CoreSync ERP السحابية بهويتكم الخاصة وشعاراتكم المستقلة مع نظام RevShare 25% وإدارة العملاء.',
    'Official sovereign gateway for European solution partners, accountants, and agencies: Resell CoreSync ERP with your custom brand identity, automated 25% RevShare, and multi-tenant client governance.'
)
c = c.replace('بوابة شركاء الحلول والوكلاء بهويتكم البيضاء', 'Sovereign White-Label & Solutions Partner Gateway')
c = c.replace('العودة للمنظومة الرئيسية', 'Return to Main Portal')
c = c.replace('منظومة التوزيع الحصري وإعادة البيع المؤسسي (RevShare 25% معتمد)', 'Exclusive Enterprise Distribution & Sovereign RevShare 25% Program')

# Sections
c = c.replace('1. استوديو تخصيص الهوية المستقلة (White-Label Studio)', '1. Custom Sovereign Brand Studio (White-Label)')
c = c.replace('2. نظام إشعارات WhatsApp Business المالي للمحاسبين', '2. WhatsApp Business Automated Financial Alert Engine')
c = c.replace('3. إدارة المؤسسات والعملاء المربوطين (Active Dutch Client Tenants)', '3. Active Multi-Tenant European Client Infrastructure')

with open('en/partner-portal.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('✅ Created en/partner-portal.html')

# 2. Developer Portal
with open('developer-portal.html', 'r', encoding='utf-8') as f:
    dev = f.read()

dev = dev.replace('<html lang="ar" dir="rtl"', '<html lang="en" dir="ltr"')
dev = dev.replace('dir="rtl"', 'dir="ltr"')

# Asset paths fix for en/ subdirectory
dev = re.sub(r'href="\./assets/', 'href="../assets/', dev)
dev = re.sub(r'src="\./assets/', 'src="../assets/', dev)
dev = re.sub(r'href="assets/', 'href="../assets/', dev)
dev = re.sub(r'src="assets/', 'src="../assets/', dev)
dev = re.sub(r'href="\./css/', 'href="../css/', dev)
dev = re.sub(r'src="\./js/', 'src="../js/', dev)
dev = re.sub(r'href="css/', 'href="../css/', dev)
dev = re.sub(r'src="js/', 'src="../js/', dev)

dev = dev.replace(
    'بوابة المطورين وواجهة الـ API العامة | S&R CoreSync Developer Gateway 2026',
    'S&R CoreSync Developer Gateway | Sovereign REST APIs, SDKs & Webhooks'
)
dev = dev.replace('بوابة المطورين والربط البرمجي السحابي المفتوح', 'Sovereign Developer Gateway & Open Cloud APIs')
dev = dev.replace('العودة للرئيسية', 'Back to Main Portal')
dev = dev.replace('العودة للمنظومة الرئيسية', 'Back to Main Portal')

with open('en/developer-portal.html', 'w', encoding='utf-8') as f:
    f.write(dev)
print('✅ Created en/developer-portal.html')

# 3. Update links in en/index.html to point to localized portals
with open('en/index.html', 'r', encoding='utf-8') as f:
    en_idx = f.read()

en_idx = en_idx.replace('href="../developer-portal.html"', 'href="./developer-portal.html"')
en_idx = en_idx.replace('href="../partner-portal.html"', 'href="./partner-portal.html"')

with open('en/index.html', 'w', encoding='utf-8') as f:
    f.write(en_idx)
print('✅ Updated en/index.html internal portal links to ./developer-portal.html and ./partner-portal.html')
