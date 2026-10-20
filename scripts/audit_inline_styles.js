const fs = require('fs');
const html = fs.readFileSync('demo.html', 'utf8');
const regex = /style=["']([^"']+)["']/g;
let match;
const styles = [];
while ((match = regex.exec(html)) !== null) {
  styles.push(match[1].trim());
}
console.log('Total style instances:', styles.length);
const unique = [...new Set(styles)];
console.log('Unique styles:', unique.length);
unique.slice(0, 15).forEach((s, i) => console.log(`${i+1}: ${s}`));
