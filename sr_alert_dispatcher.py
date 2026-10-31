import logging
import sys

logger = logging.getLogger(__name__)

def send_alert(message: str) -> None:
    """Send a native Windows toast notification if possible.

    Tries to use the ``win10toast`` package; if unavailable, falls back to a
    simple console print so that the caller never fails.
    """
    try:
        # Lazily import to avoid mandatory dependency at import time.
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        # ``duration`` is in seconds; ``threaded`` allows the script to continue.
        toaster.show_toast("S&R CoreSync Alert", message, duration=10, threaded=True)
        logger.info("Windows toast shown: %s", message)
    except Exception as e:
        # If the package is missing or any Windows API call fails, fallback.
        logger.warning("win10toast not available or failed (%s); falling back to console", e)
        print(f"[ALERT] {message}", file=sys.stderr)

if __name__ == "__main__":
    # Simple CLI for manual testing.
    if len(sys.argv) > 1:
        send_alert(" ".join(sys.argv[1:]))
    else:
        print("Usage: python sr_alert_dispatcher.py <message>")
