with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

idx1 = cnt.find('<tbody>')
idx2 = cnt.find('</tbody>', idx1) + 8

new_tbody = """<tbody>
                    <tr>
                        <td><strong>المرحلة 1: التصميم والواجهة العربية</strong></td>
                        <td>إعادة تصميم واجهة المستخدم بالكامل متجاوبة 100% مع كافة الشاشات والموبايل + هوية بصرية عصرية + واجهة عربية RTL كاملة وازدواجية لغوية دبلوماسية</td>
                        <td>3 - 5 أيام عمل</td>
                        <td style="text-align:left; font-weight:700; color:#c5a880;">€650.00</td>
                    </tr>
                    <tr>
                        <td><strong>المرحلة 2: الاستضافة ولوحة التحكم السحابية</strong></td>
                        <td>استضافة سحابية أوروبية فائقة السرعة والأمان + لوحة تحكم سهلة وسريعة لإدارة المقالات والأخبار بدون مبرمج + مستودع أوراق السياسات المشفر (GDPR)</td>
                        <td>3 - 5 أيام عمل</td>
                        <td style="text-align:left; font-weight:700; color:#c5a880;">€450.00</td>
                    </tr>
                    <tr>
                        <td><strong>المرحلة 3: النشر الرسمي والدعم الفني</strong></td>
                        <td>ربط النطاق المخصص للمركز + شهادة أمان SSL مشفرة + تدريب فريق المركز على إدارة المحتوى + دعم فني وصيانة لمدة شهر</td>
                        <td>2 - 3 أيام عمل</td>
                        <td style="text-align:left; font-weight:700; color:#c5a880;">€250.00</td>
                    </tr>
                    <tr style="background:rgba(255,255,255,0.03); font-weight:800;">
                        <td colspan="3"><strong>المجموع الصافي الأساسي (المرحلة 1 + المرحلة 2):</strong></td>
                        <td style="text-align:left; color:#f59e0b; font-size:1.05rem;">€1,100.00</td>
                    </tr>
                    <tr style="background:rgba(255,255,255,0.05); font-weight:800;">
                        <td colspan="3"><strong>المجموع الكلي لكامل المنظومة (المراحل 1 + 2 + 3):</strong></td>
                        <td style="text-align:left; color:#34d399; font-size:1.1rem;">€1,350.00</td>
                    </tr>
                    <tr style="font-size:0.75rem; color:#94a3b8;">
                        <td colspan="3">ضريبة القيمة المضافة الهولندية (BTW 21%): <em>(ملاحظة: يُعفى منها بنظام B2B Reverse Charge للجهات المؤهلة)</em></td>
                        <td style="text-align:left;">€231.00 <span style="font-size:0.7rem; color:#94a3b8;">(على الأساسية)</span></td>
                    </tr>
                    <tr style="background:linear-gradient(90deg, #021a30, #092c4e); font-weight:900; font-size:1.15rem;">
                        <td colspan="3"><strong style="color:#ffffff;">الإجمالي النهائي الشامل للضريبة (الحزمة الأساسية):</strong></td>
                        <td style="text-align:left; color:#34d399;">€1,331.00</td>
                    </tr>
                </tbody>"""

cnt = cnt[:idx1] + new_tbody + cnt[idx2:]

with open('clgid-prototype.html', 'w', encoding='utf-8') as f:
    f.write(cnt)

print("SUCCESS: Updated clgid-prototype.html pricing table!")
