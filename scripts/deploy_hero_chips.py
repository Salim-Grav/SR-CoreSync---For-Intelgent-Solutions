# -*- coding: utf-8 -*-
"""
Deploy Royal Hero AI Idea Prompt Bar & Voice Badge with Interactive Quick Chips across all 29 index pages:
1. Root index.html (Arabic master)
2. All 28 localized index.html files
"""
import io, os, re

CHIPS_DATA = {
    'ar': {
        'label': 'أمثلة سريعة:',
        'chips': [
            ('🛒 متجر إلكتروني متكامل', 'متجر إلكتروني بنظام دفع هولندي iDEAL وإدارة مخازن'),
            ('🏢 نظام CoreSync ERP', 'نظام CoreSync ERP متكامل لإدارة الحسابات والضرائب والمستودعات'),
            ('🤖 وكلاء الذكاء الاصطناعي', 'منظومة أتمتة بالذكاء الاصطناعي ووكلاء RAG لدعم العملاء والمبيعات')
        ]
    },
    'ckb': {
        'label': 'نموونەی خێرا:',
        'chips': [
            ('🛒 فرۆشگای ئۆنلاین', 'فرۆشگای ئۆنلاین بە سیستەمی پارەدانی iDEAL و بەڕێوەبردنی کۆگا'),
            ('🏢 سیستەمی CoreSync ERP', 'سیستەمی CoreSync ERP بۆ بەڕێوەبردنی ژمێریاری و باج و کۆگاکان'),
            ('🤖 بریکارەکانی AI', 'سیستەمی ئۆتۆماتیک بە زیرەکی دەستکرد و بریکاری RAG بۆ پشتگیری کڕیاران')
        ]
    },
    'ku': {
        'label': 'Nimûneyên lez:',
        'chips': [
            ('🛒 Dikana Serhêl', 'Dikana serhêl bi pergala dravdana iDEAL û rêveberiya embarkirinê'),
            ('🏢 Pergala CoreSync ERP', 'Pergala CoreSync ERP ji bo hesabdarî, bac û rêveberiya embaran'),
            ('🤖 Wekîlên AI yên Xweser', 'Pergala otomasyona pargîdaniyê bi zîrekiya sûnî û wekîlên RAG')
        ]
    },
    'en': {
        'label': 'Quick Samples:',
        'chips': [
            ('🛒 E-Commerce Platform', 'E-commerce webshop with iDEAL & Stripe payments and cloud inventory'),
            ('🏢 CoreSync ERP Suite', 'Integrated CoreSync Cloud ERP for accounting, VAT compliance, and multi-warehouse'),
            ('🤖 Autonomous AI Agents', 'Autonomous AI agent workflows and local RAG knowledgebase for enterprise automation')
        ]
    },
    'nl': {
        'label': 'Snelle voorbeelden:',
        'chips': [
            ('🛒 E-commerce Webshop', 'E-commerce webshop met iDEAL en Stripe betalingen en voorraadbeheer'),
            ('🏢 CoreSync ERP Systeem', 'Geïntegreerd CoreSync Cloud ERP voor boekhouding, BTW-aangifte en voorraadbeheer'),
            ('🤖 Autonome AI-agents', 'Autonome AI-agents en lokale RAG-kennisbank voor bedrijfsautomatisering')
        ]
    },
    'de': {
        'label': 'Schnellbeispiele:',
        'chips': [
            ('🛒 E-Commerce Plattform', 'E-Commerce Onlineshop mit iDEAL Zahlungen und Cloud-Warenwirtschaft'),
            ('🏢 CoreSync ERP System', 'CoreSync Cloud ERP für Finanzbuchhaltung, MwSt-Compliance und Lagerverwaltung'),
            ('🤖 Autonome KI-Agenten', 'Autonome KI-Agenten und lokale RAG-Wissensdatenbank für Unternehmensautomatisierung')
        ]
    },
    'fr': {
        'label': 'Exemples rapides :',
        'chips': [
            ('🛒 Boutique E-commerce', 'Plateforme e-commerce avec passerelles de paiement et gestion des stocks'),
            ('🏢 Système CoreSync ERP', 'ERP Cloud CoreSync pour la comptabilité, TVA européenne et gestion logistique'),
            ('🤖 Agents IA Autonomes', 'Agents IA autonomes et base de connaissances RAG pour l\'automatisation d\'entreprise')
        ]
    },
    'es': {
        'label': 'Ejemplos rápidos:',
        'chips': [
            ('🛒 Tienda E-Commerce', 'Tienda online con pasarelas de pago y gestión de inventario en la nube'),
            ('🏢 Sistema CoreSync ERP', 'CoreSync Cloud ERP para contabilidad, cumplimiento de IVA y almacenes'),
            ('🤖 Agentes IA Autónomos', 'Flujos de agentes de IA y base de conocimiento RAG para automatización empresarial')
        ]
    },
    'it': {
        'label': 'Esempi rapidi:',
        'chips': [
            ('🛒 Piattaforma E-commerce', 'Negozio e-commerce con gateway di pagamento e gestione magazzino cloud'),
            ('🏢 Sistema CoreSync ERP', 'CoreSync Cloud ERP per contabilità, conformità IVA e logistica aziendale'),
            ('🤖 Agenti IA Autonomi', 'Agenti IA autonomi e knowledge base RAG locale per automazione aziendale')
        ]
    },
    'pt': {
        'label': 'Exemplos rápidos:',
        'chips': [
            ('🛒 Loja E-Commerce', 'Loja virtual com gateways de pagamento e gestão de stock na nuvem'),
            ('🏢 Sistema CoreSync ERP', 'CoreSync Cloud ERP para contabilidade, conformidade de IVA e armazéns'),
            ('🤖 Agentes de IA Autónomos', 'Fluxos de trabalho de agentes de IA e base de conhecimento RAG empresarial')
        ]
    },
    'tr': {
        'label': 'Hızlı Örnekler:',
        'chips': [
            ('🛒 E-Ticaret Platformu', 'Ödeme entegrasyonlu ve bulut stok yönetimli e-ticaret mağazası'),
            ('🏢 CoreSync ERP Sistemi', 'Muhasebe, KDV uyumu ve depo yönetimi için CoreSync Cloud ERP'),
            ('🤖 Otonom Yapay Zeka', 'Kurumsal otomasyon için otonom yapay zeka ajanları ve yerel RAG veritabanı')
        ]
    },
    'el': {
        'label': 'Γρήγορα παραδείγματα:',
        'chips': [
            ('🛒 Πλατφόρμα E-Shop', 'Ηλεκτρονικό κατάστημα με πύλες πληρωμών και διαχείριση αποθήκης cloud'),
            ('🏢 Σύστημα CoreSync ERP', 'CoreSync Cloud ERP για λογιστική, συμμόρφωση ΦΠΑ και διαχείριση αποθεμάτων'),
            ('🤖 Αυτόνομοι Πράκτορες AI', 'Ροές εργασίας πρακτόρων AI και τοπική βάση γνώσεων RAG για επιχειρήσεις')
        ]
    },
    'pl': {
        'label': 'Szybkie przykłady:',
        'chips': [
            ('🛒 Sklep E-Commerce', 'Sklep internetowy z bramkami płatności i zarządzaniem magazynem w chmurze'),
            ('🏢 System CoreSync ERP', 'CoreSync Cloud ERP do księgowości, podatku VAT i zarządzania magazynem'),
            ('🤖 Autonomiczni Agenci AI', 'Autonomiczni agenci AI i lokalna baza wiedzy RAG do automatyzacji firmy')
        ]
    },
    'sv': {
        'label': 'Snabba exempel:',
        'chips': [
            ('🛒 E-handelsplattform', 'Webbutik med betalningslösningar och molnlagerhantering'),
            ('🏢 CoreSync ERP-system', 'CoreSync Cloud ERP för bokföring, momshantering och lagerkontroll'),
            ('🤖 Autonoma AI-agenter', 'Autonoma AI-agenter och lokal RAG-kunskapsbas för företagsautomatisering')
        ]
    },
    'da': {
        'label': 'Hurtige eksempler:',
        'chips': [
            ('🛒 E-handelsplatform', 'Webshop med betalingsgateways og cloud-lagerstyring'),
            ('🏢 CoreSync ERP-system', 'CoreSync Cloud ERP til regnskab, momsoverholdelse og lagerstyring'),
            ('🤖 Autonome AI-agenter', 'Autonome AI-agenter og lokal RAG-vidensbase til virksomhedsautomatisering')
        ]
    },
    'no': {
        'label': 'Hurtige eksempler:',
        'chips': [
            ('🛒 E-handelsplattform', 'Nettbutikk med betalingsløsninger og skylagerstyring'),
            ('🏢 CoreSync ERP-system', 'CoreSync Cloud ERP for regnskap, mva-etterlevelse og lagerstyring'),
            ('🤖 Autonome AI-agenter', 'Autonome AI-agenter og lokal RAG-kunnskapsbase for bedriftsautomatisering')
        ]
    },
    'fi': {
        'label': 'Nopeat esimerkit:',
        'chips': [
            ('🛒 Verkkokauppa-alusta', 'Verkkokauppa maksuyhteyksillä ja pilvivarastonhallinnalla'),
            ('🏢 CoreSync ERP -järjestelmä', 'CoreSync Cloud ERP kirjanpitoon, ALV-vaatimuksiin ja varastonhallintaan'),
            ('🤖 Autonomiset AI-agentit', 'Autonomiset AI-agentit ja paikallinen RAG-tietokanta yritysautomaatioon')
        ]
    },
    'cs': {
        'label': 'Rychlé příklady:',
        'chips': [
            ('🛒 E-Commerce Platforma', 'Internetový obchod s platebními branami a cloudovou správou skladů'),
            ('🏢 Systém CoreSync ERP', 'CoreSync Cloud ERP pro účetnictví, DPH a správu skladového hospodářství'),
            ('🤖 Autonomní AI Agenti', 'Autonomní AI agenti a lokální znalostní báze RAG pro podnikovou automatizaci')
        ]
    },
    'sk': {
        'label': 'Rýchle príklady:',
        'chips': [
            ('🛒 E-Commerce Platforma', 'Internetový obchod s platobnými bránami a cloudovou správou skladov'),
            ('🏢 Systém CoreSync ERP', 'CoreSync Cloud ERP pre účtovníctvo, DPH a riadenie skladov'),
            ('🤖 Autonómni AI Agenti', 'Autonómni AI agenti a lokálna znalostná báza RAG pre podnikovú automatizáciu')
        ]
    },
    'ro': {
        'label': 'Exemple rapide:',
        'chips': [
            ('🛒 Platformă E-Commerce', 'Magazin online cu porți de plată și gestiune stocuri în cloud'),
            ('🏢 Sistem CoreSync ERP', 'CoreSync Cloud ERP pentru contabilitate, conformitate TVA și depozite'),
            ('🤖 Agenți IA Autonomi', 'Fluxuri de lucru cu agenți IA și bază de cunoștințe RAG pentru companii')
        ]
    },
    'bg': {
        'label': 'Бързи примери:',
        'chips': [
            ('🛒 E-Commerce Платформа', 'Онлайн магазин с разплащателни шлюзове и складово управление в облак'),
            ('🏢 CoreSync ERP Система', 'CoreSync Cloud ERP за счетоводство, ДДС съответствие и складове'),
            ('🤖 Автономни AI Агенти', 'Автономни AI агенти и локална RAG база знания за бизнес автоматизация')
        ]
    },
    'hu': {
        'label': 'Gyors példák:',
        'chips': [
            ('🛒 E-Kereskedelmi Platform', 'Webáruház fizetési átjárókkal és felhőalapú raktárkezeléssel'),
            ('🏢 CoreSync ERP Rendszer', 'CoreSync Cloud ERP könyveléshez, ÁFA-megfelelőséghez és raktárakhoz'),
            ('🤖 Autonóm MI Ügynökök', 'Autonóm MI ügynökök és helyi RAG tudásbázis vállalati automatizáláshoz')
        ]
    },
    'hr': {
        'label': 'Brzi primjeri:',
        'chips': [
            ('🛒 E-Commerce Platforma', 'Web trgovina s platnim pristupnicima i upravljanjem zalihama u oblaku'),
            ('🏢 Sustav CoreSync ERP', 'CoreSync Cloud ERP za računovodstvo, usklađenost s PDV-om i skladišta'),
            ('🤖 Autonomni AI Agenti', 'Autonomni AI agenti i lokalna RAG baza znanja za automatizaciju poduzeća')
        ]
    },
    'sl': {
        'label': 'Hitri primeri:',
        'chips': [
            ('🛒 E-Trgovinska Platforma', 'Spletna trgovina s plačilnimi prehodi in upravljanjem zalog v oblaku'),
            ('🏢 Sistem CoreSync ERP', 'CoreSync Cloud ERP za računovodstvo, DDV skladnost in skladišča'),
            ('🤖 Avtonomni AI Agenti', 'Avtonomni AI agenti in lokalna baza znanja RAG za avtomatizacijo podjetij')
        ]
    },
    'et': {
        'label': 'Kiired näited:',
        'chips': [
            ('🛒 E-kaubanduse platvorm', 'Veebipood makselahenduste ja pilvepõhise laohaldusega'),
            ('🏢 CoreSync ERP süsteem', 'CoreSync Cloud ERP raamatupidamiseks, käibemaksuks ja laohalduseks'),
            ('🤖 Autonoomsed AI-agendid', 'Autonoomsed AI-agendid ja kohalik RAG teadmusbaas ettevõtte automatiseerimiseks')
        ]
    },
    'lv': {
        'label': 'Ātrie piemēri:',
        'chips': [
            ('🛒 E-komercijas platforma', 'Interneta veikals ar maksājumu vārtejām un mākoņa noliktavas pārvaldību'),
            ('🏢 CoreSync ERP sistēma', 'CoreSync Cloud ERP grāmatvedībai, PVN atbilstībai un noliktavām'),
            ('🤖 Autonomie AI aģenti', 'Autonomie AI aģenti un vietējā RAG zināšanu bāze uzņēmumu automatizācijai')
        ]
    },
    'lt': {
        'label': 'Greiti pavyzdžiai:',
        'chips': [
            ('🛒 E-prekybos platforma', 'El. parduotuvė su mokėjimo šliuzais ir debesijos atsargų valdymu'),
            ('🏢 CoreSync ERP sistema', 'CoreSync Cloud ERP apskaitai, PVM atitikčiai ir sandėliams'),
            ('🤖 Autonominiai AI agentai', 'Autonominiai AI agentai ir vietinė RAG žinių bazė verslo automatizavimui')
        ]
    },
    'mt': {
        'label': 'Eżempji rapidi:',
        'chips': [
            ('🛒 Pjattaforma E-Commerce', 'Ħanut online b\'gateways ta\' pagament u ġestjoni tal-inventarju fil-cloud'),
            ('🏢 Sistema CoreSync ERP', 'CoreSync Cloud ERP għall-kontabilità, konformità tal-VAT u mħażen'),
            ('🤖 Aġenti AI Awtonomi', 'Workflows ta\' aġenti AI u bażi ta\' għarfien RAG għall-awtomatizzazzjoni')
        ]
    },
    'ga': {
        'label': 'Samplaí gasta:',
        'chips': [
            ('🛒 Ardán Ríomhthráchtála', 'Siopa ríomhthráchtála le geataí íocaíochta agus bainistíocht fardail néil'),
            ('🏢 Córas CoreSync ERP', 'CoreSync Cloud ERP do chuntasaíocht, comhlíonadh CBL agus stórais'),
            ('🤖 Gníomhairí AI Uathrialacha', 'Sreafaí oibre gníomhairí AI agus bonn eolais RAG d\'uathoibriú fiontair')
        ]
    }
}

