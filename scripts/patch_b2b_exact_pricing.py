with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    code = f.read()

start_marker = '<div class="sr-a4-section-title">${isAr ? \'عرض السعر التعاقدي المعتمد وجدول الدفعات المرحلية (B2B Price Quote)\''
end_marker = '</table>'

start_idx = code.find(start_marker)
if start_idx != -1:
    end_idx = code.find(end_marker, start_idx) + len(end_marker)
    
    new_table = """<div class="sr-a4-section-title">${isAr ? 'عرض السعر التعاقدي المعتمد وجدول الدفعات المرحلية (B2B Price Quote)' : 'Approved B2B Phased Quotation & Milestone Budget'}</div>
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
                                <td><strong>${isAr ? 'المرحلة 1: التصميم والواجهة العربية' : 'Phase 1: Design & Arabic Portal'}</strong></td>
                                <td>${isAr ? 'إعادة تصميم واجهة المستخدم بالكامل متجاوبة 100% مع الموبايل + هوية بصرية عصرية + واجهة عربية RTL كاملة وازدواجية لغوية (عربي / هولندي / إنجليزي)' : 'Complete modern UI/UX redesign, 100% mobile-first responsiveness, full Arabic RTL & English/Dutch duality'}</td>
                                <td>3 - 5 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€650.00</td>
                            </tr>
                            <tr>
                                <td><strong>${isAr ? 'المرحلة 2: الاستضافة ولوحة التحكم' : 'Phase 2: Hosting & Easy CMS'}</strong></td>
                                <td>${isAr ? 'استضافة سحابية أوروبية فائقة السرعة والأمان + لوحة تحكم سهلة وسريعة لإدارة المقالات والأخبار بدون مبرمج + مستودع أوراق السياسات المشفر (GDPR)' : 'Fast EU Cloud hosting + lightweight CMS for non-technical article publishing + encrypted policy papers repository (GDPR Compliant)'}</td>
                                <td>3 - 5 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€450.00</td>
                            </tr>
                            <tr>
                                <td><strong>${isAr ? 'المرحلة 3: النشر الرسمي والدعم' : 'Phase 3: Deploy & Support'}</strong></td>
                                <td>${isAr ? 'ربط النطاق المخصص للمركز + شهادة أمان SSL مشفرة + تدريب فريق المركز على إدارة المحتوى + دعم فني وصيانة لمدة شهر' : 'Custom domain routing + Tier-3 SSL security + staff training session + 30 days direct SLA engineering support'}</td>
                                <td>2 - 3 ${isAr ? 'أيام عمل' : 'days'}</td>
                                <td style="text-align:left; font-weight:700;">€250.00</td>
                            </tr>
                            <tr style="background:#f8fafc; font-weight:700;">
                                <td colspan="3"><strong>${isAr ? 'المجموع الصافي الأساسي (المرحلة 1 + المرحلة 2):' : 'Core Subtotal Net (Phase 1 + 2):'}</strong></td>
                                <td style="text-align:left; color:#b45309; font-size:0.85rem;">€1,100.00</td>
                            </tr>
                            <tr style="background:#f1f5f9; font-weight:800;">
                                <td colspan="3"><strong>${isAr ? 'المجموع الكلي لكامل المنظومة (المراحل 1 + 2 + 3):' : 'Full Project Total (Phases 1 + 2 + 3):'}</strong></td>
                                <td style="text-align:left; color:#047857; font-size:0.9rem;">€1,350.00</td>
                            </tr>
                            <tr style="font-size:0.7rem; color:#64748b;">
                                <td colspan="3">${isAr ? 'ضريبة القيمة المضافة الهولندية (BTW 21%): (ملاحظة: يُعفى منها بنظام B2B Reverse Charge للجهات المؤهلة)' : 'Dutch BTW (21%): (Reverse charge applicable for eligible B2B entities)'}</td>
                                <td style="text-align:left;">€231.00 <span style="font-size:0.65rem;">(${isAr ? 'على الأساسية' : 'on Core'})</span></td>
                            </tr>
                            <tr style="background:#0f172a; color:#ffffff; font-weight:800; font-size:0.8rem;">
                                <td colspan="3"><strong>${isAr ? 'الإجمالي النهائي الشامل للضريبة (الحزمة الأساسية):' : 'Total Incl. BTW (Core Package):'}</strong></td>
                                <td style="text-align:left; color:#10b981;">€1,331.00</td>
                            </tr>
                        </tbody>
                    </table>"""
    
    code = code[:start_idx] + new_table + code[end_idx:]
    with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("SUCCESS: Replaced quotation table with updated €650 + €450 + €250 pricing!")
else:
    print("ERROR: start_marker not found!")
