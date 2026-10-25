# S&R CoreSync Python SDK (`coresync-python`)

Official Python client library for S&R CoreSync Cloud ERP, Open Banking PSD2, and automated General Ledger accounting.

## Installation

```bash
pip install coresync-python
```

## Quickstart

```python
from coresync import CoreSyncClient

# Initialize client with your API Key
client = CoreSyncClient(api_key="sr_live_2026_eu_xxxxxxxx")

# 1. Generate Belastingdienst BTW Compliant Invoice
invoice = client.generate_invoice(
    client_name="Amsterdam Tech Logistics B.V.",
    client_vat="NL864219876B01",
    client_email="finance@amsterdam-tech.nl",
    amount_net=735.54,
    btw_rate=0.21
)
print("Created Invoice:", invoice["data"]["invoice_id"])

# 2. Trigger instant WhatsApp Financial Notification
notify = client.trigger_whatsapp_notification(
    phone="+31636279435",
    invoice_id=invoice["data"]["invoice_id"],
    amount=890.00,
    client_name="Amsterdam Tech Logistics B.V."
)
print("WhatsApp Status:", notify["status"])
```
