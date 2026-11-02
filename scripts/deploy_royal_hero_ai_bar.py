# -*- coding: utf-8 -*-
"""
Deploy Royal Hero AI Idea Prompt Bar & Voice Badge across all 29 index pages:
1. Root index.html (Arabic master)
2. All 28 localized index.html files
"""
import io, os, re

LANG_DATA = {
    'ar': {
        'dir': 'rtl',
        'arrow': '←',
        'placeholder': 'اكتب فكرة مشروعك هنا (مثال: متجر إلكتروني بهولندا، نظام ERP، تطبيق ذكاء اصطناعي...)',
        'submit_text': 'حلل فكرتي بالـ AI ⚡',
        'mic_title': 'تحدث بفكرة مشروعك بالصوت التفاعلي',
        'badge_text': 'خطط لمشروعك بالصوت التفاعلي • المهندس الذكي بانتظارك',
        'badge_title': 'خطط لمشروعك بالصوت فوراً عبر محرك الذكاء الاصطناعي السيادي'
    },
    'ckb': {
        'dir': 'rtl',
        'arrow': '←',
        'placeholder': 'بیرۆکەی پڕۆژەکەت لێرە بنووسە (وەک: فرۆشگای ئۆنلاین، سیستەمی ERP، ئەپی زیرەکی دەستکرد)...',
        'submit_text': 'شیکردنەوە بە AI ⚡',
        'mic_title': 'بیرۆکەی پڕۆژەکەت بە دەنگ بڵێ',
        'badge_text': 'پڕۆژەکەت بە دەنگ پلاندانێ • ئەندازیاری AI ئامادەیە',
        'badge_title': 'پڕۆژەکەت بە دەنگ دابنێ لە ڕێگەی زیرەکی دەستکرد'
    },
    'ku': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Fikra projeya xwe li vir binivîse (mînak: Dikana serhêl, ERP, sepana AI)...',
        'submit_text': 'Bi AI analîz bike ⚡',
        'mic_title': 'Fikra projeya xwe bi deng bêje',
        'badge_text': 'Projeya xwe bi deng plan bike • Endezyarê AI amade ye',
        'badge_title': 'Bi deng projeya xwe plan bike'
    },
    'en': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Type your project idea here (e.g. E-Commerce store, Cloud ERP, AI SaaS)...',
        'submit_text': 'Analyze with AI ⚡',
        'mic_title': 'Speak your project idea with interactive voice',
        'badge_text': 'Plan your project with interactive voice • AI Engineer ready',
        'badge_title': 'Plan your project instantly with Sovereign AI Voice Engine'
    },
    'nl': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Typ hier uw projectidee (bijv. E-commerce webshop, Cloud ERP, AI-app)...',
        'submit_text': 'Analyseer met AI ⚡',
        'mic_title': 'Spreek uw projectidee in met interactieve stem',
        'badge_text': 'Plan uw project met interactieve stem • AI-ingenieur staat klaar',
        'badge_title': 'Plan uw project direct met de soevereine AI-spraakengine'
    },
    'de': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Geben Sie Ihre Projektidee hier ein (z. B. E-Commerce-Shop, Cloud ERP, KI-App)...',
        'submit_text': 'Mit KI analysieren ⚡',
        'mic_title': 'Sprechen Sie Ihre Projektidee per Sprachassistent ein',
        'badge_text': 'Projekt per Sprachassistent planen • KI-Ingenieur steht bereit',
        'badge_title': 'Planen Sie Ihr Projekt sofort mit der souveränen KI-Sprachengine'
    },
    'fr': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Saisissez votre idée de projet ici (ex. Boutique e-commerce, ERP Cloud, App IA)...',
        'submit_text': 'Analyser avec l\'IA ⚡',
        'mic_title': 'Exprimez votre idée de projet vocalement',
        'badge_text': 'Planifiez votre projet à la voix • Ingénieur IA disponible',
        'badge_title': 'Planifiez votre projet instantanément avec l\'IA vocale souveraine'
    },
    'es': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Escriba su idea de proyecto aquí (ej. Tienda online, ERP en la nube, App IA)...',
        'submit_text': 'Analizar con IA ⚡',
        'mic_title': 'Hable de su idea de proyecto por voz interactiva',
        'badge_text': 'Planifique su proyecto por voz • Ingeniero de IA listo',
        'badge_title': 'Planifique su proyecto al instante con el motor de IA de voz'
    },
    'it': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Scrivi qui la tua idea di progetto (es. E-commerce, Cloud ERP, App IA)...',
        'submit_text': 'Analizza con l\'IA ⚡',
        'mic_title': 'Racconta la tua idea a voce interattiva',
        'badge_text': 'Pianifica il tuo progetto con la voce • Ingegnere IA pronto',
        'badge_title': 'Pianifica istantaneamente con il motore vocale IA'
    },
    'pt': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Digite sua ideia de projeto aqui (ex. Loja virtual, Cloud ERP, App de IA)...',
        'submit_text': 'Analisar com IA ⚡',
        'mic_title': 'Fale a sua ideia de projeto por voz interativa',
        'badge_text': 'Planeje seu projeto por voz • Engenheiro de IA pronto',
        'badge_title': 'Planeje seu projeto instantaneamente com IA por voz'
    },
    'tr': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Proje fikrinizi buraya yazın (örn. E-ticaret mağazası, Bulut ERP, Yapay Zeka)...',
        'submit_text': 'Yapay Zeka ile Analiz Et ⚡',
        'mic_title': 'Proje fikrinizi sesli olarak anlatın',
        'badge_text': 'Projenizi sesli olarak planlayın • Yapay Zeka Mühendisi hazır',
        'badge_title': 'Projenizi egemen Yapay Zeka Ses Motoru ile hemen planlayın'
    },
    'el': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Πληκτρολογήστε την ιδέα σας εδώ (π.χ. E-shop, Cloud ERP, AI App)...',
        'submit_text': 'Ανάλυση με AI ⚡',
        'mic_title': 'Μιλήστε για την ιδέα του έργου σας',
        'badge_text': 'Σχεδιάστε το έργο σας με φωνή • Μηχανικός AI έτοιμος',
        'badge_title': 'Σχεδιάστε άμεσα το έργο σας με την κυρίαρχη μηχανή AI'
    },
    'pl': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Wpisz tutaj swój pomysł na projekt (np. Sklep e-commerce, Cloud ERP, AI App)...',
        'submit_text': 'Analizuj z AI ⚡',
        'mic_title': 'Opowiedz o swoim pomyśle głosowo',
        'badge_text': 'Zaplanuj projekt głosowo • Inżynier AI czeka',
        'badge_title': 'Zaplanuj swój projekt natychmiast z suwerennym silnikiem AI'
    },
    'sv': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Skriv din projektidé här (t.ex. E-handelsbutik, Moln-ERP, AI-app)...',
        'submit_text': 'Analysera med AI ⚡',
        'mic_title': 'Tala in din projektidé med röst',
        'badge_text': 'Planera ditt projekt med röst • AI-ingenjör redo',
        'badge_title': 'Planera ditt projekt direkt med suverän röst-AI'
    },
    'da': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Skriv din projektidé her (f.eks. E-handelsbutik, Cloud ERP, AI-app)...',
        'submit_text': 'Analyser med AI ⚡',
        'mic_title': 'Tal din projektidé ind med stemme',
        'badge_text': 'Planlæg dit projekt med stemme • AI-ingeniør klar',
        'badge_title': 'Planlæg dit projekt med suveræn stemme-AI'
    },
    'no': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Skriv prosjektideen din her (f.eks. Nettbutikk, Sky-ERP, AI-app)...',
        'submit_text': 'Analyser med AI ⚡',
        'mic_title': 'Snakk inn prosjektideen din med stemme',
        'badge_text': 'Planlegg prosjektet ditt med stemme • AI-ingeniør klar',
        'badge_title': 'Planlegg prosjektet ditt direkte med suveren stemme-AI'
    },
    'fi': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Kirjoita projektisi idea tähän (esim. Verkkokauppa, Pilvi-ERP, AI-sovellus)...',
        'submit_text': 'Analysoi tekoälyllä ⚡',
        'mic_title': 'Kerro projekti-ideasi äänellä',
        'badge_text': 'Suunnittele projektisi äänellä • AI-insinööri valmiina',
        'badge_title': 'Suunnittele projektisi heti suvereenilla ääni-AI-moottorilla'
    },
    'cs': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Zadejte svůj nápad na projekt sem (např. E-shop, Cloud ERP, AI aplikace)...',
        'submit_text': 'Analyzovat s AI ⚡',
        'mic_title': 'Řekněte svůj nápad hlasem',
        'badge_text': 'Naplánujte projekt hlasem • AI inženýr připraven',
        'badge_title': 'Naplánujte svůj projekt okamžitě s hlasovou AI'
    },
    'sk': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Zadajte svoj nápad na projekt sem (napr. E-shop, Cloud ERP, AI aplikácia)...',
        'submit_text': 'Analyzovať s AI ⚡',
        'mic_title': 'Povedzte svoj nápad hlasom',
        'badge_text': 'Naplánujte projekt hlasom • AI inžinier pripravený',
        'badge_title': 'Naplánujte svoj projekt okamžite s hlasovou AI'
    },
    'ro': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Scrieți ideea de proiect aici (ex. Magazin online, Cloud ERP, Aplicație AI)...',
        'submit_text': 'Analizează cu AI ⚡',
        'mic_title': 'Rostiți ideea de proiect vocal',
        'badge_text': 'Planificați proiectul vocal • Inginer AI gata',
        'badge_title': 'Planificați proiectul instantaneu cu motorul vocal de IA'
    },
    'bg': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Въведете идеята си за проект тук (напр. Онлайн магазин, Cloud ERP, AI приложение)...',
        'submit_text': 'Анализ с AI ⚡',
        'mic_title': 'Изговорете идеята за проекта си с глас',
        'badge_text': 'Планирайте проекта си с глас • AI инженерът е готов',
        'badge_title': 'Планирайте проекта си незабавно със суверенния AI гласов двигател'
    },
    'hu': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Írja be projektötletét ide (pl. Webáruház, Cloud ERP, MI alkalmazás)...',
        'submit_text': 'Elemzés MI-vel ⚡',
        'mic_title': 'Mondja el projektötletét hanggal',
        'badge_text': 'Tervezze meg projektjét hanggal • MI mérnök készen áll',
        'badge_title': 'Tervezze meg projektjét azonnal a szuverén MI hangmotorral'
    },
    'hr': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Upišite ideju projekta ovdje (npr. Web trgovina, Cloud ERP, AI aplikacija)...',
        'submit_text': 'Analiziraj uz AI ⚡',
        'mic_title': 'Izgovorite ideju projekta glasom',
        'badge_text': 'Planirajte projekt glasom • AI inženjer spreman',
        'badge_title': 'Planirajte svoj projekt odmah uz suvereni AI glasovni motor'
    },
    'sl': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Vnesite svojo projektno idejo sem (npr. Spletna trgovina, Oblačni ERP, AI aplikacija)...',
        'submit_text': 'Analiziraj z AI ⚡',
        'mic_title': 'Povejte svojo idejo z glasom',
        'badge_text': 'Načrtujte projekt z glasom • AI inženir pripravljen',
        'badge_title': 'Načrtujte svoj projekt takoj s suverenim AI glasovnim motorjem'
    },
    'et': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Sisestage oma projekti idee siia (nt E-pood, Pilve-ERP, AI rakendus)...',
        'submit_text': 'Analüüsi AI-ga ⚡',
        'mic_title': 'Rääkige oma projekti ideest häälega',
        'badge_text': 'Planeerige projekt häälega • AI insener valmis',
        'badge_title': 'Planeerige oma projekt koheselt hääle AI abil'
    },
    'lv': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Ievadiet sava projekta ideju šeit (piem., E-veikals, Mākoņa ERP, AI lietotne)...',
        'submit_text': 'Analizēt ar AI ⚡',
        'mic_title': 'Pastāstiet par projekta ideju ar balsi',
        'badge_text': 'Plānojiet projektu ar balsi • AI inženieris gatavs',
        'badge_title': 'Plānojiet savu projektu uzreiz ar suverēno balss AI dzinēju'
    },
    'lt': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Įveskite savo projekto idėją čia (pvz., El. parduotuvė, Debesų ERP, AI programėlė)...',
        'submit_text': 'Analizuoti su AI ⚡',
        'mic_title': 'Ištarkite savo projekto idėją balsu',
        'badge_text': 'Planuokite projektą balsu • AI inžinierius pasiruošęs',
        'badge_title': 'Planuokite savo projektą iškart su balso AI varikliu'
    },
    'mt': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Ikteb l-idea tal-proġett tiegħek hawnhekk (eż. Ħanut online, Cloud ERP, App AI)...',
        'submit_text': 'Analizza bl-AI ⚡',
        'mic_title': 'Għid l-idea tal-proġett tiegħek bil-vuċi',
        'badge_text': 'Ippjana l-proġett tiegħek bil-vuċi • Inġinier AI lest',
        'badge_title': 'Ippjana l-proġett tiegħek istantanjament bil-vuċi AI'
    },
    'ga': {
        'dir': 'ltr',
        'arrow': '→',
        'placeholder': 'Clóscríobh do smaoineamh tionscadail anseo (m.sh. Siopa ríomhthráchtála, Cloud ERP, AI App)...',
        'submit_text': 'Déan anailís le AI ⚡',
        'mic_title': 'Labhair faoi do smaoineamh tionscadail le guth',
        'badge_text': 'Pleanáil do thionscadal le guth • Innealtóir AI réidh',
        'badge_title': 'Pleanáil do thionscadal láithreach le guth-AI'
    }
}

