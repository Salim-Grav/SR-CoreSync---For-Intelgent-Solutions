"""
sr_alert_dispatcher.py — S&R CoreSync Multi-Channel Alert & Webhook Dispatcher
=============================================================================
Dispatches sovereign alerts across multiple channels in parallel:

1. External Webhooks (Non-blocking background thread):
   - Slack / Discord / Custom Webhook (via ALERT_WEBHOOK_URL, DISCORD_WEBHOOK_URL, SLACK_WEBHOOK_URL)
   - Telegram Bot API (via TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID)
2. Desktop Notifications (Non-blocking native GUI):
   - Windows MessageBox via ctypes (always available on Windows)
   - plyer BalloonTip / win10toast (system tray toaster)
   - Console stderr (guaranteed terminal fallback)
"""
import os
import sys
import json
import logging
import threading
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# Ensure .env is loaded if python-dotenv is present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

logger = logging.getLogger(__name__)


# ==============================================================================
# 1. External Webhook Delivery (Slack, Discord, Telegram, Generic)
# ==============================================================================
def _send_http_json(url: str, payload: Dict[str, Any], timeout: float = 6.0) -> bool:
    """Send JSON payload via HTTP POST using standard urllib (zero extra dependencies)."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "SR-CoreSync-AlertDispatcher/2.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            logger.info("Webhook dispatched successfully to %s (HTTP %s)", url[:35], status)
            return 200 <= status < 300
    except Exception as err:
        logger.warning("Webhook dispatch failed for %s: %s", url[:35], err)
        return False


def _dispatch_webhooks_worker(message: str, title: str, custom_webhook: Optional[str] = None) -> None:
    """Worker function executed in a background daemon thread to send webhooks."""
    generic_url = custom_webhook or os.getenv("ALERT_WEBHOOK_URL")
    discord_url = os.getenv("DISCORD_WEBHOOK_URL")
    slack_url = os.getenv("SLACK_WEBHOOK_URL")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Combined payload compatible with both Slack ('text') and Discord ('content')
    universal_payload = {
        "text": f"🚨 *{title}*\n{message}",
        "content": f"🚨 **{title}**\n{message}",
        "username": "S&R CoreSync Sovereign Watchdog",
        "icon_emoji": ":shield:",
    }

    # 1. Generic or Explicit Webhook URL
    if generic_url:
        _send_http_json(generic_url, universal_payload)

    # 2. Discord Webhook URL (if distinct)
    if discord_url and discord_url != generic_url:
        _send_http_json(discord_url, {"content": f"🚨 **{title}**\n{message}"})

    # 3. Slack Webhook URL (if distinct)
    if slack_url and slack_url != generic_url:
        _send_http_json(slack_url, {"text": f"🚨 *{title}*\n{message}"})

    # 4. Telegram Bot API
    if tg_token and tg_chat_id:
        tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        tg_payload = {
            "chat_id": tg_chat_id,
            "text": f"🚨 *{title}*\n\n{message}",
            "parse_mode": "Markdown",
        }
        _send_http_json(tg_url, tg_payload)


# ==============================================================================
# 2. Native Desktop Notification (Windows MessageBox / Toast / Stderr)
# ==============================================================================
def _windows_msgbox(title: str, message: str) -> None:
    """Show a native Windows MessageBox in a background thread."""
    try:
        import ctypes
        # MB_OK | MB_ICONWARNING | MB_SYSTEMMODAL
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000030 | 0x00001000)
    except Exception as e:
        logger.debug("MessageBoxW failed (%s)", e)


def _dispatch_desktop_alert(message: str, title: str) -> None:
    """Attempt desktop notification via ctypes, plyer, win10toast, or stderr."""
    # Strategy A: ctypes MessageBoxW (built-in Windows API, always available)
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

    # Strategy B: plyer balloon tip
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

    # Strategy C: win10toast legacy
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=10, threaded=True)
        logger.info("win10toast notification sent: %s", message)
        return
    except Exception as toast_err:
        logger.warning("win10toast also failed (%s); using console fallback.", toast_err)

    # Strategy D: Console stderr (always works)
    border = "=" * 60
    print(f"\n{border}", file=sys.stderr)
    print(f"[ALERT] {title}", file=sys.stderr)
    print(f"        {message}", file=sys.stderr)
    print(f"{border}\n", file=sys.stderr)


# ==============================================================================
# 3. Main Multi-Channel Dispatcher
# ==============================================================================
def send_alert(
    message: str,
    title: str = "S&R CoreSync Alert",
    webhook_url: Optional[str] = None,
    dispatch_desktop: bool = True,
    dispatch_webhook: bool = True,
) -> None:
    """Send multi-channel alert across Webhook (Slack/Discord/Telegram) and Desktop.

    Both channels run concurrently and non-blocking in background threads, so
    the caller application is never delayed or crashed.

    Args:
        message:          The notification body text.
        title:            The alert window/notification title.
        webhook_url:      Optional explicit webhook URL (overrides ALERT_WEBHOOK_URL).
        dispatch_desktop: Whether to trigger native Windows notification (default True).
        dispatch_webhook: Whether to trigger external webhooks if configured (default True).
    """
    # ── 1. External Webhooks Dispatch (Background Thread) ──
    if dispatch_webhook:
        try:
            wt = threading.Thread(
                target=_dispatch_webhooks_worker,
                args=(message, title, webhook_url),
                daemon=True,
                name="sr-alert-webhook-worker",
            )
            wt.start()
        except Exception as wh_err:
            logger.warning("Failed to start webhook worker thread: %s", wh_err)

    # ── 2. Desktop Notification Dispatch (Background Thread / Native) ──
    if dispatch_desktop:
        try:
            _dispatch_desktop_alert(message, title)
        except Exception as dt_err:
            logger.warning("Failed to dispatch desktop alert: %s", dt_err)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="S&R CoreSync Sovereign Multi-Channel Alert & Webhook Dispatcher"
    )
    parser.add_argument("message", nargs="*", default=["اختبار إشعار S&R CoreSync"], help="Alert message text")
    parser.add_argument("--title", default="S&R CoreSync Sovereign Alert", help="Alert title")
    parser.add_argument("--webhook", default=None, help="Explicit Webhook URL to test (Slack/Discord/Custom)")
    parser.add_argument("--no-desktop", action="store_true", help="Skip desktop notification")
    parser.add_argument("--no-webhook", action="store_true", help="Skip external webhooks")

    args = parser.parse_args()
    msg_str = " ".join(args.message)

    print(f"🚀 Dispatching alert: '{msg_str}'")
    if args.webhook:
        print(f"🔗 Target Webhook: {args.webhook}")

    send_alert(
        message=msg_str,
        title=args.title,
        webhook_url=args.webhook,
        dispatch_desktop=not args.no_desktop,
        dispatch_webhook=not args.no_webhook,
    )
    print("✅ Alert dispatch routine initiated across all enabled channels.")
