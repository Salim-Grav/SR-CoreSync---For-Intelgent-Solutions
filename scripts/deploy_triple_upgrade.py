"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
Deployment Script for Triple Upgrade:
Option 1: Multilingual Founder Voice Routing & Speech Synthesis (NL, DE, EN, AR)
Option 2: Executive VIP Booking Modal Audio Greeting (Salim & Raed Greetings)
Option 3: Sovereign Executive A4 Blueprint Preview Modal & Official Stamping
==============================================================================
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def update_css():
    css_path = os.path.join(ROOT, 'css', 'enterprise-suite.css')
    min_css_path = os.path.join(ROOT, 'css', 'enterprise-suite.min.css')
    
    extra_css = """
/* ==========================================================================
   S&R CoreSync - VIP Executive Booking Audio Greeting & A4 Blueprint Preview
   ========================================================================== */

/* 1. VIP Executive Booking Audio Greeting Bar */
.sr-booking-audio-greeting {
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(6, 78, 59, 0.45));
    border: 1px solid rgba(197, 168, 128, 0.4);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 18px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.sr-booking-audio-greeting::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #c5a880, #f3dfba, transparent);
}

.sr-booking-audio-avatar-wrap {
    position: relative;
    flex-shrink: 0;
    width: 48px;
    height: 48px;
}

.sr-booking-audio-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #c5a880;
    box-shadow: 0 0 10px rgba(197, 168, 128, 0.4);
}

.sr-booking-audio-pulse-dot {
    position: absolute;
    bottom: 2px;
    right: 2px;
    width: 12px;
    height: 12px;
    background: #10b981;
    border: 2px solid #0f172a;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: srPulseGlow 2s infinite;
}

.sr-booking-audio-greeting.is-playing .sr-booking-audio-pulse-dot {
    background: #f59e0b;
    box-shadow: 0 0 12px #f59e0b;
    animation: srPulseGlow 0.8s infinite;
}

@keyframes srPulseGlow {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.25); opacity: 0.7; }
}

.sr-booking-audio-info {
    flex: 1;
    min-width: 0;
}

.sr-booking-audio-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f3dfba;
    margin-bottom: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sr-booking-audio-desc {
    font-size: 0.8rem;
    color: #94a3b8;
    line-height: 1.3;
}

.sr-booking-audio-play-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(135deg, #c5a880, #a28359);
    color: #0f172a !important;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.25s ease;
    box-shadow: 0 2px 10px rgba(197, 168, 128, 0.35);
}

.sr-booking-audio-play-btn:hover {
    background: linear-gradient(135deg, #f3dfba, #c5a880);
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(197, 168, 128, 0.5);
}

.sr-booking-audio-greeting.is-playing .sr-booking-audio-play-btn {
    background: linear-gradient(135deg, #ef4444, #b91c1c);
    color: #ffffff !important;
    box-shadow: 0 0 14px rgba(239, 68, 68, 0.45);
}

/* 2. Action Grid inside Voice Planner Result */
.sr-blueprint-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 18px;
}

.sr-blueprint-actions-grid .sr-btn-action {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 14px;
    font-size: 0.84rem;
    font-weight: 700;
    border-radius: 9px;
    cursor: pointer;
    transition: all 0.25s ease;
    text-decoration: none;
}

.sr-btn-preview-a4 {
    background: linear-gradient(135deg, #c5a880, #8f6f42);
    color: #0b1120 !important;
    border: 1px solid #f3dfba;
    box-shadow: 0 3px 12px rgba(197, 168, 128, 0.35);
}
.sr-btn-preview-a4:hover {
    background: linear-gradient(135deg, #f3dfba, #c5a880);
    transform: translateY(-1.5px);
    box-shadow: 0 5px 16px rgba(197, 168, 128, 0.5);
}

.sr-btn-export-pdf {
    background: rgba(15, 23, 42, 0.85);
    color: #f3dfba !important;
    border: 1px solid rgba(197, 168, 128, 0.5);
}
.sr-btn-export-pdf:hover {
    background: rgba(197, 168, 128, 0.2);
    border-color: #f3dfba;
}

.sr-btn-whatsapp {
    background: linear-gradient(135deg, #10b981, #047857);
    color: #ffffff !important;
    border: 1px solid #34d399;
}
.sr-btn-whatsapp:hover {
    background: linear-gradient(135deg, #34d399, #10b981);
    transform: translateY(-1.5px);
}

.sr-btn-vip-book {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: #ffffff !important;
    border: 1px solid #60a5fa;
}
.sr-btn-vip-book:hover {
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    transform: translateY(-1.5px);
}

/* 3. Sovereign Executive A4 Blueprint Preview Modal */
.sr-a4-preview-modal {
    position: fixed;
    inset: 0;
    z-index: 999999;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(3, 7, 18, 0.85);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    overflow-y: auto;
}

.sr-a4-preview-modal.active {
    display: flex;
}

.sr-a4-preview-wrapper {
    position: relative;
    max-width: 860px;
    width: 100%;
    margin: auto;
    animation: srA4ModalSlideIn 0.3s ease-out;
}

@keyframes srA4ModalSlideIn {
    from { opacity: 0; transform: translateY(20px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.sr-a4-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(197, 168, 128, 0.4);
    border-radius: 12px;
    padding: 10px 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.sr-a4-toolbar-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #f3dfba;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sr-a4-toolbar-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}

.sr-a4-btn-action {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    font-size: 0.82rem;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
}

.sr-a4-btn-print {
    background: linear-gradient(135deg, #c5a880, #a28359);
    color: #0b1120 !important;
}
.sr-a4-btn-print:hover {
    background: linear-gradient(135deg, #f3dfba, #c5a880);
    transform: translateY(-1px);
}

.sr-a4-btn-close {
    background: rgba(255, 255, 255, 0.1);
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.sr-a4-btn-close:hover {
    background: rgba(239, 68, 68, 0.25);
    border-color: #ef4444;
    color: #fca5a5 !important;
}

/* Authentic A4 Paper Sheet Styling */
.sr-a4-sheet {
    background: #ffffff;
    color: #0f172a;
    border-radius: 4px;
    padding: 38px 44px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.5;
}

.sr-a4-watermark {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-30deg);
    font-size: 5.5rem;
    font-weight: 900;
    color: rgba(197, 168, 128, 0.05);
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
    letter-spacing: 4px;
    z-index: 1;
}

.sr-a4-sheet-header {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 16px;
    margin-bottom: 20px;
}

.sr-a4-brand-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}

.sr-a4-brand-logo img {
    width: 52px;
    height: 52px;
    border-radius: 8px;
    border: 1px solid #c5a880;
}

.sr-a4-brand-text h2 {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    line-height: 1.2;
}

.sr-a4-brand-text p {
    font-size: 0.78rem;
    color: #475569;
    margin: 2px 0 0;
    font-weight: 500;
}

.sr-a4-doc-meta {
    text-align: right;
    font-size: 0.75rem;
    color: #475569;
}

[dir="rtl"] .sr-a4-doc-meta {
    text-align: left;
}

.sr-a4-doc-ref {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0b1120;
    font-family: monospace;
    background: #f1f5f9;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
    display: inline-block;
    margin-bottom: 4px;
}

.sr-a4-confidential-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 800;
    color: #b45309;
    background: #fef3c7;
    border: 1px solid #fde68a;
    border-radius: 4px;
    padding: 2px 6px;
    letter-spacing: 0.5px;
}

.sr-a4-sheet-body {
    position: relative;
    z-index: 2;
}

.sr-a4-section-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-left: 4px solid #c5a880;
    padding-left: 10px;
    margin: 18px 0 10px;
}

[dir="rtl"] .sr-a4-section-title {
    border-left: none;
    border-right: 4px solid #c5a880;
    padding-left: 0;
    padding-right: 10px;
}

.sr-a4-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 16px;
}

.sr-a4-card-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 12px 14px;
}

.sr-a4-card-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.sr-a4-card-val {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0f172a;
}

.sr-a4-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
    font-size: 0.82rem;
}

.sr-a4-table th {
    background: #0f172a;
    color: #ffffff;
    text-align: left;
    padding: 8px 12px;
    font-weight: 700;
}

[dir="rtl"] .sr-a4-table th {
    text-align: right;
}

.sr-a4-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
}

.sr-a4-table tr:nth-child(even) td {
    background: #f8fafc;
}

.sr-a4-endorsement-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 24px;
}

.sr-a4-founder-sign-box {
    display: flex;
    align-items: center;
    gap: 14px;
}

.sr-a4-founder-sign-img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #c5a880;
}

.sr-a4-founder-sign-name {
    font-size: 0.92rem;
    font-weight: 800;
    color: #0f172a;
}

.sr-a4-founder-sign-role {
    font-size: 0.75rem;
    color: #64748b;
}

.sr-a4-official-seal {
    width: 82px;
    height: 82px;
    border: 3px double #c5a880;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4px;
    color: #854d0e;
    background: radial-gradient(circle, #fefce8, #fef08a);
    box-shadow: 0 0 10px rgba(197, 168, 128, 0.3);
}

.sr-a4-seal-title {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.5px;
    line-height: 1.1;
}

.sr-a4-seal-star {
    font-size: 0.75rem;
    line-height: 1;
    margin: 2px 0;
}

.sr-a4-seal-sub {
    font-size: 0.5rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}

.sr-a4-sheet-footer {
    position: relative;
    z-index: 2;
    border-top: 1px solid #e2e8f0;
    padding-top: 12px;
    margin-top: 20px;
    font-size: 0.7rem;
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Pristine Print Stylesheet Rule */
@media print {
    body * {
        visibility: hidden !important;
    }
    #srBlueprintPreviewModal,
    #srBlueprintPreviewModal .sr-a4-sheet,
    #srBlueprintPreviewModal .sr-a4-sheet * {
        visibility: visible !important;
    }
    #srBlueprintPreviewModal {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        background: #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
    }
    .sr-a4-preview-wrapper {
        max-width: 100% !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    .sr-a4-sheet {
        box-shadow: none !important;
        border: none !important;
        padding: 15mm 20mm !important;
        border-radius: 0 !important;
    }
    .sr-a4-toolbar, .sr-exec-modal-backdrop, .sr-exec-modal-close {
        display: none !important;
    }
}
"""
    with open(css_path, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'sr-booking-audio-greeting' not in c:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(extra_css)
        print("Appended extra CSS to enterprise-suite.css")
    else:
        print("enterprise-suite.css already contains extra CSS")

    with open(min_css_path, 'r', encoding='utf-8') as f:
        mc = f.read()
    if 'sr-booking-audio-greeting' not in mc:
        with open(min_css_path, 'a', encoding='utf-8') as f:
            f.write(extra_css)
        print("Appended extra CSS to enterprise-suite.min.css")
    else:
        print("enterprise-suite.min.css already contains extra CSS")

if __name__ == '__main__':
    update_css()
