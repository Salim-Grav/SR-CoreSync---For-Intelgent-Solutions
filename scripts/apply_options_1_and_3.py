import re

with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove JSON button from generateAiProjectBlueprint
json_btn_pattern_1 = r'<button type="button" class="sr-voice-btn-primary sr-btn-spec-json" data-sr-call="downloadBlueprintArchitectureJson">.*?</button>'
if re.search(json_btn_pattern_1, code, re.DOTALL):
    code = re.sub(json_btn_pattern_1, '', code, flags=re.DOTALL)
    print("SUCCESS: Removed JSON button from generateAiProjectBlueprint!")
else:
    print("WARNING: json_btn_pattern_1 not matched")

# 2. Remove JSON button from openBlueprintPreviewModal
json_btn_pattern_2 = r'<button type="button" class="sr-a4-btn-action sr-a4-btn-json"[^>]*>.*?</button>'
if re.search(json_btn_pattern_2, code):
    code = re.sub(json_btn_pattern_2, '', code)
    print("SUCCESS: Removed JSON button from openBlueprintPreviewModal!")
else:
    print("WARNING: json_btn_pattern_2 not matched")

# 3. Update the B2B Price Quote table in openBlueprintPreviewModal
old_table_pattern = r'<!-- B2B Official Quotation Table -->.*?<!-- /B2B Official Quotation Table -->'
new_table_html = """<!-- B2B Official Quotation Table -->
                        <div class="sr-a4-section-title" style="margin-top:20px;">
                            <span>${isAr ? 'عرض السعر المالي المقترح للتطوير والتسليم المرحلي (B2B Formal Quotation)' : 'Phased Quotation & Commercial Milestones (B2B)'}</span>
                            <span style="font-size:0.75rem; color:#b45309; font-weight:700;">${isAr ? 'عرض رسمي صالح لمدة 30 يوماً' : 'Valid for 30 days'}</span>
                        </div>
                        <table class="sr-a4-price-table" style="width:100%; border-collapse:collapse; margin-top:8px; font-size:0.8rem;">
                            <thead>
                                <tr style="background:#f1f5f9; border-bottom:2px solid #cbd5e1; color:#0f172a; text-align:right;">
                                    <th style="padding:6px 8px;">${isAr ? 'المرحلة / الحزمة' : 'Milestone'}</th>
                                    <th style="padding:6px 8px;">${isAr ? 'نطاق العمل والمخرجات الهندسية' : 'Deliverables & Engineering Scope'}</th>
                                    <th style="padding:6px 8px;">${isAr ? 'المدة التقديرية' : 'Duration'}</th>
                                    <th style="padding:6px 8px; text-align:left;">${isAr ? 'القيمة (€)' : 'Amount (€)'}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom:1px solid #e2e8f0;">
                                    <td style="padding:6px 8px;"><strong>${isAr ? 'المرحلة 1: التصميم والواجهة العربية' : 'Phase 1: UI/UX & Arabic Portal'}</strong></td>
                                    <td style="padding:6px 8px;">${isAr ? 'إعادة تصميم واجهة المستخدم بالكامل متجاوبة 100% مع الموبايل + هوية بصرية عصرية + واجهة عربية RTL كاملة وواجهة هولندية/إنجليزية' : 'Complete modern UI/UX redesign, 100% mobile-first responsiveness, full Arabic RTL & English/Dutch duality'}</td>
                                    <td style="padding:6px 8px;">3 - 5 ${isAr ? 'أيام عمل' : 'days'}</td>
                                    <td style="padding:6px 8px; text-align:left; font-weight:700; color:#0f172a;">€650.00</td>
                                </tr>
                                <tr style="border-bottom:1px solid #e2e8f0;">
                                    <td style="padding:6px 8px;"><strong>${isAr ? 'المرحلة 2: الاستضافة ولوحة التحكم' : 'Phase 2: Hosting & Easy CMS'}</strong></td>
                                    <td style="padding:6px 8px;">${isAr ? 'استضافة سحابية أوروبية عالية السرعة والأمان + لوحة تحكم سهلة وسريعة لإدارة المقالات والأخبار بدون مبرمج + مستودع أوراق السياسات المشفر (GDPR)' : 'Fast EU Cloud hosting + lightweight CMS for non-technical article publishing + encrypted policy papers repository (GDPR Compliant)'}</td>
                                    <td style="padding:6px 8px;">3 - 5 ${isAr ? 'أيام عمل' : 'days'}</td>
                                    <td style="padding:6px 8px; text-align:left; font-weight:700; color:#0f172a;">€450.00</td>
                                </tr>
                                <tr style="border-bottom:1px solid #e2e8f0;">
                                    <td style="padding:6px 8px;"><strong>${isAr ? 'المرحلة 3: النشر الرسمي والدعم' : 'Phase 3: Deploy & VIP Support'}</strong></td>
                                    <td style="padding:6px 8px;">${isAr ? 'ربط النطاق المخصص للمركز + شهادة أمان SSL مشفرة + تدريب فريق المركز على إدارة المحتوى + دعم فني وصيانة لمدة شهر' : 'Custom domain routing + Tier-3 SSL security + staff training session + 30 days direct SLA engineering support'}</td>
                                    <td style="padding:6px 8px;">2 - 3 ${isAr ? 'أيام عمل' : 'days'}</td>
                                    <td style="padding:6px 8px; text-align:left; font-weight:700; color:#0f172a;">€250.00</td>
                                </tr>
                                <tr style="background:#f8fafc; font-weight:700; border-bottom:1px solid #cbd5e1;">
                                    <td colspan="3" style="padding:8px;"><strong>${isAr ? 'المجموع الصافي الأساسي (المرحلة 1 + 2):' : 'Core Subtotal Net (Phase 1 + 2):'}</strong></td>
                                    <td style="padding:8px; text-align:left; color:#b45309; font-size:0.95rem;">€1,100.00</td>
                                </tr>
                                <tr style="background:#f1f5f9; font-weight:800; border-bottom:2px solid #cbd5e1;">
                                    <td colspan="3" style="padding:8px;"><strong>${isAr ? 'المجموع الكلي لكامل المنظومة (المراحل 1 + 2 + 3):' : 'Full Project Total (Phases 1 + 2 + 3):'}</strong></td>
                                    <td style="padding:8px; text-align:left; color:#047857; font-size:1.05rem;">€1,350.00</td>
                                </tr>
                                <tr style="font-size:0.75rem; color:#64748b;">
                                    <td colspan="3" style="padding:6px 8px;">${isAr ? 'ضريبة القيمة المضافة الهولندية (BTW 21%):' : 'Dutch Value Added Tax (BTW 21%):'}</td>
                                    <td style="padding:6px 8px; text-align:left;">€231.00 <span style="font-size:0.68rem; color:#94a3b8;">(${isAr ? 'على الحزمة الأساسية' : 'on Core'})</span></td>
                                </tr>
                                <tr style="font-size:0.75rem; color:#64748b;">
                                    <td colspan="4" style="padding:4px 8px; font-style:italic;">
                                        * ${isAr ? 'ملاحظة ضريبية: في حال إصدار الفاتورة لمنظمة غير ربحية أو جهة معفاة مسجلة في الاتحاد الأوروبي، تطبق آلية النقل الضريبي (BTW Verlegd / Reverse Charge 0%).' : 'Tax Note: Reverse Charge (BTW Verlegd 0%) applies for eligible EU VAT/ANBI registered entities.'}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <!-- /B2B Official Quotation Table -->"""

