#!/usr/bin/env python3
"""Localize shared landing-page sections and add a sanitized demo tracker."""

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

LANDING_LOCALES_PATH = SCRIPTS_DIR / "portal_shared_sections_locales.json"
TRACKER_LOCALES_PATH = SCRIPTS_DIR / "portal_demo_tracker_locales.json"
LANDING_SECTION_IDS = (
    "services-faq",
    "services-compare",
    "tech-pillars",
    "insights",
)
FRONT_SECTION_IDS = LANDING_SECTION_IDS[:3]
REQUIRED_LOCALIZED_TEXT = (
    "Autonomous AI Agents & Enterprise LLMs",
    "EU AI Act 2026",
    "Sovereign Zero-Trust Cloud & Microservices",
    "Next-Gen Enterprise ERP & Real-Time Sync",
    "FinTech, PEPPOL & ViDA Compliance",
    "Cybersecurity, Cryptography & eIDAS",
    "Next-Gen Web Platforms & Headless UI",
    "PWA / Edge Cache",
)
TRACKER_ID = "tab-tracker"
FRONT_START = "<!-- shared-index-sections:start -->"
FRONT_END = "<!-- shared-index-sections:end -->"
INSIGHTS_START = "<!-- shared-index-insights:start -->"
INSIGHTS_END = "<!-- shared-index-insights:end -->"
TRACKER_START = "<!-- localized-demo-tracker:start -->"
TRACKER_END = "<!-- localized-demo-tracker:end -->"
TRACKER_NAV_START = "<!-- localized-demo-tracker-nav:start -->"
TRACKER_NAV_END = "<!-- localized-demo-tracker-nav:end -->"
SECTION_TAG = re.compile(r"</?section\b[^>]*>", re.IGNORECASE)
TEXT_NODE = re.compile(r">([^<>]+)<")
FORBIDDEN_TRACKER_COPY = (
    re.compile(r"\bof[\s-]?2026(?:[\s-]|\b)", re.IGNORECASE),
    re.compile(r"\bmudar\b|\babu\s+fasha\b|\bnl\s*bil\s*arabi\b", re.IGNORECASE),
    re.compile(r"مضر\s+أبو\s+فاشة|منصة\s+NL\s+بالعربي"),
    re.compile(r"€|\$|£"),
    re.compile(r"\b(?:21,?000|4,?410|7,?623)\b"),
)

TRACKER_NAV_TEMPLATE = """<div class="nav-item" id="tourNav-tracker" data-sr-call="switchPortalTab" data-sr-args='["tracker"]' data-sr-this="last">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
    <span>{nav_label}</span>
</div>"""

TRACKER_TEMPLATE = """<section class="tab-section" id="tab-tracker" aria-labelledby="trackerTitle">
    <div class="section-header">
        <div class="section-title-wrap">
            <h2 id="trackerTitle">{section_title}</h2>
            <p>{section_subtitle}</p>
        </div>
    </div>
    <div class="tracker-header-box">
        <div class="tracker-project-title">{project_title}</div>
        <div class="tracker-project-sub">{project_subtitle}</div>
        <div class="d-flex justify-content-between align-items-center mt-3 text-caption text-white-64">
            <span>{readiness_label}</span>
            <strong class="text-gold font-num tracker-readiness-highlight">78% {readiness_complete}</strong>
        </div>
        <div class="tracker-progress-bar-wrap" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="78">
            <div class="tracker-progress-bar-fill" style="width:78%"></div>
        </div>
        <div class="tracker-top-stats" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(10rem,1fr));gap:12px;">
            <div class="tracker-stat-box">
                <div class="tracker-stat-lbl">{stat_total_label}</div>
                <div class="tracker-stat-val">{stat_total_value}</div>
            </div>
            <div class="tracker-stat-box">
                <div class="tracker-stat-lbl">{stat_active_label}</div>
                <div class="tracker-stat-val">{stat_active_value}</div>
            </div>
            <div class="tracker-stat-box">
                <div class="tracker-stat-lbl">{stat_delivery_label}</div>
                <div class="tracker-stat-val">{stat_delivery_value}</div>
            </div>
            <div class="tracker-stat-box">
                <div class="tracker-stat-lbl">{stat_security_label}</div>
                <div class="tracker-stat-val">{stat_security_value}</div>
            </div>
        </div>
    </div>
    <div class="tracker-stages-grid">
{stages}
    </div>
</section>"""

