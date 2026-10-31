"""
Unit & Integration Test for Multi-Channel Alert & Webhook Dispatcher
=====================================================================
"""
import http.server
import threading
import json
import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sr_alert_dispatcher import send_alert

received_payloads = []


class MockWebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        received_payloads.append(json.loads(body.decode("utf-8")))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"received"}')

    def log_message(self, format, *args):
        pass  # Quiet logs


def test_webhook_dispatch():
    server = http.server.HTTPServer(("127.0.0.1", 9292), MockWebhookHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    print("🧪 Dispatching test alert to mock webhook endpoint (http://127.0.0.1:9292/webhook)...")
    send_alert(
        message="تنبيه تجريبي: تم رصد حدث أمني عالي الأهمية",
        title="S&R CoreSync Alert System",
        webhook_url="http://127.0.0.1:9292/webhook",
        dispatch_desktop=False,
        dispatch_webhook=True,
    )

    # Wait for the daemon thread to finish HTTP request
    time.sleep(1.0)
    server.shutdown()

    if received_payloads:
        payload = received_payloads[0]
        print("✅ Webhook delivery verified 100%!")
        print("  - text format (Slack):", payload.get("text"))
        print("  - content format (Discord):", payload.get("content"))
        print("  - username:", payload.get("username"))
        return True
    else:
        print("❌ Webhook delivery failed: No payload received.")
        return False


if __name__ == "__main__":
    success = test_webhook_dispatch()
    sys.exit(0 if success else 1)
