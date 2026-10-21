const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const port = 9398;
const userDataDir = path.join(process.env.TEMP, 'edge_euro_' + Date.now());
const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

const edge = spawn(edgePath, [
  '--headless=new',
  '--remote-debugging-port=' + port,
  '--user-data-dir=' + userDataDir,
  '--window-size=1440,1100',
  'about:blank'
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
  const target = pages[0];
  if (!target) { console.log('No page found'); edge.kill(); return; }

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

  const portals = [
    { code: 'nl', url: 'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/nl/index.html' },
    { code: 'en', url: 'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/en/index.html' },
    { code: 'de', url: 'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/de/index.html' }
  ];

  for (const portal of portals) {
    console.log(`Navigating to ${portal.code.toUpperCase()} portal...`);
    await call('Page.navigate', { url: portal.url });
    await new Promise(r => setTimeout(r, 2000));

    // Scroll to Tier Matrix
    await call('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('tier-matrix');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));

    const shotMatrix = await call('Page.captureScreenshot', { format: 'png' });
    const outMatrix = path.join(artifactDir, `tier_matrix_${portal.code}.png`);
    fs.writeFileSync(outMatrix, Buffer.from(shotMatrix.result.data, 'base64'));
    console.log(`✓ Saved tier_matrix_${portal.code}.png`);

    // Scroll to Trust Ribbon
    await call('Runtime.evaluate', {
      expression: `(() => {
        const el = document.getElementById('compliance');
        if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
      })()`
    });
    await new Promise(r => setTimeout(r, 1000));

    const shotTrust = await call('Page.captureScreenshot', { format: 'png' });
    const outTrust = path.join(artifactDir, `trust_ribbon_${portal.code}.png`);
    fs.writeFileSync(outTrust, Buffer.from(shotTrust.result.data, 'base64'));
    console.log(`✓ Saved trust_ribbon_${portal.code}.png`);
  }

  ws.close();
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  console.log('All European portal screenshots captured successfully.');
}

run().catch(err => {
  console.error(err);
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
});
