#!/usr/bin/env python3
"""Normalize localized landing-page hero layout and visible copy."""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPTS_DIR.parent
LOCALES_PATH = SCRIPTS_DIR / "portal_hero_locales.json"
SHARED_STYLESHEET = "../css/multilingual-hero-layout.css"
INLINE_STYLESHEET = re.compile(
    r'<link\b[^>]*href=(["\'])\.\./css/inline-[^"\']+\.css\1[^>]*>',
    re.IGNORECASE,
)
DIV_TAG = re.compile(r"</?div\b[^>]*>", re.IGNORECASE)
HERO_CARD_OPEN = re.compile(
    r'<div\b(?=[^>]*\bid=["\']heroEmblemCard["\'])'
    r'(?=[^>]*\bclass=["\'][^"\']*\bhero-emblem-card-3d\b)[^>]*>',
    re.IGNORECASE,
)
HERO_STAGE_OPEN = re.compile(
    r'<div\b(?=[^>]*\bid=["\']heroEmblemStage["\'])[^>]*>', re.IGNORECASE
)
HERO_GRID_OPEN = re.compile(
    r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bhero-reference__grid\b)[^>]*>',
    re.IGNORECASE,
)
HERO_EMBLEM_COLUMN_OPEN = re.compile(
    r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bhero-reference__emblem-col\b)[^>]*>',
    re.IGNORECASE,
)
VOICE_BADGE_OPEN = re.compile(
    r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bhero-emblem-voice-badge-wrap\b)[^>]*>',
    re.IGNORECASE,
)


def load_locales():
    locales = json.loads(LOCALES_PATH.read_text(encoding="utf-8"))
    sys.path.insert(0, str(SCRIPTS_DIR))
    from deploy_sovereign_multilingual import LANGUAGES

    expected = {language["code"] for language in LANGUAGES if language["code"] != "ar"}
    if set(locales) != expected:
        raise ValueError(
            f"{LOCALES_PATH.name}: locale mismatch; "
            f"missing={sorted(expected - set(locales))}, "
            f"extra={sorted(set(locales) - expected)}"
        )
    keys = set(next(iter(locales.values())))
    if not keys or any(set(values) != keys for values in locales.values()):
        raise ValueError(f"{LOCALES_PATH.name}: translation keys differ by locale")
    return locales


HERO_LOCALES = load_locales()
HERO_SOURCE_COPY = tuple(next(iter(HERO_LOCALES.values())).keys())


class HeroGridParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.grid_depth = None
        self.grid_children = []
        self.emblem_inside_grid = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        if tag == "div" and "hero-reference__grid" in classes:
            if self.grid_depth is None:
                self.grid_depth = len(self.stack)
                self.grid_children = []
        elif (
            self.grid_depth is not None
            and tag == "div"
            and len(self.stack) == self.grid_depth + 1
        ):
            self.grid_children.append(classes)
        if "hero-reference__emblem-col" in classes and any(
            "hero-reference__grid" in parent_classes
            for _, parent_classes in self.stack
        ):
            self.emblem_inside_grid = True
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                removed = self.stack[index:]
                del self.stack[index:]
                if any(
                    opened_tag == "div" and "hero-reference__grid" in classes
                    for opened_tag, classes in removed
                ):
                    self.grid_depth = None
                return


def matching_div_end(content, start):
    for token in DIV_TAG.finditer(content, start):
        if token.group().startswith("</"):
            depth -= 1
            if depth == 0:
                return token.end()
        else:
            depth = 1 if token.start() == start else depth + 1
    raise ValueError("unclosed <div> in localized hero markup")


