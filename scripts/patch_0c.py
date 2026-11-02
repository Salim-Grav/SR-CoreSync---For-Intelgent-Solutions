"""
Script to apply comprehensive logic updates to:
1. js/sr-inline-13eaa28e.js
2. js/sr-inline-0c7f8fde.js
3. index.html and all 28 language index.html files
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def patch_sr_inline_0c():
    path = os.path.join(ROOT, 'js', 'sr-inline-0c7f8fde.js')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update founder name from 'أ. محمد رائد كعكة' to 'أ. رائد عزيزة' and 'أ. رائد عزيزة الشخصي'
    c = c.replace('أ. رائد كعكة', 'أ. رائد عزيزة')
    c = c.replace('أ. محمد رائد كعكة', 'أ. رائد عزيزة')
    c = c.replace('مطور نظم محاسبة الشركات // CFO', 'المسؤول التنفيذي للعمليات وتطوير الأعمال')

    # 2. Update selectBookingAdvisor to sync audio greeting bar
    old_advisor_code = 'function selectBookingAdvisor(e){const t=document.getElementById("selectedAdvisorField");t&&(t.value=e);const o=document.getElementById("advisorBtnSalim"),n=document.getElementById("advisorBtnRaed"),a=document.getElementById("advisorBtnBoth");o&&o.classList.toggle("active","salim"===e),n&&n.classList.toggle("active","raed"===e),a&&a.classList.toggle("active","both"===e);const i=document.getElementById("bookingSubmitBtnLabel");'
    new_advisor_code = '''function selectBookingAdvisor(e){
    if(typeof stopBookingAudioGreeting==="function")stopBookingAudioGreeting();
    const t=document.getElementById("selectedAdvisorField");t&&(t.value=e);
    const o=document.getElementById("advisorBtnSalim"),n=document.getElementById("advisorBtnRaed"),a=document.getElementById("advisorBtnBoth");
    o&&o.classList.toggle("active","salim"===e),n&&n.classList.toggle("active","raed"===e),a&&a.classList.toggle("active","both"===e);
    const bAvatar=document.getElementById("bookingAudioAvatar"),bName=document.getElementById("bookingAudioAdvisorName"),bSub=document.getElementById("bookingAudioAdvisorSubtitle");
    const docLang=(document.documentElement.getAttribute("lang")||"ar").toLowerCase();
    const isAr=docLang.startsWith("ar");
    const assetPrefix=window.location.pathname.includes("/en/")||window.location.pathname.includes("/nl/")||window.location.pathname.includes("/de/")||window.location.pathname.split("/").filter(Boolean).length>1?"../assets/":"./assets/";
    if(bAvatar&&bName&&bSub){
        if("raed"===e){
            bAvatar.src=assetPrefix+"founder-raed.webp";
            bName.textContent=isAr?"أ. رائد عزيزة • استشارة أنظمة ERP والحوكمة المالية":"Mr. Raed Aziza • ERP, Finance & Tax Governance";
            bSub.textContent=isAr?"المسؤول التنفيذي للعمليات وتطوير الأعمال في شركة إس آند آر":"Chief Operating Officer & Head of Business Development";
        }else if("salim"===e){
            bAvatar.src=assetPrefix+"founder-salim.webp";
            bName.textContent=isAr?"م. محمد سليم عزيزة • استشارة النظم السحابية وهندسة AI":"Eng. Mohammad Salim Aziza • Cloud Architecture & AI Engineering";
            bSub.textContent=isAr?"كبير مهندسي السحابة والذكاء الاصطناعي في شركة إس آند آر":"Lead Cloud & AI Solutions Architect";
        }else{
            bAvatar.src=assetPrefix+"founder-salim.webp";
            bName.textContent=isAr?"الشركاء المؤسسون (سليم ورائد) • جلسة استراتيجية مشتركة":"Founding Partners (Salim & Raed) • Joint Strategic Session";
            bSub.textContent=isAr?"جلسة تجمع بين المعمارية السحابية والامتثال المالي والضريبي الأوروبي":"Joint consultation combining Cloud Architecture & Financial Governance";
        }
    }
    const i=document.getElementById("bookingSubmitBtnLabel");'''

    if old_advisor_code in c:
        c = c.replace(old_advisor_code, new_advisor_code)
        print("Updated selectBookingAdvisor in js/sr-inline-0c7f8fde.js")
    else:
        print("Notice: old_advisor_code not found verbatim in js/sr-inline-0c7f8fde.js")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

if __name__ == '__main__':
    patch_sr_inline_0c()
