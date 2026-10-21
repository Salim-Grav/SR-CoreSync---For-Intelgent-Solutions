const fs = require('fs');
const path = require('path');

const projectRoot = path.join(__dirname, '..');

const PORTALS = [
    { lang: 'en', file: 'en/index.html' },
    { lang: 'nl', file: 'nl/index.html' },
    { lang: 'de', file: 'de/index.html' }
];

const CARD_ICONS = {
    gdpr: { isGreen: false, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>' },
    btw: { isGreen: true, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>' },
    amsix: { isGreen: true, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>' },
    sla: { isGreen: false, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>' },
    iso: { isGreen: true, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>' },
    zeroknowledge: { isGreen: false, svg: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="16" r="1"></circle><rect x="3" y="10" width="18" height="12" rx="2"></rect><path d="M7 10V7a5 5 0 0 1 10 0v3"></path></svg>' }
};

const CONTENT = {
    en: {
        trust: {
            title: 'European Enterprise Compliance & <span>Sovereign Cloud Standards</span>',
            subtitle: 'Legally binding European regulatory certifications, enterprise SLA guarantees, and sovereign cloud infrastructure anchored in Amsterdam, the Netherlands.',
            clickVerify: 'Click any compliance badge to verify specifications & legal parameters',
            verifyLinkText: 'Verify Technical Specs',
            badges: [
                { id: 'gdpr', code: 'GDPR EU 2016/679', status: 'Certified & Compliant ✓', title: 'European Data Protection (GDPR)', desc: 'Strict compliance with European privacy laws, full encryption at rest & transit, zero unauthorized telemetry.' },
                { id: 'btw', code: 'Belastingdienst BTW', status: 'Fiscal Compliance ✓', title: 'Dutch Fiscal & BTW Standards', desc: 'Certified PEPPOL BIS Billing 3.0 e-invoicing and automated Dutch VAT (9% & 21%) accounting integration.' },
                { id: 'amsix', code: 'AMS-IX Tier 3+', status: 'Amsterdam Infrastructure ✓', title: 'Amsterdam Sovereign Cloud Node', desc: 'Enterprise servers hosted in Amsterdam Tier 3+ datacenter adjacent to AMS-IX for sub-5ms low latency.' },
                { id: 'sla', code: '99.98% SLA', status: 'Mission Critical ✓', title: 'High-Availability Cloud SLA', desc: 'Contractually guaranteed 99.98% uptime with active disaster recovery and sub-15 minute failover response.' },
                { id: 'iso', code: 'ISO 27001 / SOC 2', status: 'Information Security ✓', title: 'Security & Risk Governance', desc: 'Rigorous alignment with ISO/IEC 27001 standards and SOC 2 Type II controls for enterprise risk governance.' },
                { id: 'zeroknowledge', code: 'Zero-Knowledge', status: 'Sovereign Encryption ✓', title: 'Cryptographic Zero-Knowledge', desc: 'Dedicated single-tenant databases with client-controlled keys (BYOK), eliminating third-party backdoors.' }
            ],
            footerLegal: 'S&R CoreSync Solutions B.V. operates strictly under Dutch and European Union jurisdictions.',
            certBtn: 'Request Enterprise Compliance Dossier (PDF) →'
        },
        matrix: {
            pill: 'Comprehensive Architecture & Features Matrix 2026',
            title: 'Compare <span>Enterprise Cloud Tiers</span> with Precision',
            subtitle: 'Choose the optimal cloud infrastructure for your enterprise across the European Union. Save 20% on annual billing plus corporate group discounts for multi-entity holdings.',
            annualBtn: 'Annual Billing',
            annualSave: 'Save 20%',
            monthlyBtn: 'Monthly Billing',
            entityLabel: 'Companies / Holdings:',
            entity1: 'Single Entity',
            entity2: '2 - 3 Entities (-10%)',
            entity4: 'Holding 4+ (-20%)',
            thFeatures: 'Architectural Specs & Standards',
            thSub: 'Detailed comparison across infrastructure, compliance, AI, and enterprise SLAs',
            starterName: 'Core Starter',
            starterDesc: 'For emerging businesses and single-scope platforms',
            proName: 'Business Pro',
            proDesc: 'For mid-size enterprises and scaling organizations',
            proBadge: 'Most Popular // Flagship',
            enterpriseName: 'Sovereign Enterprise',
            enterpriseDesc: 'For corporate holdings requiring dedicated sovereign clusters',
            ctaStarter: 'Book Tier via VIP WhatsApp',
            ctaPro: 'Deploy Cloud Tier Now ★',
            ctaEnterprise: 'Sovereign Architectural Briefing 🛡️',
            categories: [
                {
                    name: '🌐 1. Cloud Infrastructure & AMS-IX Hosting',
                    rows: [
                        { label: 'Datacenter Node & Server Location', tip: 'Primary hosting facility for sovereign cloud workloads', val1: 'Amsterdam Tier 3+ (Shared)', val2: 'Amsterdam Dedicated VPS Node', val3: 'Sovereign Isolated Cluster (Physical)' },
                        { label: 'High-Speed NVMe Cloud Storage', tip: 'Fast enterprise storage for assets and database partitions', val1: '50 GB NVMe', val2: '250 GB Ultra-Fast NVMe', val3: 'Unlimited (Scale-on-Demand)' },
                        { label: 'Monthly Traffic Bandwidth & Global CDN', tip: 'Monthly outbound transfer bandwidth and content caching', val1: '100,000 visits / month', val2: '500,000 visits + European CDN', val3: 'Unlimited + Global Anycast CDN' },
                        { label: 'Tenancy Architecture Model', tip: 'Level of database independence and workload segregation', val1: 'Logical Software Isolation', val2: 'Dedicated Private Database', val3: 'Dedicated Single-Tenant 100%' }
                    ]
                },
                {
                    name: '🛡️ 2. Security & Regulatory Compliance',
                    rows: [
                        { label: 'EU General Data Protection Regulation', tip: 'Regulation (EU) 2016/679 and custom DPA contracts', val1: '✓ Certified Standard', val2: '✓ Advanced + Custom DPA Agreement', val3: '✓ Sovereign Zero-Knowledge' },
                        { label: 'Dutch Tax Authority Compliance (BTW)', tip: 'Automated VAT calculation and PEPPOL e-invoicing', val1: 'Basic Digital Invoicing', val2: 'Automated BTW + PEPPOL BIS Billing', val3: 'Full Bank & ERP Accounting Integration' },
                        { label: 'Cryptographic Key Management', tip: 'Ownership and control over encryption keys', val1: 'AES-256 Shared Architecture', val2: 'TLS 1.3 + Enhanced SSL Certificates', val3: 'Client-Owned KMS Keys (BYOK)' },
                        { label: 'Disaster Recovery & Redundancy', tip: 'Multi-zone geographic replication and failover speed', val1: 'Weekly Cloud Backup', val2: 'Daily Multi-Zone Backup', val3: 'Real-Time Continuous (RPO < 5 mins)' }
                    ]
                },
                {
                    name: '⚡ 3. Enterprise AI & Integrations',
                    rows: [
                        { label: 'Enterprise AI Assistant (Copilot RAG)', tip: 'Trained conversational AI indexed on corporate documentation', val1: '—', val2: '✓ Standard Customer Service RAG', val3: '✓ Dedicated Sovereign Model on Enterprise Data' },
                        { label: 'European Payment Gateways', tip: 'Supported payment providers and checkout rails', val1: 'Stripe + Credit Cards', val2: 'Stripe + Mollie + iDEAL + Bancontact', val3: 'All Rails + Institutional SEPA Direct Debit' },
                        { label: 'System APIs & Webhooks Access', tip: 'Integration interfaces with third-party and legacy systems', val1: 'Basic Webhooks', val2: 'Comprehensive REST APIs & Documentation', val3: 'Full Core APIs + Custom Microservices' },
                        { label: 'White-Label Branding Rights', tip: 'Ability to strip platform branding for pure enterprise identity', val1: '"Powered by CoreSync" Badge', val2: 'Custom Brand Colors, Logo & Domain', val3: '100% White-Label (Zero CoreSync Footprint)' }
                    ]
                },
                {
                    name: '🤝 4. SLA & Executive Concierge',
                    rows: [
                        { label: 'Contractually Guaranteed Uptime (SLA)', tip: 'Guaranteed uptime threshold with penalty credits', val1: '99.5% Standard Uptime', val2: '99.9% High Availability', val3: '99.98% Mission-Critical SLA' },
                        { label: 'Technical Support Response Times', tip: 'Maximum response window for critical operational tickets', val1: 'Within 24 Hours (Support Tickets)', val2: 'Within 4 Hours (Email + WhatsApp)', val3: 'Within 15 Minutes (24/7/365 Direct Red-Line)' },
                        { label: 'Team Training & Knowledge Transfer', tip: 'Executive onboarding sessions and staff workshops', val1: 'Digital Documentation Suite', val2: '2 Live Interactive Zoom Sessions', val3: 'Unlimited On-Site Amsterdam or Remote Workshops' },
                        { label: 'Dedicated Solutions Architect', tip: 'Dedicated engineer steering your digital transformation', val1: '—', val2: 'Semi-Annual System Architecture Audit', val3: 'Senior Enterprise Solutions Architect' }
                    ]
                }
            ],
            guarantees: [
                '14-Day Money-Back Satisfaction Guarantee',
                'Official Dutch Legal Contract Protecting All IP Rights',
                'Instant Cloud Scaling & Plan Modification Anytime'
            ],
            b2bQuoteBtn: 'Request Custom Enterprise Quotation (B2B) →'
        }
    },
    nl: {
        trust: {
            title: 'Europese Bedrijfscompliance & <span>Soevereine Cloudstandaarden</span>',
            subtitle: 'Wettelijk bindende Europese certificeringen, enterprise SLA-garanties en soevereine cloudinfrastructuur verankerd in Amsterdam, Nederland.',
            clickVerify: 'Klik op een compliance-badge om specificaties en juridische kaders te bekijken',
            verifyLinkText: 'Bekijk Technische Specificaties',
            badges: [
                { id: 'gdpr', code: 'AVG / GDPR EU 2016/679', status: 'Gecertificeerd & Conform ✓', title: 'Europese Privacybescherming (AVG)', desc: 'Volledige naleving van de AVG, end-to-end encryptie en gegarandeerde bescherming tegen ongeautoriseerde telemetrie.' },
                { id: 'btw', code: 'Belastingdienst BTW', status: 'Fiscaal Conform ✓', title: 'Nederlandse Fiscale Normen (BTW)', desc: 'Gecertificeerde PEPPOL BIS 3.0 e-facturatie en geautomatiseerde BTW-berekening (9% en 21%) conform de belastingwetgeving.' },
                { id: 'amsix', code: 'AMS-IX Tier 3+', status: 'Amsterdam Knooppunt ✓', title: 'Amsterdam Soevereine Cloud', desc: 'Bedrijfsservers direct gehost in Amsterdam Tier 3+ datacenters aan het AMS-IX internetknooppunt (< 5ms latentie).' },
                { id: 'sla', code: '99.98% SLA', status: 'Mission Critical ✓', title: 'Hoge Beschikbaarheid SLA', desc: 'Contractueel gegarandeerde 99.98% systeembeschikbaarheid met actieve disaster recovery en < 15 min failover.' },
                { id: 'iso', code: 'ISO 27001 / SOC 2', status: 'Informatiebeveiliging ✓', title: 'Beveiliging & Risicobeheer', desc: 'Strikte conformiteit met ISO/IEC 27001-normen en SOC 2 Type II-principes voor integraal risicobeheer.' },
                { id: 'zeroknowledge', code: 'Zero-Knowledge', status: 'Soevereine Versleuteling ✓', title: 'Cryptografische Zero-Knowledge', desc: 'Toegewijde databases met door de klant beheerde sleutels (BYOK), zonder achterdeuren voor derden.' }
            ],
            footerLegal: 'S&R CoreSync Solutions B.V. opereert strikt onder Nederlands en Europees recht.',
            certBtn: 'Vraag Zakelijk Compliance-Dossier Aan (PDF) →'
        },
        matrix: {
            pill: 'Volledige Architectuur- en Functiematrix 2026',
            title: 'Vergelijk <span>Zakelijke Cloudpakketten</span> met Precisie',
            subtitle: 'Kies de optimale cloudinfrastructuur voor uw organisatie in Nederland en de Europese Unie. Bespaar 20% bij jaarlijkse facturatie plus holdingkorting voor meerdere entiteiten.',
            annualBtn: 'Jaarlijkse Facturatie',
            annualSave: 'Bespaar 20%',
            monthlyBtn: 'Maandelijkse Facturatie',
            entityLabel: 'Bedrijven / Holdings:',
            entity1: 'Enkele entiteit',
            entity2: '2 - 3 Entiteiten (-10%)',
            entity4: 'Holding 4+ (-20%)',
            thFeatures: 'Architectonische Specificaties',
            thSub: 'Gedetailleerde vergelijking op infrastructuur, compliance, AI en enterprise SLA\'s',
            starterName: 'Core Starter',
            starterDesc: 'Voor startende ondernemingen en enkelvoudige projecten',
            proName: 'Business Pro',
            proDesc: 'Voor middelgrote bedrijven en groeiende organisaties',
            proBadge: 'Meest Gekozen // Vlaggenschip',
            enterpriseName: 'Sovereign Enterprise',
            enterpriseDesc: 'Voor holdings en concerns met strikte soevereiniteitseisen',
            ctaStarter: 'Reserveer Pakket via VIP WhatsApp',
            ctaPro: 'Start Directe Cloud-Implementatie ★',
            ctaEnterprise: 'Soeverein Architectuurgesprek 🛡️',
            categories: [
                {
                    name: '🌐 1. Cloudinfrastructuur & AMS-IX Hosting',
                    rows: [
                        { label: 'Datacenterknooppunt & Serverlocatie', tip: 'Primaire hostingfaciliteit voor soevereine cloudworkloads', val1: 'Amsterdam Tier 3+ (Gedeeld)', val2: 'Amsterdam Dedicated VPS Node', val3: 'Soeverein Geïsoleerd Cluster (Fysiek)' },
                        { label: 'Snelle NVMe Cloudopslag', tip: 'Snelle zakelijke opslag voor bestanden en databases', val1: '50 GB NVMe', val2: '250 GB Ultrasnelle NVMe', val3: 'Onbeperkt (Scale-on-Demand)' },
                        { label: 'Maandelijks Dataverkeer & Global CDN', tip: 'Inbegrepen bandbreedte en Europese CDN-caching', val1: '100.000 bezoeken / mnd', val2: '500.000 bezoeken + Europees CDN', val3: 'Onbeperkt + Global Anycast CDN' },
                        { label: 'Tenancy-Architectuurmodel', tip: 'Mate van database-onafhankelijkheid en scheiding', val1: 'Logische Software-Isolatie', val2: 'Toegewijde Privé-Database', val3: 'Toegewijde Single-Tenant 100%' }
                    ]
                },
                {
                    name: '🛡️ 2. Beveiliging & Fiscale Regelgeving',
                    rows: [
                        { label: 'Algemene Verordening Gegevensbescherming (AVG)', tip: 'Naleving van Verordening (EU) 2016/679 en DPA-contracten', val1: '✓ Gecertificeerde Norm', val2: '✓ Geavanceerd + Maatwerk DPA', val3: '✓ Soeverein Zero-Knowledge' },
                        { label: 'Belastingdienst Fiscale Compliance (BTW)', tip: 'Automatische BTW-berekening en PEPPOL facturatie', val1: 'Digitale Basisfacturatie', val2: 'Automatische BTW + PEPPOL BIS Billing', val3: 'Volledige Bank- & Boekhoudkoppeling' },
                        { label: 'Cryptografisch Sleutelbeheer', tip: 'Eigenaarschap en controle over encryptiesleutels', val1: 'AES-256 Gedeelde Architectuur', val2: 'TLS 1.3 + Versterkt SSL-Certificaat', val3: 'Klant-Eigen KMS Sleutels (BYOK)' },
                        { label: 'Disaster Recovery & Redundantie', tip: 'Geografische replicatie en herstelsnelheid bij storing', val1: 'Wekelijkse Cloudbackup', val2: 'Dagelijkse Multi-Zone Backup', val3: 'Realtime Continu (RPO < 5 min)' }
                    ]
                },
                {
                    name: '⚡ 3. Zakelijke AI & Systeemondersteuning',
                    rows: [
                        { label: 'Bedrijfs-AI Assistent (Copilot RAG)', tip: 'Geïndexeerd AI-model op bedrijfsdocumentatie en processen', val1: '—', val2: '✓ Standaard Klantenservice RAG', val3: '✓ Toegewijd Soeverein Model op Uw Data' },
                        { label: 'Europese Betaalmethoden', tip: 'Ondersteunde betaalsystemen en gateways', val1: 'Stripe + Creditcards', val2: 'Stripe + Mollie + iDEAL + Bancontact', val3: 'Alle Gateways + Zakelijke SEPA Incasso' },
                        { label: 'Systeem-API\'s & Webhooks Toegang', tip: 'Koppeling met externe bedrijfssoftware en ERP', val1: 'Basis Webhooks', val2: 'Volledige REST API\'s & Documentatie', val3: 'Volledige Core API\'s + Custom Services' },
                        { label: 'White-Label Branding Rechten', tip: 'Mogelijkheid tot volledige eigen merkuitstraling', val1: '"Powered by CoreSync" Badge', val2: 'Eigen Kleuren, Logo & Domein', val3: '100% White-Label (Geen CoreSync Sporen)' }
                    ]
                },
                {
                    name: '🤝 4. SLA & Executive Begeleiding',
                    rows: [
                        { label: 'Contractueel Gegarandeerde Uptime (SLA)', tip: 'Gegarandeerde beschikbaarheid met contractuele boeteclausules', val1: '99.5% Standaard Beschikbaarheid', val2: '99.9% Hoge Beschikbaarheid', val3: '99.98% Mission-Critical SLA' },
                        { label: 'Technische Reactietijd Ondersteuning', tip: 'Maximale reactietijd bij operationele vragen en storingen', val1: 'Binnen 24 Uur (Tickets)', val2: 'Binnen 4 Uur (E-mail + WhatsApp)', val3: 'Binnen 15 Minuten (24/7 VIP Hotline)' },
                        { label: 'Teamtraining & Kennisoverdracht', tip: 'Interactieve implementatiesessies voor medewerkers', val1: 'Digitale Documentatiesuite', val2: '2 Interactieve Zoom-Sessies', val3: 'Onbeperkt op Locatie in Amsterdam of Online' },
                        { label: 'Toegewijde Solutions Architect', tip: 'Vaste contactpersoon die uw digitale groei begeleidt', val1: '—', val2: 'Halfjaarlijkse Systeemaudit', val3: 'Senior Enterprise Solutions Architect' }
                    ]
                }
            ],
            guarantees: [
                '14-Dagen Niet-Goed-Geld-Terug Tevredenheidsgarantie',
                'Officieel Nederlands Contract ter Bescherming van Intellectueel Eigendom',
                'Flexibel Schalen en Wijzigen van Plannen op Ieder Moment'
            ],
            b2bQuoteBtn: 'Vraag Zakelijke Maatwerkofferte Aan (B2B) →'
        }
    },
    de: {
        trust: {
            title: 'Europäische Unternehmens-Compliance & <span>Souveräne Cloud-Standards</span>',
            subtitle: 'Rechtlich verbindliche europäische Zertifizierungen, Enterprise-SLA-Garantien und souveräne Cloud-Infrastruktur mit Sitz in Amsterdam, Niederlande.',
            clickVerify: 'Klicken Sie auf ein Compliance-Siegel, um technische Parameter und Rechtsnormen einzusehen',
            verifyLinkText: 'Technische Spezifikationen Einsehen',
            badges: [
                { id: 'gdpr', code: 'DSGVO EU 2016/679', status: 'Zertifiziert & Konform ✓', title: 'Europäischer Datenschutz (DSGVO)', desc: 'Strikte Einhaltung der europäischen Datenschutzgesetze, lückenlose Verschlüsselung und Ausschluss unautorisierter Telemetrie.' },
                { id: 'btw', code: 'Belastingdienst BTW', status: 'Steuerlich Konform ✓', title: 'Niederländische & EU-Steuerstandards', desc: 'Zertifizierte PEPPOL BIS 3.0 E-Rechnungen und automatisierte MwSt/BTW-Berechnung (9% & 21%) für den EU-Binnenmarkt.' },
                { id: 'amsix', code: 'AMS-IX Tier 3+', status: 'Amsterdam Infrastruktur ✓', title: 'Amsterdam Souveräner Cloud-Knotenpunkt', desc: 'Enterprise-Server direkt am Amsterdam Internet Exchange (AMS-IX) Tier 3+ Rechenzentrum für Sub-5ms Latenz in Westeuropa.' },
                { id: 'sla', code: '99.98% SLA', status: 'Mission Critical ✓', title: 'Hochverfügbarkeits-SLA', desc: 'Vertraglich garantierte 99.98% Systemverfügbarkeit mit aktiver Disaster-Recovery und < 15 Min. Ausfallwiederherstellung.' },
                { id: 'iso', code: 'ISO 27001 / SOC 2', status: 'Informationssicherheit ✓', title: 'Sicherheit & Risikomanagement', desc: 'Konsequente Ausrichtung an ISO/IEC 27001-Vorgaben und SOC 2 Type II-Richtlinien für unternehmensweites Risikomanagement.' },
                { id: 'zeroknowledge', code: 'Zero-Knowledge', status: 'Souveräne Verschlüsselung ✓', title: 'Kryptographische Zero-Knowledge', desc: 'Dedizierte Datenbanken mit kundenkontrollierten Schlüsseln (BYOK), ohne jegliche Hintertüren für Dritte.' }
            ],
            footerLegal: 'S&R CoreSync Solutions B.V. unterliegt vollumfänglich niederländischem und EU-Recht.',
            certBtn: 'Unternehmens-Compliance-Dossier Anfordern (PDF) →'
        },
        matrix: {
            pill: 'Vollständige Architektur- und Leistungsmatrix 2026',
            title: 'Vergleichen Sie <span>Enterprise-Cloud-Tarife</span> mit Präzision',
            subtitle: 'Wählen Sie die ideale Cloud-Architektur für Ihr Unternehmen in Europa. Sparen Sie 20% bei jährlicher Zahlungsweise plus Konzernrabatte für Holding-Strukturen.',
            annualBtn: 'Jährliche Abrechnung',
            annualSave: '20% Sparen',
            monthlyBtn: 'Monatliche Abrechnung',
            entityLabel: 'Unternehmen / Einheiten:',
            entity1: 'Einzelne Einheit',
            entity2: '2 - 3 Einheiten (-10%)',
            entity4: 'Holding 4+ (-20%)',
            thFeatures: 'Architekturspezifikationen & Standards',
            thSub: 'Detaillierter Vergleich über Infrastruktur, Compliance, KI und Enterprise SLAs',
            starterName: 'Core Starter',
            starterDesc: 'Für aufstrebende Unternehmen und fokussierte Einzelprojekte',
            proName: 'Business Pro',
            proDesc: 'Für mittelständische Firmen und expandierende Organisationen',
            proBadge: 'Beliebteste Wahl // Flagship',
            enterpriseName: 'Sovereign Enterprise',
            enterpriseDesc: 'Für Konzerne und Holdings mit höchsten Souveränitätsansprüchen',
            ctaStarter: 'Tarif via VIP WhatsApp buchen',
            ctaPro: 'Cloud-Bereitstellung jetzt starten ★',
            ctaEnterprise: 'Souveräne Architekturberatung anfordern 🛡️',
            categories: [
                {
                    name: '🌐 1. Cloud-Infrastruktur & AMS-IX Hosting',
                    rows: [
                        { label: 'Rechenzentrumsknoten & Serverstandort', tip: 'Primärer Hosting-Standort für souveräne Cloud-Workloads', val1: 'Amsterdam Tier 3+ (Geteilt)', val2: 'Amsterdam Dedizierter VPS-Knoten', val3: 'Souveränes Isoliertes Cluster (Physisch)' },
                        { label: 'Hochgeschwindigkeits-NVMe Cloud-Speicher', tip: 'Schneller Speicher für Unternehmensdaten und Datenbanken', val1: '50 GB NVMe', val2: '250 GB Ultraschnelle NVMe', val3: 'Unbegrenzt (Scale-on-Demand)' },
                        { label: 'Monatlicher Datentransfer & Globales CDN', tip: 'Inkludiertes Datenvolumen und europäisches Caching', val1: '100.000 Aufrufe / Monat', val2: '500.000 Aufrufe + Europa-CDN', val3: 'Unbegrenzt + Global Anycast CDN' },
                        { label: 'Mandanten-Architekturmodell', tip: 'Grad der Datenbankunabhängigkeit und Datentrennung', val1: 'Logische Software-Isolation', val2: 'Dedizierte Private Datenbank', val3: 'Dedizierte Single-Tenant 100%' }
                    ]
                },
                {
                    name: '🛡️ 2. Sicherheit & Regulatorische Compliance',
                    rows: [
                        { label: 'EU-Datenschutz-Grundverordnung (DSGVO)', tip: 'Einhaltung der VO (EU) 2016/679 und individuelle AVVs', val1: '✓ Zertifizierter Standard', val2: '✓ Erweitert + Individueller AV-Vertrag', val3: '✓ Souveräne Zero-Knowledge' },
                        { label: 'Steuerliche Konformität (MwSt / BTW)', tip: 'Automatisierte Steuerberechnung und PEPPOL-Rechnungen', val1: 'Digitale Basis-Rechnungen', val2: 'Automatisierte MwSt + PEPPOL BIS Billing', val3: 'Vollständige ERP- & Bankanbindung' },
                        { label: 'Kryptographisches Schlüsselmanagement', tip: 'Eigentum und Kontrolle über Verschlüsselungsschlüssel', val1: 'AES-256 Geteilte Architektur', val2: 'TLS 1.3 + Gehobene SSL-Zertifikate', val3: 'Kunden-Eigene KMS-Schlüssel (BYOK)' },
                        { label: 'Notfallwiederherstellung & Redundanz', tip: 'Geografische Replikation und Wiederherstellungsgeschwindigkeit', val1: 'Wöchentliches Cloud-Backup', val2: 'Tägliches Multi-Zone Backup', val3: 'Echtzeit-Kontinuierlich (RPO < 5 Min.)' }
                    ]
                },
                {
                    name: '⚡ 3. Enterprise KI & Systemintegrationen',
                    rows: [
                        { label: 'Enterprise KI-Assistent (Copilot RAG)', tip: 'Trainiertes Sprachmodell auf Basis interner Dokumente', val1: '—', val2: '✓ Standard Kundenservice RAG', val3: '✓ Souveränes Modell auf Ihren Unternehmensdaten' },
                        { label: 'Europäische Zahlungsmethoden', tip: 'Unterstützte Zahlungsanbieter und Gateways', val1: 'Stripe + Kreditkarten', val2: 'Stripe + Mollie + iDEAL + Bancontact', val3: 'Alle Gateways + SEPA-Firmenlastschrift' },
                        { label: 'System-APIs & Webhooks Zugriff', tip: 'Schnittstellen zu Drittsystemen und Legacy-Software', val1: 'Basis Webhooks', val2: 'Vollständige REST APIs & Dokumentation', val3: 'Vollständige Core APIs + Custom Services' },
                        { label: 'White-Label Branding-Rechte', tip: 'Nutzung unter eigenem Markenauftritt ohne Plattformverweis', val1: '"Powered by CoreSync" Siegel', val2: 'Eigene Farben, Logo & Domain', val3: '100% White-Label (Keine CoreSync Referenz)' }
                    ]
                },
                {
                    name: '🤝 4. SLA & Vorstands-Concierge',
                    rows: [
                        { label: 'Vertraglich Garantierte Uptime (SLA)', tip: 'Garantierte Verfügbarkeit mit Konventionalstrafen', val1: '99.5% Standardverfügbarkeit', val2: '99.9% Hohe Verfügbarkeit', val3: '99.98% Mission-Critical SLA' },
                        { label: 'Reaktionszeiten Technischer Support', tip: 'Maximaler Zeitrahmen bis zur Bearbeitung kritischer Anfragen', val1: 'Innerhalb von 24 Std. (Tickets)', val2: 'Innerhalb von 4 Std. (E-Mail + WhatsApp)', val3: 'Innerhalb von 15 Min. (24/7 VIP-Hotline)' },
                        { label: 'Mitarbeiterschulung & Wissenstransfer', tip: 'Praktische Einführung und Workshops für Teams', val1: 'Digitale Dokumentationssuite', val2: '2 Interaktive Live-Zoom-Sessions', val3: 'Unbegrenzt vor Ort in Amsterdam oder Remote' },
                        { label: 'Dedizierter Solutions Architect', tip: 'Fester technischer Experte für die digitale Weiterentwicklung', val1: '—', val2: 'Halbjährliches Architektur-Audit', val3: 'Senior Enterprise Solutions Architect' }
                    ]
                }
            ],
            guarantees: [
                '14-Tage Geld-zurück-Garantie bei Unzufriedenheit',
                'Offizieller niederländischer Rechtsvertrag zum Schutz aller IP-Rechte',
                'Jederzeitige Skalierbarkeit und Tarifwechsel ohne Ausfallzeiten'
            ],
            b2bQuoteBtn: 'Individuelles Enterprise-Angebot Anfordern (B2B) →'
        }
    }
};

function buildTrustRibbonHtml(data) {
    const cardsHtml = data.badges.map(b => {
        const iconDef = CARD_ICONS[b.id] || CARD_ICONS.gdpr;
        const greenClass = iconDef.isGreen ? ' sr-trust-icon-box--green' : '';

        return `                    <!-- Badge: ${b.code} -->
                    <div class="sr-trust-card" data-compliance="${b.id}" role="button" tabindex="0" aria-label="Verify ${b.code}">
                        <div class="sr-trust-icon-box${greenClass}">
                            ${iconDef.svg}
                        </div>
                        <div class="sr-trust-content">
                            <div class="sr-trust-badge-row">
                                <span class="sr-trust-code">${b.code}</span>
                                <span class="sr-trust-status">${b.status}</span>
                            </div>
                            <h3 class="sr-trust-card-title">${b.title}</h3>
                            <p class="sr-trust-card-desc">${b.desc}</p>
                            <span class="sr-trust-verify-link">
                                <span>${data.verifyLinkText}</span>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </span>
                        </div>
                    </div>`;
    }).join('\n\n');

    return `
        <!-- European Sovereign Trust Ribbon & Compliance Suite -->
        <section class="sr-trust-ribbon-section" id="compliance" aria-label="European Enterprise Trust & Compliance Suite">
            <div class="container">
                <div class="sr-trust-header">
                    <div class="sr-trust-pill">
                        <span class="sr-trust-pill-dot"></span>
                        <span>SOVEREIGN CLOUD ARCHITECTURE // AMSTERDAM 2026</span>
                    </div>
                    <h2 class="sr-trust-heading">
                        ${data.title}
                    </h2>
                    <p class="sr-trust-subheading">
                        ${data.subtitle}
                    </p>
                    <div class="sr-trust-click-hint">
                        <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                        <span>${data.clickVerify}</span>
                    </div>
                </div>

                <div class="sr-trust-grid">
${cardsHtml}
                </div>

                <div class="sr-trust-legal-footer">
                    <span class="sr-trust-legal-icon">⚖️</span>
                    <span class="sr-trust-legal-text">${data.footerLegal}</span>
                    <a href="https://wa.me/31687764998?text=Hello%20S%26R%20CoreSync%2C%20we%20would%20like%20to%20request%20the%20official%20Corporate%20Compliance%20Dossier." target="_blank" rel="noopener noreferrer" class="sr-trust-audit-link">
                        ${data.certBtn}
                    </a>
                </div>
            </div>
        </section>
    `;
}

function buildTierMatrixHtml(data) {
    let categoriesHtml = '';
    data.categories.forEach(cat => {
        categoriesHtml += `
                                <tr class="sr-tier-category-row">
                                    <td colspan="4">
                                        ${cat.name}
                                    </td>
                                </tr>
        `;
        cat.rows.forEach(r => {
            categoriesHtml += `
                                <tr class="sr-tier-row">
                                    <td>
                                        <span class="sr-tier-feature-label">${r.label}</span>
                                        <span class="sr-tier-feature-tooltip">${r.tip}</span>
                                    </td>
                                    <td class="sr-tier-val-col">${r.val1}</td>
                                    <td class="sr-tier-val-col featured">${r.val2}</td>
                                    <td class="sr-tier-val-col"><span class="sr-tier-val-highlight">${r.val3}</span></td>
                                </tr>
            `;
        });
    });

    const guaranteesHtml = data.guarantees.map(g => `
                            <div class="sr-tier-guarantee-item">
                                <span class="sr-tier-guarantee-icon"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg></span>
                                <span>${g}</span>
                            </div>
    `).join('\n');

    return `
                <!-- Enterprise Tier Matrix & Institutional Calculator -->
                <div class="sr-tier-matrix-section" id="tier-matrix" aria-label="Enterprise Tier Matrix & Institutional Comparison">
                    <div class="sr-tier-header">
                        <div class="sr-tier-pill">
                            <span class="sr-tier-pill-dot"></span>
                            <span>${data.pill}</span>
                        </div>
                        <h3 class="sr-tier-title">
                            ${data.title}
                        </h3>
                        <p class="sr-tier-subtitle">
                            ${data.subtitle}
                        </p>
                    </div>

                    <!-- Controls Hub: Billing cycle + Entity discount -->
                    <div class="sr-tier-controls-hub">
                        <div class="sr-tier-billing-toggle">
                            <button type="button" class="sr-tier-toggle-btn active" data-billing="annual">
                                <span>${data.annualBtn}</span>
                                <span class="sr-tier-save-badge">${data.annualSave}</span>
                            </button>
                            <button type="button" class="sr-tier-toggle-btn" data-billing="monthly">
                                <span>${data.monthlyBtn}</span>
                            </button>
                        </div>

                        <div class="sr-tier-entities-picker">
                            <span class="sr-tier-entities-label">${data.entityLabel}</span>
                            <div class="sr-tier-entities-btns">
                                <button type="button" class="sr-tier-entity-btn active" data-entities="1">${data.entity1}</button>
                                <button type="button" class="sr-tier-entity-btn" data-entities="2">${data.entity2}</button>
                                <button type="button" class="sr-tier-entity-btn" data-entities="4">${data.entity4}</button>
                            </div>
                        </div>
                    </div>

                    <!-- Comparison Table -->
                    <div class="sr-tier-table-wrapper">
                        <table class="sr-tier-table">
                            <thead>
                                <tr>
                                    <th class="sr-tier-th-features">
                                        <div class="sr-tier-features-heading">${data.thFeatures}</div>
                                        <div class="sr-tier-features-sub">${data.thSub}</div>
                                    </th>

                                    <!-- Tier 1: Starter -->
                                    <th class="sr-tier-th-col">
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">${data.starterName}</h4>
                                            <p class="sr-tier-desc">${data.starterDesc}</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-starter">1,192</span>
                                                    <span class="sr-tier-period" id="tier-period-starter">/ month</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-starter">€1,490</span>
                                                <div class="sr-tier-billed-note" id="tier-note-starter">${data.annualSave}</div>
                                            </div>
                                            <a href="https://wa.me/31687764998" id="tier-cta-starter" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--glass">
                                                <span>${data.ctaStarter}</span>
                                            </a>
                                        </div>
                                    </th>

                                    <!-- Tier 2: Pro (Featured) -->
                                    <th class="sr-tier-th-col featured">
                                        <div class="sr-tier-ribbon-badge">${data.proBadge}</div>
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">${data.proName}</h4>
                                            <p class="sr-tier-desc">${data.proDesc}</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-pro">2,312</span>
                                                    <span class="sr-tier-period" id="tier-period-pro">/ month</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-pro">€2,890</span>
                                                <div class="sr-tier-billed-note" id="tier-note-pro">${data.annualSave}</div>
                                            </div>
                                            <a href="https://wa.me/31687764998" id="tier-cta-pro" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--primary">
                                                <span>${data.ctaPro}</span>
                                            </a>
                                        </div>
                                    </th>

                                    <!-- Tier 3: Enterprise -->
                                    <th class="sr-tier-th-col">
                                        <div class="sr-tier-card-head">
                                            <h4 class="sr-tier-name">${data.enterpriseName}</h4>
                                            <p class="sr-tier-desc">${data.enterpriseDesc}</p>
                                            <div class="sr-tier-price-box">
                                                <div class="sr-tier-price-main">
                                                    <span class="sr-tier-currency">€</span>
                                                    <span id="tier-price-enterprise">4,320</span>
                                                    <span class="sr-tier-period" id="tier-period-enterprise">/ month</span>
                                                </div>
                                                <span class="sr-tier-original-price" id="tier-orig-enterprise">€5,400</span>
                                                <div class="sr-tier-billed-note" id="tier-note-enterprise">${data.annualSave}</div>
                                            </div>
                                            <a href="https://wa.me/31687764998" id="tier-cta-enterprise" target="_blank" rel="noopener noreferrer" class="sr-tier-action-btn sr-tier-action-btn--glass">
                                                <span>${data.ctaEnterprise}</span>
                                            </a>
                                        </div>
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
${categoriesHtml}
                            </tbody>
                        </table>
                    </div>

                    <!-- Bottom Guarantees -->
                    <div class="sr-tier-bottom-bar">
                        <div class="sr-tier-guarantee-items">
${guaranteesHtml}
                        </div>

                        <a href="https://wa.me/31687764998?text=Hello%20S%26R%20CoreSync%2C%20we%20are%20requesting%20a%20custom%20B2B%20Enterprise%20Quotation." target="_blank" rel="noopener noreferrer" class="sr-tier-custom-quote-btn">
                            <span>${data.b2bQuoteBtn}</span>
                        </a>
                    </div>
                </div>
    `;
}

function processPortal(portal) {
    const filePath = path.join(projectRoot, portal.file);
    if (!fs.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        return;
    }

    let html = fs.readFileSync(filePath, 'utf8');
    const langData = CONTENT[portal.lang];

    // 1. Replace existing <section class="sr-trust-ribbon-section" id="compliance" ...>
    const newTrustHtml = buildTrustRibbonHtml(langData.trust);
    const trustRegex = /<section class="sr-trust-ribbon-section" id="compliance"[\s\S]*?<\/section>/;

    if (trustRegex.test(html)) {
        html = html.replace(trustRegex, newTrustHtml.trim());
        console.log(`[${portal.lang}] Replaced Trust Ribbon with exact luxury design system markup`);
    }

    // 2. Replace existing <div class="sr-tier-matrix-section" id="tier-matrix" ...>
    const newMatrixHtml = buildTierMatrixHtml(langData.matrix);
    const matrixRegex = /<!-- Enterprise Tier Matrix & Institutional Calculator -->[\s\S]*?<\/div>\s*<\/div>\s*(?=<\/div>\s*<\/div>\s*<\/section>)/;

    if (html.includes('id="tier-matrix"')) {
        const matrixSimpleRegex = /<div class="sr-tier-matrix-section" id="tier-matrix"[\s\S]*?<!-- Bottom Guarantees -->[\s\S]*?<\/div>\s*<\/div>/;
        if (matrixSimpleRegex.test(html)) {
            html = html.replace(matrixSimpleRegex, newMatrixHtml.trim());
            console.log(`[${portal.lang}] Updated Tier Matrix markup`);
        }
    }

    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`✓ Completed markup refresh for ${portal.file}`);
}

PORTALS.forEach(processPortal);
console.log('All European portals markup refreshed.');
