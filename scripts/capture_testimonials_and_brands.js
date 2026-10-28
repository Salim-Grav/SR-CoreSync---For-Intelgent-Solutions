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
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    console.log('Navigating to http://localhost:3000/index.html...');
    await page.goto('http://localhost:3000/index.html', { waitUntil: 'networkidle' });

    // Wait for testimonials to be initialized
    await page.waitForSelector('.swiper-testimonial.swiper-initialized', { timeout: 10000 });
    await page.waitForTimeout(1000);

    // Scroll to testimonials section
    const testimonials = page.locator('#testimonials');
    await testimonials.scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);

    const testShotPath = path.resolve(__dirname, '../live_testimonials_active_1920.png');
    await page.screenshot({ path: testShotPath, fullPage: false });
    console.log('Saved live screenshot:', testShotPath);

    // Scroll to brands marquee
    const brands = page.locator('#brands');
    await brands.scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);

    const brandShotPath = path.resolve(__dirname, '../live_brand_marquee_1920.png');
    await page.screenshot({ path: brandShotPath, fullPage: false });
    console.log('Saved brand marquee screenshot:', brandShotPath);

    await browser.close();
})();
