# -*- coding: utf-8 -*-
"""
S&R CoreSync - Deploy Top Hero & Header AI Voice Planner Call-to-Actions:
1. Header Actions: Next to #headerLiveDemoPill (.btn-header-voice-ai)
2. Hero Actions: Next to #hero-btn-demo (.hero-btn-voice-ai)
3. Under 3D Emblem: Floating interactive voice badge (.hero-emblem-voice-badge)
"""
import os
import re

INDEX_PATH = r"d:\I-Ai\App\S&R CoreSync For Intelligent Solutions\Project\index.html"

CSS_SNIPPET = """
/* ==========================================================================
   TOP HEADER & HERO VOICE PLANNER CTA BUTTONS (MILESTONE 36 EXTENSION)
   ========================================================================== */
.btn-header-voice-ai {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 5px 12px !important;
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.28) 0%, rgba(2, 7, 5, 0.95) 100%) !important;
    border: 1px solid rgba(197, 168, 128, 0.6) !important;
    color: #fff4da !important;
    border-radius: 999px !important;
    font-size: 0.76rem !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 0 14px rgba(197, 168, 128, 0.25) !important;
    white-space: nowrap !important;
    line-height: 1.2 !important;
    animation: voiceHeaderGlow 3s infinite alternate ease-in-out !important;
}

.btn-header-voice-ai:hover {
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.5) 0%, rgba(20, 15, 10, 0.98) 100%) !important;
    box-shadow: 0 0 24px rgba(197, 168, 128, 0.6) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}

@keyframes voiceHeaderGlow {
    0% { box-shadow: 0 0 10px rgba(197, 168, 128, 0.2); border-color: rgba(197, 168, 128, 0.45); }
    100% { box-shadow: 0 0 20px rgba(197, 168, 128, 0.65); border-color: #f3dfba; }
}

.voice-header-mic-icon {
    font-size: 13px !important;
    display: inline-block !important;
    animation: voiceMicPulse 1.8s infinite ease-in-out !important;
}

@keyframes voiceMicPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.22); }
    100% { transform: scale(1); }
}

/* Hero Action Voice Button */
.hero-btn-voice-ai {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.25) 0%, rgba(18, 14, 10, 0.95) 100%) !important;
    border: 1.5px solid #c5a880 !important;
    color: #fff4da !important;
    padding: 13px 24px !important;
    border-radius: 12px !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    box-shadow: 0 0 22px rgba(197, 168, 128, 0.35) !important;
    white-space: nowrap !important;
    position: relative !important;
    overflow: hidden !important;
    animation: heroVoicePulse 2.8s infinite alternate ease-in-out !important;
}

.hero-btn-voice-ai:hover {
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.48) 0%, rgba(35, 26, 18, 0.98) 100%) !important;
    box-shadow: 0 0 35px rgba(197, 168, 128, 0.7) !important;
    transform: translateY(-2px) scale(1.02) !important;
    color: #ffffff !important;
    border-color: #f3dfba !important;
}

@keyframes heroVoicePulse {
    0% { box-shadow: 0 0 16px rgba(197, 168, 128, 0.25); border-color: rgba(197, 168, 128, 0.6); }
    100% { box-shadow: 0 0 32px rgba(197, 168, 128, 0.65); border-color: #f3dfba; }
}

.hero-voice-icon-pulse {
    font-size: 16px !important;
    animation: voiceMicPulse 1.8s infinite ease-in-out !important;
}

/* Floating Under-Emblem Voice Badge */
.hero-emblem-voice-badge-wrap {
    margin-top: 18px !important;
    text-align: center !important;
    position: relative !important;
    z-index: 10 !important;
}

.hero-emblem-voice-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 18px !important;
    background: rgba(8, 12, 10, 0.88) !important;
    border: 1px solid rgba(197, 168, 128, 0.45) !important;
    border-radius: 999px !important;
    color: #f3dfba !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 16px rgba(197, 168, 128, 0.2) !important;
    transition: all 0.25s ease !important;
    backdrop-filter: blur(10px) !important;
}

.hero-emblem-voice-badge:hover {
    background: rgba(25, 20, 14, 0.95) !important;
    border-color: #f3dfba !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 25px rgba(197, 168, 128, 0.5) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}

.emblem-voice-pulse {
    font-size: 14px !important;
    animation: voiceMicPulse 1.8s infinite ease-in-out !important;
}

.emblem-voice-arrow {
    color: #c5a880 !important;
    transition: transform 0.2s ease !important;
}

[dir="rtl"] .hero-emblem-voice-badge:hover .emblem-voice-arrow {
    transform: translateX(-3px) !important;
}

@media (max-width: 768px) {
    .btn-header-voice-ai span:not(.voice-header-mic-icon) {
        display: none !important;
    }
    .btn-header-voice-ai {
        padding: 6px !important;
        border-radius: 50% !important;
        min-width: 32px !important;
        height: 32px !important;
        justify-content: center !important;
    }
}

@media (max-width: 480px) {
    .btn-header-voice-ai {
        display: none !important;
    }
    .hero-btn-voice-ai {
        width: 100% !important;
        justify-content: center !important;
    }
}
"""

