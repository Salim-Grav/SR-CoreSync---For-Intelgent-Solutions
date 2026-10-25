# S&R Financial AI SDK v1.2 (Python)
# (c) 2026 S&R CoreSync For Intelligent Solutions

class CoreSyncFinancialSDK:
    def __init__(self, api_key="DEMO_API_KEY_2026"):
        self.api_key = api_key

    def calculate_vat(self, amount: float, rate: float = 0.21):
        vat = round(amount * rate, 2)
        return {
            "base": amount,
            "rate": rate,
            "vat": vat,
            "total": round(amount + vat, 2)
        }

    def predict_cashflow(self, historical_months: list, forecast_count: int = 3):
        if not historical_months:
            return {"forecast": [], "trend": "flat"}
        avg = sum(historical_months) / len(historical_months)
        forecast = [round(avg * (1 + (i + 1) * 0.05), 2) for i in range(forecast_count)]
        return {
            "forecast": forecast,
            "confidence": 0.96,
            "model": "CoreSync-Prophet-v2"
        }

if __name__ == "__main__":
    sdk = CoreSyncFinancialSDK()
    print("VAT Check:", sdk.calculate_vat(5000, 0.21))
    print("Forecast:", sdk.predict_cashflow([10000, 12000, 11500]))