TRACKER_STAGE_TEMPLATE = """        <article class="tracker-stage-card{stage_class}">
            <div>
                <div class="tracker-stage-header">
                    <span class="tracker-stage-badge{badge_class}">{status}</span>
                    <span class="font-num text-caption text-white-64">{stage_number}/5</span>
                </div>
                <h3 class="tracker-stage-name">{title}</h3>
                <p class="tracker-stage-desc">{description}</p>
                <ul class="tracker-items-list">
                    <li class="done-item">{item_one}</li>
                    <li class="done-item">{item_two}</li>
                    <li class="pending-item">{item_three}</li>
                </ul>
            </div>
        </article>"""


def fail(message):
    raise ValueError(message)


def expected_locale_codes():
    return {language["code"] for language in LANGUAGES if language["code"] != "ar"}


def load_json(path, expected_codes):
    try:
        locales = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"{path.name}: cannot load locale data: {error}")
    if set(locales) != expected_codes:
        missing = sorted(expected_codes - set(locales))
        extra = sorted(set(locales) - expected_codes)
        fail(f"{path.name}: locale coverage mismatch; missing={missing}, extra={extra}")
    return locales


def find_section(content, section_id, label):
    opening_pattern = re.compile(
        rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])[^>]*>',
        re.IGNORECASE,
    )
    openings = list(opening_pattern.finditer(content))
    if len(openings) != 1:
        fail(f"{label}: expected one section #{section_id}, found {len(openings)}")

    start = openings[0].start()
    depth = 0
    for token in SECTION_TAG.finditer(content, start):
        if token.group().lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return start, token.end()
        else:
            depth += 1
    fail(f"{label}: section #{section_id} has no matching closing tag")


def normalize_text(value):
    return " ".join(html.unescape(value).split())


def localize_section(source, translations, label):
    normalized_translations = {
        normalize_text(key): value for key, value in translations.items()
    }

    def replace_text(match):
        raw_text = match.group(1)
        normalized = normalize_text(raw_text)
        if not normalized:
            return match.group(0)
        translated = normalized_translations.get(normalized)
        if translated is None:
            fail(f"{label}: missing translation for visible text {normalized!r}")
        decoded = html.unescape(raw_text)
        leading = re.match(r"\s*", decoded).group()
        trailing = re.search(r"\s*$", decoded).group()
        escaped = html.escape(translated, quote=False)
        return f">{leading}{escaped}{trailing}<"

    return TEXT_NODE.sub(replace_text, source)


def extract_html_section(content, section_id, label):
    start, end = find_section(content, section_id, label)
    return content[start:end]


def validate_landing_locales(source, locales):
    source_texts = set()
    for section_id in LANDING_SECTION_IDS:
        section = extract_html_section(source, section_id, "index.html")
        source_texts.update(
            normalize_text(match.group(1))
            for match in TEXT_NODE.finditer(section)
            if normalize_text(match.group(1))
        )

    for code, translations in locales.items():
        normalized = {}
        for key, value in translations.items():
            source_text = normalize_text(key)
            if source_text in normalized:
                fail(f"{code}: duplicate normalized translation key {source_text!r}")
            normalized[source_text] = value
        if set(normalized) != source_texts:
            missing = sorted(source_texts - set(normalized))
            extra = sorted(set(normalized) - source_texts)
            fail(
                f"{code}: landing translation key mismatch; "
                f"missing={missing[:5]}, extra={extra[:5]}"
            )
        empty = [
            source_text
            for source_text, value in normalized.items()
            if not isinstance(value, str) or not value.strip()
        ]
        if empty:
            fail(f"{code}: empty landing translations for {empty[:5]}")


def render_landing_sections(source, translations, code, label):
    snippets = {}
    if code != "en":
        normalized_translations = {
            normalize_text(key): normalize_text(value)
            for key, value in translations.items()
            if isinstance(value, str)
        }
        for source_text in REQUIRED_LOCALIZED_TEXT:
            translated = normalized_translations.get(normalize_text(source_text))
            if translated is None:
                fail(f"{label}: missing translation for {source_text!r}")
            if translated.casefold() == source_text.casefold():
                fail(f"{label}: English fallback remains for {source_text!r}")
    for section_id in LANDING_SECTION_IDS:
        source_section = extract_html_section(source, section_id, label)
        localized = localize_section(
            source_section,
            translations,
            f"{label} #{section_id}",
        )
        if code != "ar":
            localized = localized.replace(
                'href="./blog.html"', 'href="../blog.html"'
            ).replace(
                'href="./insights/', 'href="../insights/'
            )
        localized = localized.replace("text-align:right;", "text-align:start;")
        snippets[section_id] = localized
    return snippets


