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
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    await page.goto('http://localhost:3000/index.html');
    await page.waitForTimeout(1500);
    await page.evaluate(() => {
        const el = document.getElementById('work');
        if (el) {
            const rect = el.getBoundingClientRect();
            window.scrollTo(0, window.scrollY + rect.top + 380);
        }
    });
    await page.waitForTimeout(1500);
    await page.screenshot({ path: 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/live_work_bottom_view.png' });
    await browser.close();
    console.log('Done!');
})();
