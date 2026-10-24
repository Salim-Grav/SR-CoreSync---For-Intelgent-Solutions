const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\fb165293-a382-4790-9d97-89e32247a0a7';

async function captureApp(appId, outFilename) {
  const port = 9340 + Math.floor(Math.random() * 50);
  const userDataDir = path.join(process.env.TEMP, 'edge_sim_' + appId + '_' + Date.now());
  const url = `http://127.0.0.1:8765/software.html`;

  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--window-size=1440,960',
    url
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

    const targetPage = pages.find(p => p.url && p.url.includes('preview-software'));
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

    // Dismiss GDPR banner and trigger simulator
    const evalResult = await call('Runtime.evaluate', {
      expression: `
        (async () => {
          try {
            localStorage.setItem('coresync_gdpr_status', 'accepted');
            const banners = document.querySelectorAll('.sr-gdpr-banner, [class*="gdpr"], [class*="cookie"]');
            banners.forEach(b => b.remove());

            // Wait for openSoftwareLiveApp to be available
            let attempts = 0;
            while (typeof window.openSoftwareLiveApp !== 'function' && attempts < 25) {
              await new Promise(r => setTimeout(r, 200));
              attempts++;
            }

            if (typeof window.openSoftwareLiveApp === 'function') {
              window.openSoftwareLiveApp('${appId}');
              return 'OPENED_${appId}';
            } else {
              return 'FUNCTION_NOT_FOUND';
            }
          } catch(e) {
            return 'ERROR: ' + e.message;
          }
        })()
      `,
      awaitPromise: true
    });

    console.log(`Evaluate result for ${appId}:`, evalResult.result ? evalResult.result.value : evalResult);

    await new Promise(r => setTimeout(r, 1800));

    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const outImg = path.join(artDir, outFilename);
    fs.writeFileSync(outImg, Buffer.from(shot.result.data, 'base64'));
    console.log(`SUCCESS: Captured ${appId} simulator to ${outImg}`);

    ws.close();
  } finally {
    edge.kill();
    setTimeout(() => {
      try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch(e) {}
    }, 1000);
  }
}

async function run() {
  await captureApp('civicsync', 'simulator_civicsync_live.png');
  await captureApp('omnibakery', 'simulator_omnibakery_live.png');
  await captureApp('healthbridge', 'simulator_healthbridge_live.png');
  console.log('ALL SIMULATORS CAPTURED!');
}

run().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
