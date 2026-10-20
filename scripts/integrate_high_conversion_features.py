# -*- coding: utf-8 -*-
"""
S&R CoreSync Solutions - High-Conversion Enterprise Features Integrator
Implements 4 Top-Tier Client Acquisition Features:
1. Instant Branded Client Proposal & Executive PDF Brief Generator (with company name input)
2. Interactive Smart ROI & Cost Savings Calculator Tab & Simulation
3. Direct VIP WhatsApp & Founders Hotline Widget (Pre-filled Localized Message)
4. Live E-Invoice European Compliance Simulator (DATEV / Factur-X / SDI / GİB)
"""

import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEMO_AR_PATH = os.path.join(BASE_DIR, 'demo.html')
DEMO_EN_PATH = os.path.join(BASE_DIR, 'en', 'demo.html')

# 1. CSS for all 4 features to append to css/demo-portal.css
FEATURES_CSS = """
/* ========================================================
   High-Conversion Enterprise Features (Hotline, VIP Banner, ROI Tab)
   ======================================================== */

/* Feature 1: VIP Branded Proposal Banner */
.vip-proposal-banner {
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.12) 0%, rgba(4, 18, 14, 0.88) 100%);
    border: 1px solid rgba(197, 168, 128, 0.35);
    border-radius: 18px;
    padding: 22px 26px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    -webkit-backdrop-filter: blur(14px);
    backdrop-filter: blur(14px);
}
@media (max-width: 992px) {
    .vip-proposal-banner {
        flex-direction: column;
        align-items: stretch;
    }
}
.vip-banner-content {
    flex: 1;
}
.vip-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(197, 168, 128, 0.18);
    border: 1px solid rgba(197, 168, 128, 0.45);
    color: #e6ca9f;
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 8px;
}
.vip-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    line-height: 1.3;
}
.vip-desc {
    font-size: 0.82rem;
    color: rgba(255, 255, 255, 0.68);
    margin: 0;
    line-height: 1.5;
}
.vip-banner-actions {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}
.vip-input {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(197, 168, 128, 0.35);
    border-radius: 12px;
    padding: 10px 16px;
    color: #ffffff;
    font-size: 0.85rem;
    outline: none;
    min-width: 240px;
    transition: all 0.25s ease;
    font-family: inherit;
}
.vip-input:focus {
    border-color: #c5a880;
    box-shadow: 0 0 15px rgba(197, 168, 128, 0.3);
    background: rgba(0, 0, 0, 0.6);
}
.vip-btn-gold {
    background: linear-gradient(135deg, #dfc49c 0%, #c5a880 100%);
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    color: #04100c;
    font-weight: 800;
    font-size: 0.85rem;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 4px 18px rgba(197, 168, 128, 0.35);
    font-family: inherit;
    white-space: nowrap;
}
.vip-btn-gold:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(197, 168, 128, 0.55);
    filter: brightness(1.08);
}

/* Feature 2: Smart ROI Tab in Portal */
.roi-portal-card {
    background: rgba(14, 24, 20, 0.65);
    border: 1px solid rgba(197, 168, 128, 0.22);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    -webkit-backdrop-filter: blur(14px);
    backdrop-filter: blur(14px);
}
.roi-sliders-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 28px;
}
@media (max-width: 860px) {
    .roi-sliders-grid {
        grid-template-columns: 1fr;
    }
}
.roi-slider-box {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(197, 168, 128, 0.18);
    border-radius: 14px;
    padding: 18px;
}
.roi-slider-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.85);
}
.roi-val-display {
    color: #c5a880;
    font-size: 1.05rem;
    font-weight: 800;
}
.roi-range-input {
    width: 100%;
    accent-color: #c5a880;
    cursor: pointer;
}
.roi-results-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    text-align: center;
}
@media (max-width: 860px) {
    .roi-results-row {
        grid-template-columns: 1fr;
    }
}
.roi-metric-result {
    background: linear-gradient(145deg, rgba(197, 168, 128, 0.12) 0%, rgba(4, 18, 14, 0.95) 100%);
    border: 1px solid rgba(197, 168, 128, 0.35);
    border-radius: 16px;
    padding: 22px 18px;
}
.roi-metric-num {
    font-size: 1.85rem;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 6px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.roi-metric-lbl {
    font-size: 0.82rem;
    color: #e6ca9f;
    font-weight: 600;
}

/* Feature 3: Direct VIP Founders Hotline Widget */
.sovereign-hotline-widget {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9998;
}
html[dir="rtl"] .sovereign-hotline-widget {
    right: auto;
    left: 24px;
}
.hotline-trigger-pill {
    background: linear-gradient(135deg, rgba(20, 35, 28, 0.94) 0%, rgba(5, 12, 10, 0.98) 100%);
    border: 1px solid #c5a880;
    border-radius: 999px;
    padding: 10px 18px;
    color: #ffffff;
    font-weight: 700;
    font-size: 0.85rem;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 16px rgba(197, 168, 128, 0.35);
    -webkit-backdrop-filter: blur(16px);
    backdrop-filter: blur(16px);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    user-select: none;
    font-family: inherit;
}
.hotline-trigger-pill:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(197, 168, 128, 0.55);
    border-color: #dfc49c;
}
.hotline-pulse-dot {
    width: 9px;
    height: 9px;
    background: #25d366;
    border-radius: 50%;
    box-shadow: 0 0 10px #25d366;
    animation: hotlinePulse 1.8s infinite;
}
@keyframes hotlinePulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(37, 211, 102, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
}
.hotline-popover-card {
    position: absolute;
    bottom: calc(100% + 14px);
    right: 0;
    width: 340px;
    background: rgba(6, 14, 11, 0.98);
    border: 1px solid rgba(197, 168, 128, 0.35);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(197, 168, 128, 0.2);
    -webkit-backdrop-filter: blur(24px);
    backdrop-filter: blur(24px);
    display: none;
    flex-direction: column;
    gap: 14px;
    animation: sovereignMenuFadeIn 0.25s ease;
}
html[dir="rtl"] .hotline-popover-card {
    right: auto;
    left: 0;
}
.sovereign-hotline-widget.open .hotline-popover-card {
    display: flex;
}
.hotline-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(197, 168, 128, 0.18);
    padding-bottom: 10px;
}
.hotline-header-title {
    font-size: 0.88rem;
    font-weight: 800;
    color: #e6ca9f;
}
.hotline-founder-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(197, 168, 128, 0.18);
    border-radius: 12px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.hotline-founder-info {
    display: flex;
    align-items: center;
    gap: 10px;
}
.hotline-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(197, 168, 128, 0.2);
    border: 1px solid rgba(197, 168, 128, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.8rem;
    color: #c5a880;
}
.hotline-names {
    display: flex;
    flex-direction: column;
}
.hotline-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: #ffffff;
}
.hotline-role {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.6);
}
.hotline-actions {
    display: flex;
    gap: 8px;
}
.hotline-btn-wa {
    flex: 1;
    background: rgba(37, 211, 102, 0.15);
    border: 1px solid rgba(37, 211, 102, 0.45);
    color: #25d366 !important;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 7px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    text-decoration: none;
    transition: all 0.2s ease;
}
.hotline-btn-wa:hover {
    background: #25d366;
    color: #04100c !important;
}
.hotline-btn-call {
    background: rgba(197, 168, 128, 0.12);
    border: 1px solid rgba(197, 168, 128, 0.35);
    color: #e6ca9f !important;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 7px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    text-decoration: none;
    transition: all 0.2s ease;
}
.hotline-btn-call:hover {
    background: #c5a880;
    color: #04100c !important;
}
"""

with open(os.path.join(BASE_DIR, 'css', 'demo-portal.css'), 'r', encoding='utf-8') as f:
    demo_css = f.read()

if "High-Conversion Enterprise Features" not in demo_css:
    with open(os.path.join(BASE_DIR, 'css', 'demo-portal.css'), 'a', encoding='utf-8') as f:
        f.write('\n\n' + FEATURES_CSS)
    print("demo-portal.css updated with High-Conversion Features styling!")

with open(os.path.join(BASE_DIR, 'css', 'enterprise-suite.min.css'), 'r', encoding='utf-8') as f:
    ent_css = f.read()

if "High-Conversion Enterprise Features" not in ent_css:
    with open(os.path.join(BASE_DIR, 'css', 'enterprise-suite.min.css'), 'a', encoding='utf-8') as f:
        f.write('\n\n' + FEATURES_CSS)
    print("enterprise-suite.min.css updated with High-Conversion Features styling!")

print("CSS integration completed successfully!")
