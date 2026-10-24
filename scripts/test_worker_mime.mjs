// Throwaway harness: exercises buildMime() outside the Workers runtime.
// The worker imports 'cloudflare:sockets', which Node cannot resolve, so the
// import is stripped and the helpers are re-exported before the module loads.
import { readFile, writeFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';

const source = await readFile('workers/sr-lead-capture/src/index.js', 'utf8');
const patched = source
    .replace(/^import .*cloudflare:sockets';$/m, '')
    + '\nexport { buildMime, b64, smtpConfigured };\n';

const dir = await mkdtemp(path.join(tmpdir(), 'sr-mime-'));
const file = path.join(dir, 'worker.mjs');
await writeFile(file, patched, 'utf8');

const { buildMime, b64, smtpConfigured } = await import('file://' + file.replace(/\\/g, '/'));

let failures = 0;
function check(label, condition, detail) {
    if (condition) {
        console.log('  ok   ' + label);
    } else {
        failures++;
        console.log('  FAIL ' + label + (detail ? ' — ' + detail : ''));
    }
}

console.log('buildMime');

const html = '<p>مرحبا بالعالم — S&R CoreSync</p>';
const text = 'مرحبا بالعالم\nsecond line';
const raw = buildMime({
    from: 'info@sr-coresync.com',
    fromName: 'S&R CoreSync Solutions',
    to: 'owner@example.com',
    subject: 'استفسار جديد — LEAD-SR-1',
    html,
    text,
    replyTo: 'info@sr-coresync.com'
});

check('has From with display name', raw.includes('From: S&R CoreSync Solutions <info@sr-coresync.com>'));
check('has To', raw.includes('To: owner@example.com'));
check('subject is RFC 2047 encoded', /^Subject: =\?UTF-8\?B\?/m.test(raw));
check('Message-ID uses the sending domain', /Message-ID: <[^>]+@sr-coresync\.com>/.test(raw));
check('Date is RFC 5322', /^Date: .+\+0000$/m.test(raw));
check('multipart/alternative declared', raw.includes('Content-Type: multipart/alternative; boundary="alt-'));
check('both views present', raw.includes('Content-Type: text/plain; charset=UTF-8')
    && raw.includes('Content-Type: text/html; charset=UTF-8'));
check('header/body separator present', raw.includes('\r\n\r\n'));
check('body lines are wrapped at 76', raw.split('\r\n').every((line) => line.length <= 998));
check('Arabic subject survives round-trip',
    Buffer.from(/(?:Subject: =\?UTF-8\?B\?)([^?]+)/.exec(raw)[1], 'base64').toString('utf8')
        .includes('استفسار جديد'));

const htmlOnly = buildMime({ from: 'info@sr-coresync.com', to: 'a@b.c', subject: 'hi', html: '<b>x</b>' });
check('html-only is a single part', htmlOnly.includes('Content-Type: text/html; charset=UTF-8')
    && !htmlOnly.includes('multipart/'));

const withPdf = buildMime({
    from: 'info@sr-coresync.com', to: 'a@b.c', subject: 'contract',
    text: 'attached', attachmentName: 'contract.pdf', attachmentB64: Buffer.from('%PDF-1.4 test').toString('base64')
});
check('attachment wraps in multipart/mixed', withPdf.includes('Content-Type: multipart/mixed; boundary="mix-'));
check('attachment is named', withPdf.includes('filename="contract.pdf"'));
check('attachment has its own boundary close', withPdf.trimEnd().endsWith('--mix-' + withPdf.match(/boundary="mix-([^"]+)"/)[1] + '--'));

check('b64 handles Arabic', Buffer.from(b64('س'), 'base64').toString('utf8') === 'س');
check('smtp not configured without secrets', smtpConfigured({}) === false);
check('smtp configured with both', smtpConfigured({ PURELYMAIL_USER: 'a', PURELYMAIL_PASS: 'b' }) === true);
check('smtp not configured with only a user', smtpConfigured({ PURELYMAIL_USER: 'a' }) === false);

console.log(failures === 0 ? '\nPASS' : '\n' + failures + ' FAILED');
process.exit(failures === 0 ? 0 : 1);
