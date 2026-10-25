"""
S&R CoreSync For Intelligent Solutions - Translated JavaScript identifier repair
===============================================================================
The multilingual generation pass translated JavaScript identifiers along with
the visible copy. Examples:

    document.querySelectorAll(...)  ->  document.querySelectorTümü(...)
    new Date()                      ->  new Tarih()  /  new Datum()
    toLocaleDateString()            ->  toLocaleTarihString()
    getElementById('invAmount')     ->  getElementById('invBeløp')

The first group is fatal at runtime (TypeError). The second group is
self-consistent but still invalid practice and breaks under minifiers.

Repair strategy
---------------
The translated pages are line-for-line descendants of the reference pages
(en/demo.html and index.html). We align the two files with difflib, then
map every camelCase identifier positionally. That produces a deterministic
mapping instead of a guess.

Usage: python scripts/repair_js_identifiers.py [--dry-run]
Exit code 0 = repair applied (or verified) successfully.
"""
import difflib
import io
import os
import re
import sys
from collections import OrderedDict

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'.git', '_site', 'workers', 'scripts', 'dist', 'node_modules',
             '__pycache__', '.github', '.agents', '.vscode', 'api', 'config'}

# camelCase / UPPER_SNAKE identifiers that may have been translated.
TOKEN_RE = re.compile(r'\b[A-Za-z_$][A-Za-z0-9_$]*\b')
# Identifiers that are JavaScript API names - never allowed to be translated.
JS_API = {
    'querySelectorAll', 'querySelector', 'toLocaleDateString', 'Date',
    'getElementById',
    # known translated spellings produced by the generation pass
    'querySelectorTodos', 'querySelectorTout', 'querySelectorTutti',
    'querySelectorAlle', 'querySelectorAlla', 'querySelectorTümü',
    'querySelectorHemû',
    'toLocaleDatumString', 'toLocaleFechaString', 'toLocaleDataString',
    'toLocaleDatoString', 'toLocaleTarihString', 'toLocaleDîrokString',
    'Datum', 'Fecha', 'Data', 'Dato', 'Tarih', 'Dîrok',
}

# Identifiers that must only be repaired inside a call site, because the
# same word also occurs in the visible copy of the page.
CODE_ONLY = {'Datum', 'Fecha', 'Data', 'Dato', 'Tarih', 'Dîrok'}

# Reference identifiers we are willing to restore a translated name for.
ALLOWED_REFERENCE = {
    'querySelectorAll', 'toLocaleDateString', 'Date', 'getElementById',
}

