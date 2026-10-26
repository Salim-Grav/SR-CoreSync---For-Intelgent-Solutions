/**
 * S&R CoreSync For Intelligent Solutions — Sovereign AI Readiness Engine (shared AR / EN / NL / DE)
 * Renders the 5-axis assessment, live radar, diagnosis, WhatsApp report,
 * and a smart deep-link to the White-Label License Calculator and SLA Generator.
 */
(function () {
    'use strict';

    const LANG = (document.documentElement.getAttribute('lang') || 'ar').slice(0, 2).toLowerCase();
    const IS_SUBDIR = /\/(en|nl|de)\//.test(window.location.pathname.toLowerCase());
    const ROOT = IS_SUBDIR ? '../' : './';

    // ════════════════════════════════════════════════════════════
    //  I18N DICTIONARY
    // ════════════════════════════════════════════════════════════
    const I18N = {
        ar: {
            ui: {
                initial: 'مستوى أولي', ideal: 'مستوى سيادي مثالي', pts: 'نقطة',
                startTitle: 'أجب على الأسئلة لرؤية نتيجتك',
                startDesc: 'سيُحدَّث هذا الشريط تلقائياً مع كل إجابة. النتيجة الكاملة = 100 نقطة.',
                diagStart: 'أجب على الأسئلة للحصول على تشخيص مخصص لمؤسستك.',
                diagTotal: (t, d) => `نقطتك الإجمالية: ${t}/100. أبرز توصية: ${d}`,
                diagPriority: (n, d) => `الأولوية الفورية — ${n}: ${d}`,
                sectorAxis: 'خطوة تمهيدية — قطاع المؤسسة',
                sectorQ: 'ما القطاع الذي تعمل فيه مؤسستك؟',
                sectorDesc: 'لا يؤثر على النقاط، لكنه يحدد المنصة الأنسب في عرض السعر المقترح.',
                recommend: (p, t) => `🎯 التوصية: منصة <strong>${p}</strong> بباقة <strong>${t}</strong> — بناءً على نتيجتك وقطاعك.`,
                waIntro: 'مرحباً S&R CoreSync For Intelligent Solutions،\n\nأكملت تقييم الجاهزية الرقمية:\n\n',
                waTotal: '📊 النقطة الإجمالية', waLevel: '🏷️ المستوى', waSector: '🏢 القطاع',
                waOutro: 'أودّ الاطلاع على خارطة طريق مخصصة لمؤسستي.'
            },
            radar: ['بنية تحتية', 'بيانات', 'ذكاء اصطناعي', 'أتمتة', 'كوادر'],
            tiers: { starter: 'Starter', professional: 'Professional', enterprise: 'Enterprise' },
            sectors: [
                { id: 'community', label: 'جالية / منظمة مجتمعية / جمعية', platform: 'civicsync' },
                { id: 'health', label: 'عيادة / مركز طبي / رعاية صحية', platform: 'healthbridge' },
                { id: 'food', label: 'مخبز / مطعم / توزيع غذائي', platform: 'omnibakery' },
                { id: 'other', label: 'قطاع آخر (تجارة، خدمات، تعليم...)', platform: 'civicsync' }
            ],
            axes: [
                { name: 'البنية التحتية السحابية', q: 'ما مستوى البنية التحتية الرقمية الحالية لمؤسستك؟',
                  d: 'تشمل الخوادم، منصات الاستضافة، قواعد البيانات، وأنظمة الاحتياطي والاسترداد.',
                  o: ['لا توجد بنية تحتية رقمية — نعمل ورقياً بالكامل', 'خوادم محلية (On-Premise) بدون سحابة', 'سحابة مشتركة جزئياً (Microsoft 365 / Google Workspace)', 'سحابة هجينة مع نسخ احتياطي منتظم', 'بنية سحابية سيادية متكاملة مع SLA موثوق'] },
                { name: 'حوكمة البيانات والامتثال', q: 'ما مدى التزام مؤسستك بمعايير حماية البيانات الأوروبية (GDPR)؟',
                  d: 'يشمل سياسات الخصوصية، عقود معالجة البيانات (DPA)، وإجراءات الاستجابة للخروقات.',
                  o: ['لا توجد سياسة واضحة لحماية البيانات', 'نعرف GDPR لكن لم نطبق إجراءات رسمية', 'لدينا سياسة خصوصية أساسية ونماذج موافقة', 'امتثال جزئي مع مراجعات دورية', 'امتثال كامل + DPA موثق + تشفير AES-256 + Zero-Knowledge'] },
                { name: 'اعتماد الذكاء الاصطناعي', q: 'ما مستوى تكامل الذكاء الاصطناعي في عمليات مؤسستك؟',
                  d: 'يشمل أدوات الأتمتة، المساعدين الذكيين، تحليل البيانات، وعمليات اتخاذ القرار.',
                  o: ['لا نستخدم أي أدوات ذكاء اصطناعي', 'نستخدم ChatGPT أو أدوات مماثلة بشكل شخصي غير رسمي', 'نستخدم أتمتة أساسية (نماذج تلقائية، روبوتات دردشة بسيطة)', 'نظام AI مدمج في عمليات محددة (خدمة عملاء، تقارير)', 'AI مؤسسي متكامل مدرب على بيانات الشركة (RAG / Copilot)'] },
                { name: 'أتمتة العمليات والكفاءة', q: 'ما نسبة العمليات الإدارية والمالية التي تعمل بشكل آلي؟',
                  d: 'يشمل الفوترة، الرواتب، المخزون، إدارة العملاء CRM، وتقارير الأداء.',
                  o: ['معظم العمليات يدوية (Excel + ورق)', 'بعض التطبيقات المتخصصة غير المتكاملة', 'نظام ERP أساسي يغطي الفوترة والمحاسبة', 'ERP متكامل مع CRM وتقارير تلقائية', 'أتمتة شاملة متصلة بواجهات API مع جميع الأنظمة'] },
                { name: 'الكوادر البشرية والثقافة الرقمية', q: 'ما مستوى الكفاءة الرقمية لدى فريق مؤسستك؟',
                  d: 'يشمل مستوى التدريب التقني، مقاومة التغيير، والقيادة الداعمة للتحول الرقمي.',
                  o: ['مقاومة عالية للتغيير، الفريق يفضل الأساليب التقليدية', 'وعي محدود بالأدوات الرقمية، تدريب متفرق', 'فريق متقبل للتغيير مع تدريب أساسي متاح', 'ثقافة رقمية راسخة مع برامج تطوير مستمرة', 'قيادة رقمية استراتيجية + CDO/CTO + برامج ابتكار داخلية'] }
            ],
            axisLabel: i => `المحور ${i + 1} — `,
            levels: [
                ['مرحلة الانطلاق الرقمي', 'مؤسستك في بداية رحلتها الرقمية. الفرصة ضخمة والوقت مثالي للبناء على أسس سيادية صلبة.'],
                ['مرحلة التأسيس الرقمي', 'لديك قاعدة أولية. مع تكامل منصة S&R CoreSync ستتضاعف كفاءتك في أقل من 90 يوماً.'],
                ['مرحلة النضج التدريجي', 'تقدم ملحوظ! بعض الثغرات في الامتثال أو الأتمتة. نستطيع سدها خلال مرحلة واحدة.'],
                ['مرحلة التسارع المؤسسي', 'مؤسستك في وضع متقدم. خطوات التحسين المتبقية ستحقق ميزة تنافسية قوية في السوق الأوروبي.'],
                ['مرحلة السيادة الرقمية الكاملة', 'ممتاز! مؤسستك تعمل بمعايير الجيل القادم. نرشح الارتقاء لباقة Sovereign Enterprise لحماية هذا التفوق.']
            ],
            diag: {
                infra: ['البنية التحتية هي الأولوية القصوى. ننصح بالبدء بحزمة Core Starter للانتقال الآمن للسحابة.', 'البنية الحالية تحتاج لتحديث وتوحيد. الترقية للسحابة السيادية تُحسّن الأداء بنسبة 60%.', 'بنية تحتية متينة! ننصح بتقييم تحديث منافذ API للتكامل مع منظومة S&R CoreSync.'],
                data: ['الامتثال GDPR ضرورة قانونية في أوروبا. مخاطر الغرامات قد تصل لـ €20 مليون. ابدأ فوراً.', 'قاعدة جيدة! إضافة DPA مخصص وتشفير متقدم ستُرقّي مستواك لـ "Advanced Compliance".', 'امتثال متقدم. ننصح بتفعيل نظام Zero-Knowledge لضمان الاستقلالية الكاملة للبيانات.'],
                ai: ['مؤسستك تفقد ميزة تنافسية يومياً. محرك AI RAG يمكن تفعيله خلال أسبوعين.', 'بداية واعدة! الانتقال لـ AI مؤسسي مدرب على بياناتك سيحدث نقلة نوعية في الإنتاجية.', 'ريادة في AI! ننصح بتفعيل Sovereign AI Model لضمان استقلالية البيانات وزيادة الدقة.'],
                ops: ['الأتمتة ستوفر 40% من وقت الفريق. منصة OmniBakery ERP مصممة خصيصاً لهذا التحول.', 'تكامل الأنظمة الحالية مع ERP موحد سيُلغي الازدواجية ويُسرّع دورة الفوترة.', 'أتمتة ممتازة! ننصح بتفعيل Core APIs للتكامل مع منصات الدفع الأوروبية (iDEAL/SEPA).'],
                team: ['الاستثمار في الكوادر هو الأهم. برامجنا التدريبية المباشرة في أمستردام تُحدث فارقاً خلال 30 يوماً.', 'فريقك جاهز للتعلم. جلستا Zoom التفاعليتان المشمولتان في Business Pro ستُسرّعان التبني.', 'ثقافة رقمية راسخة. ننصح بتعيين Solutions Architect مخصص لمواصلة مسيرة الابتكار.']
            }
        },

        en: {
            ui: {
                initial: 'Initial level', ideal: 'Ideal sovereign level', pts: 'pts',
                startTitle: 'Answer the questions to see your result',
                startDesc: 'This banner updates live with every answer. Maximum score = 100 points.',
                diagStart: 'Answer the questions to receive a tailored diagnosis for your organisation.',
                diagTotal: (t, d) => `Your overall score: ${t}/100. Key recommendation: ${d}`,
                diagPriority: (n, d) => `Immediate priority — ${n}: ${d}`,
                sectorAxis: 'Preliminary step — Your sector',
                sectorQ: 'Which sector does your organisation operate in?',
                sectorDesc: 'Does not affect your score, but determines the best-fit platform in your suggested quote.',
                recommend: (p, t) => `🎯 Recommendation: <strong>${p}</strong> on the <strong>${t}</strong> tier — based on your score and sector.`,
                waIntro: 'Hello S&R CoreSync For Intelligent Solutions,\n\nI completed the Digital Readiness assessment:\n\n',
                waTotal: '📊 Overall score', waLevel: '🏷️ Level', waSector: '🏢 Sector',
                waOutro: 'I would like to receive a tailored roadmap for my organisation.'
            },
            radar: ['Infrastructure', 'Data', 'AI', 'Automation', 'People'],
            tiers: { starter: 'Starter', professional: 'Professional', enterprise: 'Enterprise' },
            sectors: [
                { id: 'community', label: 'Community / NGO / Association', platform: 'civicsync' },
                { id: 'health', label: 'Clinic / Medical centre / Healthcare', platform: 'healthbridge' },
                { id: 'food', label: 'Bakery / Restaurant / Food distribution', platform: 'omnibakery' },
                { id: 'other', label: 'Other sector (retail, services, education...)', platform: 'civicsync' }
            ],
            axes: [
                { name: 'Cloud Infrastructure', q: 'What is the current level of your digital infrastructure?',
                  d: 'Includes servers, hosting platforms, databases, and backup & recovery systems.',
                  o: ['No digital infrastructure — fully paper-based', 'On-premise servers without cloud', 'Partially shared cloud (Microsoft 365 / Google Workspace)', 'Hybrid cloud with regular backups', 'Fully integrated sovereign cloud with a reliable SLA'] },
                { name: 'Data Governance & Compliance', q: 'How compliant is your organisation with European data protection (GDPR)?',
                  d: 'Covers privacy policies, Data Processing Agreements (DPA), and breach response procedures.',
                  o: ['No clear data protection policy', 'We know GDPR but have no formal procedures', 'Basic privacy policy and consent forms', 'Partial compliance with periodic reviews', 'Full compliance + documented DPA + AES-256 + Zero-Knowledge'] },
                { name: 'AI Adoption', q: 'How deeply is AI integrated into your operations?',
                  d: 'Includes automation tools, smart assistants, data analytics, and decision-making.',
                  o: ['We use no AI tools at all', 'Informal personal use of ChatGPT or similar', 'Basic automation (auto-forms, simple chatbots)', 'AI embedded in specific processes (support, reporting)', 'Enterprise AI trained on company data (RAG / Copilot)'] },
                { name: 'Process Automation & Efficiency', q: 'What share of your administrative and financial processes is automated?',
                  d: 'Covers invoicing, payroll, inventory, CRM, and performance reporting.',
                  o: ['Mostly manual (Excel + paper)', 'Some specialised, non-integrated apps', 'Basic ERP covering invoicing and accounting', 'Integrated ERP with CRM and automated reports', 'End-to-end automation connected via APIs to all systems'] },
                { name: 'People & Digital Culture', q: 'What is the digital competence level of your team?',
                  d: 'Covers technical training, resistance to change, and leadership support for transformation.',
                  o: ['High resistance to change; team prefers traditional methods', 'Limited awareness of digital tools, ad-hoc training', 'Open to change with basic training available', 'Established digital culture with continuous development', 'Strategic digital leadership + CDO/CTO + internal innovation'] }
            ],
            axisLabel: i => `Axis ${i + 1} — `,
            levels: [
                ['Digital Launch Stage', 'Your organisation is at the start of its digital journey. A huge opportunity to build on solid sovereign foundations.'],
                ['Digital Foundation Stage', 'You have an initial base. With S&R CoreSync integration your efficiency can double in under 90 days.'],
                ['Progressive Maturity Stage', 'Notable progress! Some gaps in compliance or automation that we can close in a single phase.'],
                ['Enterprise Acceleration Stage', 'Your organisation is advanced. The remaining steps will deliver a strong competitive edge in the European market.'],
                ['Full Digital Sovereignty', 'Excellent! You operate at next-generation standards. We recommend Sovereign Enterprise to protect this lead.']
            ],
            diag: {
                infra: ['Infrastructure is the top priority. Start with the Core Starter package for a secure cloud migration.', 'Your current setup needs modernisation. Moving to sovereign cloud improves performance by up to 60%.', 'Solid infrastructure! Consider upgrading API endpoints to integrate with the S&R CoreSync ecosystem.'],
                data: ['GDPR compliance is a legal requirement in Europe — fines can reach €20 million. Start now.', 'Good foundation! A dedicated DPA and advanced encryption will lift you to "Advanced Compliance".', 'Advanced compliance. We recommend enabling Zero-Knowledge for full data independence.'],
                ai: ['You are losing competitive ground daily. An AI RAG engine can be live within two weeks.', 'Promising start! Enterprise AI trained on your data will transform productivity.', 'AI leadership! Activate a Sovereign AI Model for data independence and higher accuracy.'],
                ops: ['Automation can save 40% of team time. OmniBakery ERP is built exactly for this shift.', 'Unifying your systems in one ERP removes duplication and speeds up invoicing.', 'Excellent automation! Enable Core APIs to connect European payment rails (iDEAL/SEPA).'],
                team: ['People are the key investment. Our hands-on Amsterdam training makes a difference within 30 days.', 'Your team is ready to learn. The two interactive Zoom sessions in Business Pro accelerate adoption.', 'Strong digital culture. A dedicated Solutions Architect will sustain your innovation.']
            }
        },

        nl: {
            ui: {
                initial: 'Startniveau', ideal: 'Ideaal soeverein niveau', pts: 'pnt',
                startTitle: 'Beantwoord de vragen om uw resultaat te zien',
                startDesc: 'Deze balk wordt bij elk antwoord live bijgewerkt. Maximale score = 100 punten.',
                diagStart: 'Beantwoord de vragen voor een diagnose op maat van uw organisatie.',
                diagTotal: (t, d) => `Uw totaalscore: ${t}/100. Belangrijkste advies: ${d}`,
                diagPriority: (n, d) => `Directe prioriteit — ${n}: ${d}`,
                sectorAxis: 'Voorbereidende stap — Uw sector',
                sectorQ: 'In welke sector is uw organisatie actief?',
                sectorDesc: 'Telt niet mee in de score, maar bepaalt het best passende platform in uw voorgestelde offerte.',
                recommend: (p, t) => `🎯 Advies: <strong>${p}</strong> met het <strong>${t}</strong>-pakket — op basis van uw score en sector.`,
                waIntro: 'Hallo S&R CoreSync For Intelligent Solutions,\n\nIk heb de Digitale Gereedheidsscan voltooid:\n\n',
                waTotal: '📊 Totaalscore', waLevel: '🏷️ Niveau', waSector: '🏢 Sector',
                waOutro: 'Graag ontvang ik een roadmap op maat voor mijn organisatie.'
            },
            radar: ['Infrastructuur', 'Data', 'AI', 'Automatisering', 'Mensen'],
            tiers: { starter: 'Starter', professional: 'Professional', enterprise: 'Enterprise' },
            sectors: [
                { id: 'community', label: 'Gemeenschap / Stichting / Vereniging', platform: 'civicsync' },
                { id: 'health', label: 'Kliniek / Medisch centrum / Zorg', platform: 'healthbridge' },
                { id: 'food', label: 'Bakkerij / Restaurant / Voedseldistributie', platform: 'omnibakery' },
                { id: 'other', label: 'Andere sector (retail, diensten, onderwijs...)', platform: 'civicsync' }
            ],
            axes: [
                { name: 'Cloudinfrastructuur', q: 'Wat is het huidige niveau van uw digitale infrastructuur?',
                  d: 'Omvat servers, hostingplatforms, databases en back-up- en herstelsystemen.',
                  o: ['Geen digitale infrastructuur — volledig op papier', 'Lokale servers (on-premise) zonder cloud', 'Deels gedeelde cloud (Microsoft 365 / Google Workspace)', 'Hybride cloud met regelmatige back-ups', 'Volledig geïntegreerde soevereine cloud met betrouwbare SLA'] },
                { name: 'Datagovernance & Compliance', q: 'In hoeverre voldoet uw organisatie aan de AVG (GDPR)?',
                  d: 'Omvat privacybeleid, verwerkersovereenkomsten (DPA) en procedures bij datalekken.',
                  o: ['Geen duidelijk databeschermingsbeleid', 'We kennen de AVG maar hebben geen formele procedures', 'Basaal privacybeleid en toestemmingsformulieren', 'Gedeeltelijke naleving met periodieke reviews', 'Volledige naleving + DPA + AES-256 + Zero-Knowledge'] },
                { name: 'AI-adoptie', q: 'Hoe diep is AI geïntegreerd in uw bedrijfsprocessen?',
                  d: 'Omvat automatiseringstools, slimme assistenten, data-analyse en besluitvorming.',
                  o: ['We gebruiken geen AI-tools', 'Informeel persoonlijk gebruik van ChatGPT e.d.', 'Basisautomatisering (formulieren, eenvoudige chatbots)', 'AI ingebed in specifieke processen (support, rapportage)', 'Enterprise-AI getraind op bedrijfsdata (RAG / Copilot)'] },
                { name: 'Procesautomatisering & Efficiëntie', q: 'Welk deel van uw administratieve en financiële processen is geautomatiseerd?',
                  d: 'Omvat facturatie, salarisadministratie, voorraad, CRM en prestatierapportage.',
                  o: ['Grotendeels handmatig (Excel + papier)', 'Enkele losse, niet-gekoppelde apps', 'Basis-ERP voor facturatie en boekhouding', 'Geïntegreerd ERP met CRM en automatische rapporten', 'Volledige automatisering via API-koppelingen met alle systemen'] },
                { name: 'Mensen & Digitale Cultuur', q: 'Wat is het digitale competentieniveau van uw team?',
                  d: 'Omvat technische training, weerstand tegen verandering en leiderschap bij transformatie.',
                  o: ['Hoge weerstand; team geeft de voorkeur aan traditionele methoden', 'Beperkt bewustzijn, sporadische training', 'Open voor verandering met basistraining', 'Gevestigde digitale cultuur met continue ontwikkeling', 'Strategisch digitaal leiderschap + CDO/CTO + innovatieprogramma\'s'] }
            ],
            axisLabel: i => `As ${i + 1} — `,
            levels: [
                ['Digitale Startfase', 'Uw organisatie staat aan het begin van haar digitale reis. Een uitgelezen kans om op soevereine fundamenten te bouwen.'],
                ['Digitale Fundamentfase', 'Er is een eerste basis. Met S&R CoreSync kan uw efficiëntie binnen 90 dagen verdubbelen.'],
                ['Progressieve Volwassenheid', 'Duidelijke vooruitgang! Enkele hiaten in compliance of automatisering die we in één fase dichten.'],
                ['Enterprise Versnelling', 'Uw organisatie is gevorderd. De resterende stappen leveren een sterk concurrentievoordeel op de Europese markt.'],
                ['Volledige Digitale Soevereiniteit', 'Uitstekend! U werkt volgens next-gen standaarden. Wij adviseren Sovereign Enterprise om deze voorsprong te borgen.']
            ],
            diag: {
                infra: ['Infrastructuur heeft topprioriteit. Begin met het Core Starter-pakket voor een veilige cloudmigratie.', 'Uw huidige omgeving vraagt om modernisering. Soevereine cloud verbetert de prestaties tot 60%.', 'Solide infrastructuur! Overweeg API-upgrades voor integratie met het S&R CoreSync-ecosysteem.'],
                data: ['AVG-naleving is wettelijk verplicht — boetes tot €20 miljoen. Begin direct.', 'Goede basis! Een eigen DPA en geavanceerde encryptie tillen u naar "Advanced Compliance".', 'Geavanceerde compliance. Activeer Zero-Knowledge voor volledige data-onafhankelijkheid.'],
                ai: ['U verliest dagelijks terrein. Een AI RAG-engine kan binnen twee weken live zijn.', 'Veelbelovend! Enterprise-AI getraind op uw data verhoogt de productiviteit sterk.', 'AI-koploper! Activeer een Sovereign AI Model voor onafhankelijkheid en hogere nauwkeurigheid.'],
                ops: ['Automatisering bespaart 40% teamtijd. OmniBakery ERP is precies hiervoor gebouwd.', 'Eén geïntegreerd ERP elimineert dubbel werk en versnelt facturatie.', 'Uitstekende automatisering! Activeer Core APIs voor iDEAL/SEPA-betalingen.'],
                team: ['Investeren in mensen is cruciaal. Onze trainingen in Amsterdam maken binnen 30 dagen verschil.', 'Uw team is leergierig. De twee Zoom-sessies in Business Pro versnellen de adoptie.', 'Sterke digitale cultuur. Een vaste Solutions Architect houdt de innovatie gaande.']
            }
        },

        de: {
            ui: {
                initial: 'Einstiegsniveau', ideal: 'Ideales souveränes Niveau', pts: 'Pkt.',
                startTitle: 'Beantworten Sie die Fragen, um Ihr Ergebnis zu sehen',
                startDesc: 'Diese Leiste aktualisiert sich mit jeder Antwort. Maximale Punktzahl = 100.',
                diagStart: 'Beantworten Sie die Fragen für eine maßgeschneiderte Diagnose Ihrer Organisation.',
                diagTotal: (t, d) => `Ihre Gesamtpunktzahl: ${t}/100. Wichtigste Empfehlung: ${d}`,
                diagPriority: (n, d) => `Sofortige Priorität — ${n}: ${d}`,
                sectorAxis: 'Vorbereitender Schritt — Ihre Branche',
                sectorQ: 'In welcher Branche ist Ihre Organisation tätig?',
                sectorDesc: 'Fließt nicht in die Punktzahl ein, bestimmt aber die passende Plattform im Angebotsvorschlag.',
                recommend: (p, t) => `🎯 Empfehlung: <strong>${p}</strong> im <strong>${t}</strong>-Paket — basierend auf Ergebnis und Branche.`,
                waIntro: 'Hallo S&R CoreSync For Intelligent Solutions,\n\nich habe den Digital-Readiness-Check abgeschlossen:\n\n',
                waTotal: '📊 Gesamtpunktzahl', waLevel: '🏷️ Stufe', waSector: '🏢 Branche',
                waOutro: 'Ich wünsche mir eine maßgeschneiderte Roadmap für meine Organisation.'
            },
            radar: ['Infrastruktur', 'Daten', 'KI', 'Automatisierung', 'Team'],
            tiers: { starter: 'Starter', professional: 'Professional', enterprise: 'Enterprise' },
            sectors: [
                { id: 'community', label: 'Gemeinschaft / NGO / Verein', platform: 'civicsync' },
                { id: 'health', label: 'Klinik / Praxis / Gesundheitswesen', platform: 'healthbridge' },
                { id: 'food', label: 'Bäckerei / Restaurant / Lebensmittelvertrieb', platform: 'omnibakery' },
                { id: 'other', label: 'Andere Branche (Handel, Dienstleistung, Bildung...)', platform: 'civicsync' }
            ],
            axes: [
                { name: 'Cloud-Infrastruktur', q: 'Wie ist der aktuelle Stand Ihrer digitalen Infrastruktur?',
                  d: 'Umfasst Server, Hosting-Plattformen, Datenbanken sowie Backup- und Wiederherstellungssysteme.',
                  o: ['Keine digitale Infrastruktur — vollständig papierbasiert', 'Lokale Server (On-Premise) ohne Cloud', 'Teilweise geteilte Cloud (Microsoft 365 / Google Workspace)', 'Hybrid-Cloud mit regelmäßigen Backups', 'Vollintegrierte souveräne Cloud mit verlässlichem SLA'] },
                { name: 'Data Governance & Compliance', q: 'Wie gut erfüllt Ihre Organisation die DSGVO (GDPR)?',
                  d: 'Umfasst Datenschutzrichtlinien, AV-Verträge (DPA) und Verfahren bei Datenpannen.',
                  o: ['Keine klare Datenschutzrichtlinie', 'DSGVO bekannt, aber keine formalen Verfahren', 'Grundlegende Datenschutzerklärung und Einwilligungen', 'Teilweise Konformität mit regelmäßigen Audits', 'Volle Konformität + AVV + AES-256 + Zero-Knowledge'] },
                { name: 'KI-Einführung', q: 'Wie tief ist KI in Ihre Abläufe integriert?',
                  d: 'Umfasst Automatisierungstools, intelligente Assistenten, Datenanalyse und Entscheidungsfindung.',
                  o: ['Wir nutzen keinerlei KI-Tools', 'Informelle private Nutzung von ChatGPT o. Ä.', 'Basis-Automatisierung (Formulare, einfache Chatbots)', 'KI in bestimmten Prozessen (Support, Reporting)', 'Unternehmens-KI trainiert auf Firmendaten (RAG / Copilot)'] },
                { name: 'Prozessautomatisierung & Effizienz', q: 'Welcher Anteil Ihrer Verwaltungs- und Finanzprozesse ist automatisiert?',
                  d: 'Umfasst Rechnungsstellung, Lohnbuchhaltung, Lager, CRM und Leistungsberichte.',
                  o: ['Überwiegend manuell (Excel + Papier)', 'Einige isolierte Fachanwendungen', 'Basis-ERP für Rechnungen und Buchhaltung', 'Integriertes ERP mit CRM und automatischen Berichten', 'Durchgängige Automatisierung per API mit allen Systemen'] },
                { name: 'Team & digitale Kultur', q: 'Wie hoch ist die digitale Kompetenz Ihres Teams?',
                  d: 'Umfasst technische Schulung, Veränderungsbereitschaft und Führungsunterstützung.',
                  o: ['Hoher Widerstand; Team bevorzugt traditionelle Methoden', 'Geringes Bewusstsein, sporadische Schulungen', 'Offen für Wandel mit Basisschulungen', 'Etablierte digitale Kultur mit kontinuierlicher Entwicklung', 'Strategische digitale Führung + CDO/CTO + Innovationsprogramme'] }
            ],
            axisLabel: i => `Achse ${i + 1} — `,
            levels: [
                ['Digitale Startphase', 'Ihre Organisation steht am Anfang der digitalen Reise — die ideale Zeit, auf souveränen Fundamenten aufzubauen.'],
                ['Digitale Fundamentphase', 'Eine erste Basis ist vorhanden. Mit S&R CoreSync kann sich Ihre Effizienz in unter 90 Tagen verdoppeln.'],
                ['Fortschreitende Reife', 'Deutlicher Fortschritt! Einige Lücken bei Compliance oder Automatisierung, die wir in einer Phase schließen.'],
                ['Enterprise-Beschleunigung', 'Ihre Organisation ist weit fortgeschritten. Die letzten Schritte bringen einen starken Wettbewerbsvorteil in Europa.'],
                ['Volle digitale Souveränität', 'Hervorragend! Sie arbeiten nach Next-Gen-Standards. Wir empfehlen Sovereign Enterprise, um diesen Vorsprung zu sichern.']
            ],
            diag: {
                infra: ['Infrastruktur hat höchste Priorität. Starten Sie mit dem Core-Starter-Paket für eine sichere Cloud-Migration.', 'Ihre Umgebung braucht Modernisierung. Souveräne Cloud steigert die Leistung um bis zu 60%.', 'Solide Infrastruktur! Prüfen Sie API-Upgrades zur Integration in das S&R-CoreSync-Ökosystem.'],
                data: ['DSGVO-Konformität ist Pflicht — Bußgelder bis €20 Mio. Beginnen Sie sofort.', 'Gute Basis! Ein eigener AVV und starke Verschlüsselung bringen Sie auf "Advanced Compliance".', 'Fortgeschrittene Compliance. Aktivieren Sie Zero-Knowledge für volle Datenunabhängigkeit.'],
                ai: ['Sie verlieren täglich an Boden. Eine AI-RAG-Engine ist in zwei Wochen einsatzbereit.', 'Vielversprechend! Unternehmens-KI auf Ihren Daten steigert die Produktivität deutlich.', 'KI-Vorreiter! Aktivieren Sie ein Sovereign AI Model für Unabhängigkeit und höhere Präzision.'],
                ops: ['Automatisierung spart 40% Teamzeit. OmniBakery ERP ist genau dafür gebaut.', 'Ein einheitliches ERP beseitigt Doppelarbeit und beschleunigt die Rechnungsstellung.', 'Exzellente Automatisierung! Aktivieren Sie Core APIs für iDEAL/SEPA-Zahlungen.'],
                team: ['Menschen sind die wichtigste Investition. Unsere Schulungen in Amsterdam wirken binnen 30 Tagen.', 'Ihr Team ist lernbereit. Die zwei Zoom-Sessions in Business Pro beschleunigen die Einführung.', 'Starke digitale Kultur. Ein dedizierter Solutions Architect sichert Ihre Innovationskraft.']
            }
        }
    };

    const T = I18N[LANG] || I18N.ar;

    const AXIS_META = [
        { id: 'infra', icon: '🌐', iconClass: '',   scores: [5, 25, 50, 75, 100] },
        { id: 'data',  icon: '🛡️', iconClass: '',   scores: [5, 25, 50, 75, 100] },
        { id: 'ai',    icon: '⚡', iconClass: 'em', scores: [5, 30, 55, 80, 100] },
        { id: 'ops',   icon: '⚙️', iconClass: '',   scores: [5, 30, 55, 80, 100] },
        { id: 'team',  icon: '👥', iconClass: 'em', scores: [5, 30, 55, 80, 100] }
    ];
    const LEVEL_META = [
        { min: 0,  max: 20,  icon: '🔴', color: '#ef4444' },
        { min: 21, max: 40,  icon: '🟠', color: '#f97316' },
        { min: 41, max: 60,  icon: '🟡', color: '#f59e0b' },
        { min: 61, max: 80,  icon: '🟢', color: '#10b981' },
        { min: 81, max: 100, icon: '🏆', color: '#c5a880' }
    ];
    const PLATFORM_NAMES = { civicsync: 'S&R CivicSync™', healthbridge: 'S&R HealthBridge™', omnibakery: 'S&R OmniBakery™' };

    const AXES = AXIS_META.map((m, i) => ({ ...m, ...T.axes[i], axis: T.axisLabel(i) + T.axes[i].name }));

    // ── STATE ─────────────────────────────────────────────────
    const scores = { infra: 0, data: 0, ai: 0, ops: 0, team: 0 };
    let sector = null;

    const $ = id => document.getElementById(id);
    const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

    // ── RENDER ────────────────────────────────────────────────
    function renderQuestions() {
        const container = $('rd-questions-container');
        container.innerHTML = '';

        // Sector card (non-scored)
        const sectorCard = document.createElement('div');
        sectorCard.className = 'rd-q-card';
        sectorCard.id = 'rd-q-sector';
        sectorCard.innerHTML = `
            <div class="rd-q-header">
                <div class="rd-q-icon em">🏢</div>
                <div class="rd-q-meta">
                    <div class="rd-q-axis">${esc(T.ui.sectorAxis)}</div>
                    <div class="rd-q-text">${esc(T.ui.sectorQ)}</div>
                </div>
            </div>
            <p class="rd-q-desc">${esc(T.ui.sectorDesc)}</p>
            <div class="rd-options">${T.sectors.map(s => `
                <div class="rd-option" data-sector="${s.id}" role="button" tabindex="0" aria-label="${esc(s.label)}">
                    <div class="rd-option-radio"></div>
                    <div class="rd-option-content"><span class="rd-option-label">${esc(s.label)}</span></div>
                </div>`).join('')}
            </div>`;
        container.appendChild(sectorCard);

        AXES.forEach(axis => {
            const card = document.createElement('div');
            card.className = 'rd-q-card';
            card.id = `rd-q-${axis.id}`;
            const optionsHtml = axis.o.map((label, oi) => {
                const sc = axis.scores[oi];
                const hint = sc === 5 ? T.ui.initial : sc === 100 ? T.ui.ideal : `${sc} ${T.ui.pts}`;
                return `
                <div class="rd-option" data-axis="${axis.id}" data-score="${sc}" role="button" tabindex="0" aria-label="${esc(label)}">
                    <div class="rd-option-radio"></div>
                    <div class="rd-option-content">
                        <span class="rd-option-label">${esc(label)}</span>
                        <span class="rd-option-score">${esc(hint)}</span>
                    </div>
                </div>`;
            }).join('');
            card.innerHTML = `
                <div class="rd-q-header">
                    <div class="rd-q-icon ${axis.iconClass}">${axis.icon}</div>
                    <div class="rd-q-meta">
                        <div class="rd-q-axis">${esc(axis.axis)}</div>
                        <div class="rd-q-text">${esc(axis.q)}</div>
                    </div>
                </div>
                <p class="rd-q-desc">${esc(axis.d)}</p>
                <div class="rd-options">${optionsHtml}</div>`;
            container.appendChild(card);
        });

        $('rd-axes-bars').innerHTML = AXES.map(axis => `
            <div class="rd-axis-row">
                <div class="rd-axis-info">
                    <span class="rd-axis-name">${axis.icon} ${esc(axis.name)}</span>
                    <span class="rd-axis-val" id="rd-axval-${axis.id}">—</span>
                </div>
                <div class="rd-axis-bar"><div class="rd-axis-fill" id="rd-axfill-${axis.id}"></div></div>
            </div>`).join('');

        container.querySelectorAll('.rd-option').forEach(opt => {
            opt.addEventListener('click', () => selectOption(opt));
            opt.addEventListener('keydown', e => {
                if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectOption(opt); }
            });
        });
    }

    function selectOption(el) {
        el.closest('.rd-options').querySelectorAll('.rd-option').forEach(o => o.classList.remove('selected'));
        el.classList.add('selected');
        el.closest('.rd-q-card').classList.add('answered');
        if (el.dataset.sector) {
            sector = T.sectors.find(s => s.id === el.dataset.sector) || null;
        } else {
            scores[el.dataset.axis] = parseInt(el.dataset.score, 10);
        }
        update();
    }

    // ── RECOMMENDATION (Readiness → License Calculator) ────────
    function getRecommendation(total) {
        const platform = sector ? sector.platform : 'civicsync';
        const tier = total <= 40 ? 'starter' : total <= 75 ? 'professional' : 'enterprise';
        const sla = scores.data >= 75 || total > 75 ? 'sovereign' : total > 40 ? 'business' : 'standard';
        return { platform, tier, sla };
    }

    // ── UPDATE ────────────────────────────────────────────────
    function update() {
        const vals = AXES.map(a => scores[a.id]);
        const total = Math.round(vals.reduce((a, b) => a + b, 0) / AXES.length);
        const answered = vals.filter(v => v > 0).length;
        const pct = Math.round((answered / AXES.length) * 100);

        $('rd-progress-fill').style.width = pct + '%';
        $('rd-progress-pct').textContent = pct + '%';
        $('rd-total-score').textContent = total;

        AXES.forEach(axis => {
            const s = scores[axis.id];
            const fill = $(`rd-axfill-${axis.id}`);
            fill.style.width = s + '%';
            fill.className = 'rd-axis-fill ' + (s === 0 ? '' : s < 30 ? 'low' : s < 60 ? 'mid' : s < 90 ? 'high' : 'full');
            $(`rd-axval-${axis.id}`).textContent = s > 0 ? s + '%' : '—';
        });

        const li = Math.max(0, LEVEL_META.findIndex(l => total >= l.min && total <= l.max));
        const level = { ...LEVEL_META[li], title: T.levels[li][0], desc: T.levels[li][1] };
        if (answered > 0) {
            $('rd-maturity-icon').textContent = level.icon;
            $('rd-maturity-title').textContent = level.title;
            $('rd-maturity-desc').textContent = level.desc;
        }
        const pill = $('rd-maturity-pill');
        pill.textContent = total + ' / 100';
        pill.style.setProperty('--rd-level-color', level.color);

        updateDiagnosis(total);
        drawRadar(vals);
        updateWALink(total, level);
        updateQuoteLinks(total, answered);
    }

    function updateDiagnosis(total) {
        const answered = AXES.filter(a => scores[a.id] > 0);
        if (answered.length === 0) { $('rd-diagnosis-text').textContent = T.ui.diagStart; return; }
        const weakest = answered.reduce((p, c) => (scores[c.id] < scores[p.id] ? c : p));
        const s = scores[weakest.id];
        const diag = T.diag[weakest.id][s < 30 ? 0 : s < 70 ? 1 : 2];
        $('rd-diagnosis-text').textContent = answered.length === AXES.length
            ? T.ui.diagTotal(total, diag)
            : T.ui.diagPriority(weakest.name, diag);
    }

    function updateQuoteLinks(total, answered) {
        const rec = getRecommendation(total);
        const quoteBtn = $('rd-quote-btn');
        const box = $('rd-recommend');
        const slaBtn = $('rd-sla-btn');
        const complete = answered === AXES.length;

        if (quoteBtn) {
            quoteBtn.href = `${ROOT}whitelabel-calculator.html?platform=${rec.platform}&tier=${rec.tier}&source=readiness&score=${total}`;
            quoteBtn.classList.toggle('visible', complete);
        }
        if (box) {
            box.innerHTML = T.ui.recommend(PLATFORM_NAMES[rec.platform], T.tiers[rec.tier]);
            box.classList.toggle('visible', complete);
        }
        if (slaBtn) {
            const langDir = IS_SUBDIR ? '' : '';
            slaBtn.href = `${langDir}preview-sla-generator.html?sla=${rec.sla}&platform=${rec.platform}&source=readiness`;
        }
    }

    // ── RADAR ─────────────────────────────────────────────────
    function drawRadar(vals) {
        const canvas = $('rd-radar-canvas');
        const ctx = canvas.getContext('2d');
        const W = canvas.offsetWidth || 320, H = 300, dpr = window.devicePixelRatio || 1;
        canvas.width = W * dpr; canvas.height = H * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        const cx = W / 2, cy = H / 2 + 10, R = Math.min(W, H) * 0.35, N = vals.length;
        const ang = i => (Math.PI * 2 * i / N) - Math.PI / 2;
        ctx.clearRect(0, 0, W, H);

        [20, 40, 60, 80, 100].forEach(ring => {
            const r = (ring / 100) * R;
            ctx.beginPath();
            for (let i = 0; i < N; i++) {
                const x = cx + r * Math.cos(ang(i)), y = cy + r * Math.sin(ang(i));
                i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.strokeStyle = 'rgba(197, 168, 128, 0.12)'; ctx.lineWidth = 1; ctx.stroke();
            ctx.fillStyle = 'rgba(197, 168, 128, 0.35)'; ctx.font = '9px Alexandria, sans-serif'; ctx.textAlign = 'center';
            ctx.fillText(ring, cx + 4, cy - r + 12);
        });
        for (let i = 0; i < N; i++) {
            ctx.beginPath(); ctx.moveTo(cx, cy);
            ctx.lineTo(cx + R * Math.cos(ang(i)), cy + R * Math.sin(ang(i)));
            ctx.strokeStyle = 'rgba(197, 168, 128, 0.15)'; ctx.stroke();
        }
        ctx.beginPath();
        vals.forEach((v, i) => {
            const r = ((v || 0) / 100) * R, x = cx + r * Math.cos(ang(i)), y = cy + r * Math.sin(ang(i));
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        });
        ctx.closePath();
        const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
        grad.addColorStop(0, 'rgba(16, 185, 129, 0.45)'); grad.addColorStop(1, 'rgba(197, 168, 128, 0.15)');
        ctx.fillStyle = grad; ctx.fill();
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.85)'; ctx.lineWidth = 2; ctx.stroke();
        vals.forEach((v, i) => {
            const r = ((v || 0) / 100) * R;
            ctx.beginPath(); ctx.arc(cx + r * Math.cos(ang(i)), cy + r * Math.sin(ang(i)), 4, 0, Math.PI * 2);
            ctx.fillStyle = v >= 80 ? '#c5a880' : '#10b981'; ctx.fill();
            ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
        });
        ctx.font = 'bold 11px Alexandria, "Plus Jakarta Sans", sans-serif';
        ctx.fillStyle = 'rgba(232, 232, 232, 0.8)';
        for (let i = 0; i < N; i++) {
            const lx = cx + (R + 24) * Math.cos(ang(i)), ly = cy + (R + 24) * Math.sin(ang(i));
            ctx.textAlign = lx > cx + 5 ? 'start' : lx < cx - 5 ? 'end' : 'center';
            ctx.fillText(T.radar[i], lx, ly + 4);
        }
    }

    // ── WHATSAPP ──────────────────────────────────────────────
    function updateWALink(total, level) {
        const lines = AXES.filter(a => scores[a.id] > 0).map(a => `• ${a.name}: ${scores[a.id]}/100`);
        const msg = T.ui.waIntro + lines.join('\n') + '\n\n' +
            `${T.ui.waTotal}: ${total}/100\n${T.ui.waLevel}: ${level.title}\n` +
            (sector ? `${T.ui.waSector}: ${sector.label}\n` : '') + '\n' + T.ui.waOutro;
        $('rd-wa-btn').href = 'https://wa.me/31618111116?text=' + encodeURIComponent(msg);
    }

    // ── RESET ─────────────────────────────────────────────────
    function resetAll() {
        AXES.forEach(a => { scores[a.id] = 0; });
        sector = null;
        renderQuestions();
        $('rd-maturity-icon').textContent = '📊';
        $('rd-maturity-title').textContent = T.ui.startTitle;
        $('rd-maturity-desc').textContent = T.ui.startDesc;
        update();
        $('rd-maturity-pill').style.removeProperty('--rd-level-color');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ── INIT ──────────────────────────────────────────────────
    function init() {
        renderQuestions();
        $('rd-reset-btn').addEventListener('click', resetAll);
        update();
        $('rd-maturity-pill').style.removeProperty('--rd-level-color');
        let t;
        window.addEventListener('resize', () => {
            clearTimeout(t);
            t = setTimeout(() => drawRadar(AXES.map(a => scores[a.id])), 120);
        });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
