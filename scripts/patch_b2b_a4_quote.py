import os

p = 'js/sr-inline-13eaa28e.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

target = """                    <div class="sr-a4-endorsement-strip">"""

b2b_quote_html = """                    <div class="sr-a4-section-title">${isAr ? 'عرض السعر التعاقدي المعتمد وجدول الدفعات المرحلية (B2B Price Quote)' : 'Approved B2B Phased Quotation & Milestone Budget'}</div>
                    <table class="sr-a4-table" style="margin-bottom:14px; font-size:0.75rem;">
                        <thead>
                            <tr style="background:#f1f5f9;">
                                <th>${isAr ? 'المرحلة' : 'Milestone'}</th>
                                <th>${isAr ? 'نطاق العمل الهندسي والتسليمات' : 'Engineering Scope & Deliverables'}</th>
                                <th>${isAr ? 'المدة' : 'Timeline'}</th>
                                <th style="text-align:left;">${isAr ? 'القيمة (€)' : 'Amount (€)'}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>${isAr ? 'المرحلة 1: التصميم والهوية' : 'Phase 1: Design & Identity'}</strong></td>
                                <td>${isAr ? 'إعادة تصميم واجهة المستخدم بالكامل متجاوبة 100% مع الموبايل + هوية بصرية عصرية + واجهة عربية RTL وأجنبية' : 'Complete modern UI/UX redesign, 100% mobile-first responsiveness, RTL Arabic & English/Dutch duality'}</td>
                                <td>3 - 5 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€650.00</td>
                            </tr>
                            <tr>
                                <td><strong>${isAr ? 'المرحلة 2: البرمجة والتحكم' : 'Phase 2: CMS & Security'}</strong></td>
                                <td>${isAr ? 'لوحة تحكم سهلة وسريعة لإدارة المقالات والأخبار بدون مبرمج + مستودع أوراق السياسات المشفر + توافق تام مع GDPR' : 'Lightweight CMS for instant article publishing, encrypted policy paper repository, strict Dutch GDPR compliance'}</td>
                                <td>4 - 6 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€550.00</td>
                            </tr>
                            <tr>
                                <td><strong>${isAr ? 'المرحلة 3: النشر والتدريب' : 'Phase 3: Deploy & Training'}</strong></td>
                                <td>${isAr ? 'استضافة سحابية أوروبية فائقة السرعة + شهادة SSL مجانية + ربط النطاق المخصص + تدريب فريق المركز ودعم فني' : 'High-speed European cloud hosting, SSL tier-3 certificate, custom domain routing, staff onboarding & support'}</td>
                                <td>2 - 3 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€290.00</td>
                            </tr>
                            <tr style="background:#f8fafc; font-weight:700;">
                                <td colspan="3"><strong>${isAr ? 'المجموع الصافي (Subtotal Net):' : 'Subtotal Net:'}</strong></td>
                                <td style="text-align:left; color:#b45309;">€1,490.00</td>
                            </tr>
                            <tr style="font-size:0.7rem; color:#64748b;">
                                <td colspan="3">${isAr ? 'ضريبة القيمة المضافة الهولندية (BTW 21%): (ملاحظة: يُعفى منها بنظام B2B Reverse Charge للجهات المؤهلة)' : 'Dutch BTW (21%): (Reverse charge applicable for eligible B2B entities)'}</td>
                                <td style="text-align:left;">€312.90</td>
                            </tr>
                            <tr style="background:#0f172a; color:#ffffff; font-weight:800; font-size:0.8rem;">
                                <td colspan="3"><strong>${isAr ? 'الإجمالي النهائي الشامل للضريبة (Total Incl. BTW):' : 'Total Incl. BTW:'}</strong></td>
                                <td style="text-align:left; color:#10b981;">€1,802.90</td>
                            </tr>
                        </tbody>
                    </table>

                    <div class="sr-a4-endorsement-strip">"""

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_repl = b2b_quote_html.replace('\r\n', '\n')

if norm_target in norm_text:
    norm_text = norm_text.replace(norm_target, norm_repl, 1)
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(norm_text)
    print("Injected B2B quotation table into A4 blueprint successfully!")
else:
    print("Target endorsement strip not found")

