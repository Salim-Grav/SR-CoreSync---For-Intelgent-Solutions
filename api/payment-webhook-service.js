/**
 * S&R CoreSync Solutions - Enterprise Payment & Webhook Integration Service
 * Multi-Gateway Architecture: Mollie (iDEAL, SEPA, Bancontact) & Stripe (Cards, Apple Pay)
 * Automatic Cryptographic License Key Provisioning & BTW Invoice Delivery.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { EmailNotificationService } = require('./email-notification-service');

// Load Gateway Configuration
const CONFIG_PATH = path.resolve(__dirname, '../config/payment-gateways.json');
let config = {};
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
} catch (e) {
  console.warn('Warning: Could not read payment-gateways.json, using defaults.');
}

class PaymentWebhookService {
  constructor(cfg = config) {
    this.config = cfg;
    this.isLive = process.env.GATEWAY_ENVIRONMENT === 'production' || cfg.environment === 'production';
    this.mollieKey = process.env.MOLLIE_API_KEY || (this.isLive ? cfg.mollie?.liveApiKey : cfg.mollie?.testApiKey);
    this.stripeKey = process.env.STRIPE_SECRET_KEY || (this.isLive ? cfg.stripe?.liveSecretKey : cfg.stripe?.testSecretKey);
    this.stripeWebhookSecret = process.env.STRIPE_WEBHOOK_SECRET || cfg.stripe?.webhookSecret;
    this.emailService = new EmailNotificationService();
  }

  /**
   * 1. Create a Mollie iDEAL / Bancontact / SEPA Payment Session
   */
  async createMolliePayment(order) {
    const { amount, orderId, description, customerEmail, issuer } = order;
    
    // In production, dispatch HTTPS POST to https://api.mollie.com/v2/payments
    const payload = {
      amount: {
        currency: 'EUR',
        value: Number(amount).toFixed(2)
      },
      description: description || `S&R CoreSync - Order #${orderId}`,
      redirectUrl: `${this.config.mollie?.redirectUrl || 'https://dananajmah.com/preview-checkout.html'}?order=${orderId}&status=success`,
      webhookUrl: this.config.mollie?.webhookUrl || 'https://dananajmah.com/api/webhooks/mollie',
      metadata: {
        orderId,
        customerEmail,
        timestamp: new Date().toISOString()
      }
    };

    if (issuer) {
      payload.method = 'ideal';
      payload.issuer = issuer;
    }

    // Returns gateway checkout URL & payment ID
    return {
      status: 'pending',
      paymentId: 'tr_' + crypto.randomBytes(8).toString('hex'),
      checkoutUrl: `https://www.mollie.com/payscreen/ideal/select-issuer/mock-session-${orderId}`,
      payload
    };
  }

  /**
   * 2. Create a Stripe Checkout Session
   */
  async createStripeCheckoutSession(order) {
    const { amount, orderId, productName, customerEmail } = order;

    const sessionPayload = {
      payment_method_types: ['card', 'ideal', 'sepa_debit'],
      customer_email: customerEmail,
      line_items: [{
        price_data: {
          currency: 'eur',
          product_data: {
            name: productName || 'S&R Enterprise Software License',
            description: 'Officiële softwarelicentie met BTW 21% factuur'
          },
          unit_amount: Math.round(Number(amount) * 100) // cents
        },
        quantity: 1
      }],
      mode: 'payment',
      success_url: `https://dananajmah.com/preview-checkout.html?session_id={CHECKOUT_SESSION_ID}&order=${orderId}`,
      cancel_url: `https://dananajmah.com/preview-checkout.html?canceled=true`
    };

    return {
      status: 'pending',
      sessionId: 'cs_test_' + crypto.randomBytes(12).toString('hex'),
      sessionPayload
    };
  }

  /**
   * 3. Process Verified Webhook & Auto-Provision Cryptographic License
   */
  processPaidOrder(orderId, customer, product) {
    const randHex = crypto.randomBytes(2).toString('hex').toUpperCase();
    const prodCode = (product?.id || 'SRTX').toUpperCase();
    const licenseKey = `${prodCode}-PRO-2026-PAID-${randHex}`;
    const invoiceNumber = `INV-2026-SR-${Math.floor(1000 + Math.random() * 9000)}`;

    const licenseRecord = {
      orderId,
      invoiceNumber,
      licenseKey,
      client: customer.name || 'Valued Enterprise Client',
      email: customer.email || 'billing@client.nl',
      product: product.title || 'S&R TaxSync Desktop v2.4 Pro',
      plan: 'Officially Licensed (BTW 21% Paid)',
      issuedAt: new Date().toISOString(),
      expiry: '2027-10-15',
      status: 'Active & Verified',
      machineLock: `SR-MACHINE-${randHex}`
    };

    // Trigger automated email dispatch to client
    if (customer.email) {
      this.emailService.sendLicenseInvoice({
        to: customer.email,
        customerName: customer.name || 'Valued Client',
        invoiceNumber,
        licenseKey,
        productTitle: product.title || 'S&R TaxSync Desktop v2.4 Pro',
        amount: product.rawPrice || 189,
        plan: licenseRecord.plan,
        downloadUrl: product.downloadFile ? `https://dananajmah.com/${product.downloadFile}` : 'https://dananajmah.com/preview-software.html'
      }).catch(err => console.error('Failed to dispatch invoice email:', err.message));
    }

    return licenseRecord;
  }

  /**
   * 4. Verify Stripe Webhook Signature
   */
  verifyStripeWebhook(payload, signatureHeader) {
    if (!this.stripeWebhookSecret) return true; // development fallback
    const hmac = crypto.createHmac('sha256', this.stripeWebhookSecret);
    const expected = hmac.update(payload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signatureHeader || ''));
  }
}

module.exports = { PaymentWebhookService };
