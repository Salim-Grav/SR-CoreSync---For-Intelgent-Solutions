"""Check that mailboxes really exist on the MX host — DNS alone cannot prove it.

Connects to the domain's MX, does EHLO/MAIL FROM/RCPT TO for each address and
reads the reply.  No message is ever sent (it always ends with QUIT after RCPT).

Usage:
    python scripts/probe_recipients.py info@sr-coresync.com support@... billing@...
    python scripts/probe_recipients.py --domain sr-coresync.com --all-default

Exit code 0 when every address is accepted, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.request

UA = {"user-agent": "sr-coresync-mail-probe/1.0"}
DEFAULT_LOCALPARTS = ("info", "support", "billing", "salim", "raed")


def mx_hosts(domain: str) -> list[tuple[int, str]]:
    url = f"https://cloudflare-dns.com/dns-query?name={domain}&type=MX"
    req = urllib.request.Request(url, headers={"accept": "application/dns-json", **UA})
    with urllib.request.urlopen(req, timeout=20) as res:
        payload = json.load(res)
    hosts = []
    for answer in payload.get("Answer", []) or []:
        parts = str(answer.get("data", "")).split()
        if len(parts) == 2:
            hosts.append((int(parts[0]), parts[1].rstrip(".")))
    return sorted(hosts)


def read_reply(sock: socket.socket) -> tuple[int, str]:
    lines = []
    while True:
        chunk = sock.recv(4096).decode("utf-8", "replace")
        if not chunk:
            break
        lines.append(chunk)
        text = "".join(lines)
        # a reply may span several lines: "250-a\r\n250 b\r\n"
        if len(text.splitlines()) > 0 and text.splitlines()[-1][3:4] == " ":
            break
    text = "".join(lines)
    first = text.splitlines()[0] if text.splitlines() else ""
    return int(first[:3] or 0), " ".join(text.split())


def probe(host: str, sender: str, recipients: list[str], timeout: float) -> dict[str, tuple[int, str]]:
    results: dict[str, tuple[int, str]] = {}
    with socket.create_connection((host, 25), timeout=timeout) as sock:
        sock.settimeout(timeout)
        code, _ = read_reply(sock)
        if code != 220:
            raise RuntimeError(f"{host}: unexpected greeting {code}")

        def cmd(line: str) -> tuple[int, str]:
            sock.sendall((line + "\r\n").encode())
            return read_reply(sock)

        cmd("EHLO sr-coresync.com")
        for rcpt in recipients:
            code, text = cmd(f"MAIL FROM:<{sender}>")
            if code // 100 != 2:
                results[rcpt] = (code, text)
                continue
            code, text = cmd(f"RCPT TO:<{rcpt}>")
            results[rcpt] = (code, text)
            cmd("RSET")
        try:
            cmd("QUIT")
        except OSError:
            pass
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("addresses", nargs="*")
    ap.add_argument("--domain", default="sr-coresync.com")
    ap.add_argument("--all-default", action="store_true", help="probe the five standard local parts")
    ap.add_argument("--sender", default=None, help="envelope sender (default postmaster@domain)")
    ap.add_argument("--timeout", type=float, default=15.0)
    args = ap.parse_args()

    recipients = list(args.addresses)
    if args.all_default or not recipients:
        recipients += [f"{part}@{args.domain}" for part in DEFAULT_LOCALPARTS]
    sender = args.sender or f"postmaster@{args.domain}"

    hosts = mx_hosts(args.domain)
    if not hosts:
        print(f"no MX for {args.domain}")
        return 1
    print(f"MX for {args.domain}: " + ", ".join(f"{p} {h}" for p, h in hosts))
    primary = hosts[0][1]
    print(f"probing {primary} as <{sender}>  (no message is sent)\n")

    try:
        results = probe(primary, sender, recipients, args.timeout)
    except (OSError, RuntimeError) as exc:
        print(f"cannot reach {primary}:25 - {exc}")
        print("port 25 is often blocked on residential ISPs; run this from a VPS or CI.")
        return 2

    accepted = 0
    for rcpt, (code, text) in results.items():
        ok = code // 100 == 2
        accepted += ok
        print(f"  [{'OK  ' if ok else 'FAIL'}] {rcpt:32} {code} {text[:70]}")
    print(f"\n{accepted}/{len(results)} accepted")
    return 0 if accepted == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
