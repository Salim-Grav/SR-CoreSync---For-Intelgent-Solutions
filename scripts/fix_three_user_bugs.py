import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js_path = os.path.join(ROOT, 'js', 'sr-inline-13eaa28e.js')
css_path = os.path.join(ROOT, 'css', 'enterprise-suite.css')

# 1. Update js/sr-inline-13eaa28e.js
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix Bug 2: Routing Logic for Web / Project Development -> Salim
old_routing_snippet = 'const isRaed=e.includes("erp")||e.includes("محاسب")||e.includes("ضريب")||e.includes("ضرائب")||e.includes("vat")||e.includes("btw")||e.includes("تشغيل")||e.includes("عمليات")||e.includes("إدار")||e.includes("ادارة")||e.includes("عقد")||e.includes("عقود")||e.includes("توسع")||e.includes("شركاء")||e.includes("مالي")||e.includes("تمويل")||e.includes("مخازن")||e.includes("امداد")||e.includes("سلاسل")||e.includes("سوشيال")||e.includes("8k")||e.includes("تسويق")||e.includes("هوية")||e.includes("براند")||e.includes("business")||e.includes("operation")||e.includes("finance")||e.includes("logistics")||e.includes("supply");'

new_routing_snippet = '''// Smart Domain Routing: Tech, Web, Cloud, AI, Portals, CLGID Governance -> Eng. Salim Aziza
const isWebOrTech = e.includes("ويب") || e.includes("موقع") || e.includes("منصة") || e.includes("بوابة") || 
                    e.includes("تطبيق") || e.includes("سحاب") || e.includes("برمج") || e.includes("كود") || 
                    e.includes("ذكاء") || e.includes("api") || e.includes("web") || e.includes("website") || 
                    e.includes("portal") || e.includes("platform") || e.includes("software") || 
                    e.includes("cloud") || e.includes("app") || e.includes("code") || e.includes("ai") || 
                    e.includes("tech") || e.includes("تقني") || e.includes("مركز") || e.includes("clgid") || 
                    e.includes("governance") || e.includes("سليم") || e.includes("salim");

const isPureFinanceOrErp = (e.includes("erp") || e.includes("محاسب") || e.includes("ضريب") || e.includes("ضرائب") || 
                           e.includes("vat") || e.includes("btw") || e.includes("جمارك") || e.includes("سلاسل") || 
                           e.includes("مخازن") || e.includes("لوجستي") || e.includes("رائد") || e.includes("kaakeh")) && !isWebOrTech;

const isRaed = isPureFinanceOrErp;'''

if old_routing_snippet in js:
    js = js.replace(old_routing_snippet, new_routing_snippet)
    print("Replaced old_routing_snippet successfully!")
else:
    print("Warning: old_routing_snippet not found directly, checking regex")
    pattern = r'const isRaed=e\.includes\("erp"\)[\s\S]*?e\.includes\("supply"\);'
    js = re.sub(pattern, new_routing_snippet, js)
    print("Replaced via regex!")

# Add specific detection for CLGID / governance and web portals in generateAiProjectBlueprint
old_project_detection = '''e.includes("متجر")||e.includes("تجارة")||e.includes("شحن")||e.includes("بيع")||e.includes("store")||e.includes("shop")?(i="منصة تجارة إلكترونية سحابية PWA مع ربط محاسبي ومخازن"'''

new_project_detection = '''e.includes("clgid")||e.includes("governance")||e.includes("مركز")||e.includes("حوار")||e.includes("لاهاي")?(i="المنصة الرقمية المؤسسية لحوكمة الدراسات والاستشارات السيادية 2026",s="هندسة المنصات السيادية وبوابات الحوكمة والدراسات (لاهاي)",c="منظومة PWA متقدمة + خوادم سحابية أوروبية معزولة متوافقة مع GDPR + محرك أوراق السياسات ودراسات الجدوى المعتمدة",a="+65% كفاءة في إدارة البرامج والتقارير الاستشارية وتأمين سيادي كامل لبيانات المؤسسة"):e.includes("ويب")||e.includes("موقع")||e.includes("website")||e.includes("web")||e.includes("تطوير موقع")?(i="بوابة ومنصة ويب سحابية تفاعلية فائقة السرعة بهوية بصرية 8K",s="هندسة الويب السحابي وتطبيقات الـ Enterprise Modern Web",c="واجهة مستخدم React/Modern PWA فائقة الخفة + استضافة سحابية أوروبية + نظام إدارة محتوى سيادي متعدد اللغات (عربي/هولندي/إنجليزي)",a="+70% سرعة في استقطاب الشركاء وتحويل الزوار ومطابقة تامة لمعايير أمن البيانات الأوروبية"):e.includes("متجر")||e.includes("تجارة")||e.includes("شحن")||e.includes("بيع")||e.includes("store")||e.includes("shop")?(i="منصة تجارة إلكترونية سحابية PWA مع ربط محاسبي ومخازن"'''

