#!/usr/bin/env python3
"""Apply and validate curated locale metadata for the landing and demo pages."""

import argparse
import html
import json
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from deploy_sovereign_multilingual import LANGUAGES  # noqa: E402

LOCALES_PATH = SCRIPTS_DIR / "portal_core_locales.json"
DEMO_UI_LOCALES_PATH = SCRIPTS_DIR / "portal_demo_ui_locales.json"
ENGLISH_HERO_PHRASE = "Autonomous AI</span> Architectures"
HERO_ARCHITECTURE_TRANSLATIONS = {
    "nl": ("Autonome AI", "architecturen"),
    "de": ("autonome KI", "Architekturen"),
    "fr": ("IA autonome", "architectures"),
    "tr": ("Otonom Yapay Zekâ", "Mimarileri"),
    "es": ("IA autónoma", "Arquitecturas"),
    "it": ("IA autonoma", "Architetture"),
}
DEMO_UI_SOURCE = {
    "cloud_status": "Cloud Node Online (EU Central)",
    "start_tour": "🚀 Start Tour",
    "proposal_brief": "Proposal Brief (PDF)",
    "client_view": "Client View [P]",
    "book_session": "Book Session with this Architecture",
    "emblem_studio": "Emblem Studio",
    "return_website": "Return to Website",
    "dashboard": "Executive Dashboard",
    "erp_inventory": "ERP & Inventory Ops",
    "invoicing_vat": "E-Invoicing & VAT",
    "ai_copilot": "AI Financial Copilot",
    "cloud_servers": "Cloud Server Status",
    "white_label": "White-Label Branding",
    "software_store": "Software Hub & Store",
    "roi_calculator": "Smart ROI Calculator",
    "financial_dashboard": "Real-Time Financial Dashboard & Cash Flow Telemetry",
    "dashboard_subtitle": "Live simulation engine for automated enterprise revenue, cloud expenses, and cash telemetry",
    "currency_simulator": "Live Currency & VAT Simulator:",
    "currency": "Currency:",
    "tax_regime": "Tax Regime:",
    "tax_estimate": "Calculated Tax:",
    "vat_standard": "Dutch BTW (21%)",
    "vat_reduced": "Reduced BTW (9%)",
    "vat_gcc": "GCC VAT (15%)",
    "tax_exempt": "Tax Exempt (0%)",
}


def load_locales():
    locales = json.loads(LOCALES_PATH.read_text(encoding="utf-8"))
    expected_codes = {language["code"] for language in LANGUAGES}
    if set(locales) != expected_codes:
        missing = sorted(expected_codes - set(locales))
        extra = sorted(set(locales) - expected_codes)
        raise ValueError(f"Locale coverage mismatch; missing={missing}, extra={extra}")
    required_keys = {"page_title", "description", "demo_title"}
    for code, values in locales.items():
        if set(values) != required_keys:
            raise ValueError(f"{code}: expected exactly {sorted(required_keys)}")
        if not all(isinstance(value, str) and value.strip() for value in values.values()):
            raise ValueError(f"{code}: locale values must be non-empty strings")
    return locales


def load_demo_ui_locales():
    locales = json.loads(DEMO_UI_LOCALES_PATH.read_text(encoding="utf-8"))
    expected_codes = {language["code"] for language in LANGUAGES}
    expected_keys = set(DEMO_UI_SOURCE)
    if set(locales) != expected_codes:
        raise ValueError("Demo UI locale coverage does not match configured languages")
    for code, values in locales.items():
        if set(values) != expected_keys:
            raise ValueError(f"{code}: demo UI keys do not match the canonical source")
        if not all(isinstance(value, str) and value.strip() for value in values.values()):
            raise ValueError(f"{code}: demo UI translations must be non-empty strings")
    return locales


def replace_once(content, pattern, replacement, label, path, check_only):
    updated, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"{path}: expected one {label}, found {count}")
    if check_only and updated != content:
        raise ValueError(f"{path}: {label} is not localized to the configured value")
    return updated


def update_launchpad_language_count(content, path, check_only):
    language_count = str(len(LANGUAGES))
    updated = re.sub(
        r'(<span class="apple-dock-badge">)28(</span>)',
        rf"\g<1>{language_count}\2",
        content,
    )
    replacements = (
        ("All 28 Languages", f"All {language_count} Languages"),
        ("Open Full 28 Languages Menu", f"Open Full {language_count} Languages Menu"),
        ("28 Sovereign Languages Grid", f"{language_count} Sovereign Languages Grid"),
        (
            "28 Supported Nations & VAT Regimes",
            f"{language_count} Supported Languages & VAT Regimes",
        ),
        (
            "28 Supported Languages & VAT Regimes",
            f"{language_count} Supported Languages & VAT Regimes",
        ),
        ("اللغات الـ 28", f"اللغات الـ {language_count}"),
        ("(28 دولة ونظاماً ضريبياً)", f"({language_count} لغة ونظاماً ضريبياً)"),
    )
    for source, replacement in replacements:
        updated = updated.replace(source, replacement)
    if check_only and updated != content:
        raise ValueError(f"{path}: launchpad language count is not {language_count}")
    badges = re.findall(r'<span class="apple-dock-badge">(\d+)</span>', updated)
    if not badges or any(badge != language_count for badge in badges):
        raise ValueError(f"{path}: launchpad badge does not match {language_count} configured languages")
    return updated


