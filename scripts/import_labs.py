#!/usr/bin/env python3
"""Import the public 2025 labs into the standalone Jekyll site."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from html import escape, unescape
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit


SITE_ROOT = Path(__file__).resolve().parents[1]
COURSE_LABS = SITE_ROOT.parent / "2025"
PUBLISHED_LABS = SITE_ROOT / "source" / "2025"
YEAR_ROOT = SITE_ROOT / "2025"
IMAGE_ROOT = SITE_ROOT / "assets" / "images" / "2025"
PANDOC_VERSION = "3.10"


@dataclass(frozen=True)
class Lab:
    source: str
    slug: str
    number: str
    title: str
    description: str


LABS = (
    Lab(
        "Lab 0: String Chopping.md",
        "string-chopping",
        "0",
        "String Chopping",
        "Develop an algorithm that isolates letters by repeatedly removing parts of a string.",
    ),
    Lab(
        "Lab 1: Problem Solving.md",
        "problem-solving",
        "1",
        "Problem Solving",
        "Practise iteration and problem decomposition with three short programming tasks.",
    ),
    Lab(
        "Lab 2: Datatypes and DNA.md",
        "datatypes-and-dna",
        "2",
        "Datatypes and DNA",
        "Implement a Java datatype for DNA sequences, codons, mass, and mutation.",
    ),
    Lab(
        "Lab 3: DNA Cut-and-Splice.md",
        "dna-cut-and-splice",
        "3",
        "DNA Cut-and-Splice",
        "Debug a provided DNA implementation and add a cut-and-splice operation.",
    ),
    Lab(
        "Lab 4: Abstract Algebra.md",
        "abstract-algebra",
        "4",
        "Abstract Algebra",
        "Implement and test operations that determine whether a finite table defines a group.",
    ),
    Lab(
        "Lab 5: ADTs (The JobManager) .md",
        "adts-and-job-manager",
        "5",
        "ADTs and the JobManager",
        "Design and implement an abstract data type for assigning jobs to robots.",
    ),
    Lab(
        "Lab 6: Representation Invariants (featuring JobManager) .md",
        "representation-invariants-and-job-manager",
        "6",
        "Representation Invariants and the JobManager",
        "State and check a representation invariant, then use it to locate implementation bugs.",
    ),
    Lab(
        "Lab 7: Interfaces + Subtypes + Rep Invariants.md",
        "interfaces-subtypes-and-representation-invariants",
        "7",
        "Interfaces, Subtypes, and Representation Invariants",
        "Extend the JobManager with robot subtypes, scheduling policies, records, and comparators.",
    ),
    Lab(
        "Lab 8: Streams and Lambdas.md",
        "streams-and-lambdas",
        "8",
        "Streams and Lambdas",
        "Use stream pipelines, optional values, lambdas, and functional interfaces.",
    ),
    Lab(
        "Lab 9: Evaluating Arithmetic Expressions.md",
        "evaluating-arithmetic-expressions",
        "9",
        "Evaluating Arithmetic Expressions",
        "Build infix and postfix evaluators and practise running and packaging Java applications.",
    ),
    Lab(
        "Lab 10: Client-Server Pattern and Text Document Processing.md",
        "client-server-and-text-processing",
        "10",
        "Client-Server Pattern and Text Processing",
        "Compute document metrics through a JSON client-server protocol and examine concurrency.",
    ),
    Lab(
        "Lab 11: Stable Marriages, Shared Memory and Concurrency.md",
        "stable-matching-and-concurrency",
        "11",
        "Stable Matching, Shared Memory, and Concurrency",
        "Complete a concurrent stable-matching implementation and reason about shared state.",
    ),
    Lab(
        "Programming Practice.md",
        "programming-practice",
        "+",
        "Programming Practice",
        "Links to the short programming exercises used alongside the 2025 labs.",
    ),
)


# The stable public filename avoids spaces and export-tool suffixes in published URLs.
IMAGE_ASSETS = {
    "Lab 2: Datatypes and DNA.assets/SEO-DNA-Images-Codons-2019-01-09-12-12-20.jpeg": (
        "dna-codons.jpeg",
        "A DNA sequence grouped into codons, its corresponding RNA codons, and the amino acids in the resulting protein chain.",
    ),
    "Lab 3: DNA Cut-and-Splice.assets/Image.png": (
        "ecori-cut-site.png",
        "A DNA strand containing the EcoRI recognition sequence GAATTC, shown intact and cut between G and A.",
    ),
    "Lab 3: DNA Cut-and-Splice.assets/Image (2).png": (
        "dna-fragments-and-insert.png",
        "Two cut DNA fragments with complementary ends aligned to a DNA segment that will be inserted between them.",
    ),
    "Lab 3: DNA Cut-and-Splice.assets/Image (3).png": (
        "recombined-dna.png",
        "The recombined DNA strand after the inserted segment joins the two original fragments.",
    ),
    "Lab 9: Evaluating Arithmetic Expressions.assets/AST-JavaExample.png": (
        "java-abstract-syntax-tree.png",
        "An abstract syntax tree for three Java assignments, ending with result equal to b times the difference a minus b, plus a.",
    ),
    "Lab 10: Client-Server Pattern and Text Document Processing.assets/Image.png": (
        "docker-build-and-run.png",
        "A Dockerfile is built into a Docker image, which is then run as a Docker container.",
    ),
}


def source_root() -> Path:
    if all((COURSE_LABS / lab.source).is_file() for lab in LABS):
        return COURSE_LABS
    if all((PUBLISHED_LABS / lab.source).is_file() for lab in LABS):
        return PUBLISHED_LABS
    raise SystemExit("Cannot find the complete public 2025 lab source set")


def require_pandoc() -> None:
    try:
        result = subprocess.run(
            ["pandoc", "--version"], text=True, capture_output=True, check=True
        )
    except FileNotFoundError as error:
        raise SystemExit(f"Pandoc {PANDOC_VERSION} is required") from error
    observed = result.stdout.splitlines()[0]
    if observed != f"pandoc {PANDOC_VERSION}":
        raise SystemExit(
            f"The lab importer is pinned to pandoc {PANDOC_VERSION}; observed {observed}"
        )


def normalize_markdown(markdown: str) -> str:
    """Remove export-only trailing spaces without changing the canonical archive."""
    return "\n".join(line.rstrip() for line in markdown.splitlines()) + "\n"


def sync_public_sources(sources: Path) -> None:
    if sources == PUBLISHED_LABS:
        return
    if PUBLISHED_LABS.exists():
        shutil.rmtree(PUBLISHED_LABS)
    PUBLISHED_LABS.mkdir(parents=True)
    for lab in LABS:
        markdown = (sources / lab.source).read_text(encoding="utf-8")
        (PUBLISHED_LABS / lab.source).write_text(
            normalize_markdown(markdown), encoding="utf-8"
        )
    for source_name in IMAGE_ASSETS:
        target = PUBLISHED_LABS / source_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sources / source_name, target)


def sync_public_images(sources: Path) -> None:
    if IMAGE_ROOT.exists():
        shutil.rmtree(IMAGE_ROOT)
    IMAGE_ROOT.mkdir(parents=True)
    for source_name, (public_name, _) in IMAGE_ASSETS.items():
        shutil.copy2(sources / source_name, IMAGE_ROOT / public_name)


def rewrite_images(markdown: str) -> str:
    pattern = re.compile(r"!\[([^]]*)\]\((.+?\.(?:png|jpe?g|gif|svg))\)", re.I)

    def replace(match: re.Match[str]) -> str:
        parsed = urlsplit(match.group(2))
        if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
            return match.group(0)
        source_name = unquote(parsed.path)
        image = IMAGE_ASSETS.get(source_name)
        if image is None:
            return match.group(0)
        public_name, alt = image
        return (
            '<figure class="lab-figure">'
            f'<img src="../../assets/images/2025/{escape(public_name)}" '
            f'alt="{escape(alt)}" loading="lazy">'
            f"<figcaption>{escape(alt)}</figcaption>"
            "</figure>"
        )

    return pattern.sub(replace, markdown)


def run_pandoc(markdown: str) -> str:
    result = subprocess.run(
        [
            "pandoc",
            "--from=gfm+tex_math_dollars+raw_html",
            "--to=html5",
            "--mathml",
            "--wrap=none",
            "--syntax-highlighting=none",
        ],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def plain_text(value: str) -> str:
    return unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", value))).strip()


def transform_body(markdown: str, lab: Lab) -> tuple[str, list[tuple[str, str]]]:
    body_markdown = markdown.split("\n", 1)[1].lstrip()
    if lab.number == "0":
        body_markdown = body_markdown.replace("### Overview", "## Overview", 1)
    if lab.number == "1":
        body_markdown = body_markdown.replace("$d $", "$d$")

    body = run_pandoc(rewrite_images(body_markdown))
    body = re.sub(r"<h1(\s[^>]*)?>", r"<h2\1>", body)
    body = body.replace("</h1>", "</h2>")
    body = re.sub(r'<img(?![^>]*\bloading=)(\s)', r'<img loading="lazy"\1', body)

    sections: list[tuple[str, str]] = []
    for identifier, title in re.findall(
        r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.DOTALL
    ):
        sections.append((identifier, plain_text(title)))
    return body, sections


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_lab_page(
    lab: Lab,
    body: str,
    sections: list[tuple[str, str]],
    previous: Lab | None,
    following: Lab | None,
    digest: str,
) -> str:
    title = f"Lab {lab.number}: {lab.title}" if lab.number != "+" else lab.title
    lines = [
        "---",
        "layout: default",
        f"title: {quoted(title)}",
        f"description: {quoted(lab.description)}",
        f"hero_title: {quoted(title)}",
        'eyebrow: "CPEN 221A · 2025 lab archive"',
        'term: "2025 archive"',
        'page_kind: "lab"',
        f"lab_number: {quoted(lab.number)}",
        f"permalink: {quoted('/2025/' + lab.slug + '/')}",
        f"source_file: {quoted(lab.source)}",
        f"source_sha256: {quoted(digest)}",
        'mobile_toc_label: "Jump to a lab section"',
    ]
    if previous:
        lines.append(f"previous_slug: {quoted(previous.slug)}")
    if following:
        lines.append(f"next_slug: {quoted(following.slug)}")
    lines.append("sections:")
    for identifier, section_title in sections:
        lines.extend(
            (f"  - id: {quoted(identifier)}", f"    title: {quoted(section_title)}")
        )
    lines.extend(
        (
            "---",
            "",
            '<aside class="archive-note" aria-label="Archive status">',
            "  <strong>Archived activity.</strong> This page preserves the 2025 lab.",
            "  Submission instructions, starter repositories, and external links may have changed.",
            "</aside>",
            "",
            body,
            "",
        )
    )
    return "\n".join(lines)


def render_year_index() -> str:
    items = []
    for lab in LABS:
        label = f"Lab {lab.number}" if lab.number != "+" else "+"
        items.append(
            '<li class="lab-card">'
            f'<span class="lab-card-number">{escape(label)}</span>'
            "<div>"
            f'<h2><a href="{escape(lab.slug)}/">{escape(lab.title)}</a></h2>'
            f"<p>{escape(lab.description)}</p>"
            "</div></li>"
        )
    return "\n".join(
        (
            "---",
            "layout: default",
            'title: "2025 laboratory activities"',
            'description: "Archived CPEN 221 laboratory activities from 2025."',
            'hero_title: "2025 Laboratory Activities"',
            'eyebrow: "CPEN 221A · Laboratory archive"',
            'term: "2025 archive"',
            'permalink: "/2025/"',
            'page_kind: "year"',
            'mobile_toc_label: "Jump to the archive"',
            "sections:",
            '  - id: "lab-list"',
            '    title: "Laboratory activities"',
            "---",
            "",
            '<aside class="archive-note" aria-label="Archive status">',
            "  <strong>Archived material.</strong> These activities preserve the 2025 offering.",
            "  Submission instructions, starter repositories, and external links may have changed.",
            "</aside>",
            "",
            '<section id="lab-list" aria-labelledby="lab-list-heading">',
            '  <h1 id="lab-list-heading">Laboratory activities</h1>',
            '  <ol class="lab-grid">',
            *items,
            "  </ol>",
            "</section>",
            "",
        )
    )


def build() -> None:
    require_pandoc()
    canonical_sources = source_root()
    sync_public_sources(canonical_sources)
    sources = PUBLISHED_LABS
    sync_public_images(sources)

    if YEAR_ROOT.exists():
        shutil.rmtree(YEAR_ROOT)
    YEAR_ROOT.mkdir()
    (YEAR_ROOT / "index.md").write_text(render_year_index(), encoding="utf-8")

    for index, lab in enumerate(LABS):
        markdown = normalize_markdown(
            (sources / lab.source).read_text(encoding="utf-8")
        )
        body, sections = transform_body(markdown, lab)
        target = YEAR_ROOT / lab.slug
        target.mkdir()
        previous = LABS[index - 1] if index else None
        following = LABS[index + 1] if index + 1 < len(LABS) else None
        digest = sha256(markdown.encode("utf-8")).hexdigest()
        (target / "index.html").write_text(
            render_lab_page(lab, body, sections, previous, following, digest),
            encoding="utf-8",
        )

    print(f"Imported {len(LABS)} public pages into the 2025 lab archive.")


if __name__ == "__main__":
    build()
