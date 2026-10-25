const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    await page.goto('http://localhost:3000/index.html');
    await page.waitForTimeout(2000);
    const work = await page.$('#work');
    if (work) {
        await work.scrollIntoViewIfNeeded();
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'C:/Users/msali/.gemini/antigravity-ide/brain/c2846371-b1e6-4b8f-9fee-01dda36014e9/work_section_view.png' });
        console.log('Saved work_section_view.png');
    } else {
        console.log('Not found');
    }
    await browser.close();
})();
