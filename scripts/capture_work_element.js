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

(async () => {
    try {
        const browser = await chromium.launch();
        const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
        await page.goto('http://localhost:3000/index.html', { waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(2000);
        const el = await page.$('#work');
        if (el) {
            await el.screenshot({ path: 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/work_element.png' });
            console.log('Saved work_element.png successfully');
        } else {
            console.log('Element #work not found');
        }
        await browser.close();
    } catch (err) {
        console.error('Error:', err);
    }
})();
