const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const port = 9388;
const userDataDir = path.join(process.env.TEMP, 'edge_diag_' + Date.now());
const edge = spawn(edgePath, [
  '--headless=new',
  '--remote-debugging-port=' + port,
  '--user-data-dir=' + userDataDir,
  '--lang=nl-NL',
  'file:///D:/I-Ai/App/S%26R%20CoreSync%20Solutions/Project/index.html'
]);

async function run() {
  await new Promise(r => setTimeout(r, 2200));
  const pages = await new Promise((res, rej) => {
    http.get('http://127.0.0.1:' + port + '/json', r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });
  const target = pages.find(p => p.url && p.url.includes('index.html'));
  if (!target) { console.log('Page not found'); return; }

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

  await new Promise(r => setTimeout(r, 2500));

  const bannerRes = await call('Runtime.evaluate', {
    expression: 'document.getElementById("srGeoLangBanner") ? document.getElementById("srGeoLangBanner").className : "NOT_FOUND"'
  });
  console.log('Banner status:', bannerRes.result.result.value);

  const scriptRes = await call('Runtime.evaluate', {
    expression: 'String(window.__SR_GEO_LANG_INITIALIZED__)'
  });
  console.log('Script initialized:', scriptRes.result.result.value);

  const locRes = await call('Runtime.evaluate', {
    expression: 'window.location.href'
  });
  console.log('Current URL:', locRes.result.result.value);

  ws.close();
  edge.kill();
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
}

run().catch(e => { console.error(e); edge.kill(); });
