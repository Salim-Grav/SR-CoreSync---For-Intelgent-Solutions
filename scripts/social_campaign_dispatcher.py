#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S&R CoreSync For Intelligent Solutions - Omnichannel Campaign Dispatcher 2026
Automated Social Media Launchpad, Calendar Generator, and Webhook Dispatcher
Universal Handle: @SRCoreSync
"""

import json
import os
import sys

CAMPAIGN_REGISTRY = [
    {
        "channel": "LinkedIn",
        "handle": "@SRCoreSync",
        "category": "b2b",
        "url": "https://www.linkedin.com/company/srcoresync/",
        "asset": "assets/social-8k-branding/linkedin-8k/linkedin-company-cover-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "X (Twitter)",
        "handle": "@SRCoreSync",
        "category": "b2b",
        "url": "https://x.com/SRCoreSync",
        "asset": "assets/social-8k-branding/x-8k/x-banner-header-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "Instagram",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://instagram.com/SRCoreSync",
        "asset": "assets/social-8k-branding/instagram-8k/instagram-square-feed-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "YouTube",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://youtube.com/@SRCoreSync",
        "asset": "assets/social-8k-branding/youtube-8k/youtube-channel-banner-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "TikTok",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://tiktok.com/@SRCoreSync",
        "asset": "assets/social-8k-branding/tiktok-8k/tiktok-profile-cover-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 2
    },
    {
        "channel": "Telegram",
        "handle": "@SRCoreSync",
        "category": "messaging",
        "url": "https://t.me/SRCoreSync",
        "asset": "assets/social-8k-branding/telegram-8k/telegram-channel-cover-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "WhatsApp Business",
        "handle": "+31636279435",
        "category": "messaging",
        "url": "https://wa.me/31636279435",
        "asset": "assets/social-8k-branding/whatsapp-8k/whatsapp-business-banner-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1
    },
    {
        "channel": "Facebook",
        "handle": "@SRCoreSync",
        "category": "b2b",
        "url": "https://facebook.com/SRCoreSync",
        "asset": "assets/social-8k-branding/facebook-8k/facebook-page-cover-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 2
    },
    {
        "channel": "Snapchat",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://snapchat.com/add/SRCoreSync",
        "asset": "assets/social-8k-branding/snapchat-8k/snapchat-header-banner-8k.png",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 2
    }
]

def verify_and_export_schedule():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "assets", "social-8k-branding", "campaign_schedule.json")
    
    print(f"[Campaign Dispatcher] Verifying 9 Omni-Channels for @SRCoreSync...")
    verified_count = 0
    for ch in CAMPAIGN_REGISTRY:
        full_asset = os.path.join(base_dir, ch["asset"])
        exists = os.path.exists(full_asset)
        status_flag = "✓ FOUND" if exists else "⚠️ MISSING"
        print(f"  - [{ch['channel']}] {ch['handle']}: {status_flag}")
        if exists:
            verified_count += 1
            
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(CAMPAIGN_REGISTRY, f, ensure_ascii=False, indent=2)
        
    print(f"\n[Success] Verified {verified_count}/9 channel assets. Exported schedule to:\n{output_path}")

if __name__ == "__main__":
    verify_and_export_schedule()