if old_project_detection in js:
    js = js.replace(old_project_detection, new_project_detection)
    print("Added CLGID & Web Platform project detection!")
else:
    print("Warning: old_project_detection not found directly")

# Fix Bug 3: exportBlueprintPdf implementation
old_export_pdf = 'function exportBlueprintPdf(e){openBlueprintPreviewModal();setTimeout(()=>{window.print();},400);}'
new_export_pdf = '''function exportBlueprintPdf(e) {
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
}'''

if old_export_pdf in js:
    js = js.replace(old_export_pdf, new_export_pdf)
    print("Replaced exportBlueprintPdf successfully!")
else:
    print("Warning: old_export_pdf not found directly, checking variation")
    pattern_pdf = r'function exportBlueprintPdf\(e\)\{[\s\S]*?window\.print\(\);[\s\S]*?\}'
    js = re.sub(pattern_pdf, new_export_pdf, js)
    print("Replaced exportBlueprintPdf via regex!")

# Fix Bug 1: Attach all modal action functions to window
global_exports_block = """
// =============================================================================
// S&R CoreSync - Global Window Bindings for Strict CSP & Delegated Events
// =============================================================================
window.toggleVoiceRecording = toggleVoiceRecording;
window.startVoiceRecording = startVoiceRecording;
window.stopVoiceRecording = stopVoiceRecording;
window.resetVoicePlanner = resetVoicePlanner;
window.generateAiProjectBlueprint = generateAiProjectBlueprint;
window.fillVoiceSample = fillVoiceSample;
window.exportBlueprintPdf = exportBlueprintPdf;
window.dispatchBlueprintToWhatsApp = dispatchBlueprintToWhatsApp;
window.dispatchBlueprintToTelegram = dispatchBlueprintToTelegram;
window.bookBlueprintConsultation = bookBlueprintConsultation;
window.openExecutiveCheckoutModal = openExecutiveCheckoutModal;
window.closeExecutiveCheckoutModal = closeExecutiveCheckoutModal;
window.toggleBlueprintAudioSynthesis = toggleBlueprintAudioSynthesis;
window.stopBlueprintAudioSynthesis = stopBlueprintAudioSynthesis;
"""

if 'window.toggleVoiceRecording = toggleVoiceRecording;' not in js:
    js += "\n" + global_exports_block
    print("Appended global_exports_block to js/sr-inline-13eaa28e.js!")
else:
    print("Global exports already present.")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Saved js/sr-inline-13eaa28e.js successfully!")

# 2. Update css/enterprise-suite.css @media print
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the last @media print block
last_media_print_idx = css.lastIndexOf('@media print') if hasattr(css, 'lastIndexOf') else css.rfind('@media print')

new_media_print_rule = """@media print {
    @page {
        size: A4 portrait;
        margin: 10mm;
    }
    *, *::before, *::after {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    html, body {
        background: #ffffff !important;
        color: #0f172a !important;
        overflow: visible !important;
        height: auto !important;
        min-height: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    /* Hide all background and other modal elements */
    body > *:not(#srBlueprintPreviewModal) {
        display: none !important;
    }
    #aiVoicePlannerModal,
    .sr-exec-modal:not(#srBlueprintPreviewModal),
    .hero-cinematic,
    header,
    footer,
    nav,
    .floating-follow,
    .floating-actions,
    .es-floating-suite {
        display: none !important;
    }
    #srBlueprintPreviewModal {
        display: block !important;
        position: static !important;
        inset: auto !important;
        width: 100% !important;
        height: auto !important;
        min-height: 100% !important;
        background: #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important;
        box-shadow: none !important;
        border: none !important;
        visibility: visible !important;
    }
    .sr-a4-preview-wrapper {
        display: block !important;
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
        transform: none !important;
        visibility: visible !important;
    }
    .sr-a4-sheet {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        background: #ffffff !important;
        color: #0f172a !important;
        border-radius: 0 !important;
        overflow: visible !important;
        page-break-inside: avoid !important;
        visibility: visible !important;
    }
    .sr-a4-sheet * {
        visibility: visible !important;
    }
    .sr-a4-toolbar, 
    .sr-exec-modal-backdrop, 
    .sr-exec-modal-close,
    .sr-blueprint-actions,
    .sr-voice-waves,
    .sr-voice-status,
    .sr-blueprint-audio-controls {
        display: none !important;
    }
}
"""

if last_media_print_idx != -1:
    css = css[:last_media_print_idx] + new_media_print_rule
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Replaced @media print in css/enterprise-suite.css successfully!")
else:
    print("Warning: @media print not found in css")

print("All fixes applied successfully!")
