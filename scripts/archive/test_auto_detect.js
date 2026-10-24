const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

async function testAutoDetect(langCode) {
  const port = 9395;
  const userDataDir = path.join(process.env.TEMP, 'edge_cap_auto_' + Date.now());
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--user-data-dir=' + userDataDir,
    '--lang=' + langCode,
    'http://localhost:8092/demo.html'
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
    console.log('[Auto-Detect Test] OS/Browser Lang: ' + langCode + ' -> Final URL: ' + (targetPage ? targetPage.url : 'Not Found'));
  } finally {
    edge.kill();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
  }
}

async function run() {
  await testAutoDetect('de-DE');
  await testAutoDetect('fr-FR');
  await testAutoDetect('tr-TR');
}

run().catch(console.error);