def deploy():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add CSS before </style></head>
    if '.btn-header-voice-ai' not in html:
        style_pos = html.find('</style>\n</head>')
        if style_pos == -1:
            style_pos = html.find('</style>')
        if style_pos != -1:
            html = html[:style_pos] + CSS_SNIPPET + "\n" + html[style_pos:]
            print("[OK] Injected Voice CTA CSS styles.")

    # 2. Add Header Action Button next to #headerLiveDemoPill
    header_btn_code = """
                                <button type="button" class="tf-btn btn-header-voice-ai" id="headerVoiceAiBtn" onclick="openAiVoicePlannerModal()" data-sr-call="openAiVoicePlannerModal" title="خطط لمشروعك بالصوت فوراً عبر الذكاء الاصطناعي">
                                    <span class="voice-header-mic-icon">🎙️</span>
                                    <span>خطط لمشروعك بالصوت (AI Voice)</span>
                                </button>"""

    if 'id="headerVoiceAiBtn"' not in html:
        # Search for headerLiveDemoPill block
        pill_str = 'id="headerLiveDemoPill"'
        pill_idx = html.find(pill_str)
        if pill_idx != -1:
            # Find the closing </a>
            close_a = html.find('</a>', pill_idx)
            if close_a != -1:
                insert_pos = close_a + 4
                html = html[:insert_pos] + header_btn_code + html[insert_pos:]
                print("✓ Injected Header Voice AI button next to #headerLiveDemoPill.")

    # 3. Add Hero Action Button next to hero-btn-demo
    hero_btn_code = """
                                        <button type="button" class="tf-btn hero-reference__action hero-btn-voice-ai" id="heroVoiceAiBtn" onclick="openAiVoicePlannerModal()" data-sr-call="openAiVoicePlannerModal" title="خطط لمشروعك بالصوت فوراً عبر الذكاء الاصطناعي">
                                            <span class="hero-voice-icon-pulse">🎙️</span>
                                            <span>خطط لمشروعك بالصوت (AI Voice) ⚡</span>
                                        </button>"""

    if 'id="heroVoiceAiBtn"' not in html:
        hero_demo_str = 'class="tf-btn hero-reference__action hero-btn-demo hero-btn-primary-highlight"'
        hero_demo_idx = html.find(hero_demo_str)
        if hero_demo_idx != -1:
            close_a = html.find('</a>', hero_demo_idx)
            if close_a != -1:
                insert_pos = close_a + 4
                html = html[:insert_pos] + hero_btn_code + html[insert_pos:]
                print("✓ Injected Hero Action Voice AI button next to hero-btn-demo.")

    # 4. Add Floating Under-Emblem Voice Badge under hero-emblem-card-3d
    emblem_badge_code = """
                                    <!-- شارة المساعد الصوتي تحت الشعار الملكي -->
                                    <div class="hero-emblem-voice-badge-wrap">
                                        <button type="button" class="hero-emblem-voice-badge" onclick="openAiVoicePlannerModal()" data-sr-call="openAiVoicePlannerModal" title="تحدث بفكرة مشروعك وسيقوم الذكاء الاصطناعي ببناء الخطة فوراً">
                                            <span class="emblem-voice-pulse">🎙️</span>
                                            <span>تحدث بفكرة مشروعك | مهندس الـ AI بانتظارك</span>
                                            <span class="emblem-voice-arrow">←</span>
                                        </button>
                                    </div>"""

    if 'hero-emblem-voice-badge' not in html:
        card_end = html.find('</div>\n                                    </div>\n                                </div>\n                            </div>\n                        </div>')
        # Let's locate heroEmblemCard
        emblem_card_str = 'id="heroEmblemCard"'
        emblem_idx = html.find(emblem_card_str)
        if emblem_idx != -1:
            # find the closing </div> of heroEmblemCard
            # It contains hero-emblem-glare, then </div>, then </div>
            glare_idx = html.find('hero-emblem-glare', emblem_idx)
            if glare_idx != -1:
                # Find closing of card
                first_div = html.find('</div>', glare_idx)
                second_div = html.find('</div>', first_div + 6)
                third_div = html.find('</div>', second_div + 6)
                if third_div != -1:
                    insert_pos = third_div + 6
                    html = html[:insert_pos] + emblem_badge_code + html[insert_pos:]
                    print("✓ Injected Floating Under-Emblem Voice Badge.")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print("[OK] Successfully updated index.html with all 3 Voice CTA buttons!")

if __name__ == '__main__':
    deploy()
