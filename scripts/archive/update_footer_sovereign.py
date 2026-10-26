import re
import os

target_file = r"d:\I-Ai\App\S&R CoreSync Solutions\Project\index.html"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Locate the sovereignLangDropdownMobile block
dropdown_start = content.find('<div class="sovereign-lang-dropdown" id="sovereignLangDropdownMobile">')
if dropdown_start == -1:
    raise Exception("sovereignLangDropdownMobile not found")

dropdown_end = content.find('</div>\n            <a href="logo-studio.html"', dropdown_start)
if dropdown_end == -1:
    dropdown_end = content.find('</div>\r\n            <a href="logo-studio.html"', dropdown_start)
if dropdown_end == -1:
    raise Exception("end of sovereignLangDropdownMobile not found")

dropdown_html = content[dropdown_start : dropdown_end + 6] # includes the closing </div>

# Upgrade trigger button inside dropdown_html for luxury footer layout
old_trigger = """    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerMobile" aria-expanded="false" aria-haspopup="true" title="اختر اللغة / Select Language">
        <span class="sovereign-lang-flag">🇸🇦</span>
        <span class="sovereign-lang-current-label">AR</span>
        <svg class="sovereign-lang-chevron" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>"""

new_trigger = """    <button type="button" class="sovereign-lang-trigger" id="sovereignLangTriggerMobile" aria-expanded="false" aria-haspopup="true" title="اختر لغة المنصة / Switch Portal Language">
        <div class="sr-footer-lang-trigger-content">
            <span class="sovereign-lang-flag">🇸🇦</span>
            <span>بوابة اللغات / Language (<span class="sovereign-lang-current-label">AR</span>)</span>
        </div>
        <svg class="sovereign-lang-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>"""

if old_trigger in dropdown_html:
    dropdown_html = dropdown_html.replace(old_trigger, new_trigger)