def move_voice_badge_outside_card(content, optional=False):
    card = HERO_CARD_OPEN.search(content)
    stage = HERO_STAGE_OPEN.search(content)
    badge = VOICE_BADGE_OPEN.search(content)
    if not card or not stage or (not badge and not optional):
        raise ValueError("expected hero card, stage, and voice badge exactly once")

    card_end = matching_div_end(content, card.start())
    stage_end = matching_div_end(content, stage.start())
    if not stage.start() < card.start() < card_end <= stage_end:
        raise ValueError("hero card is not contained by the emblem stage")
    if not badge:
        return content

    badge_end = matching_div_end(content, badge.start())
    if not stage.start() < badge.start() < badge_end <= stage_end:
        raise ValueError("voice badge is not contained by the emblem stage")
    if card.start() < badge.start() < card_end:
        badge_markup = content[badge.start():badge_end]
        line_start = content.rfind("\n", 0, badge.start()) + 1
        indent = content[line_start:badge.start()]
        before = re.sub(r"[ \t]*$", "", content[:badge.start()])
        content = before + content[badge_end:]
        card = HERO_CARD_OPEN.search(content)
        card_end = matching_div_end(content, card.start())
        insertion = "\n" + indent + badge_markup + "\n"
        content = content[:card_end] + insertion + content[card_end:]
    return content


def hero_copy_bounds(content):
    start = content.find('class="section-hero-v1')
    if start < 0:
        raise ValueError("localized landing page has no hero section")
    end = content.find("<!-- 1.1 Executive Leadership & Founders Showcase Slider -->", start)
    if end < 0:
        section = re.search(
            r'<section\b(?=[^>]*\bid=["\']founders-showcase["\'])',
            content[start:],
            re.IGNORECASE,
        )
        if not section:
            raise ValueError("localized landing page has no hero end marker")
        end = start + section.start()
    return start, end


def move_emblem_column_into_grid(content, code):
    parser = HeroGridParser()
    parser.feed(content)
    if (
        parser.emblem_inside_grid
        and any("hero-reference__copy" in classes for classes in parser.grid_children)
        and any("hero-reference__emblem-col" in classes for classes in parser.grid_children)
    ):
        return content

    marker = "<!-- Right Column: Interactive 3D Luxury Master Emblem Showcase -->"
    marker_position = content.find(marker)
    if marker_position < 0:
        raise ValueError(f"{code}/index.html: hero emblem column marker is missing")

    before_marker = content[:marker_position]
    closing_tags = list(re.finditer(r"</div>[ \t]*\r?\n[ \t]*$", before_marker, re.IGNORECASE))
    if not closing_tags:
        raise ValueError(f"{code}/index.html: cannot locate hero grid closing tag")
    closing_tag = closing_tags[-1]
    content = before_marker[:closing_tag.start()] + content[marker_position:]

    parser = HeroGridParser()
    parser.feed(content)
    if not (
        parser.emblem_inside_grid
        and any("hero-reference__copy" in classes for classes in parser.grid_children)
        and any("hero-reference__emblem-col" in classes for classes in parser.grid_children)
    ):
        raise ValueError(f"{code}/index.html: hero columns cannot be normalized safely")
    return content


def normalize_index_html(content, code):
    if code == "ar":
        return content

    links = list(INLINE_STYLESHEET.finditer(content))
    if len(links) != 1:
        raise ValueError(f"{code}/index.html: expected one locale inline stylesheet link")
    expected_link = f'<link rel="stylesheet" href="../css/inline-{code}.css">'
    content = (
        content[:links[0].start()]
        + expected_link
        + content[links[0].end():]
    )

    shared_link_count = content.count(SHARED_STYLESHEET)
    shared_link = f'<link rel="stylesheet" href="{SHARED_STYLESHEET}">'
    if shared_link_count > 1:
        raise ValueError(f"{code}/index.html: duplicate shared hero stylesheet")
    if shared_link_count == 0:
        link = re.search(
            r'<link\b[^>]*href=["\']\.\./css/inline-[^"\']+\.css["\'][^>]*>',
            content,
            re.IGNORECASE,
        )
        content = content[:link.end()] + "\n" + shared_link + content[link.end():]

    content = move_voice_badge_outside_card(content, optional=code == "ckb")
    content = move_emblem_column_into_grid(content, code)
    hero_start, hero_end = hero_copy_bounds(content)
    hero = content[hero_start:hero_end]
    for source, target in HERO_LOCALES[code].items():
        if source != target:
            hero = hero.replace(source, target)
    content = content[:hero_start] + hero + content[hero_end:]
    return content


