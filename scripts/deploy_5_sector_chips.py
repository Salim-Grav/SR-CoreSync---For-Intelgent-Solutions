# -*- coding: utf-8 -*-
"""
Deploy 5 Sector-Specialized Executive Quick Chips across all 29 index pages:
1. FinTech & Payments (Salim)
2. Cloud ERP & Taxation (Raed)
3. Autonomous AI Agents (Salim)
4. Logistics & Supply Chain (Raed)
5. E-Commerce Platform (Salim)
"""
import io, os, re, json

CHIPS_5_DATA = {
    'ar': {
        'label': 'قطاعات متخصصة:',
        'chips': [
            ('💳 حلول FinTech وبوابات دفع', 'منظومة FinTech وبوابات دفع إلكتروني أوروبية متوافقة مع PSD2 و iDEAL'),
            ('🏢 نظام CoreSync ERP والضرائب', 'نظام CoreSync ERP لإدارة المحاسبة والضرائب الأوروبية BTW وسلاسل الإمداد'),
            ('🤖 وكلاء الذكاء الاصطناعي', 'منظومة أتمتة بالذكاء الاصطناعي ووكلاء RAG لدعم العمليات والمبيعات'),
            ('📦 لوجستيات وسلاسل إمداد', 'إدارة سلاسل الإمداد والخدمات اللوجستية والمخازن الذكية والتوزيع الأوروبي'),
            ('🛒 متجر إلكتروني بهولندا', 'متجر إلكتروني PWA بهولندا بنظام دفع iDEAL وربط محاسبي ومخازن آلي')
        ]
    },
    'ckb': {
        'label': 'کەرتە تایبەتمەندەکان:',
        'chips': [
            ('💳 فینتێک و پارەدانی دیجیتاڵی', 'سیستەمی FinTech و دەروازەکانی پارەدانی ئەوروپی بەپێی PSD2 و iDEAL'),
            ('🏢 سیستەمی CoreSync ERP و باج', 'سیستەمی CoreSync ERP بۆ بەڕێوەبردنی ژمێریاری و باجی BTW و کۆگاکان'),
            ('🤖 بریکارەکانی AI ی خاوەن بڕیار', 'سیستەمی ئۆتۆماتیک بە ژیری دەستکرد و بریکاری RAG بۆ فرۆشتن و پشتگیری'),
            ('📦 لۆجستی و گەیاندن', 'بەڕێوەبردنی زنجیرەی دابینکردن و لۆجستی و کۆگای زیرەک'),
            ('🛒 فرۆشگای ئۆنلاین', 'فرۆشگای ئۆنلاین PWA لە هۆڵەندا بە پارەدانی iDEAL و بەستنەوەی ژمێریاری')
        ]
    },
    'en': {
        'label': 'Executive Sectors:',
        'chips': [
            ('💳 FinTech & Payment Rails', 'European FinTech payment rail architecture compliant with PSD2 and iDEAL'),
            ('🏢 CoreSync ERP & Tax Compliance', 'CoreSync Cloud ERP suite for corporate accounting, Dutch BTW compliance, and operations'),
            ('🤖 Autonomous AI Agents', 'Autonomous AI agent workflows and sovereign local RAG knowledgebase for operations'),
            ('📦 Logistics & Supply Chain', 'Smart European supply chain orchestration, multi-warehouse ERP, and distribution'),
            ('🛒 E-Commerce Webshop', 'High-conversion PWA e-commerce platform with automated iDEAL checkout and ERP sync')
        ]
    },
    'nl': {
        'label': 'Gespecialiseerde sectoren:',
        'chips': [
            ('💳 FinTech & iDEAL Betaalsystemen', 'Europese FinTech-architectuur en iDEAL-betaalkoppelingen conform PSD2'),
            ('🏢 CoreSync ERP & BTW-administratie', 'CoreSync Cloud ERP voor financiële administratie, BTW-aangifte en supply chain'),
            ('🤖 Autonome AI-agents', 'Autonome AI-agents en lokale RAG-kennisbank voor operationele automatisering'),
            ('📦 Logistiek & Supply Chain', 'Slim voorraadbeheer, Europese logistieke distributie en ERP-koppelingen'),
            ('🛒 E-commerce Webshop Nederland', 'PWA webshop met iDEAL-integratie, geautomatiseerde boekhouding en voorraadbeheer')
        ]
    },
    'de': {
        'label': 'Fachsektoren:',
        'chips': [
            ('💳 FinTech & Zahlungssysteme', 'Europäische FinTech-Zahlungsarchitektur konform mit PSD2 und iDEAL/Stripe'),
            ('🏢 CoreSync ERP & MwSt-Compliance', 'CoreSync Cloud ERP für Finanzbuchhaltung, europäische MwSt und Betriebsführung'),
            ('🤖 Autonome KI-Agenten', 'Autonome KI-Agenten und lokale RAG-Wissensdatenbank für Geschäftsautomatisierung'),
            ('📦 Logistik & Lieferketten', 'Intelligente europäische Lieferkettensteuerung und automatisierte Lagerverwaltung'),
            ('🛒 E-Commerce Plattform', 'Hochkonvertierender PWA-Onlineshop mit Zahlungsanbindung und ERP-Synchronisation')
        ]
    },
    'fr': {
        'label': 'Secteurs d\'expertise :',
        'chips': [
            ('💳 FinTech & Systèmes de Paiement', 'Architecture de paiement FinTech européenne conforme PSD2 et passerelles Stripe/iDEAL'),
            ('🏢 ERP CoreSync & Fiscalité TVA', 'Suite ERP Cloud CoreSync pour la comptabilité, la conformité TVA et la logistique'),
            ('🤖 Agents IA Autonomes', 'Flux d\'agents IA autonomes et base de connaissances RAG pour l\'automatisation'),
            ('📦 Logistique & Chaîne d\'approvisionnement', 'Gestion intelligente des stocks européens et orchestration logistique intégrée'),
            ('🛒 Boutique E-Commerce PWA', 'Plateforme e-commerce PWA à haute conversion avec synchronisation ERP')
        ]
    }
}