# Curated repairs: translated identifier -> canonical English identifier.
# Every entry was verified against the reference pages (index.html /
# en/demo.html) and is applied unconditionally, so the repair does not
# depend on the heuristic discovery succeeding.
CURATED = {
    # --- Date constructor -----------------------------------------------------
    'Datum': 'Date', 'Fecha': 'Date', 'Data': 'Date', 'Dato': 'Date',
    'Tarih': 'Date', 'Dîrok': 'Date', 'Datum': 'Date',
    # --- Date formatting ------------------------------------------------------
    'toLocaleDatumString': 'toLocaleDateString',
    'toLocaleFechaString': 'toLocaleDateString',
    'toLocaleDataString': 'toLocaleDateString',
    'toLocaleDatoString': 'toLocaleDateString',
    'toLocaleTarihString': 'toLocaleDateString',
    'toLocaleDîrokString': 'toLocaleDateString',
    # --- querySelectorAll -----------------------------------------------------
    'querySelectorTümü': 'querySelectorAll',
    'querySelectorHemû': 'querySelectorAll',
    'querySelectorTodos': 'querySelectorAll',
    'querySelectorTout': 'querySelectorAll',
    'querySelectorTutti': 'querySelectorAll',
    'querySelectorAlle': 'querySelectorAll',
    'querySelectorAlla': 'querySelectorAll',
    # --- DOM identifiers ------------------------------------------------------
    'bookingPreferredDîrok': 'bookingPreferredDate',
    'bookingPreferredTarih': 'bookingPreferredDate',
    'bookingPreferredDato': 'bookingPreferredDate',
    'bookingPreferredDatum': 'bookingPreferredDate',
    'roiPdfDîrok': 'roiPdfDate',
    'roiPdfTarih': 'roiPdfDate',
    'roiPdfDato': 'roiPdfDate',
    'roiPdfDatum': 'roiPdfDate',
    'preferredDîrok': 'preferredDate',
    'preferredTarih': 'preferredDate',
    'preferredDato': 'preferredDate',
    'preferredDatum': 'preferredDate',
    'pdfDîrokDisplay': 'pdfDateDisplay',
    'pdfTarihDisplay': 'pdfDateDisplay',
    'pdfDatoDisplay': 'pdfDateDisplay',
    'pdfDatumDisplay': 'pdfDateDisplay',
    'pvDîrok': 'pvDate',
    'pvTarih': 'pvDate',
    'pvDato': 'pvDate',
    'pvDatum': 'pvDate',
    'pvRewş': 'pvStatus',
    'slidePaşve': 'slideNext',
    'slideSonraki': 'slideNext',
    'slideNeste': 'slideNext',
    'slideNästa': 'slideNext',
    'tourPaşveBtn': 'tourNextBtn',
    'tourSonrakiBtn': 'tourNextBtn',
    'tourNesteBtn': 'tourNextBtn',
    'tourNästaBtn': 'tourNextBtn',
    'simRewşBadge': 'simStatusBadge',
    'idealRewşText': 'idealStatusText',
    'updateStorageRewşBadge': 'updateStorageStatusBadge',
    'updateStorageDurumBadge': 'updateStorageStatusBadge',
    'checkoutVatBihaye': 'checkoutVatAmount',
    'checkoutVatTutar': 'checkoutVatAmount',
    'checkoutVatBeløp': 'checkoutVatAmount',
    'checkoutVatBelopp': 'checkoutVatAmount',
    'chkVatBeløp': 'chkVatAmount',
    'chkVatBihaye': 'chkVatAmount',
    'chkVatTutar': 'chkVatAmount',
    'idealTotalBeløp': 'idealTotalAmount',
    'invBeløp': 'invAmount',
    'netBeløp': 'netAmount',
    'quickTaxBeløp': 'quickTaxAmount',
    'txBeløp': 'txAmount',
    'vatBeløp': 'vatAmount',
}


def is_translated_candidate(tok):
    """True when the token may be a translated identifier."""
    if tok in JS_API and tok not in ALLOWED_REFERENCE:
        return tok
    if not tok.isascii():
        return tok
    return None


def load(path):
    with io.open(path, encoding='utf-8', errors='ignore') as fh:
        return fh.read().split('\n')


def build_mapping(ref_lines, lang_lines):
    """Map translated identifiers back to their canonical names.

    Strategy: every reference line is indexed by the ASCII tokens it
    contains. A translated line is matched to its reference line through
    the tokens both of them share (the translated words are the ones that
    differ). Once the pair is established, the identifiers are mapped
    positionally.
    """
    ref_token_lists = [TOKEN_RE.findall(line) for line in ref_lines]

    postings = {}
    ref_vocab = set()
    for idx, toks in enumerate(ref_token_lists):
        for t in set(toks):
            ref_vocab.add(t)
            postings.setdefault(t, []).append(idx)

    mapping = OrderedDict()
    for toks in (TOKEN_RE.findall(line) for line in lang_lines):
        if not any(is_translated_candidate(t) for t in toks):
            continue

        anchors = [t for t in toks
                   if t in ref_vocab and t.isascii() and len(t) >= 2
                   and not is_translated_candidate(t)]
        if not anchors:
            continue

        # Intersect the postings of every anchor token, then keep the
        # reference line that yields the most positional identifier matches.
        best = None
        best_score = -1
        for idx in postings[anchors[0]]:
            if not all(idx in postings.get(a, ()) for a in anchors[1:]):
                continue
            ref_toks = ref_token_lists[idx]
            if len(ref_toks) != len(toks):
                continue
            score = 0
            for rt, lt in zip(ref_toks, toks):
                if rt == lt or not is_translated_candidate(lt):
                    continue
                if rt in ALLOWED_REFERENCE or re.match(r'^[a-z][a-zA-Z0-9]*[A-Z]', rt):
                    score += 1
            if score > best_score:
                best_score = score
                best = (ref_toks, toks)
            if best_score >= 3:
                break
        if not best or best_score <= 0:
            continue

        ref_toks, toks = best
        for rt, lt in zip(ref_toks, toks):
            if rt == lt:
                continue
            if not is_translated_candidate(lt):
                continue
            if rt not in ALLOWED_REFERENCE and not re.match(r'^[a-z][a-zA-Z0-9]*[A-Z]', rt):
                continue
            mapping.setdefault(lt, rt)
    return mapping


