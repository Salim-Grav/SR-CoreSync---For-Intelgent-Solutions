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

async function captureFooter() {
  const port = 9394;
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_footer_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,900',
    'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/index.html'
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

    const target = pages.find(p => p.url && p.url.includes('index.html'));
    if (!target) throw new Error('Target page not found');

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

    // Scroll to the footer
    await call('Runtime.evaluate', {
      expression: `
        try {
          const cookie = document.querySelector('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
          if (cookie) cookie.style.display = 'none';
          const footer = document.querySelector('.tf-footer--original');
          if (footer) footer.scrollIntoView({ behavior: 'instant', block: 'end' });
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1500));

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outPath = path.join(artDir, 'sovereign_footer_redesign.png');
    fs.writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
    console.log('Successfully saved footer screenshot:', outPath);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
    }, 1000);
  }
}

captureFooter().catch(console.error);
