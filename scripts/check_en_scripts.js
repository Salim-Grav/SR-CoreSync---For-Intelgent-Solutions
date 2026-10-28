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

const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('en/demo.html', 'utf8');
const lines = html.split('\n');

let inScript = false;
let scriptLines = [];
let startLine = 0;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes('<script') && !line.includes('src=')) {
    inScript = true;
    scriptLines = [];
    startLine = i + 1;
    continue;
  }
  if (line.includes('</script>') && inScript) {
    inScript = false;
    const code = scriptLines.join('\n');
    console.log(`Checking script from line ${startLine} (${code.length} chars)...`);
    try {
      new vm.Script(code);
      console.log(`✅ Script from line ${startLine} is valid JS!`);
    } catch (err) {
      console.log(`❌ Script from line ${startLine} error:`, err.message);
      const lineMatch = err.stack.match(/evalmachine\.<anonymous>:(\d+)/);
      if (lineMatch) {
        const errRelLine = parseInt(lineMatch[1], 10);
        console.log(`Actual file line approx: ${startLine + errRelLine - 1}`);
        for (let j = Math.max(0, errRelLine - 3); j <= Math.min(scriptLines.length - 1, errRelLine + 2); j++) {
          console.log(`  ${startLine + j}: ${scriptLines[j]}`);
        }
      }
    }
    continue;
  }
  if (inScript) {
    scriptLines.push(line);
  }
}
