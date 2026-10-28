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

// 1. Inject CSS link into <head>
if (!html.includes('sr-tier-matrix.css')) {
    const trustCssMarker = '<link rel="stylesheet" href="./css/sr-trust-ribbon.css?v=20261021_trust">';
    if (html.includes(trustCssMarker)) {
        html = html.replace(
            trustCssMarker,
            trustCssMarker + '\n    <!-- مركز مقارنة الباقات المؤسسية السحابية المتقدم (Enterprise Tier Matrix) -->\n    <link rel="stylesheet" href="./css/sr-tier-matrix.css?v=20261021_matrix">'
        );
        console.log('✓ Injected sr-tier-matrix.css into <head>');
    } else {
        console.error('Could not find sr-trust-ribbon.css marker in <head>');
    }
} else {
    console.log('sr-tier-matrix.css already present in <head>');
}

// 2. Build the Tier Matrix HTML
const matrixHtml = `
                <!-- 8.5 مركز مقارنة الباقات المؤسسية السحابية المتقدم وحاسبة الخصم المؤسسي (Enterprise Tier Matrix) -->
                <div class="sr-tier-matrix-section" id="tier-matrix" aria-label="Enterprise Tier Matrix & Institutional Comparison">
                    <div class="sr-tier-header">
                        <div class="sr-tier-pill">
                            <span class="sr-tier-pill-dot"></span>
                            <span>مركز المقارنة المعماري الشامل 2026 // Architecture & Features Matrix</span>
                        </div>
                        <h3 class="sr-tier-title">
                            قارن بين <span>الباقات المؤسسية السحابية</span> بدقة وشفافية
                        </h3>
                        <p class="sr-tier-subtitle">
                            اختر البنية التقنية المثالية لمؤسستك في هولندا والاتحاد الأوروبي. استمتع بخصم 20% عند الفوترة السنوية بالإضافة إلى خصم مخصص متعدد الكيانات للمجموعات والشركات الشقيقة.
                        </p>
                    </div>

                    <!-- لوحة التحكم التفاعلية: دورة الفوترة + حاسبة الكيانات المؤسسية -->
                    <div class="sr-tier-controls-hub">
                        <!-- مفتاح دورة الفوترة -->
                        <div class="sr-tier-billing-toggle">
                            <button type="button" class="sr-tier-toggle-btn active" data-billing="annual">
                                <span>فوترة سنوية</span>
                                <span class="sr-tier-save-badge">وفّر 20%</span>
                            </button>
                            <button type="button" class="sr-tier-toggle-btn" data-billing="monthly">
                                <span>فوترة شهرية</span>
                            </button>
                        </div>

                        <!-- مضاعف الكيانات المؤسسية -->
                        <div class="sr-tier-entities-picker">
                            <span class="sr-tier-entities-label">عدد الشركات / الفروع:</span>
                            <div class="sr-tier-entities-btns">
                                <button type="button" class="sr-tier-entity-btn active" data-entities="1">كيان واحد</button>
                                <button type="button" class="sr-tier-entity-btn" data-entities="2">2 - 3 كيانات (-10%)</button>
                                <button type="button" class="sr-tier-entity-btn" data-entities="4">مجموعة 4+ (-20%)</button>
                            </div>
                        </div>
                    </div>

                    <!-- جدول المقارنة المعماري الشامل -->
                    <div class="sr-tier-table-wrapper">
                        <table class="sr-tier-table">
                            <thead>
                                <tr>
                                    <th class="sr-tier-th-features">
                                        <div class="sr-tier-features-heading">المواصفات والمعايير المعمارية</div>
                                        <div class="sr-tier-features-sub">مقارنة تفصيلية بين الخصائص السحابية والأمنية والتشغيلية</div>
                                    </th>

                                    <!-- Tier 1: Starter -->
                                    <th class="sr-tier-th-col">
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">Core Starter</h4>
                                            <p class="sr-tier-desc">للشركات الناشئة والمشاريع ذات النطاق الفردي</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-starter">1,192</span>
                                                    <span class="sr-tier-period" id="tier-period-starter">/ شهرياً</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-starter">€1,490</span>
                                                <div class="sr-tier-billed-note" id="tier-note-starter">تُدفع سنوياً (وفّر 20%)</div>
                                            </div>
                                            <a href="https://wa.me/31618111116" id="tier-cta-starter" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--glass">
                                                <span>حجز الباقة عبر واتساب VIP</span>
                                            </a>
                                        </div>
                                    </th>

                                    <!-- Tier 2: Pro (Featured) -->
                                    <th class="sr-tier-th-col featured">
                                        <div class="sr-tier-ribbon-badge">الأكثر طلباً // Flagship</div>
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">Business Pro</h4>
                                            <p class="sr-tier-desc">للشركات المتوسطة والمؤسسات التجارية المتنامية</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-pro">2,312</span>
                                                    <span class="sr-tier-period" id="tier-period-pro">/ شهرياً</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-pro">€2,890</span>
                                                <div class="sr-tier-billed-note" id="tier-note-pro">تُدفع سنوياً (وفّر 20%)</div>
                                            </div>
                                            <a href="https://wa.me/31618111116" id="tier-cta-pro" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--primary">
                                                <span>بدء النشر السحابي الفوري ★</span>
                                            </a>
                                        </div>
                                    </th>

                                    <!-- Tier 3: Enterprise -->
                                    <th class="sr-tier-th-col">
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">Sovereign Enterprise</h4>
                                            <p class="sr-tier-desc">للهيئات والشركات الكبرى ذات المتطلبات السيادية</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-enterprise">4,320</span>
                                                    <span class="sr-tier-period" id="tier-period-enterprise">/ شهرياً</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-enterprise">€5,400</span>
                                                <div class="sr-tier-billed-note" id="tier-note-enterprise">تُدفع سنوياً (وفّر 20%)</div>
                                            </div>
                                            <a href="https://wa.me/31618111116" id="tier-cta-enterprise" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--glass">
                                                <span>استشارة معمارية سيادية 🛡️</span>
                                            </a>
                                        </div>
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                <!-- Category 1: البنية السحابية والاستضافة -->
                                <tr class="sr-tier-category-row">
                                    <td colspan="4">
                                        <span class="sr-tier-cat-icon">🌐</span> 1. البنية السحابية واستضافة أمستردام (Cloud Infrastructure & AMS-IX)
                                    </td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">مركز البيانات وموقع الخوادم</span>
                                        <span class="sr-tier-feature-tooltip">موقع استضافة الخوادم وقواعد البيانات السيادية</span>
                                    </td>
                                    <td class="sr-tier-val-col">أمستردام Tier 3+ (مشترك)</td>
                                    <td class="sr-tier-val-col featured">خادم سحابي مخصص VPS في أمستردام</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">Sovereign Cloud Cluster معزول فيزيائياً</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">التخزين السحابي عالي السرعة (NVMe)</span>
                                        <span class="sr-tier-feature-tooltip">سعة التخزين الفائقة للملفات والوسائط وقواعد البيانات</span>
                                    </td>
                                    <td class="sr-tier-val-col">50 GB NVMe</td>
                                    <td class="sr-tier-val-col featured">250 GB NVMe فائقة السرعة</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">غير محدود (Scale-on-Demand)</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">حركة البيانات الشهرية والـ CDN</span>
                                        <span class="sr-tier-feature-tooltip">نطاق الباندويث المتاح وتسريع المحتوى حول العالم</span>
                                    </td>
                                    <td class="sr-tier-val-col">100,000 زيارة شهرياً</td>
                                    <td class="sr-tier-val-col featured">500,000 زيارة + شبكة CDN أوروبية</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">غير محدود + Global Anycast CDN</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">عزل المستأجرين (Tenancy Architecture)</span>
                                        <span class="sr-tier-feature-tooltip">مستوى استقلالية قاعدة البيانات وحمايتها من التداخل</span>
                                    </td>
                                    <td class="sr-tier-val-col">عزل برمجي منطقي</td>
                                    <td class="sr-tier-val-col featured">قاعدة بيانات مستقلة تماماً</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">Dedicated Single-Tenant 100%</span></td>
                                </tr>

                                <!-- Category 2: الأمان والامتثال الأوروبي -->
                                <tr class="sr-tier-category-row">
                                    <td colspan="4">
                                        <span class="sr-tier-cat-icon">🛡️</span> 2. الأمان السيادي والامتثال الأوروبي (Security & Regulatory Compliance)
                                    </td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">الامتثال للائحة حماية البيانات (GDPR EU)</span>
                                        <span class="sr-tier-feature-tooltip">Regulation EU 2016/679 وعقود معالجة البيانات DPA</span>
                                    </td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-check">✓</span> قياسي معتمد</td>
                                    <td class="sr-tier-val-col featured"><span class="sr-tier-check">✓</span> متقدم + اتفاقية DPA مخصصة</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight"><span class="sr-tier-check">✓</span> Zero-Knowledge السيادية</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">الامتثال الضريبي الهولندي (Belastingdienst)</span>
                                        <span class="sr-tier-feature-tooltip">حساب شرائح BTW والفاتورة الإلكترونية المعتمدة</span>
                                    </td>
                                    <td class="sr-tier-val-col">فواتير رقمية أساسية</td>
                                    <td class="sr-tier-val-col featured">حساب BTW آلي + معيار PEPPOL BIS</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">تكامل كامل مع البنوك والأنظمة المحاسبية</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">إدارة مفاتيح التشفير (Encryption Keys)</span>
                                        <span class="sr-tier-feature-tooltip">ملكية مفاتيح تشفير البيانات أثناء النقل والتخزين</span>
                                    </td>
                                    <td class="sr-tier-val-col">AES-256 بنية S&R المشتركة</td>
                                    <td class="sr-tier-val-col featured">TLS 1.3 + شهادة SSL بنكية معززة</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">مفاتيح تشفير خاصة بالعميل (BYOK / KMS)</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">النسخ الاحتياطي والتعافي من الكوارث</span>
                                        <span class="sr-tier-feature-tooltip">تكرار البيانات الجغرافي وسرعة استعادة العمليات</span>
                                    </td>
                                    <td class="sr-tier-val-col">أسبوعي سحابي</td>
                                    <td class="sr-tier-val-col featured">يومي عبر مركزين جغرافيين</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">لحظي مستمر (RPO < 5 دقائق / Hot-Standby)</span></td>
                                </tr>

                                <!-- Category 3: الذكاء الاصطناعي والتكاملات -->
                                <tr class="sr-tier-category-row">
                                    <td colspan="4">
                                        <span class="sr-tier-cat-icon">⚡</span> 3. الذكاء الاصطناعي والتكاملات الرقمية (AI Engines & Integrations)
                                    </td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">المساعد الذكي المؤسسي (AI Copilot RAG)</span>
                                        <span class="sr-tier-feature-tooltip">محرك ذكاء اصطناعي مدرب على وثائق وأنظمة الشركة</span>
                                    </td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-dash">—</span></td>
                                    <td class="sr-tier-val-col featured"><span class="sr-tier-check">✓</span> نموذج RAG قياسي لخدمة العملاء</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight"><span class="sr-tier-check">✓</span> نموذج سيادي معزول مدرب على أنظمتك بالكامل</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">بوابات الدفع الإلكتروني الأوروبية</span>
                                        <span class="sr-tier-feature-tooltip">دعم آليات الدفع المعتمدة في هولندا وأوروبا</span>
                                    </td>
                                    <td class="sr-tier-val-col">Stripe + بطاقات الائتمان</td>
                                    <td class="sr-tier-val-col featured">Stripe + Mollie + iDEAL + Bancontact</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">جميع البوابات + SEPA Direct Debit المؤسسي</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">واجهات الربط البرمجي (APIs & Webhooks)</span>
                                        <span class="sr-tier-feature-tooltip">ربط النظام بتطبيقات الطرف الثالث والأنظمة الحالية</span>
                                    </td>
                                    <td class="sr-tier-val-col">Webhooks أساسية</td>
                                    <td class="sr-tier-val-col featured">واجهات REST APIs كاملة وموثقة</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">وصول كامل لـ Core APIs + Custom Endpoints</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">حقوق العلامة البيضاء (White-Label Branding)</span>
                                        <span class="sr-tier-feature-tooltip">إمكانية استخدام علامتك التجارية الخالصة دون شعارنا</span>
                                    </td>
                                    <td class="sr-tier-val-col">شعار "Powered by CoreSync"</td>
                                    <td class="sr-tier-val-col featured">تخصيص الهوية والشعار والألوان</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">100% White-Label مع حجب أي إشارة تقنية</span></td>
                                </tr>

                                <!-- Category 4: الدعم واتفاقية مستوى الخدمة SLA -->
                                <tr class="sr-tier-category-row">
                                    <td colspan="4">
                                        <span class="sr-tier-cat-icon">🤝</span> 4. الدعم التنفيذي واتفاقية مستوى الخدمة (SLA & Concierge)
                                    </td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">الجاهزية السحابية المضمونة تعاقدياً (SLA)</span>
                                        <span class="sr-tier-feature-tooltip">نسبة التشغيل المستمر دون انقطاع</span>
                                    </td>
                                    <td class="sr-tier-val-col">99.5% استمرارية تشغيل</td>
                                    <td class="sr-tier-val-col featured">99.9% جاهزية عالية High Availability</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">99.98% Mission-Critical SLA</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">زمن الاستجابة للدعم الفني (Response Time)</span>
                                        <span class="sr-tier-feature-tooltip">الحد الأقصى للرد وحل الحالات الطارئة</span>
                                    </td>
                                    <td class="sr-tier-val-col">خلال 24 ساعة (تذاكر دعم)</td>
                                    <td class="sr-tier-val-col featured">خلال 4 ساعات (بريد + واتساب)</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">خلال 15 دقيقة (خط ساخن مخصص 24/7/365)</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">التدريب ونقل المعرفة للكوادر</span>
                                        <span class="sr-tier-feature-tooltip">ورش العمل والتأهيل العملي لفريق العمل</span>
                                    </td>
                                    <td class="sr-tier-val-col">دليل تدريبي رقمي شامل</td>
                                    <td class="sr-tier-val-col featured">جلستان تدريبيتان حيتان عبر Zoom</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">تدريب حضوري في أمستردام أو أونلاين غير محدود</span></td>
                                </tr>
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">الاستشاري المخصص والمراجعة التقنية</span>
                                        <span class="sr-tier-feature-tooltip">خبير مخصص يراجع الأداء ويوجه التطور الرقمي</span>
                                    </td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-dash">—</span></td>
                                    <td class="sr-tier-val-col featured">مراجعة نصف سنوية لأداء النظام</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">Senior Enterprise Solutions Architect مخصص</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- شريط الضمانات والتخصيص السفلي -->
                    <div class="sr-tier-bottom-bar">
                        <div class="sr-tier-guarantee-items">
                            <div class="sr-tier-guarantee-item">
                                <span class="sr-tier-guarantee-icon"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
                                <span>ضمان استرداد كامل خلال 14 يوماً في حال عدم الرضا</span>
                            </div>
                            <div class="sr-tier-guarantee-item">
                                <span class="sr-tier-guarantee-icon"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
                                <span>عقد قانوني هولندي رسمي يحمي كامل حقوق الملكية الفكرية</span>
                            </div>
                            <div class="sr-tier-guarantee-item">
                                <span class="sr-tier-guarantee-icon"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
                                <span>إمكانية الترقية أو تعديل مواصفات الخوادم في أي لحظة دون انقطاع</span>
                            </div>
                        </div>

                        <a href="https://wa.me/31618111116?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D9%8B%20S%26R%20CoreSync%D8%8C%20%D9%86%D8%AD%D9%86%20%D9%85%D8%A4%D8%B3%D8%B3%D8%A9%20%D9%83%D8%A8%D8%B1%D9%89%20%D9%88%D9%86%D8%B1%D8%BA%D8%A8%20%D8%A8%D8%B9%D9%82%D8%AF%20%D8%AC%D9%84%D8%B3%D8%A9%20%D8%A7%D8%B3%D8%AA%D8%B4%D8%A7%D8%B1%D8%A9%20%D8%AA%D9%86%D9%81%D9%8A%D8%B0%D9%8A%D8%A9%20%D9%84%D8%AA%D8%B5%D9%85%D9%8A%D9%85%20%D8%A8%D8%A7%D9%82%D8%A9%20Enterprise%20%D8%B3%D9%8A%D8%A7%D8%AF%D9%8A%D8%A9%20%D9%85%D8%AE%D8%B5%D8%B5%D8%A9." target="_blank" rel="noopener noreferrer" class="sr-tier-custom-quote-btn">
                            <span>طلب تسعير مؤسسي خاص (Custom B2B Quotation) ←</span>
                        </a>
                    </div>
                </div>
`;

