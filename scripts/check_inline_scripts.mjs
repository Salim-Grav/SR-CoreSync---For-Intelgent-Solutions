/**
 * S&R CoreSync Solutions - inline script syntax checker
 * Extracts every inline <script> block from the published HTML pages and
 * parses it with the JavaScript engine, so a corrupted translation cannot
 * reach production unnoticed.
 *
 * Usage: node scripts/check_inline_scripts.mjs
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import vm from 'node:vm';

const ROOT = process.cwd();
const SKIP = new Set(['.git', '_site', 'workers', 'scripts', 'dist', 'node_modules',
    '__pycache__', '.github', '.agents', '.vscode', 'api', 'config']);

function walk(dir, acc = []) {
    for (const entry of readdirSync(dir)) {
        if (SKIP.has(entry) || entry.startsWith('_')) continue;
        const full = join(dir, entry);
        const st = statSync(full);
        if (st.isDirectory()) walk(full, acc);
        else if (entry.endsWith('.html')) acc.push(full);
    }
    return acc;
}

const files = walk(ROOT);
let blocks = 0;
let jsonBlocks = 0;
let failures = 0;

console.log('='.repeat(72));
console.log('S&R CoreSync - Inline Script Syntax Check');
console.log('='.repeat(72));
console.log('HTML files: ' + files.length);

for (const file of files) {
    const html = readFileSync(file, 'utf8');
    const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
    let m;
    let index = 0;
    while ((m = re.exec(html)) !== null) {
        const attrs = m[1] || '';
        const body = m[2] || '';
        if (/src\s*=/i.test(attrs)) continue;   // external file, checked separately
        const line = html.slice(0, m.index).split('\n').length;
        const rel = relative(ROOT, file).replace(/\\/g, '/');

        if (/type\s*=\s*["']?application\/ld\+json/i.test(attrs)) {
            jsonBlocks++;
            try {
                JSON.parse(body);
            } catch (err) {
                failures++;
                console.log(`  X ${rel}  line ${line}  ->  invalid JSON-LD: ${err.message}`);
            }
            index++;
            continue;
        }

        if (/type\s*=\s*["']?(?!javascript|module|ecmascript)/i.test(attrs)) continue; // templates
        if (!body.trim()) continue;
        blocks++;
        try {
            new vm.Script(body, { filename: `${rel}#block${index + 1}` });
        } catch (err) {
            failures++;
            console.log(`  X ${rel}  line ${line}  ->  ${err.message}`);
        }
        index++;
    }
}

console.log('-'.repeat(72));
console.log(`Inline script blocks parsed: ${blocks}`);
console.log(`JSON-LD blocks validated  : ${jsonBlocks}`);
if (failures) {
    console.log(`FAILED - ${failures} block(s) contain a syntax error.`);
    console.log('='.repeat(72));
    process.exit(1);
}
console.log('PASSED - every inline script and JSON-LD block is valid.');
console.log('='.repeat(72));