def update_index(path, code, locale, check_only):
    content = path.read_text(encoding="utf-8")
    escaped_title = html.escape(locale["page_title"], quote=False)
    escaped_description = html.escape(locale["description"], quote=True)
    relative = path.relative_to(BASE_DIR)

    content = replace_once(
        content,
        r"<title>.*?</title>",
        f"<title>{escaped_title}</title>",
        "page title",
        relative,
        check_only,
    )
    content = replace_once(
        content,
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        lambda match: f"{match.group(1)}{escaped_description}{match.group(2)}",
        "meta description",
        relative,
        check_only,
    )
    content = update_launchpad_language_count(content, relative, check_only)

    if code not in {"ar", "en"}:
        og_title = html.escape(locale["page_title"], quote=True)
        twitter_title = og_title
        content = replace_once(
            content,
            r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
            lambda match: f"{match.group(1)}{og_title}{match.group(2)}",
            "Open Graph title",
            relative,
            check_only,
        )
        content = replace_once(
            content,
            r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
            lambda match: f"{match.group(1)}{escaped_description}{match.group(2)}",
            "Open Graph description",
            relative,
            check_only,
        )
        content = replace_once(
            content,
            r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
            lambda match: f"{match.group(1)}{twitter_title}{match.group(2)}",
            "Twitter title",
            relative,
            check_only,
        )
        content = replace_once(
            content,
            r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
            lambda match: f"{match.group(1)}{escaped_description}{match.group(2)}",
            "Twitter description",
            relative,
            check_only,
        )

    if code not in {"ar", "en"}:
        hero_match = re.search(
            r'(<h1 class="hero-reference__title">.*?</h1>)',
            content,
            flags=re.DOTALL,
        )
        if hero_match and ENGLISH_HERO_PHRASE in hero_match.group(1):
            translation = HERO_ARCHITECTURE_TRANSLATIONS.get(code)
            if not translation:
                raise ValueError(f"{relative}: missing hero heading translation")
            ai_term, architecture_term = (html.escape(value) for value in translation)
            localized_hero = hero_match.group(1).replace(
                ENGLISH_HERO_PHRASE,
                f"{ai_term}</span> {architecture_term}",
                1,
            )
            updated = content[: hero_match.start()] + localized_hero + content[hero_match.end() :]
            if check_only:
                raise ValueError(f"{relative}: hero heading contains untranslated English phrase")
            content = updated

    return content


def update_demo(path, code, locale, ui_locale, check_only):
    content = path.read_text(encoding="utf-8")
    relative = path.relative_to(BASE_DIR)
    content = update_launchpad_language_count(content, relative, check_only)
    title = html.escape(locale["demo_title"], quote=False)
    content = replace_once(
        content,
        r"<title>.*?</title>",
        f"<title>{title}</title>",
        "demo page title",
        relative,
        check_only,
    )
    if code == "en":
        return content

    for key, source in DEMO_UI_SOURCE.items():
        escaped_source = html.escape(source, quote=False)
        escaped_translation = html.escape(ui_locale[key], quote=False)
        source_variants = sorted({source, escaped_source}, key=len, reverse=True)
        source_pattern = "|".join(re.escape(value) for value in source_variants)
        pattern = rf">([^<>]*?)(?:{source_pattern})([^<>]*?)<"
        content, count = re.subn(
            pattern,
            lambda match: f">{match.group(1)}{escaped_translation}{match.group(2)}<",
            content,
        )
        if check_only and count:
            raise ValueError(
                f"{path.relative_to(BASE_DIR)}: untranslated demo UI text remains: {source}"
            )
    return content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if localized metadata is stale")
    args = parser.parse_args()
    locales = load_locales()
    demo_ui_locales = load_demo_ui_locales()
    errors = []
    updated_files = 0

    for language in LANGUAGES:
        code = language["code"]
        portal_dir = BASE_DIR if code == "ar" else BASE_DIR / code
        for path, updater, values in (
            (portal_dir / "index.html", update_index, (code, locales[code])),
            (
                portal_dir / "demo.html",
                update_demo,
                (code, locales[code], demo_ui_locales[code]),
            ),
        ):
            try:
                updated = updater(path, *values, args.check)
                current = path.read_text(encoding="utf-8")
                if updated != current:
                    if args.check:
                        raise ValueError(f"{path.relative_to(BASE_DIR)}: localization is out of date")
                    path.write_text(updated, encoding="utf-8", newline="")
                    updated_files += 1
            except (OSError, ValueError) as error:
                errors.append(str(error))

    if errors:
        print("Portal localization check failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    action = "validated" if args.check else f"updated {updated_files} pages"
    print(f"Portal core localization {action}: {len(locales)} languages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
