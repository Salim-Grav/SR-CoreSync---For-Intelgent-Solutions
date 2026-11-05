#!/usr/bin/env python3
"""Localize the shared founder-showcase copy and controls."""

import argparse
import html
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPTS_DIR.parent
LOCALES_PATH = SCRIPTS_DIR / "portal_founder_showcase_locales.json"
BIO_LOCALES_PATH = SCRIPTS_DIR / "portal_founder_bio_locales.json"
SECTION_PATTERN = re.compile(
    r'<section\b(?=[^>]*\bid=["\']founders-showcase["\'])[^>]*>.*?</section>',
    re.IGNORECASE | re.DOTALL,
)
TEXT_NODE = re.compile(r">([^<>]+)<")
SOURCE_KEYS = (
    "Visionary Leadership Driving",
    "Digital Transformation &amp; ERP",
    "Interactive Auto Slider 🔄",
    "Corporate Emblem 👑",
    "Full Suite Showcase",
    "Corporate Profile (PDF) 📄",
    "Smart NFC Card 📲",
    "Certified Corporate Emblem",
    "Enterprise Innovation Symbol",
    "Inspect 🔍",
    "Download 4K 🌟",
    "Services 🚀",
    "Pause",
    "Merging advanced cloud architecture and generative AI with high-precision financial acumen, managerial accounting, and enterprise ERP solutions for ambitious companies across Europe and the Middle East.",
    "Chief Technology Officer &amp; Principal Cloud &amp; AI Architect &amp; CTO",
    "Certified Principal Cloud Architect",
    "Enterprise AI &amp; LLM Automation",
    "12+ Years Software Systems Engineering",
    "Chief Financial Officer &amp; Financial ERP Systems Architect &amp; CFO",
    "Senior Financial &amp; ERP Consultant",
    "Odoo &amp; Enterprise ERP Systems Architect",
    "IFRS &amp; European Corporate Tax Compliance",
)


def load_locales():
    locales = json.loads(LOCALES_PATH.read_text(encoding="utf-8"))
    bio_locales = json.loads(BIO_LOCALES_PATH.read_text(encoding="utf-8"))
    sys.path.insert(0, str(SCRIPTS_DIR))
    from deploy_sovereign_multilingual import LANGUAGES

    expected = {language["code"] for language in LANGUAGES if language["code"] != "ar"}
    if set(locales) != expected or set(bio_locales) != expected:
        raise ValueError(
            "Founder locale mismatch; "
            f"{LOCALES_PATH.name} missing={sorted(expected - set(locales))}, "
            f"extra={sorted(set(locales) - expected)}; "
            f"{BIO_LOCALES_PATH.name} missing={sorted(expected - set(bio_locales))}, "
            f"extra={sorted(set(bio_locales) - expected)}"
        )
    for code, values in locales.items():
        merged = values | bio_locales[code]
        if set(merged) != set(SOURCE_KEYS):
            raise ValueError(f"{LOCALES_PATH.name}: incomplete source keys for {code}")
        if any(not isinstance(value, str) or not value.strip() for value in merged.values()):
            raise ValueError(f"{LOCALES_PATH.name}: empty translation for {code}")
        values.update(bio_locales[code])
    return locales


LOCALES = load_locales()


def section_bounds(content, code):
    matches = list(SECTION_PATTERN.finditer(content))
    if len(matches) != 1:
        raise ValueError(
            f"{code}/index.html: expected one founders-showcase section, found {len(matches)}"
        )
    return matches[0].start(), matches[0].end()


def normalize_text(value):
    return " ".join(html.unescape(value).split())


def localize_section(section, translations):
    normalized = {normalize_text(key): value for key, value in translations.items()}

    def replace_text(match):
        raw = match.group(1)
        key = normalize_text(raw)
        if key not in normalized:
            return match.group(0)
        decoded = html.unescape(raw)
        leading = re.match(r"\s*", decoded).group()
        trailing = re.search(r"\s*$", decoded).group()
        translated = html.escape(html.unescape(normalized[key]), quote=False)
        return f">{leading}{translated}{trailing}<"

    return TEXT_NODE.sub(replace_text, section)


def normalize_index_html(content, code):
    if code in {"ar", "en"}:
        return content
    start, end = section_bounds(content, code)
    localized = localize_section(content[start:end], LOCALES[code])
    return content[:start] + localized + content[end:]


def validate_index_content(content, code):
    if code == "en":
        return []
    start, end = section_bounds(content, code)
    section = content[start:end]
    issues = [
        f"{code}/index.html: untranslated founder-showcase text remains: {source}"
        for source in SOURCE_KEYS
        if normalize_text(LOCALES[code][source]) != normalize_text(source)
        if normalize_text(source) in {
            normalize_text(match.group(1)) for match in TEXT_NODE.finditer(section)
        }
    ]
    if "&amp;amp;" in section:
        issues.append(f"{code}/index.html: double-escaped HTML entity in founder-showcase")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="check without writing files")
    mode.add_argument("--apply", action="store_true", help="apply the scoped translations")
    args = parser.parse_args()

    sys.path.insert(0, str(SCRIPTS_DIR))
    from deploy_sovereign_multilingual import LANGUAGES

    issues = []
    for language in LANGUAGES:
        code = language["code"]
        if code == "ar":
            continue
        path = BASE_DIR / code / "index.html"
        if not path.is_file():
            issues.append(f"{code}/index.html: page is missing")
            continue
        content = path.read_text(encoding="utf-8")
        localized = normalize_index_html(content, code) if args.apply else content
        issues.extend(validate_index_content(localized, code))
        if args.apply and localized != content:
            path.write_text(localized, encoding="utf-8", newline="")

    if issues:
        print("Founder showcase localization check failed:")
        for issue in issues:
            print(f" - {issue}")
        return 1
    print(
        f"Founder showcase localization "
        f"{'applied' if args.apply else 'check passed'}: "
        f"{len(LANGUAGES) - 1} non-Arabic landing pages."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
