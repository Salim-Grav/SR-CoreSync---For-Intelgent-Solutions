import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';

const ARTIFACT_DIR = 'C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\c2846371-b1e6-4b8f-9fee-01dda36014e9';

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        defaultViewport: { width: 1920, height: 1080 }
    });

    const page = await browser.newPage();
    await page.goto('http://localhost:3000/index.html', { waitUntil: 'networkidle2', timeout: 30000 });

    // Wait 1.5s for fonts and animations to stabilize
    await new Promise(r => setTimeout(r, 1500));

    // 1. Capture the Top Hero & Header view
    const heroScreenshot = path.join(ARTIFACT_DIR, 'live_top_header_and_hero_voice_buttons_1920.png');
    await page.screenshot({ path: heroScreenshot, clip: { x: 0, y: 0, width: 1920, height: 980 } });
    console.log('[OK] Captured Top Header & Hero voice buttons:', heroScreenshot);

    // 2. Click the Header Voice AI button to verify modal opens
    await page.click('#headerVoiceAiBtn');
    await new Promise(r => setTimeout(r, 800));

    // Capture modal opened via header click
    const modalScreenshot = path.join(ARTIFACT_DIR, 'live_voice_modal_from_header_click.png');
    await page.screenshot({ path: modalScreenshot });
    console.log('[OK] Captured modal opened via Header Voice AI button:', modalScreenshot);

    await browser.close();
    console.log('[OK] All screenshots completed successfully.');
})();