# 2. Build the new luxury footer
new_footer = f"""        <!-- 10. الفوتر السيادي الفاخر المتكامل (Sovereign Luxury Footer Architecture) -->
        <footer class="tf-footer tf-footer--original">
            <div class="footer-stars" aria-hidden="true"></div>
            
            <div class="container">
                <!-- شبكة الفوتر السيادي المتوازنة (4 أعمدة تنفيذية) -->
                <div class="sr-footer-grid">
                    
                    <!-- العمود 1: الهوية المؤسسية والمقر الأوروبي -->
                    <div class="sr-footer-brand-wrap">
                        <div class="sr-footer-brand-header">
                            <img src="./assets/sr-core-emblem-official.png" alt="S&R CoreSync Emblem" class="sr-footer-emblem" width="46" height="46">
                            <h3 class="sr-footer-brand-title">S&R <span>CoreSync</span> Solutions</h3>
                        </div>
                        <p class="sr-footer-tagline">
                            نبتكر ونعمل عالميًا من أمستردام لتطوير البنى البرمجية السحابية، منظومات الـ ERP المتقدمة، وهندسة الذكاء الاصطناعي السيادي للشركات والمؤسسات الكبرى.
                        </p>
                        <div class="sr-footer-hq-box">
                            <div class="sr-footer-hq-item">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                                <span><strong>المقر الهولندي:</strong> Keizersgracht 482, 1016 GD Amsterdam</span>
                            </div>
                            <div class="sr-footer-hq-item">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M7 15h0M2 9.5h20"></path></svg>
                                <span><strong>الامتثال الضريبي:</strong> Belastingdienst BTW Compliant</span>
                            </div>
                            <div class="sr-footer-hq-item">
                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                                <span><strong>أمن البيانات الأوروبي:</strong> GDPR EU 2016/679 Certified</span>
                            </div>
                        </div>
                        <div class="sr-footer-badges">
                            <span class="sr-footer-badge">🛡️ GDPR EU</span>
                            <span class="sr-footer-badge">⚡ AMS-IX Tier 3</span>
                            <span class="sr-footer-badge">🔒 SLA 99.98%</span>
                        </div>
                    </div>

                    <!-- العمود 2: المنظومات السحابية والمنتجات -->
                    <div class="sr-footer-col">
                        <h4 class="sr-footer-heading">المنظومات السيادية</h4>
                        <ul class="sr-footer-nav-list">
                            <li><a href="./preview-work.html#platforms">S&R CivicSync™ <span class="sr-footer-pill-tag">الجاليات</span></a></li>
                            <li><a href="./preview-work.html#platforms">S&R HealthBridge™ <span class="sr-footer-pill-tag">الطبية</span></a></li>
                            <li><a href="./preview-work.html#platforms">S&R OmniBakery™ <span class="sr-footer-pill-tag">المخابز ERP</span></a></li>
                            <li><a href="./preview-whitelabel-calculator.html">حاسبة التراخيص الفورية <span class="sr-footer-pill-tag">جديد 🧮</span></a></li>
                            <li><a href="./preview-estimator.html">حاسبة التوفير المالي (ROI) 📊</a></li>
                            <li><a href="./preview-software.html">سوق البرمجيات والأنظمة 💻</a></li>
                            <li><a href="./demo.html">النظام التجريبي السحابي ⚡</a></li>
                        </ul>
                    </div>

                    <!-- العمود 3: خريطة المنصة والتنقل السريع -->
                    <div class="sr-footer-col">
                        <h4 class="sr-footer-heading">خريطة المنصة</h4>
                        <ul class="sr-footer-nav-list">
                            <li><a href="#about">القيادة التنفيذية والمؤسسون</a></li>
                            <li><a href="#work">سابقة الأعمال والمشاريع</a></li>
                            <li><a href="#service">الحلول والخدمات المؤسسية</a></li>
                            <li><a href="#pricing">باقات التراخيص والأسعار</a></li>
                            <li><a href="#faq">الأسئلة الشائعة والمعايير</a></li>
                            <li><a href="./logo-studio.html">استوديو الشعار والهوية 🎨</a></li>
                            <li><a href="#brandLogoLightboxModal" onclick="openLogoLightbox(event)">فحص الشعار الرسمي 4K 🔍</a></li>
                        </ul>
                    </div>

                    <!-- العمود 4: قنوات الاتصال VIP والمحول اللغوي العالمي -->
                    <div class="sr-footer-col">
                        <h4 class="sr-footer-heading">الاتصال والدعم VIP</h4>
                        <div class="sr-footer-contact-wrap">
                            <a href="https://wa.me/31618111116?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D9%8B%20S%26R%20CoreSync%D8%8C%20%D8%A3%D9%88%D8%AF%20%D8%AD%D8%AC%D8%B2%20%D8%A7%D8%B3%D8%AA%D8%B4%D8%A7%D8%B1%D8%A9%20%D8%AA%D9%86%D9%81%D9%8A%D8%B0%D9%8A%D8%A9%20VIP" target="_blank" rel="noopener noreferrer" class="sr-footer-contact-card">
                                <div class="sr-footer-contact-icon sr-footer-contact-icon--wa">
                                    <svg viewBox="0 0 32 32" width="18" height="18" fill="currentColor"><path d="M16.02 3.2a12.7 12.7 0 0 0-10.95 19.14L3.2 28.8l6.62-1.74A12.8 12.8 0 1 0 16.02 3.2Zm0 23.24a10.48 10.48 0 0 1-5.35-1.46l-.38-.23-3.93 1.03 1.05-3.83-.25-.4a10.5 10.5 0 1 1 8.86 4.89Zm5.76-7.85c-.32-.16-1.9-.94-2.19-1.05-.3-.11-.51-.16-.73.16-.21.32-.83 1.05-1.02 1.26-.19.21-.38.24-.7.08a8.65 8.65 0 0 1-2.55-1.57 9.57 9.57 0 0 1-1.77-2.2c-.18-.32 0-.49.14-.65.14-.14.32-.38.48-.57.16-.19.21-.32.32-.54.1-.21.05-.4-.03-.56-.08-.16-.73-1.75-1-2.39-.26-.62-.53-.54-.73-.55h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69s1.16 3.13 1.32 3.35c.16.21 2.27 3.46 5.5 4.85.77.33 1.37.53 1.84.68.77.24 1.47.2 2.03.12.62-.09 1.9-.78 2.17-1.54.27-.75.27-1.4.19-1.54-.08-.13-.3-.21-.62-.37Z"/></svg>
                                </div>
                                <div class="sr-footer-contact-text">
                                    <span class="label">واتساب VIP التنفيذي المباشر</span>
                                    <span class="value">+31 6 1811 1116</span>
                                </div>
                            </a>

                            <a href="mailto:info@sr-coresync.com" class="sr-footer-contact-card">
                                <div class="sr-footer-contact-icon">
                                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>
                                </div>
                                <div class="sr-footer-contact-text">
                                    <span class="label">البريد المؤسسي الرسمي</span>
                                    <span class="value">info@sr-coresync.com</span>
                                </div>
                            </a>

                            <div class="sr-footer-lang-button-wrap">
                                {dropdown_html}
                            </div>
                        </div>
                    </div>

                </div>

                <!-- ووترمارك الفوتر العملاق السيادي المكتمل S&R CORESYNC -->
                <div class="sr-footer-watermark-container">
                    <div class="sr-footer-grand-watermark">S&R CORESYNC</div>
                    <span class="sr-footer-grand-subtitle">AMSTERDAM • SOVEREIGN CLOUD ARCHITECTURE • 2026</span>
                </div>

                <!-- الشريط السفلي للحقوق والتحكم -->
                <div class="sr-footer-bottom-bar">
                    <div class="sr-footer-legal-wrap">
                        <p class="sr-footer-legal-text">
                            © <strong>2026</strong> S&R CoreSync Solutions B.V. — جميع الحقوق محفوظة.
                        </p>
                        <ul class="sr-footer-legal-links">
                            <li><a href="./verify.html">التحقق من التراخيص</a></li>
                            <li><a href="#cookies">سياسة الخصوصية (GDPR)</a></li>
                            <li><a href="#terms">شروط الاستخدام</a></li>
                            <li><a href="./contract-of2026-pdf.html">العقد الرسمي الموحد PDF</a></li>
                        </ul>
                    </div>

                    <div class="sr-footer-bottom-actions">
                        <div class="sr-text-resizer-widget" role="group" aria-label="التحكم في حجم الخط">
                            <span class="sr-resizer-label">الخط:</span>
                            <button type="button" class="sr-resizer-btn sr-resizer-btn--minus" onclick="window.srAdjustFontSize(-1)" aria-label="تصغير الخط">A-</button>
                            <button type="button" class="sr-resizer-indicator" onclick="window.srResetFontSize()" aria-label="إعادة الضبط">100%</button>
                            <button type="button" class="sr-resizer-btn sr-resizer-btn--plus" onclick="window.srAdjustFontSize(1)" aria-label="تكبير الخط">A+</button>
                        </div>
                        <a href="#home" class="sr-footer-back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}}); return false;">
                            <span>العودة للأعلى</span>
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
                        </a>
                    </div>
                </div>

            </div>
        </footer>"""

footer_start = content.find('<!-- 10. الفوتر الأصلي الفاخر (Footer Original) -->')
if footer_start == -1:
    footer_start = content.find('<footer class="tf-footer tf-footer--original">')

footer_end = content.find('</footer>', footer_start)
if footer_end == -1:
    raise Exception("footer_end not found")

footer_end += len('</footer>')

old_footer = content[footer_start : footer_end]
content = content[:footer_start] + new_footer + content[footer_end:]

with open(target_file, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Updated index.html footer with Sovereign Luxury Architecture!")
