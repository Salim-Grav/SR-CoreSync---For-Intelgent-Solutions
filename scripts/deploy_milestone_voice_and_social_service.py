# -*- coding: utf-8 -*-
"""
S&R CoreSync - Deploy Milestone 36:
1. Enterprise Omnichannel Social Media & 8K Visual Authority Paid Service
2. AI Voice Project Architect & Roadmap Blueprint Modal
"""
import os
import re

CSS_VOICE_PLANNER = """
/* ==========================================================================
   S&R CORESYNC - AI VOICE PROJECT ARCHITECT & ROADMAP MODAL
   ========================================================================== */
.exec-stage-btn-voice-pulse {
    background: linear-gradient(135deg, rgba(197, 168, 128, 0.28) 0%, rgba(2, 7, 5, 0.95) 100%) !important;
    border: 1px solid #c5a880 !important;
    color: #f5e5c9 !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 0 20px rgba(197, 168, 128, 0.25) !important;
    animation: voiceBtnPulse 3s infinite alternate ease-in-out !important;
}

@keyframes voiceBtnPulse {
    0% { box-shadow: 0 0 12px rgba(197, 168, 128, 0.2); border-color: rgba(197, 168, 128, 0.5); }
    100% { box-shadow: 0 0 24px rgba(197, 168, 128, 0.6); border-color: #f3dfba; }
}

.sr-voice-modal-container {
    max-width: 860px !important;
    width: 95% !important;
    background: radial-gradient(circle at 50% 0%, rgba(30, 24, 16, 0.98) 0%, rgba(2, 7, 5, 0.99) 100%) !important;
    border: 1px solid rgba(197, 168, 128, 0.35) !important;
    border-radius: 20px !important;
    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85), 0 0 40px rgba(197, 168, 128, 0.15) !important;
    padding: 32px !important;
    max-height: 90vh !important;
    overflow-y: auto !important;
    color: #f5f5f5 !important;
}

.sr-voice-mic-box {
    text-align: center !important;
    margin: 24px 0 !important;
    padding: 24px !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(197, 168, 128, 0.18) !important;
    border-radius: 16px !important;
    position: relative !important;
}

.sr-voice-mic-btn {
    width: 88px !important;
    height: 88px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #c5a880 0%, #8c7350 100%) !important;
    border: 3px solid #f3dfba !important;
    color: #020705 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    box-shadow: 0 0 30px rgba(197, 168, 128, 0.5) !important;
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
}

.sr-voice-mic-btn:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 0 45px rgba(197, 168, 128, 0.8) !important;
}

.sr-voice-mic-btn.is-recording {
    background: linear-gradient(135deg, #e53935 0%, #b71c1c 100%) !important;
    border-color: #ff8a80 !important;
    color: #ffffff !important;
    animation: micRecordingPulse 1.2s infinite ease-in-out !important;
}

@keyframes micRecordingPulse {
    0% { transform: scale(1); box-shadow: 0 0 15px rgba(229, 57, 53, 0.5); }
    50% { transform: scale(1.12); box-shadow: 0 0 40px rgba(229, 57, 53, 0.9); }
    100% { transform: scale(1); box-shadow: 0 0 15px rgba(229, 57, 53, 0.5); }
}

.sr-voice-waves {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    height: 36px !important;
    margin: 16px auto !important;
}

.sr-voice-wave-bar {
    width: 5px !important;
    height: 8px !important;
    background: #c5a880 !important;
    border-radius: 3px !important;
    transition: height 0.15s ease !important;
}

.sr-voice-mic-btn.is-recording ~ .sr-voice-waves .sr-voice-wave-bar {
    animation: waveBarDance 0.8s infinite ease-in-out alternate !important;
}

.sr-voice-waves .sr-voice-wave-bar:nth-child(1) { animation-delay: 0.1s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(2) { animation-delay: 0.25s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(3) { animation-delay: 0.4s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(4) { animation-delay: 0.15s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(5) { animation-delay: 0.3s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(6) { animation-delay: 0.45s !important; }
.sr-voice-waves .sr-voice-wave-bar:nth-child(7) { animation-delay: 0.2s !important; }

@keyframes waveBarDance {
    0% { height: 6px; }
    100% { height: 32px; background: #f3dfba; }
}

.sr-voice-transcript-box {
    width: 100% !important;
    min-height: 85px !important;
    background: rgba(0, 0, 0, 0.45) !important;
    border: 1px solid rgba(197, 168, 128, 0.25) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    color: #ffffff !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    box-sizing: border-box !important;
    outline: none !important;
}

.sr-voice-transcript-box:focus {
    border-color: #c5a880 !important;
    box-shadow: 0 0 15px rgba(197, 168, 128, 0.3) !important;
}

.sr-voice-chips-row {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    margin: 12px 0 18px !important;
    justify-content: center !important;
}

.sr-voice-chip {
    background: rgba(197, 168, 128, 0.08) !important;
    border: 1px solid rgba(197, 168, 128, 0.22) !important;
    border-radius: 999px !important;
    padding: 6px 14px !important;
    color: #e0d0b8 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
}

.sr-voice-chip:hover {
    background: rgba(197, 168, 128, 0.22) !important;
    color: #ffffff !important;
    border-color: #c5a880 !important;
    transform: translateY(-2px) !important;
}

.sr-voice-actions-row {
    display: flex !important;
    gap: 12px !important;
    justify-content: center !important;
    flex-wrap: wrap !important;
    margin-top: 14px !important;
}

.sr-voice-btn-primary {
    background: linear-gradient(135deg, #c5a880 0%, #997b53 100%) !important;
    color: #020705 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.25s ease !important;
}

.sr-voice-btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(197, 168, 128, 0.45) !important;
}

.sr-voice-btn-glass {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(197, 168, 128, 0.3) !important;
    color: #f3dfba !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    transition: all 0.25s ease !important;
}

.sr-voice-btn-glass:hover {
    background: rgba(197, 168, 128, 0.15) !important;
    color: #ffffff !important;
}

/* Blueprint Result Section */
.sr-blueprint-card {
    background: rgba(10, 15, 12, 0.85) !important;
    border: 1px solid rgba(197, 168, 128, 0.35) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-top: 24px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6) !important;
    animation: blueprintReveal 0.4s ease-out !important;
}

@keyframes blueprintReveal {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.sr-blueprint-header {
    border-bottom: 1px solid rgba(197, 168, 128, 0.2) !important;
    padding-bottom: 16px !important;
    margin-bottom: 20px !important;
}

.sr-blueprint-title {
    color: #f3dfba !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    margin: 6px 0 !important;
}

.sr-blueprint-badge {
    display: inline-block !important;
    padding: 4px 12px !important;
    background: rgba(197, 168, 128, 0.15) !important;
    border: 1px solid rgba(197, 168, 128, 0.35) !important;
    border-radius: 999px !important;
    color: #c5a880 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

.sr-blueprint-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
    gap: 16px !important;
    margin-bottom: 20px !important;
}

.sr-blueprint-box {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

.sr-blueprint-box-title {
    font-size: 14px !important;
    color: #c5a880 !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
}

.sr-blueprint-box-desc {
    font-size: 13.5px !important;
    line-height: 1.6 !important;
    color: #d8d8d8 !important;
}

.sr-roadmap-steps {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    margin: 18px 0 !important;
}

.sr-roadmap-step {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    padding: 10px 14px !important;
    background: rgba(197, 168, 128, 0.06) !important;
    border-left: 3px solid #c5a880 !important;
    border-radius: 6px !important;
    font-size: 13.5px !important;
}

[dir="rtl"] .sr-roadmap-step {
    border-left: none !important;
    border-right: 3px solid #c5a880 !important;
}

.sr-blueprint-actions {
    display: flex !important;
    gap: 12px !important;
    flex-wrap: wrap !important;
    margin-top: 20px !important;
    padding-top: 16px !important;
    border-top: 1px solid rgba(197, 168, 128, 0.2) !important;
}
"""

print("Deploy script template ready.")
