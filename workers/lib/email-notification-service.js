/**
 * @deprecated DO NOT WIRE THIS INTO THE CLOUDFLARE WORKER.
 * ---------------------------------------------------------------------------
 * This module depends on node:fs, node:path and node:tls, none of which exist
 * in the Workers runtime - it cannot run where the lead pipeline actually runs.
 * The live Worker sends mail through Resend/Brevo over fetch()
 * (see workers/sr-lead-capture/src/index.js -> notifyByEmail).
 *
 * It is kept only as a Node reference implementation. The production message
 * bodies are built by scripts/build_email_templates.py into dist/emails/.
 * ---------------------------------------------------------------------------
 */
/**
 * S&R CoreSync For Intelligent Solutions - Enterprise Email & Invoice Dispatcher
 * Multi-Provider Architecture: Native Hostinger SMTP (TLS/SSL 465) & SendGrid API
 * Automatically sends branded HTML receipt, official BTW invoice details,
 * and cryptographic license activation keys upon verified payment.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const tls = require('tls');

class EmailNotificationService {
  constructor(options = {}) {
    this.provider = process.env.EMAIL_PROVIDER || options.provider || 'smtp';
    this.smtpHost = process.env.SMTP_HOST || options.smtpHost || 'smtp.hostinger.com';
    this.smtpPort = parseInt(process.env.SMTP_PORT || options.smtpPort || '465', 10);
    this.smtpUser = process.env.SMTP_USER || options.smtpUser || 'billing@sr-coresync.com';
    this.smtpPass = process.env.SMTP_PASS || options.smtpPass || '';
    this.sendgridApiKey = process.env.SENDGRID_API_KEY || options.sendgridApiKey;
    this.postmarkToken = process.env.POSTMARK_SERVER_TOKEN || options.postmarkToken;
    this.fromEmail = process.env.EMAIL_FROM || options.fromEmail || 'billing@sr-coresync.com';
    this.fromName = process.env.EMAIL_FROM_NAME || options.fromName || 'S&R CoreSync For Intelligent Solutions';
    this.adminEmail = process.env.EMAIL_ADMIN || options.adminEmail || 'salim@sr-coresync.com';
    this.supportEmail = process.env.EMAIL_SUPPORT || options.supportEmail || 'info@sr-coresync.com';
  }

  /**
   * Bundles external CSS into an internal <style> block for bulletproof email client rendering
   */
  bundleTemplateStyles(htmlContent, cssPath) {
    try {
      if (fs.existsSync(cssPath)) {
        const cssContent = fs.readFileSync(cssPath, 'utf8');
        const styleBlock = `<style type="text/css">\n${cssContent}\n</style>`;
        // Replace external CSS link with bundled inline style block
        return htmlContent.replace(/<link\s+rel="stylesheet"\s+href="[^"]*"\s*\/?>/i, styleBlock);
      }
    } catch (err) {
      console.warn(`[EmailNotificationService] Could not bundle CSS from ${cssPath}:`, err.message);
    }
    return htmlContent;
  }

  /**
   * Compiles the official Arabic & Multi-language Invoice/Quote Email Template
   */
  compileInvoiceQuoteTemplate(data = {}) {
    const templatePath = path.resolve(__dirname, '../../templates/invoice-quote-email.html');
    const cssPath = path.resolve(__dirname, '../../css/invoice-quote-email.css');
    let html = fs.readFileSync(templatePath, 'utf8');

    // Bundle CSS
    html = this.bundleTemplateStyles(html, cssPath);

    // Apply dynamic replacements if supplied
    if (data.clientName) {
      html = html.replace(/شركة النخبة للاستشارات والتجارة/g, data.clientName);
    }
    if (data.quoteNumber) {
      html = html.replace(/#SR-2026-Q892/g, data.quoteNumber);
    }
    if (data.issueDate) {
      html = html.replace(/13 أكتوبر 2026/g, data.issueDate);
    }
    if (data.validityDays) {
      html = html.replace(/30 يوماً من تاريخه/g, `${data.validityDays} يوماً من تاريخه`);
    }
    if (data.totalFormatted) {
      html = html.replace(/€5,445\.00/g, data.totalFormatted);
    }

    return html;
  }

  /**
   * Compiles the official Welcome & Onboarding Email Template
   */
  compileWelcomeEmailTemplate(data = {}) {
    const templatePath = path.resolve(__dirname, '../../templates/welcome-email.html');
    const cssPath = path.resolve(__dirname, '../../css/welcome-email.css');
    let html = fs.readFileSync(templatePath, 'utf8');

    // Bundle CSS
    html = this.bundleTemplateStyles(html, cssPath);

    if (data.customerName) {
      html = html.replace(/نخبة الأعمال 2026/g, `${data.customerName} - 2026`);
    }

    return html;
  }

  /**
   * Generates official Dutch/English BTW Invoice & License HTML template (fallback inline)
   */
  generateInvoiceHtml({ customerName, invoiceNumber, licenseKey, productTitle, amount, plan, downloadUrl }) {
    const rawPrice = Number(amount || 189).toFixed(2);
    const netPrice = (rawPrice / 1.21).toFixed(2);
    const vatPrice = (rawPrice - parseFloat(netPrice)).toFixed(2);
    const dateStr = new Date().toLocaleDateString('nl-NL', { year: 'numeric', month: 'long', day: 'numeric' });

    return `
<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <title>Officiële Licentie &amp; BTW Factuur - S&amp;R CoreSync For Intelligent Solutions</title>
  <style>
    body { margin:0; padding:0; background:#010907; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#ffffff; }
    .email-wrapper { max-width:640px; margin:20px auto; background:#071410; border:1px solid rgba(197,168,128,0.25); border-radius:12px; overflow:hidden; }
    .header { padding:32px 24px; text-align:center; background:linear-gradient(180deg, #0d231c 0%, #071410 100%); border-bottom:1px solid rgba(197,168,128,0.15); }
    .title { color:#f3dfba; margin:8px 0 0; font-size:22px; font-weight:700; }
    .subtitle { color:rgba(255,255,255,0.64); font-size:13px; margin:4px 0 0; }
    .content { padding:32px 24px; }
    .license-card { background:#030a08; border:1px solid #10b981; border-radius:8px; padding:20px; margin:24px 0; text-align:center; }
    .key-badge { font-family:monospace; font-size:18px; font-weight:bold; color:#10b981; letter-spacing:1px; background:rgba(16,185,129,0.1); padding:8px 16px; border-radius:6px; display:inline-block; }
    .invoice-table { width:100%; border-collapse:collapse; margin:20px 0; font-size:13px; }
    .invoice-table th, .invoice-table td { padding:10px 12px; border-bottom:1px solid rgba(255,255,255,0.08); text-align:left; }
    .invoice-table th { color:#c5a880; font-weight:600; }
    .total-row td { border-top:2px solid #c5a880; font-size:15px; font-weight:bold; color:#ffffff; }
    .btn-action { display:inline-block; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff; text-decoration:none; font-weight:600; padding:12px 28px; border-radius:6px; margin:16px 0; }
    .footer { padding:24px; background:#030907; border-top:1px solid rgba(255,255,255,0.06); font-size:11px; color:rgba(255,255,255,0.45); text-align:center; line-height:1.6; }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <div class="header">
      <div style="font-size:28px;">🛡️ S&amp;R CoreSync For Intelligent Solutions</div>
      <h1 class="title">Bevestiging van Licentie &amp; Factuur</h1>
      <p class="subtitle">Amsterdam HQ, Nederland • KvK 84920183 • BTW NL863412987B01</p>
    </div>
    <div class="content">
      <p>Geachte <strong>${customerName}</strong>,</p>
      <p>Hartelijk dank voor uw aankoop bij <strong>S&amp;R CoreSync For Intelligent Solutions</strong>. Uw betaling is geverifieerd via het beveiligde Europese banknetwerk. Hieronder vindt u uw officiële licentiesleutel en factuurgegevens:</p>
      
      <div class="license-card">
        <div style="font-size:12px; color:rgba(255,255,255,0.6); margin-bottom:8px;">OFFICIËLE DIGITALE LICENTIESLEUTEL</div>
        <div class="key-badge">${licenseKey}</div>
        <div style="font-size:12px; color:rgba(255,255,255,0.7); margin-top:8px;">Status: <strong>Actief &amp; Geregistreerd</strong> • Looptijd: <strong>${plan || '1 Jaar'}</strong></div>
        <div style="margin-top:14px;">
          <a href="${downloadUrl || 'https://sr-coresync.com/preview-software.html'}" class="btn-action">Download Software Pakket ⚡</a>
        </div>
      </div>

      <h3 style="color:#c5a880; margin-top:32px; font-size:16px;">Specificatie BTW Factuur (${invoiceNumber})</h3>
      <table class="invoice-table">
        <thead>
          <tr>
            <th>Omschrijving</th>
            <th>Tarief</th>
            <th>Bedrag</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>${productTitle} (Commerciële Licentie)</td>
            <td>Excl. BTW</td>
            <td>€ ${netPrice}</td>
          </tr>
          <tr>
            <td>Nederlandse omzetbelasting (BTW 21%)</td>
            <td>21%</td>
            <td>€ ${vatPrice}</td>
          </tr>
          <tr class="total-row">
            <td colspan="2">Totaal Voldoen (Incl. BTW):</td>
            <td style="color:#10b981;">€ ${rawPrice}</td>
          </tr>
        </tbody>
      </table>

      <p style="font-size:13px; color:rgba(255,255,255,0.7); line-height:1.5;">
        <strong>Activeringsinstructies:</strong><br>
        1. Installeer het programma op uw apparaat.<br>
        2. Voer bij de eerste start uw licentiesleutel in.<br>
        3. De software valideert het certificaat automatisch met onze cryptografische architectuur.
      </p>
    </div>

    <div class="footer">
      S&amp;R CoreSync For Intelligent Solutions • Keizersgracht, 1016 Amsterdam, Nederland<br>
      Voor technische ondersteuning: <a href="mailto:info@sr-coresync.com" style="color:#c5a880;">info@sr-coresync.com</a> of WhatsApp: +31 6 1811 1116.<br>
      Dit document geldt als officieel digitaal betalingsbewijs conform de Nederlandse belastingwetgeving.
    </div>
  </div>
</body>
</html>
    `;
  }

  /**
   * Dispatches the email through Native Hostinger SMTP (TLS/SSL Port 465)
   * Zero external dependencies using Node.js 'tls' module
   */
  async sendViaHostingerSMTP({ to, subject, html }) {
    if (!this.smtpPass || this.smtpPass.includes('your_hostinger_email_password')) {
      console.log(`[Hostinger SMTP Simulation] Credentials not in .env. Simulated dispatch to: ${to} (Sender: ${this.fromEmail})`);
      return { success: true, mode: 'simulated', provider: 'smtp', sender: this.fromEmail, recipient: to, subject };
    }

    return new Promise((resolve) => {
      const socket = tls.connect({
        host: this.smtpHost,
        port: this.smtpPort,
        rejectUnauthorized: false
      }, () => {
        let step = 0;
        let responseBuffer = '';

        const commands = [
          `EHLO sr-coresync.com\r\n`,
          `AUTH LOGIN\r\n`,
          Buffer.from(this.smtpUser).toString('base64') + '\r\n',
          Buffer.from(this.smtpPass).toString('base64') + '\r\n',
          `MAIL FROM:<${this.fromEmail}>\r\n`,
          `RCPT TO:<${to}>\r\n`,
          `DATA\r\n`
        ];

        socket.on('data', (chunk) => {
          responseBuffer += chunk.toString();
          const lines = responseBuffer.split('\r\n');
          const lastLine = lines[lines.length - 2] || lines[lines.length - 1];

          if (step === 0 && lastLine.startsWith('220')) {
            socket.write(commands[0]);
            step = 1;
          } else if (step === 1 && lastLine.startsWith('250')) {
            socket.write(commands[1]);
            step = 2;
          } else if (step === 2 && lastLine.startsWith('334')) {
            socket.write(commands[2]);
            step = 3;
          } else if (step === 3 && lastLine.startsWith('334')) {
            socket.write(commands[3]);
            step = 4;
          } else if (step === 4 && lastLine.startsWith('235')) {
            socket.write(commands[4]);
            step = 5;
          } else if (step === 5 && lastLine.startsWith('250')) {
            socket.write(commands[5]);
            step = 6;
          } else if (step === 6 && lastLine.startsWith('250')) {
            socket.write(commands[6]);
            step = 7;
          } else if (step === 7 && lastLine.startsWith('354')) {
            const rawMime = [
              `From: "${this.fromName}" <${this.fromEmail}>`,
              `To: <${to}>`,
              `Subject: =?UTF-8?B?${Buffer.from(subject).toString('base64')}?=`,
              `MIME-Version: 1.0`,
              `Content-Type: text/html; charset=UTF-8`,
              `Content-Transfer-Encoding: base64`,
              ``,
              Buffer.from(html).toString('base64'),
              `.`,
              ``
            ].join('\r\n');
            socket.write(rawMime);
            step = 8;
          } else if (step === 8 && lastLine.startsWith('250')) {
            socket.write('QUIT\r\n');
            socket.end();
            resolve({ success: true, provider: 'smtp', host: this.smtpHost, to });
          } else if (lastLine.startsWith('5') || lastLine.startsWith('4')) {
            socket.end();
            resolve({ success: false, error: lastLine, provider: 'smtp' });
          }
        });
      });

      socket.on('error', (err) => {
        resolve({ success: false, error: err.message, provider: 'smtp' });
      });

      socket.setTimeout(12000, () => {
        socket.destroy();
        resolve({ success: false, error: 'SMTP Timeout', provider: 'smtp' });
      });
    });
  }

  /**
   * Dispatches the email through SendGrid API (Zero npm dependencies)
   */
  async sendViaSendGrid({ to, subject, html }) {
    if (!this.sendgridApiKey || this.sendgridApiKey.startsWith('SG.your_real')) {
      console.log(`[Email Sandbox Mock] SendGrid API Key not configured. Simulated dispatch to: ${to}`);
      return { success: true, mode: 'simulated', provider: 'sendgrid', to, subject };
    }

    const payload = JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: this.fromEmail, name: this.fromName },
      subject: subject,
      content: [{ type: 'text/html', value: html }]
    });

    return new Promise((resolve) => {
      const req = https.request({
        hostname: 'api.sendgrid.com',
        port: 443,
        path: '/v3/mail/send',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.sendgridApiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload)
        }
      }, (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ success: true, statusCode: res.statusCode, provider: 'sendgrid' });
        } else {
          resolve({ success: false, statusCode: res.statusCode, provider: 'sendgrid' });
        }
      });

      req.on('error', (err) => resolve({ success: false, error: err.message, provider: 'sendgrid' }));
      req.write(payload);
      req.end();
    });
  }

  /**
   * High-level unified dispatcher for official Arabic/Multi-lingual Invoice & Quote
   */
  async sendOfficialInvoiceQuote({ to, clientName, quoteNumber, issueDate, validityDays, totalFormatted }) {
    const subject = `فاتورة / عرض سعر رسمي معتمد #${quoteNumber || 'SR-2026-Q892'} • S&R CoreSync For Intelligent Solutions`;
    const html = this.compileInvoiceQuoteTemplate({ clientName, quoteNumber, issueDate, validityDays, totalFormatted });

    console.log(`[Email Service] Dispatching certified Invoice/Quote to ${to} (${subject})...`);
    if (this.provider === 'smtp') {
      return await this.sendViaHostingerSMTP({ to, subject, html });
    } else {
      return await this.sendViaSendGrid({ to, subject, html });
    }
  }

  /**
   * High-level unified dispatcher for Welcome & Onboarding Email
   */
  async sendOfficialWelcomeEmail({ to, customerName }) {
    const subject = `أهلاً بكم في منظومة S&R CoreSync For Intelligent Solutions | مرحباً بكم`;
    const html = this.compileWelcomeEmailTemplate({ customerName });

    console.log(`[Email Service] Dispatching Official Welcome Email to ${to}...`);
    if (this.provider === 'smtp') {
      return await this.sendViaHostingerSMTP({ to, subject, html });
    } else {
      return await this.sendViaSendGrid({ to, subject, html });
    }
  }

  /**
   * High-level unified dispatcher for Dutch BTW License invoice
   */
  async sendLicenseInvoice({ to, customerName, invoiceNumber, licenseKey, productTitle, amount, plan, downloadUrl }) {
    const subject = `Factuur & Licentie ${invoiceNumber} - ${productTitle} | S&R CoreSync For Intelligent Solutions`;
    const html = this.generateInvoiceHtml({ customerName, invoiceNumber, licenseKey, productTitle, amount, plan, downloadUrl });

    console.log(`[Email Service] Dispatching official BTW invoice to ${to} for order ${invoiceNumber} via ${this.provider}...`);
    if (this.provider === 'smtp') {
      return await this.sendViaHostingerSMTP({ to, subject, html });
    } else {
      return await this.sendViaSendGrid({ to, subject, html });
    }
  }
}

module.exports = { EmailNotificationService };
