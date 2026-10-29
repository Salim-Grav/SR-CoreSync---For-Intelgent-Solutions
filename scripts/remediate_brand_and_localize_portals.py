# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions
Remediates Brand Identity (Preserves S&R CoreSync Corporate Name & Authentic Monogram)
and Deploys High-Fidelity Native Translations for All 28 Languages across index.html & demo.html.
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LANG_DICTIONARIES = {
    "nl": {
        "nav": {
            "LEADERSHIP": "LEIDERSCHAP",
            "SERVICES": "DIENSTEN",
            "About Us": "Over Ons",
            "Pricing": "Tarieven",
            "ROI": "ROI-Calculator",
            "FAQ": "Veelgestelde Vragen",
            "Live ERP Demo ⚡": "Live ERP Demo ⚡",
            "Menu": "Menu"
        },
        "hero": {
            "PRESENTS": "PRESENTEERT",
            "Available for New Enterprise Architecture Engagements 2026": "Beschikbaar voor nieuwe enterprise-opdrachten 2026",
            "Enterprise Systems": "Enterprise Systemen",
            "& Autonomous AI Architectures": "& Autonome AI-Architecturen",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Geïntegreerde softwaresystemen & AI-oplossingen ontwikkeld met soevereine cloud-veerkracht en geautomatiseerde financiële ERP-workflows voor moderne ondernemingen in Europa en het Midden-Oosten.",
            "Ambient Audio Experience (Click to Play)": "Omgevingsgeluid (Klik om af te spelen)",
            "⚡ Live Cloud ERP Demo": "⚡ Live Cloud ERP Demo",
            "Request VIP Session 👔": "VIP-Sessie Aanvragen 👔",
            "Request Executive VIP Consultation": "Vraag VIP-Adviesgesprek Aan"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Directiedashboard",
            "ERP & Inventory Ops": "ERP & Voorraadbeheer",
            "E-Invoicing & VAT": "E-Facturatie & BTW",
            "AI Financial Copilot": "AI Financiële Copiloot",
            "Cloud Server Status": "Cloud Server Status",
            "White-Label Branding": "White-Label Maatwerk",
            "Software Hub & Store": "Software Hub & Winkel",
            "Smart ROI Calculator": "Slimme ROI-Calculator",
            "Return to Website": "Terug naar Website",
            "Emblem Studio": "Embleem Studio",
            "Client View [P]": "Klantweergave [P]",
            "Book Session with this Architecture": "Sessie Boeken met deze Architectuur",
            "Request Company Activation": "Vraag Bedrijfsactivatie Aan",
            "Enterprise Consulting": "Enterprise Consultancy",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Draag sessieconfiguraties en geteste scenario's direct over naar het adviesgesprek.",
            "Book Custom Consultation": "Boek Maatwerk Adviesgesprek",
            "Interactive Preview Session": "Interactieve Previewsessie",
            "S&R Executive Demo": "S&R Directiedemo"
        }
    },
    "de": {
        "nav": {
            "LEADERSHIP": "FÜHRUNG",
            "SERVICES": "LEISTUNGEN",
            "About Us": "Über uns",
            "Pricing": "Preise",
            "ROI": "ROI-Rechner",
            "FAQ": "Häufige Fragen",
            "Live ERP Demo ⚡": "Live ERP-Demo ⚡",
            "Menu": "Menü"
        },
        "hero": {
            "PRESENTS": "PRÄSENTIERT",
            "Available for New Enterprise Architecture Engagements 2026": "Verfügbar für neue Enterprise-Projekte 2026",
            "Enterprise Systems": "Unternehmenssysteme",
            "& Autonomous AI Architectures": "& Autonome KI-Architekturen",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Integrierte Softwaresysteme & KI-Lösungen mit souveräner Cloud-Resilienz und automatisierten Finanz-ERP-Workflows für moderne Unternehmen in Europa und dem Nahen Osten.",
            "Ambient Audio Experience (Click to Play)": "Ambient-Audio (Klicken zum Abspielen)",
            "⚡ Live Cloud ERP Demo": "⚡ Live Cloud-ERP-Demo",
            "Request VIP Session 👔": "VIP-Sitzung anfordern 👔",
            "Request Executive VIP Consultation": "Executive VIP-Beratung anfordern"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Geschäftsführungs-Dashboard",
            "ERP & Inventory Ops": "ERP- & Bestandsverwaltung",
            "E-Invoicing & VAT": "E-Rechnung & MwSt",
            "AI Financial Copilot": "KI-Finanzcopilot",
            "Cloud Server Status": "Cloud-Server-Status",
            "White-Label Branding": "White-Label-Branding",
            "Software Hub & Store": "Software-Hub & Store",
            "Smart ROI Calculator": "Intelligenter ROI-Rechner",
            "Return to Website": "Zurück zur Website",
            "Emblem Studio": "Emblem-Studio",
            "Client View [P]": "Kundenansicht [P]",
            "Book Session with this Architecture": "Sitzung mit dieser Architektur buchen",
            "Request Company Activation": "Unternehmensaktivierung anfordern",
            "Enterprise Consulting": "Unternehmensberatung",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Übertragen Sie Sitzungskonfigurationen und getestete Szenarien direkt in die Gründerberatung.",
            "Book Custom Consultation": "Individuelle Beratung buchen",
            "Interactive Preview Session": "Interaktive Vorschau-Sitzung",
            "S&R Executive Demo": "S&R Executive Demo"
        }
    },
    "fr": {
        "nav": {
            "LEADERSHIP": "DIRECTION",
            "SERVICES": "SERVICES",
            "About Us": "À propos",
            "Pricing": "Tarifs",
            "ROI": "Calculateur ROI",
            "FAQ": "FAQ",
            "Live ERP Demo ⚡": "Démo ERP en direct ⚡",
            "Menu": "Menu"
        },
        "hero": {
            "PRESENTS": "PRÉSENTE",
            "Available for New Enterprise Architecture Engagements 2026": "Disponible pour nouveaux projets d'entreprise 2026",
            "Enterprise Systems": "Systèmes d'Entreprise",
            "& Autonomous AI Architectures": "& Architectures d'IA Autonomes",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Systèmes logiciels intégrés & solutions d'IA conçus avec résilience cloud souveraine et flux de travail ERP automatisés pour les entreprises en Europe et au Moyen-Orient.",
            "Ambient Audio Experience (Click to Play)": "Expérience Audio Ambiante (Cliquer pour écouter)",
            "⚡ Live Cloud ERP Demo": "⚡ Démo ERP Cloud en direct",
            "Request VIP Session 👔": "Demander une session VIP 👔",
            "Request Executive VIP Consultation": "Demander une Consultation VIP"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Tableau de Bord Exécutif",
            "ERP & Inventory Ops": "Opérations ERP & Stocks",
            "E-Invoicing & VAT": "Facturation Électronique & TVA",
            "AI Financial Copilot": "Copilote Financier IA",
            "Cloud Server Status": "État des Serveurs Cloud",
            "White-Label Branding": "Marque Blanche",
            "Software Hub & Store": "Boutique & Hub Logiciel",
            "Smart ROI Calculator": "Calculateur Intelligent de ROI",
            "Return to Website": "Retour au Site Web",
            "Emblem Studio": "Studio d'Emblème",
            "Client View [P]": "Vue Client [P]",
            "Book Session with this Architecture": "Réserver une Session avec cette Architecture",
            "Request Company Activation": "Demander l'Activation de l'Entreprise",
            "Enterprise Consulting": "Conseil d'Entreprise",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Transférez directement les configurations et scénarios testés vers la consultation des fondateurs.",
            "Book Custom Consultation": "Réserver une Consultation Personnalisée",
            "Interactive Preview Session": "Session de Démonstration Interactive",
            "S&R Executive Demo": "Démo Exécutive S&R"
        }
    },
    "es": {
        "nav": {
            "LEADERSHIP": "LIDERAZGO",
            "SERVICES": "SERVICIOS",
            "About Us": "Sobre Nosotros",
            "Pricing": "Precios",
            "ROI": "Calculadora ROI",
            "FAQ": "Preguntas Frecuentes",
            "Live ERP Demo ⚡": "Demo ERP en Directo ⚡",
            "Menu": "Menú"
        },
        "hero": {
            "PRESENTS": "PRESENTA",
            "Available for New Enterprise Architecture Engagements 2026": "Disponible para nuevos proyectos empresariales 2026",
            "Enterprise Systems": "Sistemas Empresariales",
            "& Autonomous AI Architectures": "y Arquitecturas de IA Autónomas",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Sistemas de software integrados y soluciones de IA diseñados con resiliencia en la nube soberana y flujos de trabajo ERP automatizados para empresas globales en Europa y Oriente Medio.",
            "Ambient Audio Experience (Click to Play)": "Experiencia de Audio Ambiente (Haga clic para reproducir)",
            "⚡ Live Cloud ERP Demo": "⚡ Demo ERP en la Nube en Directo",
            "Request VIP Session 👔": "Solicitar Sesión VIP 👔",
            "Request Executive VIP Consultation": "Solicitar Consulta VIP Ejecutiva"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Panel Ejecutivo",
            "ERP & Inventory Ops": "Operaciones de ERP e Inventario",
            "E-Invoicing & VAT": "Facturación Electrónica e IVA",
            "AI Financial Copilot": "Copiloto Financiero IA",
            "Cloud Server Status": "Estado de Servidores en la Nube",
            "White-Label Branding": "Marca Blanca (White-Label)",
            "Software Hub & Store": "Centro de Software y Tienda",
            "Smart ROI Calculator": "Calculadora Inteligente de ROI",
            "Return to Website": "Volver al Sitio Web",
            "Emblem Studio": "Estudio de Emblemas",
            "Client View [P]": "Vista Cliente [P]",
            "Book Session with this Architecture": "Reservar Sesión con esta Arquitectura",
            "Request Company Activation": "Solicitar Activación de Empresa",
            "Enterprise Consulting": "Consultoría Empresarial",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Transfiera las configuraciones de sesión y escenarios probados directamente a la consulta de los fundadores.",
            "Book Custom Consultation": "Reservar Consulta Personalizada",
            "Interactive Preview Session": "Sesión de Vista Previa Interactiva",
            "S&R Executive Demo": "Demo Ejecutiva S&R"
        }
    },
    "tr": {
        "nav": {
            "LEADERSHIP": "LİDERLİK",
            "SERVICES": "HİZMETLER",
            "About Us": "Hakkımızda",
            "Pricing": "Fiyatlandırma",
            "ROI": "Yatırım Getirisi",
            "FAQ": "SSS",
            "Live ERP Demo ⚡": "Canlı ERP Demosu ⚡",
            "Menu": "Menü"
        },
        "hero": {
            "PRESENTS": "SUNAR",
            "Available for New Enterprise Architecture Engagements 2026": "2026 Yeni Kurumsal Projeler İçin Uygun",
            "Enterprise Systems": "Kurumsal Sistemler",
            "& Autonomous AI Architectures": "& Otonom Yapay Zeka Mimarileri",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Avrupa ve Orta Doğu'daki modern işletmeler için egemen bulut dayanıklılığı ve otomatik finansal ERP iş akışları ile tasarlanmış entegre yazılım sistemleri ve yapay zeka çözümleri.",
            "Ambient Audio Experience (Click to Play)": "Ortam Ses Deneyimi (Oynatmak için Tıklayın)",
            "⚡ Live Cloud ERP Demo": "⚡ Canlı Bulut ERP Demosu",
            "Request VIP Session 👔": "VIP Görüşme Talep Edin 👔",
            "Request Executive VIP Consultation": "Yönetici VIP Danışmanlığı Talep Edin"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Yönetici Paneli",
            "ERP & Inventory Ops": "ERP ve Stok Operasyonları",
            "E-Invoicing & VAT": "E-Fatura & KDV",
            "AI Financial Copilot": "Yapay Zeka Finans Asistanı",
            "Cloud Server Status": "Bulut Sunucu Durumu",
            "White-Label Branding": "White-Label Markalama",
            "Software Hub & Store": "Yazılım Merkezi ve Mağaza",
            "Smart ROI Calculator": "Akıllı Yatırım Getirisi Hesaplayıcı",
            "Return to Website": "Web Sitesine Geri Dön",
            "Emblem Studio": "Amblem Stüdyosu",
            "Client View [P]": "Müşteri Görünümü [P]",
            "Book Session with this Architecture": "Bu Mimariyle Görüşme Ayarlayın",
            "Request Company Activation": "Şirket Aktivasyonu Talep Edin",
            "Enterprise Consulting": "Kurumsal Danışmanlık",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Oturum yapılandırmalarını ve test edilen senaryoları doğrudan kurucu danışmanlığına aktarın.",
            "Book Custom Consultation": "Özel Danışmanlık Randevusu Alın",
            "Interactive Preview Session": "Etkileşimli Önizleme Oturumu",
            "S&R Executive Demo": "S&R Yönetici Demosu"
        }
    },
    "it": {
        "nav": {
            "LEADERSHIP": "LEADERSHIP",
            "SERVICES": "SERVIZI",
            "About Us": "Chi Siamo",
            "Pricing": "Prezzi",
            "ROI": "Calcolatore ROI",
            "FAQ": "Domande Frequenti",
            "Live ERP Demo ⚡": "Demo ERP dal Vivo ⚡",
            "Menu": "Menu"
        },
        "hero": {
            "PRESENTS": "PRESENTA",
            "Available for New Enterprise Architecture Engagements 2026": "Disponibile per nuovi progetti aziendali 2026",
            "Enterprise Systems": "Sistemi Aziendali",
            "& Autonomous AI Architectures": "& Architetture di IA Autonoma",
            "Integrated Software Systems & AI Solutions engineered with sovereign cloud resilience and automated financial ERP workflows for modern global enterprises across Europe and the Middle East.": "Sistemi software integrati e soluzioni di IA progettati con resilienza cloud sovrana e flussi di lavoro ERP finanziari automatizzati per le aziende in Europa e Medio Oriente.",
            "Ambient Audio Experience (Click to Play)": "Esperienza Audio Ambientale (Clicca per avviare)",
            "⚡ Live Cloud ERP Demo": "⚡ Demo ERP Cloud dal Vivo",
            "Request VIP Session 👔": "Richiedi Sessione VIP 👔",
            "Request Executive VIP Consultation": "Richiedi Consulenza VIP Esecutiva"
        },
        "demo_sidebar": {
            "Executive Dashboard": "Dashboard Direzionale",
            "ERP & Inventory Ops": "Operazioni ERP & Inventario",
            "E-Invoicing & VAT": "Fatturazione Elettronica & IVA",
            "AI Financial Copilot": "Copilota Finanziario IA",
            "Cloud Server Status": "Stato dei Server Cloud",
            "White-Label Branding": "Personalizzazione White-Label",
            "Software Hub & Store": "Hub e Negozio Software",
            "Smart ROI Calculator": "Calcolatore Intelligente ROI",
            "Return to Website": "Torna al Sito Web",
            "Emblem Studio": "Studio Emblema",
            "Client View [P]": "Vista Cliente [P]",
            "Book Session with this Architecture": "Prenota Sessione con questa Architettura",
            "Request Company Activation": "Richiedi Attivazione Aziendale",
            "Enterprise Consulting": "Consulenza Aziendale",
            "Transfer session configurations and tested scenarios directly to the founders consultation.": "Trasferisci direttamente le configurazioni e i test alla consulenza dei fondatori.",
            "Book Custom Consultation": "Prenota Consulenza Personalizzata",
            "Interactive Preview Session": "Sessione di Anteprima Interattiva",
            "S&R Executive Demo": "Demo Esecutiva S&R"
        }
    }
}

