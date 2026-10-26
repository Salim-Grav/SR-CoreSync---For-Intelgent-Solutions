const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ARTIFACT_DIR = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\85966c0a-c8d5-464f-b0e6-0664f5664ec5';

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    console.log('Navigating to http://localhost:8181/index.html...');
    await page.goto('http://localhost:8181/index.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // 1. Capture the hero and floating social rail
    const heroShotLocal = path.resolve(__dirname, '../live_linkedin_floating_rail_1920.png');
    const heroShotArtifact = path.join(ARTIFACT_DIR, 'live_linkedin_floating_rail_1920.png');
    
    await page.screenshot({
        path: heroShotLocal,
        clip: { x: 0, y: 0, width: 1920, height: 980 }
    });
    fs.copyFileSync(heroShotLocal, heroShotArtifact);
    console.log('[OK] Captured Hero & Floating Social Rail:', heroShotLocal);

    // 2. Scroll to footer social strip
    const footerElement = await page.$('.sr-footer-social-strip');
    if (footerElement) {
        await footerElement.scrollIntoViewIfNeeded();
        await page.waitForTimeout(1000);
        const footerShotLocal = path.resolve(__dirname, '../live_linkedin_footer_strip_1920.png');
        const footerShotArtifact = path.join(ARTIFACT_DIR, 'live_linkedin_footer_strip_1920.png');
        await page.screenshot({
            path: footerShotLocal,
            clip: { x: 0, y: Math.max(0, (await page.evaluate(() => window.scrollY)) - 100), width: 1920, height: 900 }
        });
        fs.copyFileSync(footerShotLocal, footerShotArtifact);
        console.log('[OK] Captured Footer Social Strip:', footerShotLocal);
    }

    await browser.close();
    console.log('[OK] All captures done successfully!');
})();
