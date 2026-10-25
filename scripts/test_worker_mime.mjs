// Unit checks for the enquiry routing rules and the MIME builder.
// The worker imports 'cloudflare:sockets', which Node cannot resolve, so the
// import is stripped and the helpers are re-exported before the module loads.
import { readFile, writeFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';

const source = await readFile('workers/sr-lead-capture/src/index.js', 'utf8');
const patched = source
    .replace(/^import .*cloudflare:sockets';$/m, '')
    + '\nexport { buildMime, b64, smtpConfigured, leadRecipients, departmentsFor };\n';

const dir = await mkdtemp(path.join(tmpdir(), 'sr-worker-'));
const file = path.join(dir, 'worker.mjs');
await writeFile(file, patched, 'utf8');

const { buildMime, b64, smtpConfigured, leadRecipients, departmentsFor } =
    await import('file://' + file.replace(/\\/g, '/'));

let failures = 0;
function check(label, condition, detail) {
    if (condition) {
        console.log('  ok   ' + label);
    } else {
        failures++;
        console.log('  FAIL ' + label + (detail ? ' — ' + detail : ''));
    }
}

const env = { NOTIFY_EMAIL: 'info@sr-coresync.com' };

console.log('routing');
check('every enquiry reaches the owner',
    leadRecipients({ clientName: 'A', notes: 'we would like a demo' }, env).recipients
        .join(',') === 'info@sr-coresync.com');
check('invoice wording adds billing',
    leadRecipients({ notes: 'please send the invoice for the license' }, env)
        .recipients.includes('billing@sr-coresync.com'));
check('support wording adds support',
    leadRecipients({ notes: 'we hit an error during migration' }, env)
        .recipients.includes('support@sr-coresync.com'));
check('both can fire together',
    leadRecipients({ notes: 'invoice error' }, env).departments.sort().join(',') === 'billing,support');
check('"private" does not trigger VAT',
    !leadRecipients({ notes: 'a private matter' }, env).departments.includes('billing'));
check('owner stays first',
    leadRecipients({ notes: 'invoice needed' }, env).recipients[0] === 'info@sr-coresync.com');
check('no duplicate recipients',
    (() => {
        const list = leadRecipients({ notes: 'invoice and payment' }, env).recipients;
        return new Set(list).size === list.length;
    })());
check('LEAD_ROUTES overrides an address',
    leadRecipients({ notes: 'invoice' }, { ...env, LEAD_ROUTES: 'billing=finance@example.com' })
        .recipients.includes('finance@example.com'));
check('LEAD_ROUTES can disable a department',
    !leadRecipients({ notes: 'invoice' }, { ...env, LEAD_ROUTES: 'billing=' }).departments.length);
check('empty enquiry still reaches the owner',
    leadRecipients({}, env).recipients.length === 1);

console.log('executive routing');
const big = leadRecipients({ notes: 'Our corporate group is running an RFP for ERP.' }, env);
check('enterprise wording adds both founders',
    big.recipients.includes('raed@sr-coresync.com') && big.recipients.includes('salim@sr-coresync.com'),
    big.recipients.join(','));
check('executive route named once', big.departments.filter((d) => d === 'executive').length === 1);
check('founders keep the owner informed too', big.recipients[0] === 'info@sr-coresync.com');
check('a tender also reaches billing? no', !big.departments.includes('billing'));
check('white-label triggers executives',
    leadRecipients({ notes: 'we want to resell your platform white-label' }, env)
        .departments.includes('executive'));
check('a plain demo request does not page founders',
    !leadRecipients({ notes: 'please show me a demo' }, env).departments.includes('executive'));
check('executive route can be switched off',
    !leadRecipients({ notes: 'corporate RFP' }, { ...env, LEAD_ROUTES: 'executive=' })
        .departments.includes('executive'));
check('a comma list overrides both founders',
    leadRecipients({ notes: 'corporate RFP' }, { ...env, LEAD_ROUTES: 'executive=a@x.com,b@x.com' })
        .recipients.filter((r) => r.endsWith('@x.com')).length === 2);

console.log('multipart addressing');
const multi = buildMime({
    from: 'info@sr-coresync.com', to: 'info@sr-coresync.com, billing@sr-coresync.com',
    subject: 'two recipients', html: '<p>x</p>'
});
check('To header carries both', multi.includes('To: info@sr-coresync.com, billing@sr-coresync.com'));

const html = '<p>مرحبا بالعالم — S&R CoreSync</p>';
const raw = buildMime({
    from: 'info@sr-coresync.com', fromName: 'S&R CoreSync For Intelligent Solutions',
    to: 'owner@example.com', subject: 'استفسار جديد — LEAD-SR-1',
    html, text: 'مرحبا\nsecond line', replyTo: 'info@sr-coresync.com'
});
check('From has a display name', raw.includes('From: S&R CoreSync For Intelligent Solutions <info@sr-coresync.com>'));
check('subject is RFC 2047 encoded', /^Subject: =\?UTF-8\?B\?/m.test(raw));
check('Message-ID uses the sending domain', /Message-ID: <[^>]+@sr-coresync\.com>/.test(raw));
check('multipart/alternative declared', raw.includes('Content-Type: multipart/alternative; boundary="alt-'));
check('Arabic subject survives', Buffer.from(/(?:Subject: =\?UTF-8\?B\?)([^?]+)/.exec(raw)[1], 'base64')
    .toString('utf8').includes('استفسار جديد'));

const withPdf = buildMime({
    from: 'info@sr-coresync.com', to: 'a@b.c', subject: 'contract', text: 'attached',
    attachmentName: 'contract.pdf', attachmentB64: Buffer.from('%PDF-1.4 test').toString('base64')
});
check('attachment wraps in multipart/mixed', withPdf.includes('Content-Type: multipart/mixed; boundary="mix-'));

check('b64 handles Arabic', Buffer.from(b64('س'), 'base64').toString('utf8') === 'س');
check('smtp off without secrets', smtpConfigured({}) === false);
check('smtp on with both', smtpConfigured({ PURELYMAIL_USER: 'a', PURELYMAIL_PASS: 'b' }) === true);

console.log(failures === 0 ? '\nPASS' : '\n' + failures + ' FAILED');
process.exit(failures === 0 ? 0 : 1);