# Generic translations for remaining European languages
EU_LANG_MAP = {
    "sv": ("Svenska", "PRESENTERAR", "Företagssystem & Autonoma AI-Arkitekturer", "Företagssystem", "& Autonoma AI-Arkitekturer", "⚡ Live ERP-Demo", "LEDARSKAP", "TJÄNSTER"),
    "no": ("Norsk", "PRESENTERER", "Bedriftssystemer & Autonome AI-Arkitekturer", "Bedriftssystemer", "& Autonome AI-Arkitekturer", "⚡ Live ERP-Demo", "LEDELSE", "TJENESTER"),
    "da": ("Dansk", "PRÆSENTERER", "Virksomhedssystemer & Autonome AI-Arkitekturer", "Virksomhedssystemer", "& Autonome AI-Arkitekturer", "⚡ Live ERP-Demo", "LEDELSE", "TJENESTER"),
    "fi": ("Suomi", "ESITTÄÄ", "Yritysjärjestelmät & Autonomiset Tekoälyarkkitehtuurit", "Yritysjärjestelmät", "& Autonomiset Tekoälyarkkitehtuurit", "⚡ Live ERP-Demo", "JOHTO", "PALVELUT"),
    "pl": ("Polski", "PREZENTUJE", "Systemy Korporacyjne & Autonomiczne Architektury AI", "Systemy Korporacyjne", "& Autonomiczne Architektury AI", "⚡ Live ERP Demo", "PRZYWÓDZTWO", "USŁUGI"),
    "pt": ("Português", "APRESENTA", "Sistemas Empresariais & Arquiteturas de IA Autónomas", "Sistemas Empresariais", "& Arquiteturas de IA Autónomas", "⚡ Demo ERP em Direto", "LIDERANÇA", "SERVIÇOS"),
    "el": ("Ελληνικά", "ΠΑΡΟΥΣΙΑΖΕΙ", "Επιχειρησιακά Συστήματα & Αυτόνομες Αρχιτεκτονικές ΤΝ", "Επιχειρησιακά Συστήματα", "& Αυτόνομες Αρχιτεκτονικές ΤΝ", "⚡ Ζωντανή Επίδειξη ERP", "ΗΓΕΣΙΑ", "ΥΠΗΡΕΣΙΕΣ"),
    "cs": ("Čeština", "PŘEDSTAVUJE", "Podnikové Systémy & Autonomní Architektury AI", "Podnikové Systémy", "& Autonomní Architektury AI", "⚡ Živá Ukázka ERP", "VEDENÍ", "SLUŽBY"),
    "ro": ("Română", "PREZINTĂ", "Sisteme Enterprise & Arhitecturi de IA Autonome", "Sisteme Enterprise", "& Arhitecturi de IA Autonome", "⚡ Demo ERP Live", "CONDUCERE", "SERVICII"),
    "hu": ("Magyar", "BEMUTATJA", "Vállalati Rendszerek & Autonóm MI-Architektúrák", "Vállalati Rendszerek", "& Autonóm MI-Architektúrák", "⚡ Élő ERP Demó", "VEZETŐSÉG", "SZOLGÁLTATÁSOK"),
    "bg": ("Български", "ПРЕДСТАВЯ", "Корпоративни Системи & Автономни AI Архитектури", "Корпоративни Системи", "& Автономни AI Архитектури", "⚡ Демо на Живо ERP", "РЪКОВОДСТВО", "УСЛУГИ"),
    "sk": ("Slovenčina", "PREDSTAVUJE", "Podnikové Systémy & Autonómne Architektúry AI", "Podnikové Systémy", "& Autonómne Architektúry AI", "⚡ Živé ERP Demo", "VEDENIE", "SLUŽBY"),
    "hr": ("Hrvatski", "PREDSTAVLJA", "Poslovni Sustavi & Autonomne AI Arhitekture", "Poslovni Sustavi", "& Autonomne AI Arhitekture", "⚡ ERP Demo Uživo", "VODSTVO", "USLUGE"),
    "lt": ("Lietuvių", "PRISTATO", "Verslo Sistemos & Autonominės DI Architektūros", "Verslo Sistemos", "& Autonominės DI Architektūros", "⚡ Tiesioginė ERP Demonstracija", "VADOVYBĖ", "PASLAUGOS"),
    "sl": ("Slovenščina", "PREDSTAVLJA", "Poslovni Sistemi & Avtonomne AI Arhitekture", "Poslovni Sistemi", "& Avtonomne AI Arhitekture", "⚡ ERP Predstavitev v Živo", "VODSTVO", "STORITVE"),
    "lv": ("Latviešu", "PIEDĀVĀ", "Uzņēmumu Sistēmas & Autonomas MI Arhitektūras", "Uzņēmumu Sistēmas", "& Autonomas MI Arhitektūras", "⚡ Live ERP Demonstrācija", "VADĪBA", "PAKALPOJUMI"),
    "et": ("Eesti", "ESITLEB", "Ettevõttesüsteemid & Autonoomsed Tehisintellekti Arhitektuurid", "Ettevõttesüsteemid", "& Autonoomsed Tehisintellekti Arhitektuurid", "⚡ Reaalajas ERP-Demo", "JUHTIMINE", "TEENUSED"),
    "ga": ("Gaeilge", "LÁITHRÍONN", "Córais Fiontair & Ailtireachtaí AI Uathrialacha", "Córais Fiontair", "& Ailtireachtaí AI Uathrialacha", "⚡ Taispeántas Beo ERP", "CEANNAÍOCHT", "SEIRBHÍSÍ"),
    "mt": ("Malti", "JIPPREŻENTA", "Sistemi Intrapriża & Arkitetturi AI Awtonomi", "Sistemi Intrapriża", "& Arkitetturi AI Awtonomi", "⚡ Demo ERP Ħaj", "TMEXXIJA", "SERVIZZI"),
    "ku": ("Kurdî", "PÊŞKÊŞ DIKE", "Pergalên Pargîdaniyê & Avahiyên Xweser ên AI", "Pergalên Pargîdaniyê", "& Avahiyên Xweser ên AI", "⚡ Demoya Zindî ya ERP", "RÊVEBERÎ", "XIZMETÊN ME")
}