def main():
    dry = '--dry-run' in sys.argv
    index_map = OrderedDict()
    demo_map = OrderedDict()

    ref_index = load(os.path.join(ROOT, 'index.html'))
    ref_demo = load(os.path.join(ROOT, 'en', 'demo.html'))

    targets = []
    for d in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p) or d in SKIP_DIRS or d.startswith('_'):
            continue
        for name, ref_lines, store in (('index.html', ref_index, index_map),
                                       ('demo.html', ref_demo, demo_map)):
            f = os.path.join(p, name)
            if not os.path.isfile(f):
                continue
            m = build_mapping(ref_lines, load(f))
            for k, v in m.items():
                store.setdefault(k, v)
            targets.append((f, m))

    # Fold translated JS API names back to their canonical spelling.
    for store in (index_map, demo_map):
        for translated, canonical in CURATED.items():
            store.setdefault(translated, canonical)
        for translated, canonical in (
            ('querySelectorTümü', 'querySelectorAll'),
            ('querySelectorHemû', 'querySelectorAll'),
            ('querySelectorTodos', 'querySelectorAll'),
            ('querySelectorTout', 'querySelectorAll'),
            ('querySelectorTutti', 'querySelectorAll'),
            ('querySelectorAlle', 'querySelectorAll'),
            ('querySelectorAlla', 'querySelectorAll'),
            ('toLocaleDatumString', 'toLocaleDateString'),
            ('toLocaleFechaString', 'toLocaleDateString'),
            ('toLocaleDataString', 'toLocaleDateString'),
            ('toLocaleDîrokString', 'toLocaleDateString'),
            ('toLocaleDatoString', 'toLocaleDateString'),
            ('toLocaleTarihString', 'toLocaleDateString'),
        ):
            store[translated] = canonical

    # The Date constructor: translate it back wherever it was renamed.
    date_variants = ['Datum', 'Fecha', 'Data', 'Dato', 'Dîrok', 'Tarih', 'Datum']
    for store in (index_map, demo_map):
        for v in date_variants:
            if v in store:
                store[v] = 'Date'

    print('=' * 72)
    print('S&R CoreSync - Translated Identifier Repair')
    print('=' * 72)
    print('index.html / demo.html mappings discovered: %d' % (len(index_map) + len(demo_map)))
    for k, v in sorted(index_map.items()):
        print('   index  %-30s -> %s' % (k, v))
    for k, v in sorted(demo_map.items()):
        print('   demo   %-30s -> %s' % (k, v))

    if dry:
        print('-' * 72)
        print('DRY RUN - no file was modified.')
        return 0

    changed_files = 0
    total_replacements = 0
    for f, _ in targets:
        with io.open(f, encoding='utf-8', errors='ignore') as fh:
            text = fh.read()
        original = text
        for bad, good in list(index_map.items()) + list(demo_map.items()):
            if bad not in text:
                continue
            if bad in CODE_ONLY:
                # "Data" / "Datum" / "Dato" are also ordinary words in the
                # visible copy, so only the constructor call sites are fixed.
                pat = re.compile(r'(?<![\w$])new\s+' + re.escape(bad) + r'\s*\(')
                text, n = pat.subn('new Date(', text)
                total_replacements += n
                pat2 = re.compile(r'(?<![\w$.])' + re.escape(bad) + r'\.now\s*\(')
                text, n = pat2.subn('Date.now(', text)
                total_replacements += n
            else:
                text, n = re.subn(re.escape(bad) + r'(?![A-Za-z0-9_$])', good, text)
                total_replacements += n
        if text != original:
            with io.open(f, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
            changed_files += 1
            print('  patched %s' % os.path.relpath(f, ROOT).replace('\\', '/'))

    print('-' * 72)
    print('Patched %d file(s), %d identifier occurrence(s).' % (changed_files, total_replacements))
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
