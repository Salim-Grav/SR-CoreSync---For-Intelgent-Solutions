#!/usr/bin/env python3
"""Localize service headings, descriptions, and calls to action on landing pages."""

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
LOCALES_PATH = SCRIPTS_DIR / "portal_services_locales.json"
UI_LOCALES_PATH = SCRIPTS_DIR / "portal_service_ui_locales.json"
SECTION_PATTERN = re.compile(
    r'<section\b(?=[^>]*\bid=["\']services["\'])[^>]*>.*?</section>',
    re.IGNORECASE | re.DOTALL,
)
TEXT_NODE = re.compile(r">([^<>]+)<")
VISIBLE_ATTRIBUTE = re.compile(
    r'\b(data-text|aria-label|title|placeholder)\s*=\s*(["\'])(.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
SOURCE_KEYS = (
    "Our Services",
    "Visual Identity",
    "Distinct visual identities built with strategy, clarity, and consistency.",
    "Website Design & Optimization",
    "Modern, high-performance websites designed for clarity, trust, and growth.",
    "E-Commerce Store",
    "Clear, intuitive online stores that turn visitors into seamless buyers.",
    "Book Session 📅",
    "Order via WhatsApp",
    "📊 Comprehensive Package & Feature Comparison",
    "Enterprise Systems & Cloud Architectures",
    "Custom Cloud Software",
    "Engineering high-assurance enterprise cloud backbones with modular microservices, unyielding security, and infinite elasticity.",
    "High-Performance Mobile & Web Apps",
    "Developing native iOS & Android applications and responsive web applications engineered for sub-second execution speeds.",
    "Cloud ERP & Financial Integration",
    "End-to-end ERP integration with automated multi-currency accounting, inventory tracking, and full Dutch/EU tax compliance.",
    "Process Automation & AI Workflows",
    "Deploying autonomous AI agents, intelligent document recognition, and Robotic Process Automation to eliminate administrative friction.",
    "Financial Strategy & Digital Governance",
    "Engineering real-time CFO executive dashboards, cashflow forecasting, and automated audits compliant with European regulatory laws.",
    "Cloud Infrastructure & Cybersecurity",
    "Hardened multi-region infrastructure on AWS and Azure with automated failover, zero-trust security, and 99.98% uptime SLA.",
    "Book Consultation 📅",
    "Live ERP Demo ⚡",
    "ROI Calculator 📊",
    "WhatsApp 💬",
)
UI_SOURCE_KEYS = (
    "Transparent Price:",
    "Direct Savings",
    "🚀 40% Reduction in Legacy Infrastructure Overhead",
    "⚡ Sub-second response & offline PWA readiness",
)


def fail(message):
    raise ValueError(message)


def load_locales():
    try:
        locales = json.loads(LOCALES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{LOCALES_PATH.name}: cannot load locale data: {error}")
    sys.path.insert(0, str(SCRIPTS_DIR))
    from deploy_sovereign_multilingual import LANGUAGES

    expected = {language["code"] for language in LANGUAGES if language["code"] != "ar"}
    if set(locales) != expected:
        fail(
            f"{LOCALES_PATH.name}: locale mismatch; missing="
            f"{sorted(expected - set(locales))}, extra={sorted(set(locales) - expected)}"
        )
    for code, values in locales.items():
        if not isinstance(values, list) or len(values) != len(SOURCE_KEYS):
            fail(f"{LOCALES_PATH.name}: expected {len(SOURCE_KEYS)} ordered values for {code}")
        if any(not isinstance(value, str) or not value.strip() for value in values):
            fail(f"{LOCALES_PATH.name}: empty translation for {code}")
        locales[code] = dict(zip(SOURCE_KEYS, values))
    return locales


LOCALES = load_locales()


def load_ui_locales():
    try:
        locales = json.loads(UI_LOCALES_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{UI_LOCALES_PATH.name}: cannot load locale data: {error}")
    expected = set(LOCALES)
    if set(locales) != expected:
        fail(
            f"{UI_LOCALES_PATH.name}: locale mismatch; missing="
            f"{sorted(expected - set(locales))}, extra={sorted(set(locales) - expected)}"
        )
    for code, values in locales.items():
        if set(values) != set(UI_SOURCE_KEYS):
            fail(f"{UI_LOCALES_PATH.name}: incomplete UI translations for {code}")
    return locales


UI_LOCALES = load_ui_locales()


def section_bounds(content, code):
    openings = list(SECTION_PATTERN.finditer(content))
    if len(openings) != 1:
        fail(f"{code}/index.html: expected one #services section, found {len(openings)}")
    start = openings[0].start()
    depth = 0
    tag_pattern = re.compile(r"</?section\b[^>]*>", re.IGNORECASE)
    for token in tag_pattern.finditer(content, start):
        if token.group().lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return start, token.end()
        else:
            depth += 1
    fail(f"{code}/index.html: #services section is not closed")


def normalize_text(value):
    return " ".join(html.unescape(value).split())


def localize_section(section, translations):
    normalized = {normalize_text(key): value for key, value in translations.items()}

    def replace_text(match):
        raw = match.group(1)
        key = normalize_text(raw)
        translation = normalized.get(key)
        if translation is None:
            return match.group(0)
        decoded = html.unescape(raw)
        leading = re.match(r"\s*", decoded).group()
        trailing = re.search(r"\s*$", decoded).group()
        escaped = html.escape(html.unescape(translation), quote=False)
        return f">{leading}{escaped}{trailing}<"

    section = TEXT_NODE.sub(replace_text, section)

    def replace_attribute(match):
        source = normalize_text(match.group(3))
        translation = normalized.get(source)
        if translation is None:
            return match.group(0)
        quote = match.group(2)
        escaped = html.escape(html.unescape(translation), quote=False)
        escaped = escaped.replace(quote, "&quot;" if quote == '"' else "&#x27;")
        return f'{match.group(1)}={quote}{escaped}{quote}'

    return VISIBLE_ATTRIBUTE.sub(replace_attribute, section)


def normalize_index_html(content, code):
    if code in {"ar", "en"}:
        return content
    start, end = section_bounds(content, code)
    translations = {**LOCALES[code], **UI_LOCALES[code]}
    return content[:start] + localize_section(content[start:end], translations) + content[end:]


def validate_index_content(content, code):
    if code == "en":
        return []
    start, end = section_bounds(content, code)
    section = content[start:end]
    visible = {
        normalize_text(match.group(1))
        for match in TEXT_NODE.finditer(section)
    }
    visible.update(
        normalize_text(match.group(3))
        for match in VISIBLE_ATTRIBUTE.finditer(section)
    )
    return [
        f"{code}/index.html: untranslated service text remains: {key}"
        for key in (*SOURCE_KEYS, *UI_SOURCE_KEYS)
        if normalize_text({**LOCALES[code], **UI_LOCALES[code]}[key]) != normalize_text(key)
        and normalize_text(key) in visible
    ] + (
        [f"{code}/index.html: double-escaped entity in #services"]
        if "&amp;amp;" in section
        else []
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="check without writing files")
    mode.add_argument("--apply", action="store_true", help="apply scoped service translations")
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
            path.write_text(localized, encoding="utf-8", newline="\n")

    if issues:
        print("Service localization check failed:")
        for issue in issues:
            print(f" - {issue}")
        return 1
    print(
        f"Service localization {'applied' if args.apply else 'check passed'}: "
        f"{len(LANGUAGES) - 1} non-Arabic landing pages."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