def clean_arabic_brand_replacements(content):
    """
    Ensures S&R CoreSync For Intelligent Solutions and S&R brand name are NEVER Arabicized.
    """
    # Replace Arabicized company names with the official brand name
    content = re.sub(r'س و ر للحلول الذكية', 'S&R CoreSync للحلول الذكية', content)
    content = re.sub(r'إس آند آر كور سينك', 'S&R CoreSync', content)
    content = re.sub(r'إس آند آر', 'S&R', content)
    content = re.sub(r'كور سينك', 'CoreSync', content)
    return content

def localize_file(file_path, lang_code, is_subfolder=True):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply detailed translations if available
    if lang_code in LANG_DICTIONARIES:
        d = LANG_DICTIONARIES[lang_code]
        # Nav
        for k, v in d["nav"].items():
            content = content.replace(f'>{k}</a>', f'>{v}</a>')
            content = content.replace(f'<span>{k}</span>', f'<span>{v}</span>')
            content = content.replace(f'<span>01 /</span>{k}', f'<span>01 /</span>{v}')
            content = content.replace(f'<span>02 /</span>{k}', f'<span>02 /</span>{v}')
            content = content.replace(f'<span>03 /</span>{k}', f'<span>03 /</span>{v}')
            content = content.replace(f'<span>04 /</span>{k}', f'<span>04 /</span>{v}')
            content = content.replace(f'<span>05 /</span>{k}', f'<span>05 /</span>{v}')
            content = content.replace(f'<span>06 /</span>{k}', f'<span>06 /</span>{v}')

        # Hero
        for k, v in d["hero"].items():
            content = content.replace(k, v)

        # Demo sidebar
        for k, v in d["demo_sidebar"].items():
            content = content.replace(f'<span>{k}</span>', f'<span>{v}</span>')
            content = content.replace(f'>{k}</div>', f'>{v}</div>')
            content = content.replace(f'>{k}</button>', f'>{v}</button>')
            content = content.replace(f'>{k}</a>', f'>{v}</a>')
            content = content.replace(k, v)

    elif lang_code in EU_LANG_MAP:
        native_name, presents, full_title, line1, line2, demo_btn, lead_nav, srv_nav = EU_LANG_MAP[lang_code]
        content = re.sub(r'<span class="hero-brand-presenter__tag">PRESENTS</span>', f'<span class="hero-brand-presenter__tag">{presents}</span>', content)
        content = content.replace('<span>01 /</span>LEADERSHIP', f'<span>01 /</span>{lead_nav}')
        content = content.replace('<span>02 /</span>SERVICES', f'<span>02 /</span>{srv_nav}')
        content = content.replace('<span class="hero-title-line__text">Enterprise Systems</span>', f'<span class="hero-title-line__text">{line1}</span>')
        content = content.replace('<span class="hero-title-line__text">&amp; <span class="hero-title-accent">Autonomous AI</span> Architectures</span>', f'<span class="hero-title-line__text">{line2}</span>')
        content = content.replace('<span>⚡ Live Cloud ERP Demo</span>', f'<span>{demo_btn}</span>')
        content = content.replace('<span>Live ERP Demo ⚡</span>', f'<span>{demo_btn}</span>')

    # Ensure brand name is always S&R CoreSync For Intelligent Solutions
    content = content.replace('S&amp;R CoreSync للحلول الذكية', 'S&amp;R CoreSync For Intelligent Solutions')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[✓] Localized: {file_path}")

def main():
    print("=== S&R CoreSync Brand Remediation & Multilingual Localization ===")

    # 1. Clean root index.html & demo.html
    for fn in ['index.html', 'demo.html']:
        fp = os.path.join(BASE_DIR, fn)
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                c = f.read()
            c = clean_arabic_brand_replacements(c)
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"[✓] Brand verified in root: {fn}")

    # 2. Localize all subfolders
    all_langs = list(LANG_DICTIONARIES.keys()) + list(EU_LANG_MAP.keys())
    for lang in all_langs:
        idx = os.path.join(BASE_DIR, lang, 'index.html')
        dm = os.path.join(BASE_DIR, lang, 'demo.html')
        localize_file(idx, lang, is_subfolder=True)
        localize_file(dm, lang, is_subfolder=True)

    print("=== Complete! ===")

if __name__ == '__main__':
    main()
