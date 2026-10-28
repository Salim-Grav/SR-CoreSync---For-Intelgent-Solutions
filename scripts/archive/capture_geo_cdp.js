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

async function captureGeoScenario(url, langCode, outFilename) {
  const port = 9380 + Math.floor(Math.random() * 50);
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_geo_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,900',
    '--lang=' + langCode,
    url
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

    const target = pages.find(p => p.url && (p.url.includes('index.html') || p.url.includes('preview-')));
    if (!target) throw new Error('Target page not found for ' + url);

    const ws = new WebSocket(target.webSocketDebuggerUrl);
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

    // Wait 2.2s for banner to animate in fully
    await new Promise(r => setTimeout(r, 2200));

    // Ensure cookie banner is dismissed so geo banner shines cleanly at top
    await call('Runtime.evaluate', {
      expression: `
        try {
          const cookie = document.querySelector('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
          if (cookie) cookie.style.opacity = '0';
        } catch(e) {}
      `
    });

    const bannerState = await call('Runtime.evaluate', {
      expression: 'document.getElementById("srGeoLangBanner") ? document.getElementById("srGeoLangBanner").className : "NOT_FOUND"'
    });
    console.log(`[${langCode}] Banner on ${url} ->`, bannerState.result?.result?.value);

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outPath = path.join(artDir, outFilename);
    fs.writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
    console.log('Successfully saved screenshot:', outPath);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }, 1000);
  }
}

async function main() {
  // Scenario 1: Dutch visitor on Arabic index.html
  await captureGeoScenario('file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/index.html', 'nl-NL', 'geolang_banner_nl_on_ar.png');

  // Scenario 2: Arabic visitor on English index.html
  await captureGeoScenario('file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/en/index.html', 'ar-SA', 'geolang_banner_ar_on_en.png');

  // Scenario 3: German visitor on Dutch index.html
  await captureGeoScenario('file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/nl/index.html', 'de-DE', 'geolang_banner_de_on_nl.png');
}

main().catch(console.error);
