# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

css_rules = """
/* ==========================================================================
   Omnichannel Social Follow Rail & Hero 3D Emblem Polish
   ========================================================================== */
[dir="rtl"] .hero-reference__emblem-col {
    padding-left: clamp(50px, 7vw, 110px) !important;
    padding-right: 0 !important;
}
[dir="ltr"] .hero-reference__emblem-col {
    padding-right: clamp(50px, 7vw, 110px) !important;
    padding-left: 0 !important;
}
.hero-emblem-interactive-stage {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    max-width: 540px !important;
}
.hero-emblem-card-3d {
    margin: 0 auto !important;
}
.hero-emblem-actions-bar {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    margin-top: 32px !important;
    z-index: 10 !important;
    width: 100% !important;
}
.btn-emblem-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 7px 16px !important;
    border-radius: 999px !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    border: 1px solid rgba(197, 168, 128, 0.45) !important;
    background: rgba(7, 13, 10, 0.88) !important;
    color: #f3dfba !important;
    text-decoration: none !important;
    cursor: pointer !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.5) !important;
}
.btn-emblem-pill:hover {
    border-color: rgba(243, 223, 186, 0.85) !important;
    color: #ffffff !important;
    background: rgba(197, 168, 128, 0.22) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 15px rgba(197, 168, 128, 0.3) !important;
}
.btn-emblem-inspect {
    border-color: rgba(243, 223, 186, 0.65) !important;
}
.btn-emblem-cloud {
    background: rgba(6, 182, 212, 0.12) !important;
    border-color: rgba(56, 189, 248, 0.4) !important;
    color: #bae6fd !important;
}
.btn-emblem-cloud:hover {
    border-color: rgba(56, 189, 248, 0.9) !important;
    color: #ffffff !important;
    background: rgba(6, 182, 212, 0.28) !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 15px rgba(56, 189, 248, 0.4) !important;
}

/* Floating Follow Omnichannel Sidebar */
.floating-follow {
    position: fixed !important;
    z-index: 900 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 7px !important;
    padding: 10px 5px 12px !important;
    border: 1px solid rgba(197, 168, 128, 0.35) !important;
    border-radius: 999px !important;
    background: linear-gradient(160deg, rgba(12, 21, 17, 0.94), rgba(4, 9, 7, 0.96)) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 25px rgba(197, 168, 128, 0.15) !important;
    max-height: calc(100vh - 70px) !important;
    width: 42px !important;
}
[dir="rtl"] .floating-follow,
html[lang="ar"] .floating-follow {
    left: 14px !important;
    right: auto !important;
}
[dir="ltr"] .floating-follow,
html:not([dir="rtl"]) .floating-follow {
    right: 14px !important;
    left: auto !important;
}
.floating-follow__icons {
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
    align-items: center !important;
}
.floating-follow__link {
    width: 30px !important;
    height: 30px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    background: rgba(255, 255, 255, 0.05) !important;
    color: rgba(243, 223, 186, 0.85) !important;
    text-decoration: none !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.floating-follow__link svg {
    width: 14px !important;
    height: 14px !important;
}
.floating-follow__link:hover {
    transform: scale(1.15) !important;
    color: #ffffff !important;
}
.floating-follow__link--whatsapp:hover { border-color: #25d366 !important; background: rgba(37, 211, 102, 0.25) !important; color: #25d366 !important; box-shadow: 0 0 10px rgba(37, 211, 102, 0.45) !important; }
.floating-follow__link--linkedin:hover { border-color: #0a66c2 !important; background: rgba(10, 102, 194, 0.25) !important; color: #38bdf8 !important; box-shadow: 0 0 10px rgba(10, 102, 194, 0.45) !important; }
.floating-follow__link--mail:hover { border-color: #f59e0b !important; background: rgba(245, 158, 11, 0.25) !important; color: #fbbf24 !important; box-shadow: 0 0 10px rgba(245, 158, 11, 0.45) !important; }
.floating-follow__link--facebook:hover { border-color: #1877f2 !important; background: rgba(24, 119, 242, 0.25) !important; color: #60a5fa !important; box-shadow: 0 0 10px rgba(24, 119, 242, 0.45) !important; }
.floating-follow__link--instagram:hover { border-color: #e1306c !important; background: rgba(225, 48, 108, 0.25) !important; color: #f472b6 !important; box-shadow: 0 0 10px rgba(225, 48, 108, 0.45) !important; }
.floating-follow__link--x:hover { border-color: #ffffff !important; background: rgba(255, 255, 255, 0.25) !important; color: #ffffff !important; box-shadow: 0 0 10px rgba(255, 255, 255, 0.45) !important; }
.floating-follow__link--youtube:hover { border-color: #ff0000 !important; background: rgba(255, 0, 0, 0.25) !important; color: #f87171 !important; box-shadow: 0 0 10px rgba(255, 0, 0, 0.45) !important; }
.floating-follow__link--tiktok:hover { border-color: #00f2ea !important; background: rgba(0, 242, 234, 0.25) !important; color: #22d3ee !important; box-shadow: 0 0 10px rgba(0, 242, 234, 0.45) !important; }
.floating-follow__link--snapchat:hover { border-color: #fffc00 !important; background: rgba(255, 252, 0, 0.25) !important; color: #fef08a !important; box-shadow: 0 0 10px rgba(255, 252, 0, 0.45) !important; }

.floating-follow__line {
    width: 1px !important;
    height: 16px !important;
    background: rgba(197, 168, 128, 0.45) !important;
    margin: 1px 0 !important;
}
.floating-follow__label {
    color: #f3dfba !important;
    font-weight: 800 !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.22em !important;
    writing-mode: vertical-rl !important;
    transform: rotate(180deg) !important;
    white-space: nowrap !important;
    margin: 4px 0 !important;
    text-shadow: 0 0 8px rgba(197, 168, 128, 0.4) !important;
}
.floating-follow__chat-bottom {
    margin-top: 1px !important;
    background: rgba(6, 182, 212, 0.16) !important;
    border: 1.5px solid rgba(56, 189, 248, 0.5) !important;
    color: #38bdf8 !important;
    position: relative !important;
}
.floating-follow__chat-bottom:hover {
    border-color: rgba(56, 189, 248, 0.95) !important;
    background: rgba(6, 182, 212, 0.35) !important;
    color: #ffffff !important;
    box-shadow: 0 0 16px rgba(6, 182, 212, 0.6) !important;
}
"""

for target in [os.path.join(ROOT, 'css', 'enterprise-suite.css'), os.path.join(ROOT, 'css', 'enterprise-suite.min.css')]:
    with open(target, 'a', encoding='utf-8') as f:
        f.write('\n' + css_rules + '\n')
    print('Successfully appended CSS to', target)
