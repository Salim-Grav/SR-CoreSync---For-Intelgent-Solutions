import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Localized dictionaries for Row 2 (Developer Portal & Partner Portal)
PORTAL_LOCALIZATIONS = {
    'en': {
        'dev_label': 'Developer Portal & 3D Interactive ⚡',
        'dev_title': 'Developer Portal, APIs, and Interactive 3D Hologram',
        'partner_label': 'Partners & Licensing Portal 💼',
        'partner_title': 'Global Partner Network, Exclusive Agency, and Enterprise Licensing'
    },
    'nl': {
        'dev_label': 'Ontwikkelaarsportaal & 3D Interactief ⚡',
        'dev_title': "Ontwikkelaarsportaal, API's en interactief 3D-hologram",
        'partner_label': 'Partners- & Licentieportaal 💼',
        'partner_title': 'Wereldwijd partnernetwerk, exclusief agentschap en enterprise-licenties'
    },
    'de': {
        'dev_label': 'Entwicklerportal & 3D Interaktiv ⚡',
        'dev_title': 'Entwicklerportal, APIs und interaktives 3D-Hologramm',
        'partner_label': 'Partner- & Lizenzportal 💼',
        'partner_title': 'Globales Partnernetzwerk, Exklusivagentur und Unternehmenslizenzierung'
    },
    'fr': {
        'dev_label': 'Portail Développeurs & 3D Interactif ⚡',
        'dev_title': "Portail Développeurs, API et hologramme 3D interactif",
        'partner_label': 'Portail Partenaires & Licences 💼',
        'partner_title': "Réseau mondial de partenaires, agence exclusive et licences d'entreprise"
    },
    'es': {
        'dev_label': 'Portal Desarrolladores y 3D Interactivo ⚡',
        'dev_title': 'Portal de Desarrolladores, APIs y holograma 3D interactivo',
        'partner_label': 'Portal de Socios y Licencias 💼',
        'partner_title': 'Red global de socios, agencia exclusiva y licencias corporativas'
    },
    'it': {
        'dev_label': 'Portale Sviluppatori & 3D Interattivo ⚡',
        'dev_title': 'Portale Sviluppatori, API e ologramma 3D interattivo',
        'partner_label': 'Portale Partner & Licenze 💼',
        'partner_title': 'Rete globale di partner, agenzia esclusiva e licenze aziendali'
    },
    'pt': {
        'dev_label': 'Portal de Desenvolvedores e 3D Interativo ⚡',
        'dev_title': 'Portal de Desenvolvedores, APIs e holograma 3D interativo',
        'partner_label': 'Portal de Parceiros e Licenciamento 💼',
        'partner_title': 'Rede global de parceiros, agência exclusiva e licenciamento corporativo'
    },
    'tr': {
        'dev_label': 'Geliştirici Portalı ve 3D Etkileşimli ⚡',
        'dev_title': "Geliştirici Portalı, API'ler ve Etkileşimli 3D Hologram",
        'partner_label': 'Ortaklık ve Lisans Portalı 💼',
        'partner_title': 'Küresel Ortaklık Ağı, Özel Acentelik ve Kurumsal Lisanslama'
    },
    'pl': {
        'dev_label': 'Portal Programistów i Interaktywny 3D ⚡',
        'dev_title': 'Portal Programistów, API i interaktywny hologram 3D',
        'partner_label': 'Portal Partnerów i Licencji 💼',
        'partner_title': 'Globalna sieć partnerów, wyłączne agencje i licencjonowanie korporacyjne'
    },
    'cs': {
        'dev_label': 'Vývojářský Portál a Interaktivní 3D ⚡',
        'dev_title': 'Vývojářský portál, API a interaktivní 3D hologram',
        'partner_label': 'Portál Partnerů a Licencí 💼',
        'partner_title': 'Globální partnerská síť, výhradní zastoupení a podnikové licencování'
    },
    'sk': {
        'dev_label': 'Vývojársky Portál a Interaktívny 3D ⚡',
        'dev_title': 'Vývojársky portál, API a interaktívny 3D hologram',
        'partner_label': 'Portál Partnerov a Licencií 💼',
        'partner_title': 'Globálna partnerská sieť, výhradné zastúpenie a podnikové licencovanie'
    },
    'hu': {
        'dev_label': 'Fejlesztői Portál & Interaktív 3D ⚡',
        'dev_title': 'Fejlesztői portál, API-k és interaktív 3D hologram',
        'partner_label': 'Partner & Licenc Portál 💼',
        'partner_title': 'Globális partnerhálózat, exkluzív ügynökség és vállalati licencelés'
    },
    'ro': {
        'dev_label': 'Portal Dezvoltatori & 3D Interactiv ⚡',
        'dev_title': 'Portal pentru Dezvoltatori, API-uri și hologramă 3D interactivă',
        'partner_label': 'Portal Parteneri & Licențe 💼',
        'partner_title': 'Rețea globală de parteneri, agenție exclusivă și licențiere enterprise'
    },
    'bg': {
        'dev_label': 'Портал за Разработчици & 3D Интерактив ⚡',
        'dev_title': 'Портал за разработчици, API и интерактивна 3D холограма',
        'partner_label': 'Портал за Партньори и Лицензи 💼',
        'partner_title': 'Глобална партньорска мрежа, ексклузивно представителство и корпоративно лицензиране'
    },
    'el': {
        'dev_label': 'Πύλη Προγραμματιστών & 3D Διαδραστικό ⚡',
        'dev_title': 'Πύλη Προγραμματιστών, API και διαδραστικό τρισδιάστατο ολόγραμμα',
        'partner_label': 'Πύλη Συνεργατών & Αδειών 💼',
        'partner_title': 'Παγκόσμιο δίκτυο συνεργατών, αποκλειστική αντιπροσωπεία και εταιρικές άδειες'
    },
    'da': {
        'dev_label': 'Udviklerportal & 3D Interaktiv ⚡',
        'dev_title': "Udviklerportal, API'er og interaktivt 3D-hologram",
        'partner_label': 'Partner- & Licensportal 💼',
        'partner_title': 'Globalt partnernetværk, eksklusivt agentur og virksomhedslicensering'
    },
    'sv': {
        'dev_label': 'Utvecklarportal & 3D Interaktiv ⚡',
        'dev_title': 'Utvecklarportal, API:er och interaktivt 3D-hologram',
        'partner_label': 'Partner- & Licensportal 💼',
        'partner_title': 'Globalt partnernätverk, exklusiv agentur och företagslicensiering'
    },
    'no': {
        'dev_label': 'Utviklerportal & 3D Interaktiv ⚡',
        'dev_title': 'Utviklerportal, API-er og interaktivt 3D-hologram',
        'partner_label': 'Partner- & Lisensportal 💼',
        'partner_title': 'Globalt partnernettverk, eksklusivt byrå og bedriftslisensiering'
    },
    'fi': {
        'dev_label': 'Kehittäjäportaali & Interaktiivinen 3D ⚡',
        'dev_title': 'Kehittäjäportaali, API:t ja interaktiivinen 3D-hologrammi',
        'partner_label': 'Kumppani- ja Lisenssiportaali 💼',
        'partner_title': 'Globaali kumppaniverkosto, yksinoikeusedustus ja yrityslisenssit'
    },
    'et': {
        'dev_label': 'Arendajate Portaal & 3D Interaktiivne ⚡',
        'dev_title': 'Arendajate portaal, API-d ja interaktiivne 3D-hologramm',
        'partner_label': 'Partnerite ja Litsentside Portaal 💼',
        'partner_title': 'Ülemaailmne partnerivõrgustik, ainuagentuur ja ettevõttelitsentsid'
    },
    'lv': {
        'dev_label': 'Izstrādātāju Portāls & 3D Interaktīvs ⚡',
        'dev_title': 'Izstrādātāju portāls, API un interaktīva 3D holograma',
        'partner_label': 'Partneru un Licenču Portāls 💼',
        'partner_title': 'Globālais partneru tīkls, ekskluzīva aģentūra un uzņēmumu licencēšana'
    },
    'lt': {
        'dev_label': 'Kūrėjų Portalas ir 3D Interaktyvus ⚡',
        'dev_title': 'Kūrėjų portalas, API ir interaktyvi 3D holograma',
        'partner_label': 'Partnerių ir Licencijų Portalas 💼',
        'partner_title': 'Pasaulinis partnerių tinklas, išskirtinė agentūra ir įmonių licencijavimas'
    },
    'sl': {
        'dev_label': 'Portal za Razvijalce & 3D Interaktivno ⚡',
        'dev_title': 'Portal za razvijalce, API-ji in interaktivni 3D hologram',
        'partner_label': 'Portal za Partnerje in Licence 💼',
        'partner_title': 'Globalna partnerska mreža, ekskluzivno zastopstvo in podjetniško licenciranje'
    },
    'hr': {
        'dev_label': 'Portal za Razvojne Inženjere & 3D Interaktivan ⚡',
        'dev_title': 'Portal za programere, API-ji i interaktivni 3D hologram',
        'partner_label': 'Portal za Partnere i Licence 💼',
        'partner_title': 'Globalna mreža partnera, ekskluzivno zastupstvo i licenciranje za poduzeća'
    },
    'ga': {
        'dev_label': 'Tairseach Forbróirí & Idirghníomhach 3D ⚡',
        'dev_title': 'Tairseach Forbróirí, APIanna agus Holagram 3D Idirghníomhach',
        'partner_label': 'Tairseach Comhpháirtithe & Ceadúnaithe 💼',
        'partner_title': 'Líonra Comhpháirtíochta Domhanda, Gníomhaireacht Eisiach agus Ceadúnú Fiontraíochta'
    },
    'mt': {
        'dev_label': 'Portal tal-Iżviluppaturi & 3D Interattiv ⚡',
        'dev_title': 'Portal tal-Iżviluppaturi, APIs u Olagramm 3D Interattiv',
        'partner_label': 'Portal tal-Imsieħba u Liċenzji 💼',
        'partner_title': "Netwerk Globali ta' Msieħba, Aġenzija Esklussiva u Liċenzjar Korporattiv"
    },
    'ku': {
        'dev_label': 'Portala Pêşvebiran & 3D Înteraktîf ⚡',
        'dev_title': 'Portala Pêşvebiran, API û Holograma 3D ya Înteraktîf',
        'partner_label': 'Portala Hevalbendan & Lîsansê 💼',
        'partner_title': 'Tora gerdûnî ya hevalbendan, nûnertiya taybet û lîsanskirina saziyî'
    }
}

