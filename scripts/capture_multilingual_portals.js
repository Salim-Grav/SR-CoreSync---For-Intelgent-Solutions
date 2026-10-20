const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\eda8867d-4637-48b6-b108-cbac02b9a95e';

async function captureUrl(url, outName, evalScript = null) {
  const port = 9336 + Math.floor(Math.random() * 50);
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_multi_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,900',
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

    const targetPage = pages.find(p => p.url && p.url.includes('localhost:8092'));
    if (!targetPage) throw new Error('Target page not found for ' + url);

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

    if (evalScript) {
      await call('Runtime.evaluate', { expression: evalScript });
      await new Promise(r => setTimeout(r, 600));
    }

    await new Promise(r => setTimeout(r, 1200));

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outPath = path.join(artifactDir, outName);
    fs.writeFileSync(outPath, Buffer.from(shot.result.data, 'base64'));
    console.log(`Saved screenshot: ${outName}`);

    ws.close();
  } finally {
    edge.kill();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  }
}

async function main() {
  console.log('Capturing Sovereign Language Dropdown Menu on demo.html...');
  await captureUrl(
    'http://localhost:8092/demo.html',
    'multilingual_dropdown_open.png',
    `document.getElementById('sovereignLangDropdown').classList.add('open');`
  );

  console.log('Capturing German (DE) demo portal...');
  await captureUrl('http://localhost:8092/de/demo.html', 'de_demo_portal.png');

  console.log('Capturing French (FR) demo portal...');
  await captureUrl('http://localhost:8092/fr/demo.html', 'fr_demo_portal.png');

  console.log('Capturing Turkish (TR) demo portal...');
  await captureUrl('http://localhost:8092/tr/demo.html', 'tr_demo_portal.png');

  console.log('Capturing Swedish (SV) demo portal...');
  await captureUrl('http://localhost:8092/sv/demo.html', 'sv_demo_portal.png');

  console.log('Capturing Kurdish (KU) demo portal...');
  await captureUrl('http://localhost:8092/ku/demo.html', 'ku_demo_portal.png');

  console.log('All multilingual portal screenshots captured successfully!');
}

main().catch(err => {
  console.error('Error during capture:', err);
  process.exit(1);
});