def validate_index_content(content, code):
    issues = []
    expected_inline = f'href="../css/inline-{code}.css"'
    if content.count(expected_inline) != 1:
        issues.append(f"{code}/index.html: locale-specific CSS link is missing or duplicated")
    if content.count(SHARED_STYLESHEET) != 1:
        issues.append(f"{code}/index.html: shared hero stylesheet link is missing or duplicated")

    card = HERO_CARD_OPEN.search(content)
    stage = HERO_STAGE_OPEN.search(content)
    grid = HERO_GRID_OPEN.search(content)
    emblem_column = HERO_EMBLEM_COLUMN_OPEN.search(content)
    badge = VOICE_BADGE_OPEN.search(content)
    if not card or not stage or not grid or not emblem_column or (not badge and code != "ckb"):
        issues.append(f"{code}/index.html: hero emblem structure is incomplete")
    else:
        try:
            card_end = matching_div_end(content, card.start())
            stage_end = matching_div_end(content, stage.start())
            grid_parser = HeroGridParser()
            grid_parser.feed(content)
            direct_child_classes = grid_parser.grid_children
            if (
                not grid_parser.emblem_inside_grid
                or not any("hero-reference__copy" in classes for classes in direct_child_classes)
                or not any("hero-reference__emblem-col" in classes for classes in direct_child_classes)
            ):
                issues.append(f"{code}/index.html: emblem column is outside the hero grid")
            if badge:
                badge_end = matching_div_end(content, badge.start())
                if card.start() < badge.start() < card_end:
                    issues.append(f"{code}/index.html: voice badge is inside the emblem card")
                if not stage.start() < badge.start() < badge_end <= stage_end:
                    issues.append(f"{code}/index.html: voice badge is outside the emblem stage")
        except ValueError as error:
            issues.append(f"{code}/index.html: {error}")

    if code != "en":
        try:
            hero_start, hero_end = hero_copy_bounds(content)
            hero = content[hero_start:hero_end]
        except ValueError as error:
            issues.append(f"{code}/index.html: {error}")
            hero = content
        for source in HERO_SOURCE_COPY:
            if source in hero:
                issues.append(f"{code}/index.html: untranslated hero copy remains: {source}")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="check without writing files")
    mode.add_argument("--apply", action="store_true", help="apply the scoped hero fixes")
    args = parser.parse_args()

    sys.path.insert(0, str(SCRIPTS_DIR))
    from deploy_sovereign_multilingual import LANGUAGES

    issues = []
    changed = 0
    for language in LANGUAGES:
        code = language["code"]
        if code == "ar":
            continue
        path = BASE_DIR / code / "index.html"
        if not path.is_file():
            issues.append(f"{code}/index.html: page is missing")
            continue
        raw = path.read_bytes()
        content = raw.decode("utf-8")
        normalized = normalize_index_html(content, code)
        if args.check and content != normalized:
            issues.append(f"{code}/index.html: run fix_multilingual_hero.py --apply")
        if args.apply and content != normalized:
            newline = b"\r\n" if b"\r\n" in raw else b"\n"
            path.write_bytes(normalized.replace("\n", newline.decode()).encode("utf-8"))
            changed += 1
            content = normalized
        issues.extend(validate_index_content(content, code))

        css_path = BASE_DIR / "css" / f"inline-{code}.css"
        if not css_path.is_file():
            issues.append(f"css/inline-{code}.css: locale stylesheet is missing")

    shared_css = BASE_DIR / "css" / "multilingual-hero-layout.css"
    if not shared_css.is_file():
        issues.append("css/multilingual-hero-layout.css: shared layout stylesheet is missing")

    if issues:
        print("Localized hero validation failed:")
        for issue in issues:
            print(f" - {issue}")
        return 1
    action = f"updated {changed} pages" if args.apply else "check passed"
    print(f"Localized hero {action}: {len(HERO_LOCALES)} non-Arabic landing pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
