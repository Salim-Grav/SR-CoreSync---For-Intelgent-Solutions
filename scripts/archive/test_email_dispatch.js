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

/**
 * S&R CoreSync Solutions — Live Email Dispatcher & SMTP Test Suite
 * Automated Test Runner for Invoice/Quote and Welcome Email Templates
 */

const fs = require('fs');
const path = require('path');
const { EmailNotificationService } = require('../api/email-notification-service');

async function runTestSuite() {
  console.log('===================================================================');
  console.log(' S&R CoreSync Solutions — Automated Email & SMTP Test Suite');
  console.log(' Enterprise Cloud & Financial ERP Systems • Amsterdam HQ');
  console.log('===================================================================\n');

  const startTime = Date.now();
  const emailService = new EmailNotificationService();
  const distEmailsDir = path.resolve(__dirname, '../dist/emails');

  if (!fs.existsSync(distEmailsDir)) {
    fs.mkdirSync(distEmailsDir, { recursive: true });
  }

  const results = {
    total: 0,
    passed: 0,
    failed: 0,
    tests: []
  };

  function recordResult(testName, passed, details) {
    results.total++;
    if (passed) results.passed++;
    else results.failed++;
    results.tests.push({ testName, passed, details });
    console.log(`[${passed ? 'PASS' : 'FAIL'}] ${testName}`);
    if (details) console.log(`       ↳ ${details}`);
  }

  // --- Test 1: Compile & Bundle Invoice/Quote Template ---
  try {
    const compiledInvoiceHtml = emailService.compileInvoiceQuoteTemplate({
      clientName: 'مؤسسة الرياض القابضة للاستثمارات التقنية',
      quoteNumber: 'SR-2026-TEST-9901',
      issueDate: '14 أكتوبر 2026',
      validityDays: '30',
      totalFormatted: '€5,445.00'
    });

    const hasEmbeddedStyles = compiledInvoiceHtml.includes('<style type="text/css">');
    const hasDynamicClient = compiledInvoiceHtml.includes('مؤسسة الرياض القابضة');
    const isValid = hasEmbeddedStyles && hasDynamicClient && compiledInvoiceHtml.length > 5000;

    const outFile = path.join(distEmailsDir, 'invoice-quote-compiled.html');
    fs.writeFileSync(outFile, compiledInvoiceHtml, 'utf8');

    recordResult(
      'Invoice/Quote Template Compilation & CSS Bundling',
      isValid,
      `Output saved: ${path.relative(process.cwd(), outFile)} (${(compiledInvoiceHtml.length / 1024).toFixed(1)} KB)`
    );
  } catch (err) {
    recordResult('Invoice/Quote Template Compilation & CSS Bundling', false, err.message);
  }

  // --- Test 2: Compile & Bundle Welcome Email Template ---
  try {
    const compiledWelcomeHtml = emailService.compileWelcomeEmailTemplate({
      customerName: 'شركة النماء الدولية'
    });

    const hasEmbeddedStyles = compiledWelcomeHtml.includes('<style type="text/css">');
    const hasDynamicCustomer = compiledWelcomeHtml.includes('شركة النماء الدولية');
    const isValid = hasEmbeddedStyles && hasDynamicCustomer && compiledWelcomeHtml.length > 3000;

    const outFile = path.join(distEmailsDir, 'welcome-email-compiled.html');
    fs.writeFileSync(outFile, compiledWelcomeHtml, 'utf8');

    recordResult(
      'Welcome Email Template Compilation & CSS Bundling',
      isValid,
      `Output saved: ${path.relative(process.cwd(), outFile)} (${(compiledWelcomeHtml.length / 1024).toFixed(1)} KB)`
    );
  } catch (err) {
    recordResult('Welcome Email Template Compilation & CSS Bundling', false, err.message);
  }

  // --- Test 3: Dispatch Certified Invoice/Quote Email ---
  try {
    const invoiceDispatch = await emailService.sendOfficialInvoiceQuote({
      to: 'client-audit@sr-coresync.com',
      clientName: 'مجموعة الفيصل للتجارة والخدمات اللوجستية',
      quoteNumber: 'SR-2026-Q9021',
      issueDate: '14 أكتوبر 2026',
      validityDays: '30',
      totalFormatted: '€5,445.00'
    });

    const isSuccess = invoiceDispatch && invoiceDispatch.success === true;
    recordResult(
      'Certified Invoice/Quote Email Dispatch',
      isSuccess,
      `Mode: ${invoiceDispatch.mode || 'live'} | Provider: ${invoiceDispatch.provider} | To: client-audit@sr-coresync.com`
    );
  } catch (err) {
    recordResult('Certified Invoice/Quote Email Dispatch', false, err.message);
  }

  // --- Test 4: Dispatch Certified Welcome Email ---
  try {
    const welcomeDispatch = await emailService.sendOfficialWelcomeEmail({
      to: 'onboarding-test@sr-coresync.com',
      customerName: 'مكتب الابتكار الهندسي'
    });

    const isSuccess = welcomeDispatch && welcomeDispatch.success === true;
    recordResult(
      'Corporate Welcome Email Dispatch',
      isSuccess,
      `Mode: ${welcomeDispatch.mode || 'live'} | Provider: ${welcomeDispatch.provider} | To: onboarding-test@sr-coresync.com`
    );
  } catch (err) {
    recordResult('Corporate Welcome Email Dispatch', false, err.message);
  }

  // --- Test 5: Dispatch Dutch BTW License Invoice ---
  try {
    const licenseDispatch = await emailService.sendLicenseInvoice({
      to: 'license-client@bedrijf-nl.com',
      customerName: 'Van Dijk Logistics B.V.',
      invoiceNumber: 'INV-2026-BTW-7729',
      licenseKey: 'SRTX-PRO-2026-TEST-7729',
      productTitle: 'CoreSync Cloud ERP Enterprise',
      amount: 189,
      plan: '1 Jaar Licentie'
    });

    const isSuccess = licenseDispatch && licenseDispatch.success === true;
    recordResult(
      'Dutch BTW License & Key Dispatch',
      isSuccess,
      `Mode: ${licenseDispatch.mode || 'live'} | Provider: ${licenseDispatch.provider} | Order: INV-2026-BTW-7729`
    );
  } catch (err) {
    recordResult('Dutch BTW License & Key Dispatch', false, err.message);
  }

  const durationMs = Date.now() - startTime;
  console.log('\n===================================================================');
  console.log(` Test Execution Finished in ${durationMs}ms`);
  console.log(` Total Tests: ${results.total} | Passed: ${results.passed} | Failed: ${results.failed}`);
  console.log(' Status: ' + (results.failed === 0 ? 'ALL SYSTEMS OPERATIONAL (100% PASS)' : 'SOME TESTS FAILED'));
  console.log('===================================================================\n');

  if (results.failed > 0) {
    process.exit(1);
  }
}

runTestSuite().catch((err) => {
  console.error('Fatal Test Suite Error:', err);
  process.exit(1);
});
