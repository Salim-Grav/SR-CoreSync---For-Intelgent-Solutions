const fs = require('fs');
const path = require('path');

const demoHtmlPath = path.join(__dirname, '..', 'demo.html');
const demoCssPath = path.join(__dirname, '..', 'css', 'demo-portal.css');

let html = fs.readFileSync(demoHtmlPath, 'utf8');

// Regex to find style attributes on tags
// Matches: style="value" or style='value'
// Accommodates single quotes inside double quotes (like font-family: 'Alexandria', sans-serif;)
const styleAttrRegex = /\sstyle=(["'])([\s\S]*?)\1(?=[\s>/])/g;

const matches = [];
let m;
while ((m = styleAttrRegex.exec(html)) !== null) {
  matches.push({
    fullMatch: m[0],
    quote: m[1],
    css: m[2].trim(),
    index: m.index
  });
}

console.log('Total style attributes matched:', matches.length);

const uniqueStyles = new Map();
let classCounter = 1;

matches.forEach(item => {
  if (!uniqueStyles.has(item.css)) {
    uniqueStyles.set(item.css, `ds-u${classCounter++}`);
  }
});

console.log('Unique CSS rules generated:', uniqueStyles.size);
