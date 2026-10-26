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
        "url": "https://www.linkedin.com/company/146883282/",
        "asset": "assets/social-8k-branding/linkedin/linkedin-company-cover-8k.png",
        "dimensions": "6768x1146 (5.91:1)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Monday",
        "post_title": "التدشين الرسمي لمنظومة S&R CoreSync السحابية الذكية",
        "hashtags": ["#SRCoreSync", "#ERP", "#CloudSolutions", "#B2BTech", "#Innovation", "#Netherlands"]
    },
    {
        "channel": "Facebook",
        "handle": "@SRCoreSync",
        "category": "b2b",
        "url": "https://facebook.com/SRCoreSync",
        "asset": "assets/social-8k-branding/facebook/facebook-page-cover-8k.png",
        "dimensions": "6560x2496 (2.63:1)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Tuesday",
        "post_title": "إطلاق الصفحة الرسمية لحلول S&R CoreSync الذكية في أوروبا والشرق الأوسط",
        "hashtags": ["#CoreSync", "#SovereignCloud", "#BusinessGrowth", "#SmartSolutions"]
    },
    {
        "channel": "X (Twitter)",
        "handle": "@SRCoreSync",
        "category": "b2b",
        "url": "https://x.com/SRCoreSync",
        "asset": "assets/social-8k-branding/x-twitter/x-header-cover-8k.png",
        "dimensions": "7680x2560 (3:1)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Wednesday",
        "post_title": "مستقبل إدارة الأعمال السيادية وهندسة السحابة يبدأ اليوم مع S&R CoreSync",
        "hashtags": ["#SRCoreSync", "#TechNews", "#CloudERP", "#FinTech", "#AI"]
    },
    {
        "channel": "Instagram",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://instagram.com/SRCoreSync",
        "asset": "assets/social-8k-branding/instagram/instagram-post-square-8k.png",
        "dimensions": "4320x4320 (1:1)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Thursday",
        "post_title": "أناقة التقنية وقوة الهندسة السحابية - هوية S&R CoreSync الملكية 8K",
        "hashtags": ["#LuxuryTech", "#DesignExcellence", "#CoreSync", "#8KBranding"]
    },
    {
        "channel": "YouTube",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://youtube.com/@SRCoreSync",
        "asset": "assets/social-8k-branding/youtube/youtube-channel-banner-8k.png",
        "dimensions": "7680x4320 (16:9)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Friday",
        "post_title": "العرض التعريفي الشامل: كيف تحول S&R CoreSync منظومة أعمالك إلى قوة رقمية متكاملة",
        "hashtags": ["#CloudArchitecture", "#CoreSyncERP", "#TechDocumentary"]
    },
    {
        "channel": "Telegram",
        "handle": "@SRCoreSync",
        "category": "messaging",
        "url": "https://t.me/SRCoreSync",
        "asset": "assets/social-8k-branding/telegram/telegram-post-card-8k.png",
        "dimensions": "4320x3240 (4:3)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Saturday",
        "post_title": "قناة النخبة التقنية: تحديثات وتطويرات منظومة S&R CoreSync الحصرية",
        "hashtags": ["#SRCoreSync_Updates", "#DevCommunity", "#FintechInsights"]
    },
    {
        "channel": "WhatsApp Business",
        "handle": "+31636279435",
        "category": "messaging",
        "url": "https://wa.me/31636279435",
        "asset": "assets/social-8k-branding/whatsapp/whatsapp-catalog-header-8k.png",
        "dimensions": "7680x4320 (16:9)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 1,
        "day": "Sunday",
        "post_title": "الكتالوج الرسمي المعتمد لخدمات وباقات S&R CoreSync الاستشارية والتقنية",
        "hashtags": ["#CustomerSuccess", "#ExecutiveConsulting", "#DirectSupport"]
    },
    {
        "channel": "TikTok",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://tiktok.com/@SRCoreSync",
        "asset": "assets/social-8k-branding/tiktok/tiktok-video-cover-8k.png",
        "dimensions": "4320x7680 (9:16)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 2,
        "day": "Monday",
        "post_title": "كواليس بناء أسرع محرك ERP سحابي متوافق مع معايير الضرائب والـ BTW الأوروبية",
        "hashtags": ["#TechTok", "#CodingLife", "#StartupJourney", "#CloudTech"]
    },
    {
        "channel": "Snapchat",
        "handle": "@SRCoreSync",
        "category": "visual",
        "url": "https://snapchat.com/add/SRCoreSync",
        "asset": "assets/social-8k-branding/snapchat/snapchat-story-frame-8k.png",
        "dimensions": "4320x7680 (9:16)",
        "status": "READY_FOR_PUBLISH",
        "scheduled_week": 2,
        "day": "Tuesday",
        "post_title": "يوميات المهندسين والمؤسسين: هندسة الحلول الذكية خلف الكواليس",
        "hashtags": ["#InsideLook", "#TechLeaders", "#InnovationLab"]
    }
]

def verify_and_export_schedule():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "assets", "social-8k-branding", "campaign_schedule.json")
    
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    print("[Campaign Dispatcher] Verifying 9 Omni-Channels for @SRCoreSync...")
    verified_count = 0
    for ch in CAMPAIGN_REGISTRY:
        full_asset = os.path.join(base_dir, ch["asset"])
        exists = os.path.exists(full_asset)
        status_flag = "[FOUND]" if exists else "[MISSING]"
        print(f"  - [{ch['channel']}] {ch['handle']}: {status_flag}")
        if exists:
            verified_count += 1
            
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(CAMPAIGN_REGISTRY, f, ensure_ascii=False, indent=2)
        
    print(f"\n[Success] Verified {verified_count}/9 channel assets. Exported schedule to:\n{output_path}")

if __name__ == "__main__":
    verify_and_export_schedule()
