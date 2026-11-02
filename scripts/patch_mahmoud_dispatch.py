import os

p = 'js/sr-inline-13eaa28e.js'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

old_dispatch_inputs = """            <form onsubmit="executeClientReportDispatch(event)">
                <div class="sr-dispatch-form-group">
                    <label>اسم العميل أو المؤسسة المستهدفة:</label>
                    <input type="text" id="srClientOrgName" value="مركز CLGID للدراسات والحوكمة - لاهاي (The Hague)" required />
                </div>
                <div class="sr-dispatch-form-group">
                    <label>البريد الإلكتروني الرسمي للعميل:</label>
                    <input type="email" id="srClientTargetEmail" placeholder="director@clgid.org (أو بريد المسؤول)" value="info@clgid-governance.org" required />
                </div>
                <div class="sr-dispatch-form-group">
                    <label>رقم هاتف / واتساب العميل (مع الرمز الدولي):</label>
                    <input type="tel" id="srClientTargetPhone" placeholder="+31 6 ... أو +963 / +971" value="+31 6 18111116" required />
                </div>"""

new_dispatch_inputs = """            <form onsubmit="executeClientReportDispatch(event)">
                <div class="sr-dispatch-form-group">
                    <label>اسم العميل أو المؤسسة المستهدفة:</label>
                    <input type="text" id="srClientOrgName" value="مركز CLGID للدراسات والحوكمة - لاهاي (أ. محمود الناصر)" required />
                </div>
                <div class="sr-dispatch-form-group">
                    <label>البريد الإلكتروني المعتمد للعميل:</label>
                    <input type="email" id="srClientTargetEmail" value="Mahmoud.alnaser1996@gmail.com" required />
                </div>
                <div class="sr-dispatch-form-group">
                    <label>رقم هاتف / واتساب العميل (مع الرمز الدولي):</label>
                    <input type="tel" id="srClientTargetPhone" value="+31 6 83709854" required />
                </div>"""

norm_text = text.replace('\r\n', '\n')
norm_old = old_dispatch_inputs.replace('\r\n', '\n')
norm_new = new_dispatch_inputs.replace('\r\n', '\n')

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new, 1)
    print("Updated dispatch inputs with Mahmoud al-Naser data successfully!")
else:
    print("Old dispatch inputs not found")

# Also in executeClientReportDispatch defaults:
old_exec_defaults = """    const clientOrg = document.getElementById("srClientOrgName") ? document.getElementById("srClientOrgName").value.trim() : "مركز CLGID لاهاي";
    const clientEmail = document.getElementById("srClientTargetEmail") ? document.getElementById("srClientTargetEmail").value.trim() : "info@clgid-governance.org";
    const clientPhone = document.getElementById("srClientTargetPhone") ? document.getElementById("srClientTargetPhone").value.trim() : "+31618111116";"""

new_exec_defaults = """    const clientOrg = document.getElementById("srClientOrgName") ? document.getElementById("srClientOrgName").value.trim() : "مركز CLGID لاهاي (أ. محمود الناصر)";
    const clientEmail = document.getElementById("srClientTargetEmail") ? document.getElementById("srClientTargetEmail").value.trim() : "Mahmoud.alnaser1996@gmail.com";
    const clientPhone = document.getElementById("srClientTargetPhone") ? document.getElementById("srClientTargetPhone").value.trim() : "+31683709854";"""

norm_old_exec = old_exec_defaults.replace('\r\n', '\n')
norm_new_exec = new_exec_defaults.replace('\r\n', '\n')

if norm_old_exec in norm_text:
    norm_text = norm_text.replace(norm_old_exec, norm_new_exec, 1)
    print("Updated execute defaults with Mahmoud data successfully!")

# Also add link to interactive prototype in the blueprint actions
old_blueprint_prototype_anchor = """                            <button type="button" class="sr-btn-action" style="background:linear-gradient(135deg,#059669,#047857);color:#fff;" data-sr-call="openClientReportDispatchModal"><span>📨 إرسال التقرير النهائي للعميل بالبريد والواتساب</span></button>"""
new_blueprint_prototype_anchor = """                            <a href="clgid-prototype.html" target="_blank" rel="noopener noreferrer" class="sr-btn-action" style="background:linear-gradient(135deg,#0284c7,#0369a1);color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:6px;"><span>🏛️ معاينة النموذج الأولي الحي للواجهة العربية (CLGID)</span></a>
                            <button type="button" class="sr-btn-action" style="background:linear-gradient(135deg,#059669,#047857);color:#fff;" data-sr-call="openClientReportDispatchModal"><span>📨 إرسال التقرير وعرض السعر للأستاذ محمود الناصر</span></button>"""

norm_old_proto = old_blueprint_prototype_anchor.replace('\r\n', '\n')
norm_new_proto = new_blueprint_prototype_anchor.replace('\r\n', '\n')

if norm_old_proto in norm_text:
    norm_text = norm_text.replace(norm_old_proto, norm_new_proto, 1)
    print("Added prototype link button to blueprint actions successfully!")

with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(norm_text)

print("Patch complete!")