if re.search(old_table_pattern, code, re.DOTALL):
    code = re.sub(old_table_pattern, new_table_html, code, flags=re.DOTALL)
    print("SUCCESS: Updated B2B Price Quote table with Phase 1 (€650) + Phase 2 (€450) + Phase 3 (€250)!")
else:
    print("WARNING: old_table_pattern not matched")

# Also enhance exportBlueprintPdf to inject print-clean CSS if needed
old_export_pdf = """function exportBlueprintPdf(e) {
    if (typeof openBlueprintPreviewModal === "function") {
        openBlueprintPreviewModal();
    }
    const prevBodyOverflow = document.body.style.overflow;
    const prevHtmlOverflow = document.documentElement.style.overflow;
    document.body.style.overflow = "visible";
    document.documentElement.style.overflow = "visible";
    setTimeout(() => {
        window.print();
        setTimeout(() => {
            document.body.style.overflow = prevBodyOverflow;
            document.documentElement.style.overflow = prevHtmlOverflow;
        }, 800);
    }, 300);
}"""

new_export_pdf = """function exportBlueprintPdf(e) {
    if (typeof openBlueprintPreviewModal === "function") {
        openBlueprintPreviewModal();
    }
    const prevBodyOverflow = document.body.style.overflow;
    const prevHtmlOverflow = document.documentElement.style.overflow;
    document.body.style.overflow = "visible";
    document.documentElement.style.overflow = "visible";
    
    // Ensure all print styles recognize the modal
    const modal = document.getElementById("srBlueprintPreviewModal");
    if (modal) {
        modal.classList.add("active");
        modal.style.display = "block";
    }

    setTimeout(() => {
        window.print();
        setTimeout(() => {
            document.body.style.overflow = prevBodyOverflow;
            document.documentElement.style.overflow = prevHtmlOverflow;
        }, 800);
    }, 350);
}"""

if old_export_pdf in code:
    code = code.replace(old_export_pdf, new_export_pdf)
    print("SUCCESS: Enhanced exportBlueprintPdf!")
else:
    print("WARNING: old_export_pdf not found exactly")

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch complete.")
