import io

def remove_hero_badges(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We remove the voice badge wrap block
    pattern = '''                                    <!-- شارة خطط لمشروعك بالصوت والمساعد الذكي تحت الشعار الملكي متباعدة بأناقة -->
                                    <div class="hero-emblem-voice-badge-wrap">
                                        <button type="button" class="hero-emblem-voice-badge" onclick="openAiVoicePlannerModal()" data-sr-call="openAiVoicePlannerModal" title="خطط لمشروعك بالصوت فوراً عبر محرك الذكاء الاصطناعي السيادي">
                                            <span class="emblem-voice-pulse">🎙️</span>
                                            <span>خطط لمشروعك بالصوت التفاعلي • المهندس الذكي بانتظارك</span>
                                            <span class="emblem-voice-arrow">←</span>
                                        </button>
                                        <a href="developer-portal.html#avatarSection" class="hero-emblem-avatar-badge" title="تحدث مع النسخة الرقمية الذكية ثلاثية الأبعاد للمهندس سليم عزيزة">
                                            <span>✨</span>
                                            <span>المهندس سليم الرقمي • النسخة التفاعلية ثلاثية الأبعاد</span>
                                            <span>↗</span>
                                        </a>
                                    </div>'''

    if pattern in content:
        content = content.replace(pattern, '')
        with io.open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"Successfully removed hero badges from {filepath}")
    else:
        # Try with CRLF
        pattern_crlf = pattern.replace('\n', '\r\n')
        if pattern_crlf in content:
            content = content.replace(pattern_crlf, '')
            with io.open(filepath, 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(content)
            print(f"Successfully removed hero badges (CRLF) from {filepath}")
        else:
            print(f"Pattern not found in {filepath}")

remove_hero_badges('index.html')
remove_hero_badges('ckb/index.html')
