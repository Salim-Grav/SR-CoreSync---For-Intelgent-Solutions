"""
Update and unify navigation across all Mission Suite pages
==========================================================
"""
import re
import os

pages_and_labels = [
    ("sovereign-arbitration-hub.html", "روابط مركز التحكيم"),
    ("multi-cbdc-bridge.html", "روابط جسر العملات الرقمية"),
    ("zkp-confidential-enclave.html", "روابط الحوسبة السرية"),
    ("digital-forensics-litigation-hub.html", "روابط منصة الأدلة الجنائية"),
    ("smart-escrow-milestone.html", "روابط منصة الضمان الذكي"),
    ("sovereign-mission-suite-dashboard.html", "روابط لوحة التحكم الموحدة"),
]

def generate_nav(active_file, label):
    links = [
        ("centennial-sovereign-command-bridge.html", "👑 غرفة القيادة المئوية"),
        ("sovereign-arbitration-hub.html", "⚖️ التحكيم الدولي (104)"),
        ("multi-cbdc-bridge.html", "💱 جسر CBDC (105)"),
        ("zkp-confidential-enclave.html", "🔐 الحوسبة السرية (106)"),
        ("digital-forensics-litigation-hub.html", "🔍 الأدلة الجنائية (107)"),
        ("smart-escrow-milestone.html", "🤝 الضمان الذكي (107)"),
        ("sovereign-mission-suite-dashboard.html", "📊 لوحة جناح المهام"),
        ("index.html", "🏠 الرئيسية"),
    ]
    
    lines = [f'            <nav class="nav-links" aria-label="{label}">']
    for url, text in links:
        cls = 'nav-link active' if url == active_file else 'nav-link'
        lines.append(f'                <a href="{url}" class="{cls}">{text}</a>')
    lines.append('            </nav>')
    return '\n'.join(lines)

for filename, label in pages_and_labels:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_nav = generate_nav(filename, label)
        updated = re.sub(r'<nav class="nav-links"[\s\S]*?</nav>', new_nav, content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"✅ Updated navigation in: {filename}")

print("\nAll Mission Suite pages unified with cross-navigation links!")