# For all other languages, generate tailored English-based localized sector chips
for lang in ['es', 'it', 'pt', 'tr', 'el', 'pl', 'sv', 'da', 'no', 'fi', 'cs', 'sk', 'ro', 'bg', 'hu', 'hr', 'sl', 'et', 'lv', 'lt', 'mt', 'ga', 'ku']:
    CHIPS_5_DATA[lang] = CHIPS_5_DATA['en']

def make_chips_5_html(lang):
    cd = CHIPS_5_DATA.get(lang, CHIPS_5_DATA['en'])
    chips_html = f'''                                        <!-- رقاقات الأفكار والقطاعات التخصصية (Executive Sector Chips) -->
                                        <div class="hero-ai-chips-wrap" aria-label="{cd['label']}">
                                            <span class="hero-ai-chips-label">{cd['label']}</span>'''
    for title, prompt in cd['chips']:
        args_json = json.dumps([prompt], ensure_ascii=False)
        chips_html += f'''
                                            <button type="button" class="hero-ai-chip" data-sr-call="fillHeroPromptSample" data-sr-args='{args_json}'>
                                                <span>{title}</span>
                                            </button>'''
    chips_html += '\n                                        </div>'
    return chips_html

def replace_chips_in_file(filepath, lang):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # Look for existing .hero-ai-chips-wrap and replace it
    m = re.search(r'([ \t]*<!-- [^\n]*chips[^\n]*-->\s*)?<div class="hero-ai-chips-wrap".*?</div>', c, re.DOTALL | re.IGNORECASE)
    if m:
        new_html = make_chips_5_html(lang)
        c = c[:m.start()] + new_html + c[m.end():]
        with io.open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(c)
        print(f"[{lang}] Updated with 5 sector chips in {filepath}")
    else:
        # If not present, insert after </form> in hero-ai-idea-bar
        m2 = re.search(r'(<div class="hero-ai-idea-bar"[^>]*>.*?)(</form>)', c, re.DOTALL)
        if m2:
            new_html = make_chips_5_html(lang)
            insert_pos = m2.end()
            c = c[:insert_pos] + "\n" + new_html + c[insert_pos:]
            with io.open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(c)
            print(f"[{lang}] Inserted 5 sector chips in {filepath}")
        else:
            print(f"[{lang}] ERROR: hero-ai-idea-bar not found in {filepath}!")

def main():
    print("--- Updating 5 Sector Chips across all 29 pages ---")
    replace_chips_in_file('index.html', 'ar')
    for lang in sorted(CHIPS_5_DATA.keys()):
        if lang == 'ar':
            continue
        p = os.path.join(lang, 'index.html')
        if os.path.exists(p):
            replace_chips_in_file(p, lang)

if __name__ == '__main__':
    main()

