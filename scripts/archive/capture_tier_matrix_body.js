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

const port = 9396;
const userDataDir = path.join(process.env.TEMP, 'edge_matrix_body_' + Date.now());
const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

const edge = spawn(edgePath, [
  '--headless=new',
  '--remote-debugging-port=' + port,
  '--user-data-dir=' + userDataDir,
  '--window-size=1440,1100',
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

  await new Promise(r => setTimeout(r, 2000));

  // Scroll to table body rows
  await call('Runtime.evaluate', {
    expression: `(() => {
      const el = document.querySelector('.sr-tier-category-row');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
    })()`
  });

  await new Promise(r => setTimeout(r, 1200));

  const shot = await call('Page.captureScreenshot', { format: 'png' });
  const outPath = path.join(artifactDir, 'enterprise_tier_matrix_body.png');
  fs.writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
  console.log('✓ Captured enterprise_tier_matrix_body.png');

  ws.close();
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
}

run().catch(err => {
  console.error(err);
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
});