dirs = sorted(list(PORTAL_LOCALIZATIONS.keys()))
print(f"Processing {len(dirs)} languages...")

# Regex to find the hero action block
pattern = re.compile(
    r'(<div class="hero-reference__actions[^"]*"[^>]*>)(.*?)(</div>(\s*<!--[^\n]*-->)?\s*</div>)',
    re.DOTALL
)

updated_count = 0

for d in dirs:
    path = f"{d}/index.html"
    if not os.path.exists(path):
        print(f"Skipping {d}: file not found")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    m = pattern.search(content)
    if not m:
        print(f"Skipping {d}: hero actions pattern not matched")
        continue

    inner = m.group(2)
    # Extract demo button
    demo_match = re.search(r'<a\s+href="demo\.html"[^>]*>.*?</a>', inner, re.DOTALL)
    # Extract vip button
    vip_match = re.search(r'<button\s+type="button"[^>]*openExecutiveBookingModal[^>]*>.*?</button>', inner, re.DOTALL)

    if not demo_match or not vip_match:
        print(f"Skipping {d}: demo or vip button not found in inner html")
        continue

    demo_html = demo_match.group(0)
    vip_html = vip_match.group(0)

    # Standardize classes for demo button: ensure hero-btn-gold-pair and hero-btn-primary-highlight
    if 'hero-btn-gold-pair' not in demo_html:
        demo_html = demo_html.replace('hero-btn-demo', 'hero-btn-gold-pair hero-btn-demo')
    if 'hero-btn-primary-highlight' not in demo_html:
        demo_html = demo_html.replace('hero-btn-demo', 'hero-btn-demo hero-btn-primary-highlight')

    # Standardize classes for vip button: ensure hero-btn-gold-pair and hero-btn-primary-highlight
    if 'hero-btn-gold-pair' not in vip_html:
        vip_html = vip_html.replace('hero-btn-vip', 'hero-btn-gold-pair hero-btn-vip')
    if 'hero-btn-primary-highlight' not in vip_html:
        vip_html = vip_html.replace('hero-btn-vip', 'hero-btn-vip hero-btn-primary-highlight')

    loc = PORTAL_LOCALIZATIONS[d]

    row1 = f"""                                        <!-- Row 1: Gold Luxury Pair (Live Demo & VIP Executive Consultation) -->
                                        <div class="hero-actions-row">
                                            {demo_html.strip()}
                                            {vip_html.strip()}
                                        </div>"""

    row2 = f"""                                        <!-- Row 2: Dark Emerald Portal Pair (Developer Portal & Partner Portal) -->
                                        <div class="hero-actions-row">
                                            <a href="../developer-portal.html" class="tf-btn hero-reference__action hero-btn-portal-pair hero-btn-dev-portal" title="{loc['dev_title']}">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg>
                                                <span>{loc['dev_label']}</span>
                                            </a>
                                            <a href="../partner-portal.html" class="tf-btn hero-reference__action hero-btn-portal-pair hero-btn-partner-portal" title="{loc['partner_title']}">
                                                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                                                <span>{loc['partner_label']}</span>
                                            </a>
                                        </div>"""

    new_hero_actions = f"""<div class="hero-reference__actions hero-actions-2x2">
{row1}

{row2}
                                    </div>"""

    # Replace the hero actions container
    # Span of full match m: m.group(1) + m.group(2) + "</div>"
    # To be very precise, find where the inner ends
    start_pos = m.start(1)
    # The container ends at m.group(3)'s first </div>
    # Let's replace the whole container up to m.end(3) minus the trailing closing div
    # Or replace m.group(1) + m.group(2) + "</div>"
    container_old = m.group(1) + m.group(2) + "</div>"
    
    if container_old not in content:
        print(f"Error matching container_old in {d}")
        continue

    content = content.replace(container_old, new_hero_actions, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    updated_count += 1
    print(f"Updated {d}/index.html successfully.")

print(f"\nTotal languages updated: {updated_count}/{len(dirs)}")
