const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

async function capture() {
  const port = 9335;
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_clean_layout_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://localhost:3000/index.html'
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

    const targetPage = pages.find(p => p.url && p.url.includes('localhost:3000'));
    if (!targetPage) throw new Error('Target page not found');

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

    // Dismiss cookie/GDPR banners and scroll top
    await call('Runtime.evaluate', {
      expression: `
        try {
          localStorage.setItem('coresync_gdpr_status', 'accepted');
          const banner = document.querySelector('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
          if (banner) banner.style.display = 'none';
          window.scrollTo(0, 0);
        } catch(e) {}
      `
    });

    await new Promise(r => setTimeout(r, 1200));

    // Capture clean header and hero view
    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outImg = 'C:\\\\Users\\\\msali\\\\.gemini\\\\antigravity-ide\\\\brain\\\\e95ea78a-2d22-4f0f-8610-eae376ecc506\\\\live_clean_layout.png';
    fs.writeFileSync(outImg, Buffer.from(shot.result.data, 'base64'));
    console.log('SUCCESS: Captured clean layout to ' + outImg);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 1000);
  }
}

capture().catch(err => {
  console.error('Capture error:', err);
  process.exit(1);
});
