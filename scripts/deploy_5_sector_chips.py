# -*- coding: utf-8 -*-
"""
Deploy 5 Sector-Specialized Executive Quick Chips across all 29 index pages:
1. FinTech & Payments (Salim)
2. Cloud ERP & Taxation (Raed)
3. Autonomous AI Agents (Salim)
4. Logistics & Supply Chain (Raed)
5. E-Commerce Platform (Salim)
"""
import argparse, io, os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO_LOCALES_PATH = os.path.join(ROOT, 'scripts', 'portal_hero_locales.json')
PROMPT_LOCALES_PATH = os.path.join(ROOT, 'scripts', 'portal_hero_prompts_locales.json')
CHIP_KEYS = (
    'FinTech & Payment Rails',
    'CoreSync ERP & Tax Compliance',
    'Autonomous AI Agents',
    'Logistics & Supply Chain',
    'E-Commerce Webshop',
)

with io.open(HERO_LOCALES_PATH, 'r', encoding='utf-8') as f:
    HERO_LOCALES = json.load(f)
with io.open(PROMPT_LOCALES_PATH, 'r', encoding='utf-8') as f:
    PROMPT_LOCALES = json.load(f)

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

def make_chips_5_html(lang):
    if lang not in HERO_LOCALES or lang not in PROMPT_LOCALES:
        raise ValueError(f'Missing sector-chip translations for {lang}')
    cd = HERO_LOCALES[lang]
    prompts = PROMPT_LOCALES[lang]
    if len(prompts) != len(CHIP_KEYS):
        raise ValueError(f'Expected {len(CHIP_KEYS)} prompts for {lang}')
    chips_html = f'''                                        <!-- رقاقات الأفكار والقطاعات التخصصية (Executive Sector Chips) -->
                                        <div class="hero-ai-chips-wrap" aria-label="{cd['Executive Sectors:']}">
                                            <span class="hero-ai-chips-label">{cd['Executive Sectors:']}</span>'''
    for key, prompt in zip(CHIP_KEYS, prompts):
        title = cd[key]
        args_json = json.dumps([prompt], ensure_ascii=False)
        chips_html += f'''
                                            <button type="button" class="hero-ai-chip" data-sr-call="fillHeroPromptSample" data-sr-args='{args_json}'>
                                                <span>{title}</span>
                                            </button>'''
    chips_html += '\n                                        </div>'
    return chips_html

def replace_chips_in_file(filepath, lang, apply):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    m = re.search(r'([ \t]*<!-- [^\n]*chips[^\n]*-->\s*)?<div class="hero-ai-chips-wrap".*?</div>', c, re.DOTALL | re.IGNORECASE)
    if not m:
        raise ValueError(f'[{lang}] hero-ai-chips-wrap not found in {filepath}')
    block = m.group(0)
    locale = HERO_LOCALES[lang]
    prompts = PROMPT_LOCALES[lang]
    expected = [locale['Executive Sectors:'], *[locale[key] for key in CHIP_KEYS], *prompts]
    if all(value in block for value in expected) and len(re.findall(r'class="hero-ai-chip"', block)) == 5:
        print(f"[{lang}] Sector chips are localized in {filepath}")
        return False
    if not apply:
        print(f"[{lang}] Sector chip translations need updating in {filepath}")
        return True

    updated = c[:m.start()] + make_chips_5_html(lang) + c[m.end():]
    with io.open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(updated)
    print(f"[{lang}] Updated localized sector chips in {filepath}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Check or update localized sector chips.')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='check without writing files')
    mode.add_argument('--apply', action='store_true', help='apply localized sector-chip data')
    args = parser.parse_args()
    apply = args.apply

    print("--- Checking localized sector chips across all 29 pages ---")
    issues = 0
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    from deploy_sovereign_multilingual import LANGUAGES
    languages = [language['code'] for language in LANGUAGES if language['code'] != 'ar']
    if set(HERO_LOCALES) != set(languages) or set(PROMPT_LOCALES) != set(languages) | {'ar'}:
        raise ValueError('Sector-chip locale files must cover every non-Arabic language.')
    for lang in sorted(languages):
        p = os.path.join(ROOT, lang, 'index.html')
        if not os.path.isfile(p):
            raise ValueError(f'Missing landing page: {p}')
        issues += replace_chips_in_file(p, lang, apply)
    if issues and not apply:
        print(f'{issues} page(s) need localized sector-chip updates.')
        return 1
    print('Sector-chip localization check passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
