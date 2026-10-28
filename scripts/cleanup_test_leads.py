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
Remove test rows from D1
========================
Only rows whose client name starts with "TEST" are touched; real leads are
never deleted. Default is a dry run.

  python scripts/cleanup_test_leads.py            # list what would be deleted
  python scripts/cleanup_test_leads.py --apply    # delete them
"""
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
TEST_PATTERN = "client_name LIKE 'TEST%' or client_name LIKE 'Telegram Probe%' or client_name LIKE 'Rate Test%'"


def run(sql, as_json=False):
    args = ['node', WRANGLER, 'd1', 'execute', DB, '--remote', '--command', sql, '--yes']
    if as_json:
        args.append('--json')
    res = subprocess.run(args, cwd=WORKER, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        raise SystemExit('D1 failed:\n%s' % (res.stderr or res.stdout)[-500:])
    return res.stdout


def main():
    apply = '--apply' in sys.argv

    raw = run('SELECT lead_id, client_name, received_at FROM leads WHERE ' + TEST_PATTERN +
              ' ORDER BY received_at DESC', as_json=True)
    start = raw.find('[')
    rows = json.loads(raw[start:])[0].get('results', [])

    print('=' * 70)
    print('D1 test-row cleanup' + (' (APPLY)' if apply else ' (DRY RUN)'))
    print('=' * 70)
    print('test rows matched: %d' % len(rows))
    for row in rows:
        print('  - %-26s %-26s %s' % (row.get('lead_id'), row.get('client_name'), row.get('received_at')))

    keep = run("SELECT COUNT(*) AS n FROM leads WHERE NOT (" + TEST_PATTERN + ")", as_json=True)
    keep_rows = json.loads(keep[keep.find('['):])[0].get('results', [])
    print('real rows kept  : %d' % (keep_rows[0]['n'] if keep_rows else 0))

    if not rows:
        print('Nothing to clean.')
        return 0
    if not apply:
        print('-' * 70)
        print('DRY RUN — add --apply to delete these rows.')
        return 0

    run('DELETE FROM leads WHERE ' + TEST_PATTERN)
    print('-' * 70)
    print('Deleted %d test row(s).' % len(rows))
    return 0


if __name__ == '__main__':
    sys.exit(main())