def make_ai_idea_bar_html(lang):
    d = LANG_DATA.get(lang, LANG_DATA['en'])
    return f'''                                    <!-- شريط كتابة الفكرة وهندسة المشروع الفوري بالذكاء الاصطناعي (Hero AI Idea Prompt Bar) -->
                                    <div class="hero-ai-idea-bar" id="heroAiIdeaBar">
                                        <form class="hero-ai-idea-form" data-sr-call="submitHeroAiIdea" data-sr-on="submit" data-sr-prevent="1">
                                            <div class="hero-ai-idea-icon-wrap" aria-hidden="true">
                                                <span class="hero-ai-idea-sparkle">✨</span>
                                            </div>
                                            <div class="hero-ai-idea-input-wrap">
                                                <input type="text" id="heroAiIdeaInput" class="hero-ai-idea-input" placeholder="{d['placeholder']}" autocomplete="off" aria-label="Project Idea AI Input">
                                            </div>
                                            <div class="hero-ai-idea-btns">
                                                <button type="button" class="hero-ai-idea-mic-btn" data-sr-call="openVoicePlannerFromHero" title="{d['mic_title']}" aria-label="{d['mic_title']}">
                                                    <span class="hero-ai-mic-icon">🎙️</span>
                                                </button>
                                                <button type="submit" class="hero-ai-idea-submit-btn" title="{d['submit_text']}" aria-label="{d['submit_text']}">
                                                    <span class="hero-ai-submit-text">{d['submit_text']}</span>
                                                    <span class="hero-ai-submit-arrow">{d['arrow']}</span>
                                                </button>
                                            </div>
                                        </form>
                                    </div>'''

