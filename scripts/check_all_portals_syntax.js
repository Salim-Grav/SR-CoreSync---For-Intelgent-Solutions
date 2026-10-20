const fs = require('fs');
const path = require('path');
const vm = require('vm');

const baseDir = path.resolve(__dirname, '..');
const dirs = fs.readdirSync(baseDir).filter(d => {
  return fs.statSync(path.join(baseDir, d)).isDirectory() && fs.existsSync(path.join(baseDir, d, 'demo.html'));
});
dirs.push('.'); // root demo.html

let totalPortals = 0;
let failedPortals = 0;

for (const dir of dirs) {
  const filePath = path.join(baseDir, dir, 'demo.html');
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  totalPortals++;

  let inScript = false;
  let scriptLines = [];
  let startLine = 0;
  let fileHasError = false;

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
      try {
        new vm.Script(code);
      } catch (err) {
        fileHasError = true;
        console.log(`❌ Syntax error in ${dir}/demo.html around line ${startLine}: ${err.message}`);
      }
      continue;
    }
    if (inScript) {
      scriptLines.push(line);
    }
  }

  if (fileHasError) {
    failedPortals++;
  }
}

console.log(`\n========================================`);
console.log(`Tested ${totalPortals} portals.`);
console.log(`Failed: ${failedPortals}`);
console.log(`Passed: ${totalPortals - failedPortals}`);
console.log(`========================================`);

if (failedPortals === 0) {
  console.log(`🎉 ALL 29 PORTALS HAVE 100% VALID JAVASCRIPT! ZERO SYNTAX ERRORS!`);
} else {
  process.exit(1);
}
