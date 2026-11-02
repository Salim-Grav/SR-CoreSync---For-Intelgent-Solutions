import sys

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect clientWaMsg
start_marker = "const clientWaMsg ="
end_marker = "const clientWaUrl ="

start_idx = code.find(start_marker)
end_idx = code.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_wa_msg = """const clientWaMsg = 
        `🏛️ *وثيقة دراسة الجدوى وعرض السعر المعتمد 2026*\\n` +
        `━━━━━━━━━━━━━━━━━━━━━━\\n` +
        `السيد الأستاذ: *محمود الناصر* المحترم\\n` +
        `مدير مركز CLGID للحوكمة والدراسات - لاهاي\\n\\n` +
        `يسر شركة *S&R CoreSync For Intelligent Solutions* (أمستردام) تزويدكم بالدراسة الفنية وعرض السعر المعتمد لتطوير الموقع:\\n\\n` +
        `📋 *كود الوثيقة:* ${docRef}\\n` +
        `🔍 *نتائج الفحص الأمني والتقني:* رفع مؤشر الأمان من 41/100 إلى 99/100 مع امتثال تام لقانون حماية البيانات الهولندي (GDPR)\\n\\n` +
        `💰 *جدول عرض السعر المرحلي المقترح (B2B):*\\n` +
        `• *المرحلة 1 (التصميم والواجهة العربية):* €650.00\\n` +
        `  (واجهة عصرية متجاوبة 100% مع الموبايل + لغة عربية RTL كاملة وازدواجية دبلوماسية)\\n` +
        `• *المرحلة 2 (الاستضافة ولوحة التحكم السحابية):* €450.00\\n` +
        `  (استضافة سحابية أوروبية فائقة السرعة + لوحة تحكم سهلة لنشر المقالات بدون مبرمج + مستودع أوراق السياسات المشفر)\\n` +
        `• *المرحلة 3 (النشر الرسمي والدعم الفني):* €250.00\\n` +
        `  (ربط النطاق + شهادة SSL مشفرة + تدريب فريق المركز ودعم فني)\\n\\n` +
        `📊 *المجموع الصافي الأساسي (1 + 2):* €1,100.00\\n` +
        `⚡ *المجموع الشامل للمشروع كاملاً:* €1,350.00\\n` +
        `*(ملاحظة: تُعفى المنظمات المؤهلة من ضريبة BTW 21% بنظام Reverse Charge 0%)*\\n\\n` +
        `🌐 *رابط النموذج الأولي الحي للواجهة العربية:*\\n` +
        `https://sr-coresync.com/clgid-prototype.html\\n\\n` +
        `🔒 *بوابة التحقق السيادية الرقمية:*\\n` +
        `https://sr-coresync.com/verify.html?ref=${docRef}\\n\\n` +
        `المسؤول الفني المشرف: *م. محمد سليم عزيزة*\\n` +
        `كبير مهندسي السحابة والذكاء الاصطناعي - S&R CoreSync B.V.\\n` +
        `━━━━━━━━━━━━━━━━━━━━━━\\n` +
        `يسعدنا تأكيدكم لاعتماد خطة العمل وبدء التنفيذ الفوري.`;\\n    """
    
    code = code[:start_idx] + new_wa_msg + code[end_idx:]
    print("SUCCESS: Updated clientWaMsg!")
else:
    print("WARNING: start/end marker for clientWaMsg not found")

# Now let's update emailBody
start_email = "const emailBody = encodeURIComponent("
end_email = "const mailtoUrl = `mailto:${clientEmail}"

start_em_idx = code.find(start_email)
end_em_idx = code.find(end_email)

if start_em_idx != -1 and end_em_idx != -1:
    new_email_block = """const emailBody = encodeURIComponent(
        `السيد الأستاذ محمود الناصر المحترم،
مدير مركز CLGID للحوكمة والدراسات (لاهاي - هولندا)

تحية طيبة وبعد،

يسر شركة S&R CoreSync For Intelligent Solutions B.V. (أمستردام) أن ترفق لكم دراسة الجدوى الفنية وعرض السعر المالي المعتمد لإعادة تطوير وتأمين الموقع الإلكتروني لمركزكم الموقر:

1. نتائج التدقيق الفني المباشر (CLGID The Hague):
- الموقع الحالي يعمل في بيئة تجريبية ويفتقر للغة العربية ومعايير الأمان الأوروبية (مؤشر 41/100).
- خطة التطوير تضمن رفع مؤشر الأداء والأمان إلى 99/100 والامتثال التام للائحة العامة لحماية البيانات (GDPR).

2. جدول التكاليف والتسليم المرحلي المعتمد (B2B):
- المرحلة 1 (التصميم والواجهة العربية والهوية الرقمية): €650.00
- المرحلة 2 (الاستضافة السحابية الأوروبية ولوحة التحكم السهلة ومستودع أوراق السياسات): €450.00
- المرحلة 3 (النشر الرسمي، ربط النطاق المخصص، شهادة SSL، والتدريب والدعم الفني): €250.00

* المجموع الصافي الأساسي (المرحلة 1 + 2): €1,100.00
* المجموع الكلي لكامل المنظومة (المراحل 1 + 2 + 3): €1,350.00
(تطبق آلية الإعفاء أو النقل الضريبي BTW Verlegd 0% للمنظمات المؤهلة).

3. الروابط المباشرة والمعاينة الحية:
- تجربة النموذج الأولي الحي للواجهة العربية ولوحة النشر: https://sr-coresync.com/clgid-prototype.html
- رابط التحقق السيادي المعتمد: https://sr-coresync.com/verify.html?ref=${docRef}

المسؤول التنفيذي المشرف على المشروع:
المهندس محمد سليم عزيزة
كبير مهندسي السحابة والذكاء الاصطناعي
S&R CoreSync For Intelligent Solutions B.V.
Amsterdam - The Netherlands
WhatsApp: +31 6 18111116`
    );\\n    """
    code = code[:start_em_idx] + new_email_block + code[end_em_idx:]
    print("SUCCESS: Updated emailBody!")
else:
    print("WARNING: start/end marker for emailBody not found")

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Dispatch flow patch complete.")
