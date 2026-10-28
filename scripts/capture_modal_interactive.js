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

(async () => {
    // Launch Chrome using installed channel
    const browser = await chromium.launch({
        channel: 'chrome',
        headless: true
    });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    console.log('Navigating to http://localhost:3000/index.html#testimonials...');
    await page.goto('http://localhost:3000/index.html#testimonials', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 1. Capture testimonial cards with the new ROI triggers
    const cardsPath = 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/live_testimonials_with_roi_triggers_1920.png';
    await page.screenshot({ path: cardsPath });
    console.log('Saved cards with ROI triggers screenshot:', cardsPath);

    // 2. Click on the first testimonial card (Hendrik van Dijk) to open the interactive ROI modal
    console.log('Clicking on Hendrik van Dijk card to open Case Study modal...');
    const card = page.locator('.testimonial-v01').first();
    await card.click();
    await page.waitForTimeout(1000);

    // Capture the open Case Study & ROI Modal
    const modalPath = 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/live_casestudy_modal_open_1920.png';
    await page.screenshot({ path: modalPath });
    console.log('Saved open Case Study modal screenshot:', modalPath);

    // Close modal
    const closeBtn = page.locator('.sr-casestudy-close');
    await closeBtn.click();
    await page.waitForTimeout(600);

    // 3. Open Sultan Al-Rashid's case study modal
    console.log('Opening Sultan Al-Rashid case study...');
    await page.evaluate(() => {
        window.openCaseStudy('sultan');
    });
    await page.waitForTimeout(800);

    const sultanModalPath = 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/live_casestudy_sultan_modal_1920.png';
    await page.screenshot({ path: sultanModalPath });
    console.log('Saved Sultan modal screenshot:', sultanModalPath);

    await browser.close();
    console.log('All screenshots captured successfully!');
})();
