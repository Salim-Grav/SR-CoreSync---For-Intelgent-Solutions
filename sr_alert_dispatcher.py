"""
sr_alert_dispatcher.py — S&R CoreSync Native Windows Alert Module
=================================================================
Sends desktop notifications using multiple strategies with automatic fallback.

Backends tried in order:
  1. Windows MessageBox via ctypes (always works on Windows, modal popup)
  2. plyer BalloonTip (system tray notification, requires tray support)
  3. win10toast legacy fallback
  4. Console stderr (absolute last resort)
"""
import logging
import sys
import threading

logger = logging.getLogger(__name__)


def _windows_msgbox(title: str, message: str) -> None:
    """Show a native Windows MessageBox in a background thread (non-blocking)."""
    import ctypes
    # MB_OK | MB_ICONWARNING | MB_SYSTEMMODAL
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000030 | 0x00001000)


def send_alert(message: str, title: str = "S&R CoreSync Alert") -> None:
    """Send a native Windows desktop alert notification.

    Tries multiple backends in order so the caller never crashes:

    1. **ctypes MessageBoxW** — built-in Windows API, always available.
       Runs in a daemon thread so it does NOT block the calling code.
    2. **plyer** — modern cross-platform balloon tip (requires tray context).
    3. **win10toast** — legacy toaster fallback.
    4. **Console stderr** — absolute last resort.

    Args:
        message: The notification body text.
        title:   The notification window title.
    """
    # ── Strategy 1: ctypes MessageBoxW (always available on Windows) ──
    if sys.platform == "win32":
        try:
            t = threading.Thread(
                target=_windows_msgbox,
                args=(title, message),
                daemon=True,
                name="sr-alert-msgbox",
            )
            t.start()
            logger.info("Windows MessageBox alert dispatched: %s", message)
            return
        except Exception as ctypes_err:
            logger.debug("ctypes MessageBox failed (%s), trying plyer…", ctypes_err)

    # ── Strategy 2: plyer balloon tip ──
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

    # ── Strategy 3: win10toast legacy ──
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10, threaded=True)
        logger.info("win10toast notification sent: %s", message)
        return
    except Exception as toast_err:
        logger.warning("win10toast also failed (%s); using console fallback.", toast_err)

    # ── Strategy 4: Console fallback (always works) ──
    border = "=" * 60
    print(f"\n{border}", file=sys.stderr)
    print(f"[ALERT] {title}", file=sys.stderr)
    print(f"        {message}", file=sys.stderr)
    print(f"{border}\n", file=sys.stderr)


if __name__ == "__main__":
    # CLI usage: python sr_alert_dispatcher.py "Your message here"
    if len(sys.argv) > 1:
        send_alert(" ".join(sys.argv[1:]))
    else:
        print("Usage: python sr_alert_dispatcher.py <message>")
        print("Example: python sr_alert_dispatcher.py \"ALERT: High memory usage detected\"")