// 3. Inject HTML before cost-estimator
if (!html.includes('id="tier-matrix"')) {
    const estimatorMarker = '<div class="cost-estimator-wrapper" id="cost-estimator">';
    if (html.includes(estimatorMarker)) {
        html = html.replace(estimatorMarker, matrixHtml + '\n                ' + estimatorMarker);
        console.log('✓ Injected sr-tier-matrix-section before cost-estimator');
    } else {
        console.error('Could not find cost-estimator-wrapper marker in index.html');
    }
} else {
    console.log('id="tier-matrix" already present in index.html');
}

// 4. Inject JS script before </body>
if (!html.includes('sr-tier-matrix.js')) {
    const endBodyMarker = '</body>';
    if (html.includes(endBodyMarker)) {
        html = html.replace(
            endBodyMarker,
            '    <!-- S&R CoreSync Enterprise Tier Matrix Controller -->\n    <script src="./js/sr-tier-matrix.js" defer></script>\n</body>'
        );
        console.log('✓ Injected sr-tier-matrix.js before </body>');
    } else {
        console.error('Could not find </body> in index.html');
    }
} else {
    console.log('sr-tier-matrix.js already present in index.html');
}

fs.writeFileSync(indexPath, html, 'utf8');
console.log('index.html updated successfully with Enterprise Tier Matrix.');
