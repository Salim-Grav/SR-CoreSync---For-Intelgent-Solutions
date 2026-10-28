/**
 * ==============================================================================
 * S&R CoreSync For Intelligent Solutions - Sovereign Platform
 * PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY
 * 
 * Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
 * Unauthorized copying, decompilation, redistribution, or external model training
 * of this file, via any medium, is strictly prohibited.
 * ==============================================================================
 */

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const edgePath = fs.existsSync('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
  ? 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  : 'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe';

async function test() {
  const port = 9391;
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=' + port,
    'http://localhost:8092/demo.html'
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
      const el = document.getElementById('sovereignHotlineWidget');
      if (!el) return { found: false };
      const cs = window.getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return {
        found: true,
        display: cs.display,
        position: cs.position,
        zIndex: cs.zIndex,
        bottom: cs.bottom,
        left: cs.left,
        right: cs.right,
        rect: { x: r.x, y: r.y, width: r.width, height: r.height, top: r.top, bottom: r.bottom }
      };
    })()`,
    returnByValue: true
  });
  console.log('Full res:', JSON.stringify(res));
  ws.close();
  edge.kill();
}
test().catch(console.error);
