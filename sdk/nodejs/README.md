# S&R CoreSync Node.js SDK (`@coresync/sdk`)

Official Node.js SDK for S&R CoreSync Cloud ERP, Open Banking PSD2, and automated General Ledger accounting.

## Installation

```bash
npm install @coresync/sdk
```

## Quickstart

```javascript
const { CoreSyncClient } = require('@coresync/sdk');

// Initialize with your live API Key
const client = new CoreSyncClient({
  apiKey: 'sr_live_2026_eu_xxxxxxxx'
});

async function main() {
  // 1. Generate compliant BTW tax invoice
  const invoice = await client.generateInvoice({
    clientName: 'Amsterdam Tech Logistics B.V.',
    clientVat: 'NL864219876B01',
    clientEmail: 'finance@amsterdam-tech.nl',
    amountNet: 735.54,
    btwRate: 0.21
  });
  console.log('Invoice Generated:', invoice.data.invoice_id);

  // 2. Dispatch instant WhatsApp settlement alert
  const alert = await client.triggerWhatsAppNotification({
    phone: '+31636279435',
    invoiceId: invoice.data.invoice_id,
    amount: 890.00,
    clientName: 'Amsterdam Tech Logistics B.V.'
  });
  console.log('WhatsApp Notification Dispatched:', alert.status);
}

main().catch(console.error);
```
