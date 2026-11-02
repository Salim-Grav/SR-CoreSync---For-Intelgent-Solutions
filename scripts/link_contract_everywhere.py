with open('clgid-prototype.html', 'r', encoding='utf-8') as f:
    proto = f.read()

cta_block = """
        <div style="display:flex; justify-content:center; gap:16px; margin-top:24px; flex-wrap:wrap;">
            <a href="clgid-contract.html" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:8px; padding:12px 24px; background:linear-gradient(135deg, #c5a880, #9a7b52); color:#010907; border-radius:8px; font-weight:800; font-size:0.95rem; text-decoration:none; box-shadow:0 6px 20px rgba(197,168,128,0.3); transition:all 0.2s ease;">
                <span>📜 فتح وتوقيع مسودة العقد الرسمي المباشر B2B (Dutch Law)</span>
            </a>
            <a href="https://wa.me/31683709854" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:8px; padding:12px 24px; background:#25D366; color:#ffffff; border-radius:8px; font-weight:800; font-size:0.95rem; text-decoration:none;">
                <span>📱 التواصل المباشر مع الأستاذ محمود الناصر (واتساب)</span>
            </a>
        </div>
    </section>"""

if 'id="pricing"' in proto:
    proto = proto.replace('</section>\n\n    <!-- Footer -->', cta_block + '\n\n    <!-- Footer -->')
    with open('clgid-prototype.html', 'w', encoding='utf-8') as f:
        f.write(proto)
    print("SUCCESS: Linked contract in clgid-prototype.html")
else:
    print("WARNING: pricing not found in clgid-prototype.html")

# Now in js/sr-inline-13eaa28e.js
with open('js/sr-inline-13eaa28e.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

old_blueprint_action = '<a href="clgid-prototype.html" target="_blank" rel="noopener noreferrer" class="sr-btn-action" style="background:linear-gradient(135deg,#0284c7,#0369a1);color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:6px;"><span>🏛️ معاينة النموذج الأولي الحي للواجهة العربية (CLGID)</span></a>'
new_blueprint_action = old_blueprint_action + '\\n                            <a href="clgid-contract.html" target="_blank" rel="noopener noreferrer" class="sr-btn-action" style="background:linear-gradient(135deg,#0a1e36,#1e293b);color:#c5a880;border:1px solid #c5a880;text-decoration:none;display:inline-flex;align-items:center;gap:6px;"><span>📜 مسودة العقد الرسمي المباشر (Dutch Law)</span></a>'

if old_blueprint_action in js_code:
    js_code = js_code.replace(old_blueprint_action, new_blueprint_action)
    print("SUCCESS: Added contract link in blueprint actions!")
else:
    print("WARNING: old_blueprint_action not matched in js")

old_a4_toolbar = '<button type="button" class="sr-a4-btn-action sr-a4-btn-dispatch" data-sr-call="dispatchBlueprintToClientAndManagement">'
new_a4_toolbar = '<a href="clgid-contract.html" target="_blank" rel="noopener noreferrer" class="sr-a4-btn-action" style="background:#0a1e36; color:#c5a880; border:1px solid #c5a880; text-decoration:none; display:inline-flex; align-items:center;">📜 ${isAr ? "مسودة العقد الرسمي B2B" : "B2B Contract Draft"}</a>\\n                    ' + old_a4_toolbar

if old_a4_toolbar in js_code:
    js_code = js_code.replace(old_a4_toolbar, new_a4_toolbar)
    print("SUCCESS: Added contract link in A4 preview modal toolbar!")
else:
    print("WARNING: old_a4_toolbar not matched in js")

with open('js/sr-inline-13eaa28e.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("Linking complete.")
