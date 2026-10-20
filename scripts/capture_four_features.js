const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\eda8867d-4637-48b6-b108-cbac02b9a95e';

async function captureFeature(url, outName, evalScript = null) {
  const port = 9380 + Math.floor(Math.random() * 50);
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_feat_' + Date.now());
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
      await new Promise(r => setTimeout(r, 800));
    }

    await new Promise(r => setTimeout(r, 1000));

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
  console.log('1. Capturing VIP Proposal Banner...');
  await captureFeature(
    'http://localhost:8092/demo.html',
    'feature1_vip_proposal_banner.png',
    `const inp = document.getElementById('quickClientNameInput'); if (inp) { inp.value = 'Al-Noor European Trading B.V.'; inp.dispatchEvent(new Event('input')); }`
  );

  console.log('2. Capturing Smart ROI Calculator Tab...');
  await captureFeature(
    'http://localhost:8092/demo.html',
    'feature2_roi_calculator.png',
    `switchPortalTab('roi', document.getElementById('tourNav-roi'));`
  );

  console.log('3. Capturing Direct Founders Hotline Widget...');
  await captureFeature(
    'http://localhost:8092/demo.html',
    'feature3_hotline_widget.png',
    `const widget = document.getElementById('sovereignHotlineWidget'); if (widget) widget.classList.add('open');`
  );

  console.log('4. Capturing Live E-Invoicing Simulator...');
  await captureFeature(
    'http://localhost:8092/demo.html',
    'feature4_einvoicing_simulator.png',
    `switchPortalTab('invoices', document.getElementById('tourNav-invoices'));`
  );

  console.log('All 4 feature screenshots captured successfully!');
}

main().catch(err => {
  console.error('Error during capture:', err);
  process.exit(1);
});
