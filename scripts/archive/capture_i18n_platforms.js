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

const artDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

async function captureLang(lang, filename) {
  const port = 9330 + Math.floor(Math.random() * 50);
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_i18n_' + lang + '_' + Date.now());
  const url = `http://127.0.0.1:8765/${lang}/index.html`;

  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    url
  ]);

  try {
    await new Promise(r => setTimeout(r, 2500));
    const pages = await new Promise((res, rej) => {
      http.get('http://127.0.0.1:' + port + '/json', r => {
        let d = '';
        r.on('data', c => d += c);
        r.on('end', () => res(JSON.parse(d)));
      }).on('error', rej);
    });

    const targetPage = pages.find(p => p.url && p.url.includes(lang));
    if (!targetPage) throw new Error(`Target page for ${lang} not found`);

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

    // Dismiss GDPR, switch to platforms tab, and scroll to work section
    await call('Runtime.evaluate', {
      expression: `
        try {
          localStorage.setItem('coresync_gdpr_status', 'accepted');
          const banner = document.querySelector('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
          if (banner) banner.style.display = 'none';

          // Activate platforms tab
          const platBtn = document.getElementById('tab-btn-platforms');
          if (platBtn) {
            platBtn.click();
          }

          const workSec = document.getElementById('work');
          if (workSec) {
            workSec.scrollIntoView({ behavior: 'instant', block: 'start' });
          }
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1200));

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outImg = path.join(artDir, filename);
    fs.writeFileSync(outImg, Buffer.from(shot.result.data, 'base64'));
    console.log(`SUCCESS: Captured ${lang} platforms view to ${outImg}`);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 1000);
  }
}

async function run() {
  await captureLang('en', 'i18n_en_platforms_view.png');
  await captureLang('nl', 'i18n_nl_platforms_view.png');
  console.log('ALL CAPTURES COMPLETED');
}

run().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