def replace_or_insert_block(
    content,
    start_marker,
    end_marker,
    block,
    anchor_pattern,
    label,
    check_only,
    forbidden_ids=(),
):
    start_count = content.count(start_marker)
    end_count = content.count(end_marker)
    expected_block = f"{start_marker}\n{block}\n{end_marker}"
    if start_count or end_count:
        if start_count != 1 or end_count != 1:
            fail(f"{label}: incomplete or duplicate generated-section markers")
        start = content.index(start_marker)
        end = content.index(end_marker, start) + len(end_marker)
        current = content[start:end]
        if check_only and current != expected_block:
            fail(f"{label}: generated section content is out of date")
        return content if check_only else content[:start] + expected_block + content[end:]

    for section_id in forbidden_ids:
        if re.search(
            rf'<section\b(?=[^>]*\bid=["\']{re.escape(section_id)}["\'])',
            content,
            re.IGNORECASE,
        ):
            fail(f"{label}: #{section_id} exists outside the managed block")
    if check_only:
        fail(f"{label}: generated section block is missing")

    anchors = list(re.finditer(anchor_pattern, content, re.IGNORECASE))
    if len(anchors) != 1:
        fail(f"{label}: expected one insertion anchor, found {len(anchors)}")
    position = anchors[0].start()
    return content[:position] + expected_block + "\n\n" + content[position:]


def replace_tracker(content, tracker_html, label, check_only):
    start_count = content.count(TRACKER_START)
    end_count = content.count(TRACKER_END)
    expected = f"{TRACKER_START}\n{tracker_html}\n{TRACKER_END}"
    if start_count or end_count:
        if start_count != 1 or end_count != 1:
            fail(f"{label}: incomplete or duplicate tracker markers")
        start = content.index(TRACKER_START)
        end = content.index(TRACKER_END, start) + len(TRACKER_END)
        current = content[start:end]
        if check_only and current != expected:
            fail(f"{label}: generated tracker is out of date")
        return content if check_only else content[:start] + expected + content[end:]

    section_matches = list(
        re.finditer(
            rf'<section\b(?=[^>]*\bid=["\']{TRACKER_ID}["\'])',
            content,
            re.IGNORECASE,
        )
    )
    if len(section_matches) > 1:
        fail(f"{label}: duplicate #{TRACKER_ID} sections")
    if check_only:
        fail(f"{label}: sanitized tracker block is missing")

    if section_matches:
        start, end = find_section(content, TRACKER_ID, label)
        return content[:start] + expected + content[end:]

    closing_main = list(re.finditer(r"</main\s*>", content, re.IGNORECASE))
    if len(closing_main) != 1:
        fail(f"{label}: expected one </main> tracker insertion point")
    position = closing_main[0].start()
    return content[:position] + expected + "\n\n" + content[position:]


def replace_tracker_nav(content, nav_html, label, check_only):
    start_count = content.count(TRACKER_NAV_START)
    end_count = content.count(TRACKER_NAV_END)
    expected = f"{TRACKER_NAV_START}\n{nav_html}\n{TRACKER_NAV_END}"
    if start_count or end_count:
        if start_count != 1 or end_count != 1:
            fail(f"{label}: incomplete or duplicate tracker navigation markers")
        start = content.index(TRACKER_NAV_START)
        end = content.index(TRACKER_NAV_END, start) + len(TRACKER_NAV_END)
        current = content[start:end]
        if check_only and current != expected:
            fail(f"{label}: tracker navigation is out of date")
        return content if check_only else content[:start] + expected + content[end:]

    nav_match = re.search(
        r'<div\b(?=[^>]*\bid=["\']tourNav-tracker["\'])[^>]*>.*?</div>',
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if check_only:
        fail(f"{label}: localized tracker navigation is missing")
    if nav_match:
        return content[: nav_match.start()] + expected + content[nav_match.end() :]

    spacer_matches = list(
        re.finditer(
            r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bsidebar-spacer\b)[^>]*>',
            content,
            re.IGNORECASE,
        )
    )
    if len(spacer_matches) != 1:
        fail(f"{label}: expected one sidebar navigation insertion point")
    position = spacer_matches[0].start()
    return content[:position] + expected + "\n" + content[position:]


