/**
 * S&R CoreSync Solutions — live DNS / e-mail authentication checker
 * -----------------------------------------------------------------
 * The previous version of this script read `config/dns-records.json` and
 * validated the JSON against itself, which is how a completely unconfigured
 * domain passed as "compliant". This version resolves the records that the
 * world actually sees.
 *
 * Usage:
 *   node scripts/verify_dns_records.js            # report only
 *   node scripts/verify_dns_records.js --strict   # exit 1 when e-mail auth is incomplete
 */
import { Resolver } from 'node:dns/promises';

const DOMAIN = 'sr-coresync.com';
const SEND_DOMAIN = `send.${DOMAIN}`;
const STRICT = process.argv.includes('--strict');
const DKIM_SELECTORS = ['resend._domainkey', 'mail._domainkey', 'hostingermail-a._domainkey'];

const resolver = new Resolver({ timeout: 5000, tries: 2 });
const results = [];

function record(label, status, detail) {
  results.push({ label, status, detail });
  const tag = { pass: 'PASS', fail: 'FAIL', warn: 'WARN', info: 'INFO' }[status] || 'INFO';
  console.log(`[${tag}] ${label}${detail ? '\n       ↳ ' + detail : ''}`);
}

async function txt(name) {
  try {
    const rows = await resolver.resolveTxt(name);
    return rows.map((parts) => parts.join(''));
  } catch (err) {
    if (['ENOTFOUND', 'ENODATA', 'ESERVFAIL'].includes(err.code)) return [];
    throw err;
  }
}

async function mx(name) {
  try {
    return (await resolver.resolveMx(name)).sort((a, b) => a.priority - b.priority);
  } catch {
    return [];
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log(` S&R CoreSync — live DNS authentication check for ${DOMAIN}`);
  console.log('='.repeat(70));

  // MX
  const mxRecords = await mx(DOMAIN);
  record('MX records', mxRecords.length ? 'pass' : 'fail',
    mxRecords.map((m) => `${m.priority} ${m.exchange}`).join(', ') || 'no MX — inbound mail cannot be delivered');

  // SPF (root)
  const rootTxt = await txt(DOMAIN);
  const spf = rootTxt.find((t) => /^v=spf1/i.test(t));
  record('SPF (root)', spf ? 'pass' : 'fail', spf || 'missing');
  const spfLookups = spf ? (spf.match(/include:|a:|mx|ptr|exists:/g) || []).length : 0;
  if (spf && spfLookups > 10) record('SPF lookup count', 'fail', `${spfLookups} lookups > 10 (RFC 7208 limit)`);

  // SPF (sending subdomain)
  const sendTxt = await txt(SEND_DOMAIN);
  const sendSpf = sendTxt.find((t) => /^v=spf1/i.test(t));
  record(`SPF (${SEND_DOMAIN})`, sendSpf ? 'pass' : 'warn',
    sendSpf || 'not configured — transactional mail is still sent as the root domain');

  // DKIM
  let dkimFound = false;
  for (const selector of DKIM_SELECTORS) {
    const name = `${selector}.${DOMAIN}`;
    let value = null;
    try {
      value = (await resolver.resolveTxt(name))[0]?.join('') || null;
    } catch {
      try {
        value = (await resolver.resolveCname(name))[0] || null;
      } catch { /* not present */ }
    }
    if (value) dkimFound = true;
    record(`DKIM ${name}`, value ? 'pass' : 'warn', value ? `present (${value.slice(0, 60)}…)` : 'absent');
  }

  // DMARC
  const dmarc = (await txt(`_dmarc.${DOMAIN}`)).find((t) => /^v=DMARC1/i.test(t));
  if (!dmarc) {
    record('DMARC', 'fail', 'no _dmarc record — the domain can be spoofed and Gmail/Yahoo bulk rules are unmet');
  } else {
    const policy = (dmarc.match(/p=([a-z]+)/i) || [])[1] || 'none';
    const rua = /rua=mailto:/i.test(dmarc);
    record('DMARC', policy === 'none' ? 'warn' : 'pass', `${dmarc}${rua ? '' : ' (no rua= reporting address)'}`);
  }

  // TLS-RPT
  const tlsrpt = (await txt(`_smtp._tls.${DOMAIN}`)).find((t) => /^v=TLSRPTv1/i.test(t));
  record('TLS-RPT', tlsrpt ? 'pass' : 'warn', tlsrpt || 'optional, absent');

  // BIMI
  const bimi = (await txt(`default._bimi.${DOMAIN}`)).find((t) => /^v=BIMI1/i.test(t));
  record('BIMI', bimi ? 'pass' : 'info', bimi || 'absent (needs DMARC enforcement + a VMC certificate)');

  const failing = results.filter((r) => r.status === 'fail');
  const warning = results.filter((r) => r.status === 'warn');

  console.log('-'.repeat(70));
  console.log(`PASS ${results.filter((r) => r.status === 'pass').length}  WARN ${warning.length}  FAIL ${failing.length}`);
  if (failing.length) {
    console.log('Blocking gaps:');
    for (const f of failing) console.log(`  X ${f.label}: ${f.detail}`);
  }
  if (!dkimFound) console.log('  ! No DKIM selector resolved — provider setup incomplete.');
  console.log(STRICT && failing.length ? 'STRICT MODE: failing.' : 'Report only — see EMAIL-DNS-RUNBOOK.md for the fix order.');
  console.log('='.repeat(70));
  process.exit(STRICT && failing.length ? 1 : 0);
}

main().catch((err) => {
  console.error('DNS check crashed:', err);
  process.exit(2);
});
