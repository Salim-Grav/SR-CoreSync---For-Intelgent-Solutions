const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

const artifactDir = 'C:\\Users\\msali\\.gemini\\antigravity-ide\\brain\\eda8867d-4637-48b6-b108-cbac02b9a95e';

async function capture() {
  const port = 9394;
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--window-size=1440,900',
    'http://localhost:8092/demo.html?noredirect=1'
  ]);

  await new Promise(r => setTimeout(r, 2200));
  const pages = await new Promise((res, rej) => {
    http.get('http://127.0.0.1:' + port + '/json', r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });

  const p = pages.find(p => p.url && p.url.includes('demo.html'));
  const ws = new WebSocket(p.webSocketDebuggerUrl);
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

  // Trigger hotline open
  const evalRes = await call('Runtime.evaluate', {
    expression: `(() => {
      const w = document.getElementById('sovereignHotlineWidget');
      if (!w) return 'widget not found';
      w.classList.add('open');
      const card = document.getElementById('hotlinePopoverCard');
      return {
        classes: w.className,
        cardDisplay: window.getComputedStyle(card).display,
        cardRect: { x: card.getBoundingClientRect().x, y: card.getBoundingClientRect().y, w: card.getBoundingClientRect().width, h: card.getBoundingClientRect().height }
      };
    })()`,
    returnByValue: true
  });
  console.log('Eval result:', evalRes.result.result.value);

  await new Promise(r => setTimeout(r, 1200));

  const shot = await call('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(path.join(artifactDir, 'feature3_hotline_open_verified.png'), Buffer.from(shot.result.data, 'base64'));
  console.log('Saved feature3_hotline_open_verified.png');

  ws.close();
  edge.kill();
}

capture().catch(console.error);
