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

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

async function capture() {
  const port = 9331;
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_emblem_locations_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://localhost:3000/index.html'
  ]);

  try {
    await new Promise(r => setTimeout(r, 2200));
    const pages = await new Promise((res, rej) => {
      http.get('http://127.0.0.1:' + port + '/json', r => {
        let d = '';
        r.on('data', c => d += c);
        r.on('end', () => res(JSON.parse(d)));
      }).on('error', rej);
    });

    const targetPage = pages.find(p => p.url && p.url.includes('localhost:3000'));
    if (!targetPage) throw new Error('Target page not found');

    const ws = new WebSocket(targetPage.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    const call = (method, params = {}) => new Promise(res => {
      const curId = id++;
      const handler = (evt) => {
        const m = JSON.parse(evt.data);
        if (m.id === curId) {
          ws.removeEventListener('message', handler);
          res(m);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });

    await call('Runtime.enable');
    await call('Page.enable');

    // Dismiss cookie/GDPR banners
    await call('Runtime.evaluate', {
      expression: `
        try {
          localStorage.setItem('coresync_gdpr_status', 'accepted');
          const banner = document.querySelector('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
          if (banner) banner.style.display = 'none';
          window.scrollTo(0, 0);
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1000));

    // 1. Capture Header Navbar
    const shot1 = await call('Page.captureScreenshot', { format: 'png' });
    const outImg1 = 'C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\e95ea78a-2d22-4f0f-8610-eae376ecc506\\\\live_navbar_emblem.png';
    fs.writeFileSync(outImg1, Buffer.from(shot1.result.data, 'base64'));
    console.log('SUCCESS: Captured Navbar emblem to ' + outImg1);

    // 2. Scroll to founderCentralBadge in the About/Partners section
    await call('Runtime.evaluate', {
      expression: `
        try {
          const badge = document.getElementById('founderCentralBadge');
          if (badge) {
            badge.scrollIntoView({ behavior: 'instant', block: 'center' });
          }
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1200));

    const shot2 = await call('Page.captureScreenshot', { format: 'png' });
    const outImg2 = 'C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\e95ea78a-2d22-4f0f-8610-eae376ecc506\\\\live_central_badge_emblem.png';
    fs.writeFileSync(outImg2, Buffer.from(shot2.result.data, 'base64'));
    console.log('SUCCESS: Captured Central Badge emblem to ' + outImg2);

    // 3. Open Logo Lightbox Modal
    await call('Runtime.evaluate', {
      expression: `
        try {
          const badge = document.getElementById('founderCentralBadge');
          if (badge) badge.click();
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1200));

    const shot3 = await call('Page.captureScreenshot', { format: 'png' });
    const outImg3 = 'C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\e95ea78a-2d22-4f0f-8610-eae376ecc506\\\\live_modal_emblem.png';
    fs.writeFileSync(outImg3, Buffer.from(shot3.result.data, 'base64'));
    console.log('SUCCESS: Captured Logo Modal emblem to ' + outImg3);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 1000);
  }
}

capture().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
