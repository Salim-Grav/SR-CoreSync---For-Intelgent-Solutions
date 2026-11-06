#!/usr/bin/env python3
"""
deploy_multilingual_currencies.py
Deploys dynamic multi-currency converter (EUR, USD, GBP, SAR, AED) across all 28 multilingual portals:
1. Adds data-eur-price attributes to all pricing tier amounts.
2. Injects localized es-currency-bar-pricing with 5-currency switcher (EUR, USD, GBP, SAR, AED) and localized VAT badge.
3. Synchronizes dana-services-currency-bar to include GBP.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CURRENCY_BAR_TITLES = {
    'ar': 'اختر العملة واحتساب الضريبة:',
    'nl': 'Kies valuta en belastingberekening:',
    'en': 'Select Currency & Tax Calculation:',
    'de': 'Währung & Steuerberechnung wählen:',
    'fr': 'Sélectionnez la devise et le calcul fiscal :',
    'es': 'Seleccione moneda y cálculo de impuestos:',
    'it': 'Seleziona valuta e calcolo delle imposte:',
    'pt': 'Selecione a moeda e o cálculo de impostos:',
    'sv': 'Välj valuta och skatteberäkning:',
    'no': 'Velg valuta og skatteberegning:',
    'da': 'Vælg valuta og skatteberegning:',
    'fi': 'Valitse valuutta ja verolaskenta:',
    'pl': 'Wybierz walutę i kalkulację podatku:',
    'el': 'Επιλέξτε νόμισμα και υπολογισμό φόρου:',
    'cs': 'Vyberte měnu a výpočet daně:',
    'ro': 'Selectați moneda și calculul taxelor:',
    'hu': 'Válasszon pénznemet és adószámítást:',
    'bg': 'Изберете валута и изчисление на данъка:',
    'sk': 'Vyberte menu a výpočet dane:',
    'hr': 'Odaberite valutu i izračun poreza:',
    'lt': 'Pasirinkite valiutą ir mokesčių skaičiavimą:',
    'sl': 'Izberite valuto in izračun davka:',
    'lv': 'Izvēlieties valūtu un nodokļu aprēķinu:',
    'et': 'Valige valuuta ja maksuarvutus:',
    'ga': 'Roghnaigh airgeadra agus ríomh cánach:',
    'mt': 'Agħżel il-munita u l-kalkolu tat-taxxa:',
    'tr': 'Para Birimi ve Vergi Hesaplamasını Seçin:',
    'ku': 'Dirav û Hesabkirina Bacê Hilbijêre:',
    'ckb': 'دراو و حیسابکردنی باج هەڵبژێرە:'
}

PRICE_MAPPINGS = [
    ('1,490', '1490'),
    ('2,890', '2890'),
    ('4,990', '4990'),
    ('1,890', '1890'),
    ('3,490', '3490'),
    ('5,990', '5990'),
    ('490', '490'),
    ('890', '890'),
    ('149', '149'),
    ('290', '290'),
    ('590', '590'),
    ('980', '980'),
    ('1,450', '1450'),
    ('3,020', '3020'),
    ('1,990', '1990'),
]

def update_portal(code, vat_info):
    portal_file = os.path.join(BASE_DIR, code, 'index.html')
    if not os.path.exists(portal_file):
        return False

    with open(portal_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add data-eur-price to plan-price__amount spans
    for formatted, raw in PRICE_MAPPINGS:
        # Match <span class="plan-price__amount">1,490</span> without data-eur-price
        pattern = re.compile(rf'<span class=[\x22\x27]plan-price__amount[\x22\x27]>{re.escape(formatted)}</span>')
        replacement = f'<span class="plan-price__amount" data-eur-price="{raw}">{formatted}</span>'
        html = pattern.sub(replacement, html)

    # 2. Inject es-currency-bar-pricing if not present
    if 'es-currency-bar-pricing' not in html:
        title = CURRENCY_BAR_TITLES.get(code, 'Select Currency & Tax Calculation:')
        bar_html = f'''                <!-- Live Currency & VAT Switcher Bar -->
                <div class="es-currency-bar-pricing">
                    <div class="es-currency-bar-pricing-left">
                        <span class="es-currency-bar-title">{title}</span>
                        <div class="es-currency-bar">
                            <button class="es-currency-btn active" data-currency="EUR" data-sr-call="switchCurrency" data-sr-args='["EUR"]'>🇪🇺 EUR (€)</button>
                            <button class="es-currency-btn" data-currency="USD" data-sr-call="switchCurrency" data-sr-args='["USD"]'>🇺🇸 USD ($)</button>
                            <button class="es-currency-btn" data-currency="SAR" data-sr-call="switchCurrency" data-sr-args='["SAR"]'>🇸🇦 SAR (﷼)</button>
                            <button class="es-currency-btn" data-currency="AED" data-sr-call="switchCurrency" data-sr-args='["AED"]'>🇦🇪 AED (د.إ)</button>
                            <button class="es-currency-btn" data-currency="GBP" data-sr-call="switchCurrency" data-sr-args='["GBP"]'>🇬🇧 GBP (£)</button>
                        </div>
                    </div>
                    <div class="es-pricing-vat-notice">
                        <span class="es-vat-live-badge">{vat_info}</span>
                    </div>
                </div>

                <ul class="pricing-tab_btn"'''

        html = re.sub(r'<ul class=[\x22\x27]pricing-tab_btn[\x22\x27]', bar_html, html, count=1)

    # 3. Synchronize dana-services-currency-bar to include GBP if missing
    if 'data-currency="GBP"' not in html and 'dana-services-currency-bar' in html:
        gbp_btn = '<button type="button" class="dana-cur-pill" data-currency="GBP" data-sr-call="switchCurrency" data-sr-args=\'["GBP"]\'>🇬🇧 GBP (£)</button>\n</div>'
        html = re.sub(r'</div>(?=\s*</div>\s*<!--\s*Services\s*Grid|\s*</div>\s*<div class=[\x22\x27]row)', gbp_btn, html, count=1)

    with open(portal_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"SUCCESS: Deployed multi-currency suite to {code}/index.html")
    return True

def main():
    import sys
    sys.path.append(os.path.join(BASE_DIR, 'scripts'))
    from deploy_sovereign_multilingual import LANGUAGES

    count = 0
    for l in LANGUAGES:
        code = l['code']
        if code == 'ar':
            continue
        vat_desc = f"{l['flag']} {l['vat']} ({code.upper()} Tax Compliant)"
        if update_portal(code, vat_desc):
            count += 1

    print(f"\nAll done! Multi-currency suite active in {count} language portals + index.html.")

if __name__ == '__main__':
    main()
