const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const port = 9394;
const userDataDir = path.join(process.env.TEMP, 'edge_matrix_' + Date.now());
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
  await call('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 1100,
    deviceScaleFactor: 1,
    mobile: false
  });

  await new Promise(r => setTimeout(r, 2000));

  // 1. Scroll into view of #tier-matrix
  await call('Runtime.evaluate', {
    expression: `(() => {
      const el = document.getElementById('tier-matrix');
      if (el) {
        el.scrollIntoView({ behavior: 'instant', block: 'start' });
      }
    })()`
  });

  await new Promise(r => setTimeout(r, 1200));

  // Capture State 1: Annual billing (default)
  const shot1 = await call('Page.captureScreenshot', { format: 'png' });
  const outPath1 = path.join(artifactDir, 'enterprise_tier_matrix_annual.png');
  fs.writeFileSync(outPath1, Buffer.from(shot1.result.data, 'base64'));
  console.log('✓ Captured enterprise_tier_matrix_annual.png');

  // 2. Switch to Monthly
  await call('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.querySelector('.sr-tier-toggle-btn[data-billing="monthly"]');
      if (btn) btn.click();
    })()`
  });

  await new Promise(r => setTimeout(r, 800));

  const shot2 = await call('Page.captureScreenshot', { format: 'png' });
  const outPath2 = path.join(artifactDir, 'enterprise_tier_matrix_monthly.png');
  fs.writeFileSync(outPath2, Buffer.from(shot2.result.data, 'base64'));
  console.log('✓ Captured enterprise_tier_matrix_monthly.png');

  // 3. Switch to 4+ Entities (Group Holding Discount)
  await call('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.querySelector('.sr-tier-entity-btn[data-entities="4"]');
      if (btn) btn.click();
    })()`
  });

  await new Promise(r => setTimeout(r, 800));

  const shot3 = await call('Page.captureScreenshot', { format: 'png' });
  const outPath3 = path.join(artifactDir, 'enterprise_tier_matrix_multi_entity.png');
  fs.writeFileSync(outPath3, Buffer.from(shot3.result.data, 'base64'));
  console.log('✓ Captured enterprise_tier_matrix_multi_entity.png');

  ws.close();
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('Tier Matrix verification completed.');
}

run().catch(err => {
  console.error('Error during capture:', err);
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
});
