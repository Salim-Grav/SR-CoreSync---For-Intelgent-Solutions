const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

async function test() {
  const port = 9395;
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    '--window-size=1440,900',
    'http://localhost:8092/demo.html?noredirect=1'
  ]);
  await new Promise(r => setTimeout(r, 2000));
  const pages = await new Promise((res, rej) => {
    http.get('http://127.0.0.1:' + port + '/json', r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => res(JSON.parse(d)));
    }).on('error', rej);
  });
  const p = pages.find(p => p.url.includes('demo.html'));
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

  const res = await call('Runtime.evaluate', {
    expression: `(() => {
      const w = document.getElementById('sovereignHotlineWidget');
      const b = document.getElementById('hotlineTriggerBtn');
      const c = document.getElementById('hotlinePopoverCard');
      return {
        windowH: window.innerHeight,
        windowW: window.innerWidth,
        wDisplay: window.getComputedStyle(w).display,
        wPos: window.getComputedStyle(w).position,
        wZ: window.getComputedStyle(w).zIndex,
        wBottom: window.getComputedStyle(w).bottom,
        wLeft: window.getComputedStyle(w).left,
        wRight: window.getComputedStyle(w).right,
        bDisplay: window.getComputedStyle(b).display,
        bOpacity: window.getComputedStyle(b).opacity,
        bVisibility: window.getComputedStyle(b).visibility,
        bRect: { x: b.getBoundingClientRect().x, y: b.getBoundingClientRect().y, w: b.getBoundingClientRect().width, h: b.getBoundingClientRect().height },
        cDisplay: window.getComputedStyle(c).display,
        cOpacity: window.getComputedStyle(c).opacity
      };
    })()`,
    returnByValue: true
  });
  console.log('DOM info:', JSON.stringify(res.result.result.value, null, 2));
  ws.close();
  edge.kill();
}
test().catch(console.error);
