#!/usr/bin/env python3
"""Validate the standalone laboratory site source and Jekyll build."""

from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from import_labs import (
    COURSE_LABS,
    IMAGE_ASSETS,
    IMAGE_ROOT,
    LABS,
    PUBLISHED_LABS,
    SITE_ROOT,
    normalize_markdown,
    render_lab_page,
    render_year_index,
    transform_body,
)


BUILD = SITE_ROOT / "_site"
TYPEFACE_CHOICES = {"plex", "google-sans"}
REQUIRED_FILES = (
    ".gitignore",
    "_config.yml",
    "_layouts/default.html",
    "index.md",
    "2025/index.md",
    "404.html",
    "Gemfile",
    "README.md",
    "assets/css/main.scss",
    "assets/js/site.js",
    "assets/js/typeface-switcher.js",
    "assets/fonts/fonts.css",
    "assets/fonts/licenses/googlesanscode-OFL.txt",
    "assets/fonts/licenses/googlesansflex-OFL.txt",
    "assets/fonts/licenses/ibmplexmono-OFL.txt",
    "assets/fonts/licenses/ibmplexsans-OFL.txt",
    "assets/fonts/licenses/ibmplexserif-OFL.txt",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.landmarks: set[str] = set()
        self.images_without_alt: list[str] = []
        self.title_parts: list[str] = []
        self.typeface_pickers = 0
        self.language = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        identifier = values.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)
        if tag in {"header", "nav", "main", "footer"}:
            self.landmarks.add(tag)
        if tag == "html":
            self.language = values.get("lang") or ""
        if tag == "a" and values.get("href"):
            self.references.append(("href", values["href"] or ""))
        if tag in {"img", "script"} and values.get("src"):
            self.references.append(("src", values["src"] or ""))
        if tag == "link" and values.get("href"):
            self.references.append(("href", values["href"] or ""))
        if tag == "img" and not (values.get("alt") or "").strip():
            self.images_without_alt.append(values.get("src") or "unknown image")
        if tag == "select" and "data-typeface-picker" in values:
            self.typeface_pickers += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def local_target(current_page: Path, url: str) -> tuple[Path, str] | None:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith(("mailto:", "tel:")):
        return None

    path = unquote(parsed.path)
    if path == "/labs":
        path = "/"
    elif path.startswith("/labs/"):
        path = path[len("/labs") :]

    if path.startswith("/"):
        target = BUILD / path.lstrip("/")
    elif path:
        target = current_page.parent / path
    else:
        target = current_page
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve(), unquote(parsed.fragment)


