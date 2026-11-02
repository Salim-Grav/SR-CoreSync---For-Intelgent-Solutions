import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("Generating localized portals for Dutch (nl), German (de), and French (fr)...")

# Base English template files
with open('en/partner-portal.html', 'r', encoding='utf-8') as f:
    en_partner_base = f.read()

with open('en/developer-portal.html', 'r', encoding='utf-8') as f:
    en_dev_base = f.read()

# -----------------------------------------------------------------------------
# 1. Dutch (Nederlands - nl)
# -----------------------------------------------------------------------------
nl_partner = en_partner_base.replace('lang="en" dir="ltr"', 'lang="nl" dir="ltr"')
nl_partner = nl_partner.replace(
    'S&R CoreSync | White-Label Partner & Solutions Provider Gateway',
    'S&R CoreSync | White-Label Partner & Oplossingenportaal (Nederland & EU)'
)
nl_partner = nl_partner.replace(
    'Official sovereign gateway for European solution partners, accountants, and agencies: Resell CoreSync ERP with your custom brand identity, automated 25% RevShare, and multi-tenant client governance.',
    'Officieel soeverein portaal voor Nederlandse en Europese partners, accountants en IT-adviseurs: Herverkoop CoreSync ERP onder uw eigen merkidentiteit met 25% RevShare en BTW/KVK-integratie.'
)
nl_partner = nl_partner.replace('Sovereign White-Label & Solutions Partner Gateway', 'Soeverein White-Label & Partner Oplossingenportaal')
nl_partner = nl_partner.replace('Return to Main Portal', 'Terug naar Hoofdplatform')
nl_partner = nl_partner.replace('Exclusive Enterprise Distribution & Sovereign RevShare 25% Program', 'Exclusief Distributieprogramma & 25% RevShare Partnerschap')
nl_partner = nl_partner.replace('1. Custom Sovereign Brand Studio (White-Label)', '1. White-Label Merkstudio & Huisstijlaapassing')
nl_partner = nl_partner.replace('2. WhatsApp Business Automated Financial Alert Engine', '2. Geautomatiseerde Financiële Meldingen via WhatsApp Business')
nl_partner = nl_partner.replace('3. Active Multi-Tenant European Client Infrastructure', '3. Beheer van Actieve Nederlandse & Europese Bedrijfsomgevingen')

with open('nl/partner-portal.html', 'w', encoding='utf-8') as f:
    f.write(nl_partner)
print("✅ Created nl/partner-portal.html")

nl_dev = en_dev_base.replace('lang="en" dir="ltr"', 'lang="nl" dir="ltr"')
nl_dev = nl_dev.replace(
    'S&R CoreSync Developer Gateway | Sovereign REST APIs, SDKs & Webhooks',
    'S&R CoreSync Ontwikkelaarsportaal | Soevereine REST API\'s, SDK\'s & Webhooks'
)
nl_dev = nl_dev.replace('Sovereign Developer Gateway & Open Cloud APIs', 'Soeverein Ontwikkelaarsportaal & Open Cloud API\'s')
nl_dev = nl_dev.replace('Back to Main Portal', 'Terug naar Hoofdplatform')

with open('nl/developer-portal.html', 'w', encoding='utf-8') as f:
    f.write(nl_dev)
print("✅ Created nl/developer-portal.html")

# -----------------------------------------------------------------------------
# 2. German (Deutsch - de)
# -----------------------------------------------------------------------------
de_partner = en_partner_base.replace('lang="en" dir="ltr"', 'lang="de" dir="ltr"')
de_partner = de_partner.replace(
    'S&R CoreSync | White-Label Partner & Solutions Provider Gateway',
    'S&R CoreSync | White-Label Partner & Lösungspartner-Portal'
)
de_partner = de_partner.replace(
    'Official sovereign gateway for European solution partners, accountants, and agencies: Resell CoreSync ERP with your custom brand identity, automated 25% RevShare, and multi-tenant client governance.',
    'Offizielles souveränes Portal für europäische Partner, Systemhäuser und Steuerberater: CoreSync ERP unter eigener Marke vertreiben mit 25% RevShare und DSGVO-Konformität.'
)
de_partner = de_partner.replace('Sovereign White-Label & Solutions Partner Gateway', 'Souveränes White-Label & Lösungspartner-Portal')
de_partner = de_partner.replace('Return to Main Portal', 'Zurück zur Hauptplattform')
de_partner = de_partner.replace('Exclusive Enterprise Distribution & Sovereign RevShare 25% Program', 'Exklusives Enterprise-Vertriebsprogramm & 25% RevShare')
de_partner = de_partner.replace('1. Custom Sovereign Brand Studio (White-Label)', '1. White-Label Markenstudio & Individuelles Branding')
de_partner = de_partner.replace('2. WhatsApp Business Automated Financial Alert Engine', '2. Automatisierte WhatsApp Business Finanz-Benachrichtigungen')
de_partner = de_partner.replace('3. Active Multi-Tenant European Client Infrastructure', '3. Verwaltung aktiver europäischer Mandanten & Unternehmen')

