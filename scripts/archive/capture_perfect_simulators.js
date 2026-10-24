const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

async function captureSimulator(appId, outName) {
  const port = 9390 + Math.floor(Math.random() * 20);
  const userDataDir = path.join(process.env.TEMP, 'edge_sim_' + appId + '_' + Date.now());

  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://127.0.0.1:8765/software.html'
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

    const target = pages.find(p => p.url && p.url.includes('preview-software'));
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

    // 1. Dismiss cookies/banners
    await call('Runtime.evaluate', {
      expression: `
        try {
          localStorage.setItem('coresync_gdpr_status', 'accepted');
          document.querySelectorAll('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]').forEach(el => el.remove());
        } catch(e) {}
      `
    });

    // 2. Open live app
    const res = await call('Runtime.evaluate', {
      expression: `
        try {
          window.openSoftwareLiveApp('${appId}');
          const modal = document.getElementById('srSoftwareAppModal');
          modal ? modal.className : 'NOT_FOUND';
        } catch(e) {
          e.message;
        }
      `,
      returnByValue: true
    });
    console.log(`[${appId}] modal class:`, res.result?.result?.value || res.result?.value);

    await new Promise(r => setTimeout(r, 1200));

    // 3. Capture screenshot
    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outImg = path.join(artDir, outName);
    fs.writeFileSync(outImg, Buffer.from(shot.result.data, 'base64'));
    console.log(`[${appId}] SUCCESS -> ${outImg}`);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 800);
  }
}

async function run() {
  await captureSimulator('omnibakery', 'simulator_omnibakery_live_clean.png');
  await captureSimulator('civicsync', 'simulator_civicsync_live_clean.png');
  await captureSimulator('healthbridge', 'simulator_healthbridge_live_clean.png');
  console.log('ALL THREE PLATFORM SIMULATORS CAPTURED!');
}

run().catch(err => {
  console.error('Run error:', err);
  process.exit(1);
});
