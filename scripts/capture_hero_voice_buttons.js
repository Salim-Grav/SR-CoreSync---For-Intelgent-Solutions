/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ARTIFACT_DIR = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\c2846371-b1e6-4b8f-9fee-01dda36014e9';

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    console.log('Navigating to http://localhost:3000/index.html...');
    await page.goto('http://localhost:3000/index.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(1500);

    // 1. Capture Top Header & Hero section with the new voice buttons
    const heroShotLocal = path.resolve(__dirname, '../live_top_header_and_hero_voice_buttons_1920.png');
    const heroShotArtifact = path.join(ARTIFACT_DIR, 'live_top_header_and_hero_voice_buttons_1920.png');
    
    await page.screenshot({
        path: heroShotLocal,
        clip: { x: 0, y: 0, width: 1920, height: 980 }
    });
    fs.copyFileSync(heroShotLocal, heroShotArtifact);
    console.log('[OK] Captured Top Header & Hero voice buttons:', heroShotLocal);

    // 2. Click the Header Voice AI button to verify modal opens
    console.log('Clicking #headerVoiceAiBtn...');
    await page.click('#headerVoiceAiBtn');
    await page.waitForTimeout(800);

    // Capture modal opened via header button
    const modalShotLocal = path.resolve(__dirname, '../live_voice_modal_from_header_click.png');
    const modalShotArtifact = path.join(ARTIFACT_DIR, 'live_voice_modal_from_header_click.png');

    await page.screenshot({ path: modalShotLocal, fullPage: false });
    fs.copyFileSync(modalShotLocal, modalShotArtifact);
    console.log('[OK] Captured modal opened via Header Voice AI button:', modalShotLocal);

    await browser.close();
    console.log('[OK] All captures done successfully!');
})();