with open('de/partner-portal.html', 'w', encoding='utf-8') as f:
    f.write(de_partner)
print("✅ Created de/partner-portal.html")

de_dev = en_dev_base.replace('lang="en" dir="ltr"', 'lang="de" dir="ltr"')
de_dev = de_dev.replace(
    'S&R CoreSync Developer Gateway | Sovereign REST APIs, SDKs & Webhooks',
    'S&R CoreSync Entwickler-Gateway | Souveräne REST-APIs, SDKs & Webhooks'
)
de_dev = de_dev.replace('Sovereign Developer Gateway & Open Cloud APIs', 'Souveränes Entwickler-Gateway & Offene Cloud-APIs')
de_dev = de_dev.replace('Back to Main Portal', 'Zurück zur Hauptplattform')

with open('de/developer-portal.html', 'w', encoding='utf-8') as f:
    f.write(de_dev)
print("✅ Created de/developer-portal.html")

# -----------------------------------------------------------------------------
# 3. French (Français - fr)
# -----------------------------------------------------------------------------
fr_partner = en_partner_base.replace('lang="en" dir="ltr"', 'lang="fr" dir="ltr"')
fr_partner = fr_partner.replace(
    'S&R CoreSync | White-Label Partner & Solutions Provider Gateway',
    'S&R CoreSync | Portail Partenaires & Fournisseurs de Solutions White-Label'
)
fr_partner = fr_partner.replace(
    'Official sovereign gateway for European solution partners, accountants, and agencies: Resell CoreSync ERP with your custom brand identity, automated 25% RevShare, and multi-tenant client governance.',
    'Portail souverain officiel pour les partenaires, intégrateurs et cabinets comptables européens : distribuez CoreSync ERP sous votre propre marque avec 25% de RevShare.'
)
fr_partner = fr_partner.replace('Sovereign White-Label & Solutions Partner Gateway', 'Portail Partenaires & Solutions Marque Blanche')
fr_partner = fr_partner.replace('Return to Main Portal', 'Retour au Portail Principal')
fr_partner = fr_partner.replace('Exclusive Enterprise Distribution & Sovereign RevShare 25% Program', 'Programme de Distribution Entreprise & 25% RevShare')
fr_partner = fr_partner.replace('1. Custom Sovereign Brand Studio (White-Label)', '1. Studio de Personnalisation de Marque Blanche')
fr_partner = fr_partner.replace('2. WhatsApp Business Automated Financial Alert Engine', '2. Alertes Financières Automatisées WhatsApp Business')
fr_partner = fr_partner.replace('3. Active Multi-Tenant European Client Infrastructure', '3. Gestion Multi-Entreprises des Clients Européens')

with open('fr/partner-portal.html', 'w', encoding='utf-8') as f:
    f.write(fr_partner)
print("✅ Created fr/partner-portal.html")

fr_dev = en_dev_base.replace('lang="en" dir="ltr"', 'lang="fr" dir="ltr"')
fr_dev = fr_dev.replace(
    'S&R CoreSync Developer Gateway | Sovereign REST APIs, SDKs & Webhooks',
    'S&R CoreSync Passerelle Développeurs | APIs REST, SDKs & Webhooks'
)
fr_dev = fr_dev.replace('Sovereign Developer Gateway & Open Cloud APIs', 'Passerelle Développeurs Souveraine & APIs Cloud Ouvertes')
fr_dev = fr_dev.replace('Back to Main Portal', 'Retour au Portail Principal')

with open('fr/developer-portal.html', 'w', encoding='utf-8') as f:
    f.write(fr_dev)
print("✅ Created fr/developer-portal.html")

# -----------------------------------------------------------------------------
# 4. Update index.html links in nl/, de/, fr/
# -----------------------------------------------------------------------------
for lang in ['nl', 'de', 'fr']:
    idx_p = f'{lang}/index.html'
    if os.path.exists(idx_p):
        with open(idx_p, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace('href="../developer-portal.html"', 'href="./developer-portal.html"')
        content = content.replace('href="../partner-portal.html"', 'href="./partner-portal.html"')
        with open(idx_p, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated internal portal links in {idx_p} to point to local portals!")

print("All European localized portals built and linked successfully!")