def render_tracker(values, label):
    required_keys = {
        "section_title",
        "section_subtitle",
        "nav_label",
        "project_title",
        "project_subtitle",
        "readiness_label",
        "readiness_complete",
        "stat_total_label",
        "stat_total_value",
        "stat_active_label",
        "stat_active_value",
        "stat_delivery_label",
        "stat_delivery_value",
        "stat_security_label",
        "stat_security_value",
        "status_done",
        "status_active",
        "status_planned",
        "stages",
    }
    if set(values) != required_keys:
        fail(f"{label}: tracker keys do not match the canonical schema")
    if len(values["stages"]) != 5:
        fail(f"{label}: expected five tracker stages")

    escaped = {
        key: html.escape(values[key], quote=False)
        for key in required_keys
        if key != "stages"
    }
    rendered_stages = []
    for index, stage in enumerate(values["stages"], start=1):
        if set(stage) != {"title", "description", "items"} or len(stage["items"]) != 3:
            fail(f"{label}: stage {index} must have a title, description, and three items")
        stage_values = {
            "stage_class": " in-progress" if index == 2 else "",
            "badge_class": " active" if index == 2 else "",
            "status": values["status_active"]
            if index == 2
            else values["status_done"]
            if index == 1
            else values["status_planned"],
            "stage_number": str(index),
            "title": stage["title"],
            "description": stage["description"],
            "item_one": stage["items"][0],
            "item_two": stage["items"][1],
            "item_three": stage["items"][2],
        }
        rendered_stages.append(
            TRACKER_STAGE_TEMPLATE.format(
                **{
                    key: html.escape(value, quote=False)
                    for key, value in stage_values.items()
                }
            )
        )
    escaped["stages"] = "\n".join(rendered_stages)
    rendered = TRACKER_TEMPLATE.format(**escaped)
    if any(pattern.search(rendered) for pattern in FORBIDDEN_TRACKER_COPY):
        fail(f"{label}: tracker contains customer-specific or financial data")
    return rendered


def render_index(path, code, source, translations, check_only):
    relative = path.relative_to(BASE_DIR)
    content = path.read_text(encoding="utf-8")
    sections = render_landing_sections(source, translations, code, str(relative))
    front_block = "\n\n".join(sections[section_id] for section_id in FRONT_SECTION_IDS)
    content = replace_or_insert_block(
        content,
        FRONT_START,
        FRONT_END,
        front_block,
        rf'<section\b(?=[^>]*\bid=["\']executive-solutions-stage["\'])',
        str(relative),
        check_only,
        forbidden_ids=FRONT_SECTION_IDS,
    )
    content = replace_or_insert_block(
        content,
        INSIGHTS_START,
        INSIGHTS_END,
        sections["insights"],
        r"</main\s*>",
        str(relative),
        check_only,
        forbidden_ids=("insights",),
    )
    return content


def render_demo(path, code, tracker_locales, check_only):
    relative = path.relative_to(BASE_DIR)
    content = path.read_text(encoding="utf-8")
    tracker_html = render_tracker(tracker_locales[code], f"{relative}")
    content = replace_tracker(content, tracker_html, str(relative), check_only)
    nav_html = TRACKER_NAV_TEMPLATE.format(
        nav_label=html.escape(tracker_locales[code]["nav_label"], quote=False)
    )
    content = replace_tracker_nav(content, nav_html, str(relative), check_only)
    return content


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="verify localized pages without writing")
    mode.add_argument("--apply", action="store_true", help="update only the shared localized sections")
    parser.add_argument(
        "--demo-only",
        action="store_true",
        help="process only the sanitized demo tracker and its navigation item",
    )
    args = parser.parse_args()
    check_only = args.check
    codes = expected_locale_codes()
    tracker_locales = load_json(TRACKER_LOCALES_PATH, codes)
    landing_locales = (
        {} if args.demo_only else load_json(LANDING_LOCALES_PATH, codes)
    )
    source_index = (
        None
        if args.demo_only
        else (BASE_DIR / "index.html").read_text(encoding="utf-8")
    )
    if not args.demo_only:
        validate_landing_locales(source_index, landing_locales)
    updates = {}

    for language in LANGUAGES:
        code = language["code"]
        if code == "ar":
            continue
        if code not in tracker_locales:
            fail(f"Missing demo tracker translations for {code}")
        if not args.demo_only and code not in landing_locales:
            fail(f"Missing landing section translations for {code}")
        portal_dir = BASE_DIR / code
        demo_path = portal_dir / "demo.html"
        if not args.demo_only:
            index_path = portal_dir / "index.html"
            updates[index_path] = render_index(
                index_path,
                code,
                source_index,
                landing_locales[code],
                check_only,
            )
        updates[demo_path] = render_demo(
            demo_path,
            code,
            tracker_locales,
            check_only,
        )

    action = "check passed" if check_only else "updated"
    if not check_only:
        for path, content in updates.items():
            path.write_text(content, encoding="utf-8", newline="")
    page_count = len(codes) if args.demo_only else len(codes) * 2
    print(
        f"Shared portal sections {action}: "
        f"{len(codes)} localized languages / {page_count} pages."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"Shared portal localization failed: {error}", file=sys.stderr)
        raise SystemExit(1)
