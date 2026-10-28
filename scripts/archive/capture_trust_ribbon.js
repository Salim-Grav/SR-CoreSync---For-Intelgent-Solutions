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

const port = 9390;
const userDataDir = path.join(process.env.TEMP, 'edge_ribbon_' + Date.now());
const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

const edge = spawn(edgePath, [
  '--headless=new',
  '--remote-debugging-port=' + port,
  '--user-data-dir=' + userDataDir,
  '--window-size=1440,1050',
  'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/index.html'
]);

async function run() {
  await new Promise(r => setTimeout(r, 2500));
  const pages = await new Promise((res, rej) => {
    http.get('http://127.0.0.1:' + port + '/json', r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });
  const target = pages.find(p => p.url && p.url.includes('index.html'));
  if (!target) { console.log('Page not found'); edge.kill(); return; }

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
  await call('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 1050,
    deviceScaleFactor: 1,
    mobile: false
  });

  await new Promise(r => setTimeout(r, 2000));

  // Scroll into view of #compliance
  await call('Runtime.evaluate', {
    expression: `(() => {
      const el = document.getElementById('compliance');
      if (el) {
        el.scrollIntoView({ behavior: 'instant', block: 'center' });
      }
    })()`
  });

  await new Promise(r => setTimeout(r, 1200));

  // Capture Trust Ribbon Section
  const shot1 = await call('Page.captureScreenshot', { format: 'png' });
  const outPath1 = path.join(artifactDir, 'sovereign_trust_ribbon.png');
  fs.writeFileSync(outPath1, Buffer.from(shot1.result.data, 'base64'));
  console.log('✓ Captured sovereign_trust_ribbon.png');

  // Click on GDPR compliance card to test interactive modal
  await call('Runtime.evaluate', {
    expression: `(() => {
      const card = document.querySelector('.sr-trust-card[data-compliance="gdpr"]');
      if (card) card.click();
    })()`
  });

  await new Promise(r => setTimeout(r, 1000));

  // Capture Active Modal
  const shot2 = await call('Page.captureScreenshot', { format: 'png' });
  const outPath2 = path.join(artifactDir, 'sovereign_trust_modal_active.png');
  fs.writeFileSync(outPath2, Buffer.from(shot2.result.data, 'base64'));
  console.log('✓ Captured sovereign_trust_modal_active.png');

  ws.close();
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('Verification finished successfully.');
}

run().catch(err => {
  console.error('Error during capture:', err);
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
});
