import logging
import sys

logger = logging.getLogger(__name__)

def send_alert(message: str, title: str = "S&R CoreSync Alert") -> None:
    """Send a native Windows desktop notification.

    Tries multiple backends in order:
    1. ``plyer`` — modern cross-platform notification library (preferred).
    2. ``win10toast`` — legacy Windows-only toaster (fallback).
    3. Console stderr — last-resort fallback so the caller never crashes.

    Args:
        message: The notification body text.
        title:   The notification window title (default: S&R CoreSync Alert).
    """
    # ── Strategy 1: plyer (recommended, works with Python 3.14 venv) ──
    try:
        from plyer import notification as plyer_notify
        plyer_notify.notify(
            title=title,
            message=message,
            app_name="S&R CoreSync",
            timeout=10,
        )
        logger.info("plyer notification sent: %s", message)
        return
    except Exception as plyer_err:
        logger.debug("plyer failed (%s), trying win10toast…", plyer_err)

    # ── Strategy 2: win10toast legacy fallback ──
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10, threaded=True)
        logger.info("win10toast notification sent: %s", message)
        return
    except Exception as toast_err:
        logger.warning(
            "win10toast also failed (%s); using console fallback.", toast_err
        )

    # ── Strategy 3: Console fallback (always works) ──
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"[ALERT] {title}", file=sys.stderr)
    print(f"        {message}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)


if __name__ == "__main__":
    # Simple CLI for manual testing:
    #   python sr_alert_dispatcher.py "Test message here"
    if len(sys.argv) > 1:
        send_alert(" ".join(sys.argv[1:]))
    else:
        print("Usage: python sr_alert_dispatcher.py <message>")