def check_source(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (SITE_ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    config = (SITE_ROOT / "_config.yml").read_text(encoding="utf-8")
    if 'url: "https://cpen-221.github.io"' not in config:
        fail(errors, "_config.yml must use https://cpen-221.github.io")
    if 'baseurl: "/labs"' not in config:
        fail(errors, "_config.yml must use /labs as its baseurl")
    if (SITE_ROOT / ".github" / "workflows").exists():
        fail(errors, "GitHub Actions workflows are not allowed for branch publishing")

    if "https://cpen-221.github.io/labs/" not in (
        SITE_ROOT / "README.md"
    ).read_text(encoding="utf-8"):
        fail(errors, "README.md does not state the production URL")

    if COURSE_LABS.is_dir():
        for lab in LABS:
            canonical = normalize_markdown(
                (COURSE_LABS / lab.source).read_text(encoding="utf-8")
            )
            published = (PUBLISHED_LABS / lab.source).read_text(encoding="utf-8")
            if published != canonical:
                fail(errors, f"source/2025/{lab.source}: stale public source copy")

    expected_source_files = {lab.source for lab in LABS} | set(IMAGE_ASSETS)
    observed_source_files = {
        str(path.relative_to(PUBLISHED_LABS))
        for path in PUBLISHED_LABS.rglob("*")
        if path.is_file()
    }
    if observed_source_files != expected_source_files:
        fail(errors, "source/2025 contains an unexpected set of public files")
    for path in PUBLISHED_LABS.rglob("*"):
        if path.is_file() and "guide" in path.name.casefold():
            fail(errors, f"teaching-team guide was copied into source/: {path.name}")

    if (SITE_ROOT / "2025" / "index.md").read_text(
        encoding="utf-8"
    ) != render_year_index():
        fail(errors, "2025/index.md is stale; run python3 scripts/import_labs.py")

    for index, lab in enumerate(LABS):
        markdown = normalize_markdown(
            (PUBLISHED_LABS / lab.source).read_text(encoding="utf-8")
        )
        body, sections = transform_body(markdown, lab)
        previous = LABS[index - 1] if index else None
        following = LABS[index + 1] if index + 1 < len(LABS) else None
        digest = sha256(markdown.encode("utf-8")).hexdigest()
        expected = render_lab_page(
            lab, body, sections, previous, following, digest
        )
        target = SITE_ROOT / "2025" / lab.slug / "index.html"
        if not target.is_file():
            fail(errors, f"missing generated page: 2025/{lab.slug}/index.html")
        elif target.read_text(encoding="utf-8") != expected:
            fail(
                errors,
                f"2025/{lab.slug}/index.html is stale; run python3 scripts/import_labs.py",
            )

    expected_slugs = {lab.slug for lab in LABS}
    observed_slugs = {
        path.parent.name for path in (SITE_ROOT / "2025").glob("*/index.html")
    }
    if observed_slugs != expected_slugs:
        fail(errors, "2025/ contains an unexpected set of generated lab pages")

    expected_images = {public_name for public_name, _ in IMAGE_ASSETS.values()}
    observed_images = {path.name for path in IMAGE_ROOT.iterdir() if path.is_file()}
    if observed_images != expected_images:
        fail(errors, "assets/images/2025 contains an unexpected set of images")
    for source_name, (public_name, _) in IMAGE_ASSETS.items():
        source = PUBLISHED_LABS / source_name
        target = IMAGE_ROOT / public_name
        if not source.is_file() or not target.is_file() or source.read_bytes() != target.read_bytes():
            fail(errors, f"assets/images/2025/{public_name}: stale or missing image")

    layout = (SITE_ROOT / "_layouts" / "default.html").read_text(encoding="utf-8")
    for required in (
        "data-typeface-picker",
        "lab-source-sha256",
        "relative_url",
        "https://cpen-221.github.io/textbook/",
        "https://cpen-221.github.io/fall2026/",
    ):
        if required not in layout:
            fail(errors, f"layout is missing {required}")

    css = (SITE_ROOT / "assets" / "css" / "main.scss").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        fail(errors, "stylesheet braces are unbalanced")
    for choice in TYPEFACE_CHOICES:
        if f'html[data-typeface="{choice}"]' not in css:
            fail(errors, f"stylesheet is missing the {choice} typeface mapping")

    font_css = (SITE_ROOT / "assets" / "fonts" / "fonts.css").read_text(
        encoding="utf-8"
    )
    if re.search(r"(?:@import|https?://)", font_css):
        fail(errors, "font stylesheet must use only self-hosted assets")
    for value in re.findall(r"url\((?:['\"])?([^)'\"]+)", font_css):
        if not (SITE_ROOT / "assets" / "fonts" / value).is_file():
            fail(errors, f"missing font referenced by fonts.css: {value}")


def check_build(errors: list[str]) -> None:
    if not BUILD.exists():
        print("Build directory not present; skipped rendered-site checks.")
        return

    html_files = sorted(BUILD.rglob("*.html"))
    parsed_pages: dict[Path, PageParser] = {}
    for page in html_files:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed_pages[page.resolve()] = parser

    expected_pages = {
        (BUILD / "index.html").resolve(),
        (BUILD / "404.html").resolve(),
        (BUILD / "2025" / "index.html").resolve(),
        *{
            (BUILD / "2025" / lab.slug / "index.html").resolve()
            for lab in LABS
        },
    }
    missing_pages = expected_pages - set(parsed_pages)
    for page in sorted(missing_pages):
        fail(errors, f"built page is missing: {page.relative_to(BUILD.resolve())}")
    unexpected_pages = set(parsed_pages) - expected_pages
    for page in sorted(unexpected_pages):
        fail(errors, f"unexpected built page: {page.relative_to(BUILD.resolve())}")

    for page, parser in parsed_pages.items():
        display = page.relative_to(BUILD.resolve())
        if parser.language != "en-CA":
            fail(errors, f'{display}: expected lang="en-CA"')
        missing_landmarks = {"header", "nav", "main", "footer"} - parser.landmarks
        if missing_landmarks:
            fail(errors, f"{display}: missing landmarks: {', '.join(sorted(missing_landmarks))}")
        if parser.typeface_pickers != 1:
            fail(errors, f"{display}: expected one reading-type selector")
        if not "".join(parser.title_parts).strip():
            fail(errors, f"{display}: missing page title")
        for identifier in parser.duplicate_ids:
            fail(errors, f"{display}: duplicate id #{identifier}")
        for image in parser.images_without_alt:
            fail(errors, f"{display}: image has empty alt text: {image}")

        source = page.read_text(encoding="utf-8")
        choices = set(re.findall(r'<option value="([^"]+)">', source))
        if choices != TYPEFACE_CHOICES:
            fail(errors, f"{display}: reading-type choices do not match the contract")

        for attribute, url in parser.references:
            local = local_target(page, url)
            if local is None:
                continue
            target, fragment = local
            if not target.exists():
                fail(errors, f"{display}: broken local {attribute} {url}")
                continue
            if fragment and target.suffix == ".html":
                target_parser = parsed_pages.get(target)
                if target_parser and fragment not in target_parser.ids:
                    fail(errors, f"{display}: missing fragment #{fragment} in {url}")


def main() -> int:
    errors: list[str] = []
    check_source(errors)
    check_build(errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"Validated {len(LABS)} public lab pages, source fidelity, local assets, "
        "navigation, and branch-publishing configuration."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
