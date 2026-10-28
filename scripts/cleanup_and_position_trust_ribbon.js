/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

// The new luxury 6-card ribbon HTML
const ribbonHtml = `        <!-- 9.5 شريط الثقة السيادي الأوروبي ومعايير الامتثال المؤسسي (European Sovereign Trust Ribbon) -->
        <section class="sr-trust-ribbon-section" id="compliance" aria-label="European Sovereign Compliance & Trust Ribbon">
            <div class="container">
                <div class="sr-trust-header">
                    <div class="sr-trust-pill">
                        <span class="sr-trust-pill-dot"></span>
                        <span>معايير الثقة والامتثال المؤسسي الأوروبي 2026</span>
                    </div>
                    <h2 class="sr-trust-title">
                        بنية سحابية سيادية محصنة بأعلى <span>المعايير التنظيمية الأوروبية</span>
                    </h2>
                    <p class="sr-trust-subtitle">
                        تلتزم S&R CoreSync For Intelligent Solutions بحماية بيانات عملائها وأصولهم الرقمية وفق أشد الأطر القانونية والتقنية صرامة في هولندا والاتحاد الأوروبي. انقر على أي معيار للتحقق الفوري.
                    </p>
                </div>

                <div class="sr-trust-grid">
                    <!-- Badge 1: GDPR -->
                    <div class="sr-trust-card" data-compliance="gdpr" role="button" tabindex="0" aria-label="تحقق من اعتماد اللائحة العامة لحماية البيانات GDPR">
                        <div class="sr-trust-icon-box sr-trust-icon-box--green">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">EU 2016/679</span>
                                <span class="sr-trust-status">معتمد ومطابق ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">حماية البيانات (GDPR)</h3>
                            <p class="sr-trust-card-desc">امتثال كامل للائحة الخصوصية الأوروبية مع تشفير فائق وعزل تام للبيانات.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>

                    <!-- Badge 2: Belastingdienst BTW -->
                    <div class="sr-trust-card" data-compliance="btw" role="button" tabindex="0" aria-label="تحقق من الامتثال الضريبي الهولندي BTW">
                        <div class="sr-trust-icon-box">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M7 15h0M2 9.5h20"></path></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">Belastingdienst</span>
                                <span class="sr-trust-status">فوترة متوافقة ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">الامتثال الضريبي الهولندي</h3>
                            <p class="sr-trust-card-desc">فوترة رقمية متوافقة مع مصلحة الضرائب الهولندية وحساب آلي لـ BTW.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>

                    <!-- Badge 3: AMS-IX -->
                    <div class="sr-trust-card" data-compliance="amsix" role="button" tabindex="0" aria-label="تحقق من بنية استضافة أمستردام AMS-IX">
                        <div class="sr-trust-icon-box sr-trust-icon-box--green">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">AMS-IX Tier 3+</span>
                                <span class="sr-trust-status">أمستردام السيادية ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">استضافة أمستردام AMS-IX</h3>
                            <p class="sr-trust-card-desc">سيرفرات فائقة السرعة بجوار قلب الإنترنت الأوروبي بأقل من 5ms تأخير.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>

                    <!-- Badge 4: SLA 99.98% -->
                    <div class="sr-trust-card" data-compliance="sla" role="button" tabindex="0" aria-label="تحقق من اتفاقية الجاهزية السحابية SLA">
                        <div class="sr-trust-icon-box">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">99.98% SLA</span>
                                <span class="sr-trust-status">تشغيل مستمر ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">اتفاقية مستوى الخدمة السحابية</h3>
                            <p class="sr-trust-card-desc">ضمان استمرارية التشغيل 99.98% مع منظومة تعافي فوري ونسخ لحظي.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>

                    <!-- Badge 5: ISO 27001 -->
                    <div class="sr-trust-card" data-compliance="iso" role="button" tabindex="0" aria-label="تحقق من معايير حوكمة أمن المعلومات ISO 27001">
                        <div class="sr-trust-icon-box sr-trust-icon-box--green">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">ISO 27001 / SOC 2</span>
                                <span class="sr-trust-status">أمن معلومات مشدد ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">حوكمة أمن المعلومات</h3>
                            <p class="sr-trust-card-desc">ضوابط أمان سيبراني معيارية، وسجلات تدقيق غير قابلة للتعديل والتحريف.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>

                    <!-- Badge 6: Zero-Knowledge -->
                    <div class="sr-trust-card" data-compliance="zeroknowledge" role="button" tabindex="0" aria-label="تحقق من التشفير السيادي المعزول Zero-Knowledge">
                        <div class="sr-trust-icon-box">
                            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="16" r="1"></circle><rect x="3" y="10" width="18" height="12" rx="2"></rect><path d="M7 10V7a5 5 0 0 1 10 0v3"></path></svg>
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">Zero-Knowledge</span>
                                <span class="sr-trust-status">بيانات معزولة ✓</span>
                            </div>
                            <h3 class="sr-trust-card-title">التشفير السيادي المعزول</h3>
                            <p class="sr-trust-card-desc">عزل كامل لقواعد البيانات ومفاتيح خاصة بالعميل لمنع أي وصول غير مصرح.</p>
                            <span class="sr-trust-verify-link">
                                <span>فحص المواصفات والتوثيق</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>`;

// 1. Remove the old static <section class="section-compliance-ribbon" ... </section>
const oldRibbonRegex = /<!--\s*9\.5[\s\S]*?<\/section>/;
if (oldRibbonRegex.test(html)) {
    // Replace old ribbon with new ribbon
    html = html.replace(oldRibbonRegex, ribbonHtml);
    console.log('✓ Replaced old static compliance ribbon with new sovereign trust ribbon');
} else {
    console.log('Old ribbon not matched with regex');
}

// 2. Remove duplicate ribbon before footer if present
const duplicateRegex = /<!--\s*9\.5\s*شريط الثقة السيادي الأوروبي[\s\S]*?<\/section>\s*(?=\s*<!--\s*10\.|\s*<footer)/;
// Check if there is more than one occurrence
const occurrences = (html.match(/class="sr-trust-ribbon-section"/g) || []).length;
console.log('Occurrences of sr-trust-ribbon-section:', occurrences);

if (occurrences > 1) {
    // Find the second occurrence and remove it
    const firstIdx = html.indexOf('class="sr-trust-ribbon-section"');
    const secondIdx = html.indexOf('class="sr-trust-ribbon-section"', firstIdx + 1);
    if (secondIdx !== -1) {
        // Find start of this section (the comment or section tag before secondIdx)
        const commentStart = html.lastIndexOf('<!-- 9.5 شريط الثقة', secondIdx);
        const sectionEnd = html.indexOf('</section>', secondIdx) + '</section>'.length;
        if (commentStart !== -1 && sectionEnd !== -1) {
            html = html.slice(0, commentStart) + html.slice(sectionEnd);
            console.log('✓ Removed duplicate ribbon before footer');
        }
    }
}

fs.writeFileSync(indexPath, html, 'utf8');
console.log('Finished updating index.html');
