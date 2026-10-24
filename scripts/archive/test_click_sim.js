const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

async function testClick(slug, filename) {
  const port = 9380 + Math.floor(Math.random() * 20);
  const userDataDir = path.join(process.env.TEMP, 'test_click_' + slug + '_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    'http://127.0.0.1:8765/software.html'
  ]);

  try {
    await new Promise(r => setTimeout(r, 2500));
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

    // Click simulator button directly
    const res = await call('Runtime.evaluate', {
      expression: `
        (() => {
          const banner = document.querySelector('.sr-gdpr-banner, [class*="gdpr"]');
          if (banner) banner.remove();

          const btn = document.querySelector("button[onclick*='${slug}']");
          if (btn) {
            btn.click();
            return 'CLICKED_BUTTON_SUCCESS';
          }
          if (typeof openSoftwareLiveApp === 'function') {
            openSoftwareLiveApp('${slug}');
            return 'CALLED_FUNCTION_DIRECTLY';
          }
          return 'NOT_FOUND';
        })()
      `,
      returnByValue: true
    });

    console.log('Click result for ' + slug + ':', res.result ? res.result.value : res);

    await new Promise(r => setTimeout(r, 1200));

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outImg = path.join(artDir, filename);
    fs.writeFileSync(outImg, Buffer.from(shot.result.data, 'base64'));
    console.log('Saved screenshot to ' + outImg);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 800);
  }
}

async function main() {
  await testClick('omnibakery', 'test_omnibakery_sim.png');
  await testClick('civicsync', 'test_civicsync_sim.png');
}
main();
