# -*- coding: utf-8 -*-
"""
Backfill KV leads into D1
=========================
D1 became the durable store after KV had already collected leads. This copies
the KV ledger (lead:index + lead:<id>) into the D1 `leads` table so history is
not split across two stores.

Idempotent: uses INSERT OR IGNORE, so re-running only adds what is missing.

Usage:
  python scripts/backfill_kv_to_d1.py            # dry run, prints what it would do
  python scripts/backfill_kv_to_d1.py --apply
"""
import io
import json
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKER = os.path.join(ROOT, 'workers', 'sr-lead-capture')
WRANGLER = os.path.join(WORKER, 'node_modules', 'wrangler', 'bin', 'wrangler.js')
NAMESPACE = 'd23f177169fb4501b854056e67d21ed5'
DB = 'sr-coresync'


def wrangler(args):
    cmd = ['node', WRANGLER] + args
    res = subprocess.run(cmd, cwd=WORKER, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        raise SystemExit('wrangler failed: %s\n%s' % (' '.join(args), res.stderr[-600:]))
    return res.stdout


def kv_get(key):
    out = wrangler(['kv', 'key', 'get', key, '--namespace-id=' + NAMESPACE, '--remote'])
    return out.strip()


def sql_literal(value):
    if value is None:
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"


def main():
    apply = '--apply' in sys.argv

    index_raw = kv_get('lead:index')
    if not index_raw:
        print('KV index is empty - nothing to backfill.')
        return 0
    entries = json.loads(index_raw)
    print('KV index entries: %d' % len(entries))

    statements = []
    for entry in entries:
        lead_id = entry.get('id')
        if not lead_id:
            continue
        raw = kv_get('lead:' + lead_id)
        if not raw:
            print('  - %s: record missing in KV, skipped' % lead_id)
            continue
        try:
            lead = json.loads(raw)
        except ValueError:
            print('  - %s: unreadable JSON, skipped' % lead_id)
            continue
        statements.append(
            "INSERT OR IGNORE INTO leads "
            "(lead_id, client_name, company_name, email, phone, package, notes, language, channel, source_url, received_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" % (
                sql_literal(lead.get('leadId') or lead_id),
                sql_literal(lead.get('clientName')),
                sql_literal(lead.get('companyName')),
                sql_literal(lead.get('email')),
                sql_literal(lead.get('phone')),
                sql_literal(lead.get('package')),
                sql_literal(lead.get('notes')),
                sql_literal(lead.get('language')),
                sql_literal(lead.get('channel')),
                sql_literal(lead.get('sourceUrl')),
                sql_literal(lead.get('receivedAt') or entry.get('at'))))
        print('  + %-26s %s' % (lead_id, lead.get('clientName') or '(no name)'))

    if not statements:
        print('Nothing to insert.')
        return 0

    print('-' * 60)
    print('INSERT statements prepared: %d' % len(statements))

    if not apply:
        print('DRY RUN - add --apply to write them into D1.')
        return 0

    handle, path = tempfile.mkstemp(suffix='.sql')
    os.close(handle)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(statements) + '\n')

    try:
        out = wrangler(['d1', 'execute', DB, '--remote', '--file=' + path, '--yes'])
        print(out.strip().splitlines()[-1] if out.strip() else 'executed')
    finally:
        os.unlink(path)

    print('Backfill applied.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
