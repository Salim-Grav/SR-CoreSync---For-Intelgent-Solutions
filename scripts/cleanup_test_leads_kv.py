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
Remove the test leads that only exist in KV
==========================================
D1 is clean, but the KV ledger still holds the test records (the feed now reads
D1, so they are invisible — they would resurface if the binding were removed).

  python scripts/cleanup_test_leads_kv.py            # dry run
  python scripts/cleanup_test_leads_kv.py --apply
"""
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
NS = 'd23f177169fb4501b854056e67d21ed5'
MARKERS = ('test', 'telegram probe', 'rate test')


def run(args):
    res = subprocess.run(['node', WRANGLER] + args, cwd=WORKER,
                         capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        raise SystemExit('wrangler failed: %s\n%s' % (' '.join(args), (res.stderr or res.stdout)[-400:]))
    return res.stdout


def main():
    apply = '--apply' in sys.argv

    index = json.loads(run(['kv', 'key', 'get', 'lead:index',
                            '--namespace-id=' + NS, '--remote']).strip() or '[]')
    print('KV index entries: %d' % len(index))

    doomed = []
    keep = []
    for entry in index:
        lead_id = entry.get('id')
        raw = run(['kv', 'key', 'get', 'lead:' + lead_id,
                   '--namespace-id=' + NS, '--remote']).strip()
        name = ''
        if raw:
            try:
                name = (json.loads(raw).get('clientName') or '').lower()
            except ValueError:
                name = ''
        if name.startswith('test') or any(m in name for m in MARKERS):
            doomed.append((lead_id, name))
        else:
            keep.append(entry)

    print('-' * 60)
    for lead_id, name in doomed:
        print('  delete  %-26s %s' % (lead_id, name))
    print('  keep    %d entr(ies)' % len(keep))

    if not apply:
        print('-' * 60)
        print('DRY RUN - add --apply to delete them from KV.')
        return 0

    for lead_id, _ in doomed:
        run(['kv', 'key', 'delete', 'lead:' + lead_id, '--namespace-id=' + NS, '--remote'])

    run(['kv', 'key', 'put', 'lead:index', json.dumps(keep),
         '--namespace-id=' + NS, '--remote'])

    print('-' * 60)
    print('Deleted %d KV record(s); index rewritten with %d.' % (len(doomed), len(keep)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