def make_voice_badge_html(lang):
    d = LANG_DATA.get(lang, LANG_DATA['en'])
    return f'''                                    <!-- شارة خطط لمشروعك بالصوت والمساعد الذكي تحت الشعار الملكي متباعدة بأناقة -->
                                    <div class="hero-emblem-voice-badge-wrap">
                                        <button type="button" class="hero-emblem-voice-badge" data-sr-call="openAiVoicePlannerModal" title="{d['badge_title']}">
                                            <span class="emblem-voice-pulse">🎙️</span>
                                            <span>{d['badge_text']}</span>
                                            <span class="emblem-voice-arrow">{d['arrow']}</span>
                                        </button>
                                    </div>'''

def update_page(filepath, lang):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. Insert hero AI Idea Bar after hero-reference__actions
    if 'hero-ai-idea-bar' not in content:
        # Check if hero-trust-metrics-strip is present
        trust_pattern = re.search(r'([ \t]*)(<div class="hero-trust-metrics-strip")', content)
        if trust_pattern:
            bar_html = make_ai_idea_bar_html(lang)
            insert_pos = trust_pattern.start()
            content = content[:insert_pos] + bar_html + "\n" + content[insert_pos:]
            modified = True
            print(f"[{lang}] Inserted hero-ai-idea-bar before hero-trust-metrics-strip")
        else:
            # Match closing </div> of hero-reference__actions
            m = re.search(r'(<div class="hero-reference__actions[^>]*>.*?</div>)', content, re.DOTALL)
            if m:
                bar_html = make_ai_idea_bar_html(lang)
                insert_pos = m.end()
                content = content[:insert_pos] + "\n" + bar_html + content[insert_pos:]
                modified = True
                print(f"[{lang}] Inserted hero-ai-idea-bar after hero-reference__actions")
            else:
                print(f"[{lang}] ERROR: Could not locate hero-reference__actions!")
    else:
        print(f"[{lang}] hero-ai-idea-bar already present")
        
    # 2. Insert voice badge wrap under 3D emblem
    if 'hero-emblem-voice-badge-wrap' not in content:
        emblem_match = re.search(r'(<div class="hero-emblem-frame">.*?</div>\s*</div>)', content, re.DOTALL)
        if emblem_match:
            badge_html = make_voice_badge_html(lang)
            end_pos = emblem_match.end()
            content = content[:end_pos] + "\n" + badge_html + content[end_pos:]
            modified = True
            print(f"[{lang}] Inserted hero-emblem-voice-badge-wrap under hero-emblem-frame")
        else:
            print(f"[{lang}] WARNING: hero-emblem-frame closing not found!")
    else:
        print(f"[{lang}] hero-emblem-voice-badge-wrap already present")
        
    if modified:
        with io.open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"[{lang}] Successfully saved {filepath}")
    else:
        print(f"[{lang}] No changes needed")

def main():
    # Update Arabic master
    print("--- Updating Root index.html (Arabic master) ---")
    update_page('index.html', 'ar')
    
    # Update all 28 sub-languages
    for lang in sorted(LANG_DATA.keys()):
        if lang == 'ar':
            continue
        p = os.path.join(lang, 'index.html')
        if os.path.exists(p):
            print(f"--- Updating {p} ({lang}) ---")
            update_page(p, lang)
        else:
            print(f"File not found: {p}")

if __name__ == '__main__':
    main()
