# -*- coding: utf-8 -*-
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Fix line 2469 tour step across all languages
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f == 'demo.html' and root != BASE_DIR and not root.endswith('ckb'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Fix tour desc
            content = re.sub(r"desc: 'مؤشرات مالية دقيقة للإيرادات السنوية[^']*',", "desc: 'Accurate real-time metrics for annual revenue, operating cash flow, and cloud automation hours saved.',", content)

            # Dutch specific cleanups
            if root.endswith('nl'):
                content = content.replace('<th>BTW المحتسبة</th>', '<th>Berekende Btw</th>')
                content = content.replace('<span>Totaalbedrag المستحق والمقيد بالدفاتر:</span>', '<span>Totaalbedrag Verschuldigd & Geregistreerd:</span>')
                content = content.replace('aiResponse = "توجد 1 factuur معلقة بقيمة €35,000 لعميل في الرياض vervalt binnen 14 dagen مع بند Reverse Charge ضريبي سليم. لا توجد أي فواتير متعثرة تتجاوز 30 يوماً بفضل التنبيهات الآلية للواتساب والإيميل.";',
                                          'aiResponse = "Er is 1 openstaande factuur van €35.000 met vervaldatum binnen 14 dagen en geldige btw-verleggingsregeling (Reverse Charge). Geen achterstallige vorderingen ouder dan 30 dagen dankzij geautomatiseerde herinneringen.";')
                content = content.replace('Gesynchroniseerd فوراً', 'Direct Gesynchroniseerd')
                content = content.replace('<span>وضع Klantpresentatie [P]</span>', '<span>Klantpresentatie [P]</span>')
                content = content.replace("'معفى من BTW (0%)'", "'Vrijgesteld van btw (0%)'")
                content = content.replace("showPortalToast(`⚡ بدأ Installatiepakket Downloaden لـ [${title}] بنجاح!`);", "showPortalToast(`⚡ Installatiepakket voor [${title}] wordt gedownload...`);")
                content = content.replace("showPortalToast(`🎉 تم إتمام الدفع بنجاح وإصدار الفاتورة [${invNum}] وActiveren الترخيص!`);", "showPortalToast(`🎉 Betaling voltooid. Factuur [${invNum}] uitgegeven en licentie geactiveerd!`);")

            # English specific cleanups in features JS
            if root.endswith('en'):
                content = content.replace("? 'موظف' : 'staff'", "? 'staff' : 'staff'")
                content = content.replace("? 'ساعة/أسبوع' : 'hrs/wk'", "? 'hrs/wk' : 'hrs/wk'")
                content = content.replace("? 'ساعة' : 'hr'", "? 'hr' : 'hr'")
                content = content.replace("? 'ساعة' : 'hours'", "? 'hours' : 'hours'")
                content = content.replace("msg.replace('Salim', 'Raed').replace('سليم', 'رائد')", "msg.replace('Salim', 'Raed')")
                content = content.replace("if (lang === 'ar') triggerText.innerText = '💬 تواصل مع المؤسسين';", "triggerText.innerText = '💬 Founder Hotline';")
                content = content.replace("else if (lang === 'ckb') triggerText.innerText = '💬 پەیوەندی بە دامەزرێنەران';", "")

            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(content)

print("Targeted language isolation clean finished!")