import json

def make_chips_html(lang):
    cd = CHIPS_DATA.get(lang, CHIPS_DATA['en'])
    chips_html = f'''                                        <!-- رقاقات الأفكار السريعة الجاهزة (Quick Prompt Chips) -->
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

def update_page_with_chips(filepath, lang):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    if 'hero-ai-chips-wrap' in c:
        print(f"[{lang}] hero-ai-chips-wrap already present")
        return

    # Find the closing </form> inside <div class="hero-ai-idea-bar" id="heroAiIdeaBar">
    m = re.search(r'(<div class="hero-ai-idea-bar"[^>]*>.*?)(</form>)', c, re.DOTALL)
    if m:
        chips_str = make_chips_html(lang)
        insert_pos = m.end()
        c = c[:insert_pos] + "\n" + chips_str + c[insert_pos:]
        with io.open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(c)
        print(f"[{lang}] Added chips to {filepath}")
    else:
        print(f"[{lang}] Could not find hero-ai-idea-bar form in {filepath}!")

def main():
    print("--- Adding Quick Chips to root index.html ---")
    update_page_with_chips('index.html', 'ar')

    for lang in sorted(CHIPS_DATA.keys()):
        if lang == 'ar':
            continue
        p = os.path.join(lang, 'index.html')
        if os.path.exists(p):
            update_page_with_chips(p, lang)

if __name__ == '__main__':
    main()
