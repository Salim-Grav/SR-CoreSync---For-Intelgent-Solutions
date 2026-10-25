import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class CoreSyncError(Exception):
    """Exception raised for errors in S&R CoreSync API responses."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class CoreSyncClient:
    """Official Python Client for S&R CoreSync ERP & Open Banking PSD2 Gateway."""
    
    BASE_URL = "https://api.sr-coresync.com/v1"
    
    def __init__(self, api_key: str, environment: str = "production", timeout: int = 30):
        if not api_key:
            raise ValueError("api_key must be provided to initialize CoreSyncClient.")
        self.api_key = api_key
        self.environment = environment
        self.timeout = timeout
        
    def _request(self, method: str, endpoint: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "CoreSync-Python-SDK/2.4.0",
            "X-CoreSync-Environment": self.environment
        }
        
        data = json.dumps(payload).encode('utf-8') if payload else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                body = response.read().decode('utf-8')
                return json.loads(body)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
            except Exception:
                error_json = {"error": error_body}
            raise CoreSyncError(f"HTTP {e.code}: {e.reason}", status_code=e.code, response_data=error_json)
        except Exception as e:
            raise CoreSyncError(f"Network error communicating with CoreSync API: {str(e)}")

    def generate_invoice(self, client_name: str, client_vat: str, client_email: str, 
                         amount_net: float, package_code: str = "SOCIAL_8K_SUITE", 
                         btw_rate: float = 0.21, currency: str = "EUR") -> Dict[str, Any]:
        """Generate a certified Belastingdienst BTW compliant invoice and general ledger entry."""
        payload = {
            "client_name": client_name,
            "client_vat": client_vat,
            "client_email": client_email,
            "amount_net": amount_net,
            "package_code": package_code,
            "btw_rate": btw_rate,
            "currency": currency
        }
        return self._request("POST", "/erp/invoices/generate", payload)

    def trigger_whatsapp_notification(self, phone: str, invoice_id: str, amount: float, 
                                     client_name: str) -> Dict[str, Any]:
        """Trigger instant WhatsApp Business API notification for settled transactions."""
        payload = {
            "recipient_phone": phone,
            "invoice_id": invoice_id,
            "amount": amount,
            "client_name": client_name,
            "template": "financial_settlement_v2026"
        }
        return self._request("POST", "/notifications/whatsapp/dispatch", payload)

    def get_ledger_entries(self, limit: int = 50) -> Dict[str, Any]:
        """Query balanced double-entry General Ledger records."""
        return self._request("GET", f"/general-ledger/entries?limit={limit}")
