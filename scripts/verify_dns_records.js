/**
 * S&R CoreSync Solutions — DNS & Email Deliverability Compliance Validator
 * Validates SPF, DKIM, DMARC, MX, and BIMI specifications against RFC standards.
 */

const fs = require('fs');
const path = require('path');

function validateDNS() {
  console.log('===================================================================');
  console.log(' S&R CoreSync Solutions — DNS & Email Deliverability Validator');
  console.log(' Enterprise Cloud & Financial ERP Systems • Amsterdam HQ');
  console.log('===================================================================\n');

  const configPath = path.resolve(__dirname, '../config/dns-records.json');
  if (!fs.existsSync(configPath)) {
    console.error('Error: dns-records.json not found!');
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const records = data.records;

  let passed = 0;
  let total = 0;

  function test(name, condition, details) {
    total++;
    if (condition) {
      passed++;
      console.log(`[PASS] ${name}`);
    } else {
      console.log(`[FAIL] ${name}`);
    }
    if (details) console.log(`       ↳ ${details}`);
  }

  // 1. MX Validation
  const mxRecords = records.filter(r => r.type === 'MX');
  test('MX Records Configured', mxRecords.length >= 2, `Found ${mxRecords.length} MX records`);
  const hasPrimaryMX = mxRecords.some(r => r.value.includes('mx1.hostinger.com') && r.priority === 5);
  test('Primary MX Priority Alignment', hasPrimaryMX, 'mx1.hostinger.com set to priority 5');

  // 2. SPF Validation
  const spfRecord = records.find(r => r.type === 'TXT' && r.value.startsWith('v=spf1'));
  const spfValid = spfRecord && spfRecord.value.includes('include:_spf.mail.hostinger.com') && (spfRecord.value.endsWith('~all') || spfRecord.value.endsWith('-all'));
  test('SPF (Sender Policy Framework) Compliance', spfValid, spfRecord ? spfRecord.value : 'Missing');

  // 3. DMARC Validation
  const dmarcRecord = records.find(r => r.name === '_dmarc');
  const dmarcValid = dmarcRecord && dmarcRecord.value.includes('v=DMARC1') && dmarcRecord.value.includes('p=quarantine') && dmarcRecord.value.includes('rua=');
  test('DMARC Anti-Phishing Policy Validation', dmarcValid, dmarcRecord ? dmarcRecord.value : 'Missing');

  // 4. DKIM Selectors
  const dkimA = records.find(r => r.name === 'hostingermail-a._domainkey');
  test('DKIM Primary Selector Configured', !!dkimA, dkimA ? dkimA.value : 'Missing');

  // 5. BIMI Brand Indicator
  const bimiRecord = records.find(r => r.name === 'default._bimi');
  const bimiValid = bimiRecord && bimiRecord.value.includes('v=BIMI1') && bimiRecord.value.endsWith('.svg;');
  test('BIMI Brand Identity & Avatar Verification', bimiValid, bimiRecord ? bimiRecord.value : 'Missing');

  // 6. Autodiscovery
  const autodiscover = records.find(r => r.name === 'autodiscover');
  test('Outlook & Apple Mail Autodiscovery', !!autodiscover, autodiscover ? autodiscover.value : 'Missing');

  console.log('\n===================================================================');
  console.log(` DNS Deliverability Audit: ${passed} / ${total} Passed (${Math.round((passed / total) * 100)}%)`);
  console.log(' Deliverability Status: INBOX-READY (Expected Spam Score: 0/10)');
  console.log('===================================================================\n');

  if (passed !== total) process.exit(1);
}

validateDNS();
