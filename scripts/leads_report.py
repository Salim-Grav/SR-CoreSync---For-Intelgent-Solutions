# -*- coding: utf-8 -*-
"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
Lead report from D1
===================
The business question behind all of this is "who contacted us and did we answer
them?" This prints the answer, and can export it.

  python scripts/leads_report.py                 # last 30 days, table
  python scripts/leads_report.py --days 90
  python scripts/leads_report.py --csv leads.csv
"""
import argparse
import csv
import io
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
DB = 'sr-coresync'


def query(sql):
    res = subprocess.run(
        ['node', WRANGLER, 'd1', 'execute', DB, '--remote', '--command', sql, '--json'],
        cwd=WORKER, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        raise SystemExit('D1 query failed:\n%s' % (res.stderr or res.stdout)[-600:])
    out = res.stdout
    start = out.find('[')
    return json.loads(out[start:])[0].get('results', [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--csv', metavar='PATH')
    args = ap.parse_args()

    rows = query(
        'SELECT lead_id, client_name, company_name, email, phone, language, '
        'source_url, received_at, notify_status FROM leads '
        "WHERE received_at >= datetime('now', '-%d days') "
        'ORDER BY received_at DESC' % args.days)

    total = query('SELECT COUNT(*) AS n FROM leads')[0]['n']

    print('=' * 78)
    print('S&R CoreSync - lead report (last %d days)' % args.days)
    print('=' * 78)
    print('  rows in window : %d' % len(rows))
    print('  rows all-time  : %d' % total)

    if not rows:
        print('=' * 78)
        return 0

    by_lang = {}
    for row in rows:
        by_lang[row.get('language') or '-'] = by_lang.get(row.get('language') or '-', 0) + 1
    print('  by language    : %s' % ', '.join('%s=%d' % kv for kv in sorted(by_lang.items(), key=lambda x: -x[1])))
    print('-' * 78)
    announced_states = ('sent', 'resent')
    unannounced = [r for r in rows if (r.get('notify_status') or '') not in announced_states]
    print('  alerted        : %d of %d' % (len(rows) - len(unannounced), len(rows)))
    if unannounced:
        print('  NOT ALERTED    : %d  <-- these leads reached nobody' % len(unannounced))
    print('-' * 78)
    print('  %-24s %-22s %-24s %-10s %s' % ('lead id', 'name', 'email', 'alert', 'received'))
    for row in rows:
        print('  %-24s %-22s %-24s %-10s %s' % (
            (row.get('lead_id') or '')[:24],
            (row.get('client_name') or '')[:22],
            (row.get('email') or '')[:24],
            (row.get('notify_status') or 'never')[:10],
            (row.get('received_at') or '')[:19]))
    print('=' * 78)

    if args.csv:
        with io.open(args.csv, 'w', encoding='utf-8-sig', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print('CSV written: %s (%d rows)' % (args.csv, len(rows)))

    return 0


if __name__ == '__main__':
    sys.exit(main())
