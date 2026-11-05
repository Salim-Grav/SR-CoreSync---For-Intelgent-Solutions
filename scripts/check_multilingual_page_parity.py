#!/usr/bin/env python3
"""Check shared structure and language metadata for configured portals."""

from html.parser import HTMLParser
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from deploy_sovereign_multilingual import LANGUAGES  # noqa: E402


INDEX_SECTIONS = (
    "founders-showcase",
    "services",
    "services-faq",
    "services-compare",
    "tech-pillars",
    "executive-solutions-stage",
    "about",
    "testimonials",
    "pricing",
    "roi-calculator",
    "software-hub",
    "faq",
    "contact",
    "compliance",
    "newsletter",
    "insights",
)

DEMO_TABS = (
    "tab-overview",
    "tab-erp",
    "tab-invoices",
    "tab-ai",
    "tab-cloud",
    "tab-whitelabel",
    "tab-software",
    "tab-roi",
    "tab-tracker",
)


class PortalParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_tags = []
        self.sections = []
        self.tracker_navs = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "html":
            self.html_tags.append(attributes)
        elif attributes.get("id") == "tourNav-tracker":
            self.tracker_navs.append(attributes)
        elif tag == "section" and attributes.get("id"):
            self.sections.append(attributes["id"])


def inspect_page(path, lang, direction, required_ids, require_tracker_nav=False):
    if not path.is_file():
        return [f"{path.relative_to(BASE_DIR)}: page is missing"]

    parser = PortalParser()
    parser.feed(path.read_text(encoding="utf-8"))
    relative_path = path.relative_to(BASE_DIR)
    issues = []

    if len(parser.html_tags) != 1:
        issues.append(f"{relative_path}: expected one <html> tag, found {len(parser.html_tags)}")
    else:
        html_attrs = parser.html_tags[0]
        if html_attrs.get("lang", "").lower() != lang:
            issues.append(
                f"{relative_path}: lang={html_attrs.get('lang')!r}, expected {lang!r}"
            )
        if html_attrs.get("dir", "").lower() != direction:
            issues.append(
                f"{relative_path}: dir={html_attrs.get('dir')!r}, expected {direction!r}"
            )
        if html_attrs.get("data-page-language", "").lower() != lang:
            issues.append(
                f"{relative_path}: data-page-language="
                f"{html_attrs.get('data-page-language')!r}, expected {lang!r}"
            )

    positions = []
    for section_id in required_ids:
        occurrences = parser.sections.count(section_id)
        if occurrences != 1:
            issues.append(
                f"{relative_path}: expected section #{section_id} once, found {occurrences}"
            )
        else:
            positions.append(parser.sections.index(section_id))

    if len(positions) == len(required_ids) and positions != sorted(positions):
        issues.append(f"{relative_path}: shared sections are out of canonical order")
    if require_tracker_nav:
        if len(parser.tracker_navs) != 1:
            issues.append(
                f"{relative_path}: expected one tracker navigation item, "
                f"found {len(parser.tracker_navs)}"
            )
        elif (
            parser.tracker_navs[0].get("data-sr-call") != "switchPortalTab"
            or parser.tracker_navs[0].get("data-sr-args") != '["tracker"]'
        ):
            issues.append(f"{relative_path}: tracker navigation does not target #tab-tracker")
    return issues


def main():
    issues = []
    codes = [language["code"] for language in LANGUAGES]
    if len(codes) != len(set(codes)):
        issues.append("deploy_sovereign_multilingual.LANGUAGES contains duplicate language codes")

    for language in LANGUAGES:
        code = language["code"]
        portal_dir = BASE_DIR if code == "ar" else BASE_DIR / code
        issues.extend(
            inspect_page(portal_dir / "index.html", code, language["dir"], INDEX_SECTIONS)
        )
        issues.extend(
            inspect_page(
                portal_dir / "demo.html",
                code,
                language["dir"],
                DEMO_TABS,
                require_tracker_nav=True,
            )
        )

    if issues:
        print("Multilingual portal parity check failed:")
        for issue in issues:
            print(f" - {issue}")
        return 1

    print(
        f"Multilingual portal parity check passed: "
        f"{len(codes)} configured languages, {len(codes) * 2} pages."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
