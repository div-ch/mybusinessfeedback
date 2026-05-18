#!/usr/bin/env python3
"""Generate llms.txt, llms-full.txt, and per-page .md sidecars.

This site is pure static HTML committed to the repo root and served by
Cloudflare Pages with no build command. The generated files must be
committed for Cloudflare to serve them; the GitHub Action in
.github/workflows/llms.yml regenerates and commits them on push to main.
Run it locally with: python3 scripts/generate_llms.py

The script self-bootstraps its Python dependencies into scripts/.venv
because the system Python is externally managed (PEP 668). In CI the
dependencies are pip-installed directly so the bootstrap is skipped.

Two site-specific protections:

1. Pages under robots.txt Disallow paths (private client funnels) are
   never processed, so the AI layer only exposes public pages.

2. A forbidden-phrase gate runs after markdown generation and before any
   file is written. mybusinessfeedback.com public positioning must never
   reference review gating, score protection, suppressing or filtering
   negative reviews, or routing unhappy customers away. If any generated
   markdown matches, the script prints the offending source files and
   exits non-zero without writing anything.
"""

import os
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
VENV = SCRIPTS / ".venv"
REQ = SCRIPTS / "requirements.txt"

SITE = "https://mybusinessfeedback.com"


def _venv_python() -> pathlib.Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def _ensure_deps() -> None:
    """Import deps, bootstrapping a venv on first run if they are missing."""
    try:
        import bs4  # noqa: F401
        import markdownify  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    if os.environ.get("LLMS_BOOTSTRAPPED") == "1":
        sys.stderr.write(
            "ERROR: markdownify/beautifulsoup4 still unavailable after bootstrap.\n"
            "Install them with: pip install -r scripts/requirements.txt\n"
        )
        sys.exit(1)

    vpy = _venv_python()
    if not vpy.exists():
        sys.stderr.write("Creating scripts/.venv for generate_llms.py dependencies...\n")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)])
        subprocess.check_call(
            [str(vpy), "-m", "pip", "install", "--quiet", "--upgrade", "pip"]
        )
    subprocess.check_call(
        [str(vpy), "-m", "pip", "install", "--quiet", "-r", str(REQ)]
    )
    env = dict(os.environ, LLMS_BOOTSTRAPPED="1")
    os.execve(str(vpy), [str(vpy), __file__, *sys.argv[1:]], env)


_ensure_deps()

import json  # noqa: E402

from bs4 import BeautifulSoup  # noqa: E402
from markdownify import markdownify as html_to_md  # noqa: E402

# Directories never walked for source HTML. Robots.txt Disallow directories
# are added to this set at runtime so private client funnels are excluded.
STATIC_SKIP_DIRS = {".git", "node_modules", ".venv", "scripts", "google-apps-script"}

# Directories whose non-index *.html files are standalone pages. This site's
# blog uses subdirectory index pages, so none are needed.
FLAT_HTML_DIRS: set[str] = set()

# Elements removed from the main content before markdown conversion. These are
# site chrome, navigation, repeated calls to action, and metadata that add no
# value for an AI crawler reading the page body.
STRIP_SELECTORS = [
    "nav",
    "header",
    "footer",
    "aside",
    "script",
    "style",
    "noscript",
    "svg",
    "form",
    "iframe",
    ".cta-section",
    ".cta-band",
    ".cta-band-inner",
    ".cta-box",
    ".cta-trust",
    ".intake-form-section",
    ".publications",
    ".breadcrumb",
    ".article-meta",
    ".site-footer",
    ".nav",
    ".related",
    ".related-articles",
    ".sidebar",
    ".share",
    ".social-share",
    ".newsletter",
]

# llms.txt section taxonomy, most important first.
PRODUCT_ORDER = ["how-it-works", "pricing", "faq"]
COMPANY_ORDER = ["about", "partner-with-us"]
USECASE_PREFIX = "for-"

# Forbidden public-positioning language. mybusinessfeedback.com is framed as a
# customer satisfaction and communication tool, never as review gating or
# negative-review suppression. These run on the generated markdown before any
# file is written; a single hit aborts the run.
FORBIDDEN_PATTERNS = [
    r"review gating|review-gating|gating reviews",
    r"score protection|protect (?:your |the )?(?:google |star )?(?:rating|score|reviews?)",
    r"suppress(?:ing)? (?:negative |bad )?reviews?",
    r"filter(?:ing)? (?:out )?(?:negative |bad )?reviews?",
    r"hide (?:negative |bad )?reviews?",
    r"block (?:negative |bad )?reviews?",
    r"intercept(?:ing)? (?:negative |bad )?(?:feedback|reviews?)",
    r"route (?:unhappy |dissatisfied )?customers? away",
    r"prevent (?:negative |bad )?reviews? (?:from )?(?:reaching|posting|appearing)",
    r"divert (?:negative |bad )?(?:feedback|reviews?)",
]
FORBIDDEN_RE = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PATTERNS]

# Char class: pipe, hyphen, U+2013 en dash, U+2014 em dash. Strips a trailing
# branding segment whichever separator a page title used. Escapes are used so
# this source file contains no literal dash glyph.
_SEP = "[|\\-" + chr(0x2013) + chr(0x2014) + "]"
BRAND_TAIL_RE = re.compile(
    _SEP + r"\s*(?:MyBusinessFeedback|My Business Feedback)\s*$",
    re.IGNORECASE,
)
WS_RE = re.compile(r"\s+")
MULTI_BLANK_RE = re.compile(r"\n{3,}")

# Brand rule: no em dashes and no emoji or decorative icon glyphs in any
# Nexus-family content, including these generated artifacts. The site HTML
# may carry icon glyphs and the odd em dash; they are normalized out of the
# generated markdown. [ \t] (not \s) keeps newlines intact.
_DASH_RE = re.compile("[ \\t]*[\u2013\u2014][ \\t]*")
_BULLET_RE = re.compile("[ \\t]*\u2022[ \\t]*")
# Arrows, misc symbols, dingbats, geometric shapes, astral, VS16.
EMOJI_RE = re.compile(
    "[\u2190-\u21ff\u2300-\u27bf\u2b00-\u2bff\U0001F000-\U0001FAFF\ufe0f]"
)


# Smart punctuation normalized to ASCII so generated output is ASCII clean.
# Keyed by codepoint so this source file stays free of literal glyphs.
_PUNCT_MAP = {
    0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'",
    0x201C: '"', 0x201D: '"', 0x201E: '"', 0x201F: '"',
    0x2032: "'", 0x2033: '"', 0x2026: "...", 0x00A0: " ",
}


def _strip_glyphs(text: str) -> str:
    """Normalize smart punctuation, em/en dash, bullets; drop icon glyphs."""
    text = text.translate(_PUNCT_MAP)
    text = _DASH_RE.sub(" - ", text)
    text = _BULLET_RE.sub(" - ", text)
    return EMOJI_RE.sub("", text)


def _clean_inline(text: str) -> str:
    return WS_RE.sub(" ", _strip_glyphs(text)).strip()


def _robots_skip_dirs() -> set[str]:
    """Top-level directory names under a robots.txt Disallow path."""
    robots = REPO / "robots.txt"
    skip: set[str] = set()
    if not robots.exists():
        return skip
    for line in robots.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip().strip("/")
            if path and "/" not in path:
                skip.add(path)
    return skip


SKIP_DIRS = STATIC_SKIP_DIRS | _robots_skip_dirs()


class Page:
    """A single source HTML page and its extracted content."""

    def __init__(self, html_path: pathlib.Path):
        self.html_path = html_path
        rel = html_path.relative_to(REPO).as_posix()
        if rel == "index.html":
            self.rel_dir = ""  # site root
            self.url = f"{SITE}/"
        elif rel.endswith("/index.html"):
            self.rel_dir = rel[: -len("/index.html")]
            self.url = f"{SITE}/{self.rel_dir}/"
        else:
            # Flat .html page. The canonical URL keeps the .html extension.
            self.rel_dir = rel[: -len(".html")]
            self.url = f"{SITE}/{rel}"

        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        self.title = self._extract_title(soup)
        self.description = self._extract_description(soup)
        self.date = self._extract_date(soup)
        self.link_title = self._extract_h1(soup) or self.title
        self.body_md = self._extract_body(soup)
        self.kind = self._classify()

    # --- extraction helpers -------------------------------------------------

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        if not soup.title:
            return ""
        raw = WS_RE.sub(" ", soup.title.get_text()).strip()
        # Drop a trailing site-branding segment, then any residual pipe tail
        # (titles read "Primary | Secondary"; keep the primary).
        cleaned = BRAND_TAIL_RE.sub("", raw).strip()
        return _clean_inline(cleaned.split(" | ")[0])

    @staticmethod
    def _extract_description(soup: BeautifulSoup) -> str:
        tag = soup.find("meta", attrs={"name": "description"})
        if tag and tag.get("content"):
            return _clean_inline(tag["content"])
        return ""

    @staticmethod
    def _extract_h1(soup: BeautifulSoup) -> str:
        main = soup.find("main") or soup
        h1 = main.find("h1")
        if h1:
            return _clean_inline(h1.get_text(" ", strip=True))
        return ""

    @staticmethod
    def _extract_date(soup: BeautifulSoup) -> str:
        # Prefer JSON-LD datePublished, then article:published_time.
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            raw = script.string or script.get_text()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except (ValueError, TypeError):
                continue
            for node in _iter_jsonld(data):
                if isinstance(node, dict) and node.get("datePublished"):
                    return str(node["datePublished"])[:10]
        tag = soup.find("meta", attrs={"property": "article:published_time"})
        if tag and tag.get("content"):
            return str(tag["content"])[:10]
        return ""

    def _extract_body(self, soup: BeautifulSoup) -> str:
        main = soup.find("main") or soup.find("article") or soup.body
        if main is None:
            return ""
        for selector in STRIP_SELECTORS:
            if selector.startswith("."):
                cls = selector[1:]
                for el in main.select(f'[class~="{cls}"]'):
                    el.decompose()
            else:
                for el in main.find_all(selector):
                    el.decompose()
        # The page title is re-added as the markdown H1, so drop in-body H1s
        # to avoid a duplicate heading.
        for el in main.find_all("h1"):
            el.decompose()

        markdown = html_to_md(
            str(main),
            heading_style="ATX",
            bullets="-",
            escape_asterisks=False,
            escape_underscores=False,
            escape_misc=False,
        )
        return _clean_markdown(markdown)

    def _classify(self) -> str:
        parts = [p for p in self.rel_dir.split("/") if p]
        if not parts:
            return "home"
        seg = parts[0]
        if seg == "blog":
            return "blog-index" if len(parts) == 1 else "blog"
        if seg == "locations":
            return "locations-index" if len(parts) == 1 else "locations"
        if seg.startswith(USECASE_PREFIX):
            return "usecases"
        if seg in PRODUCT_ORDER:
            return "product"
        if seg in COMPANY_ORDER:
            return "company"
        return "company"

    # --- derived values -----------------------------------------------------

    @property
    def slug(self) -> str:
        parts = [p for p in self.rel_dir.split("/") if p]
        return parts[-1] if parts else ""

    @property
    def label(self) -> str:
        """Concise link label for llms.txt: title, then H1, then slug."""
        return self.title or self.link_title or self.slug

    @property
    def summary(self) -> str:
        text = self.description
        if not text:
            # Fall back to the first sentence of the body.
            plain = re.sub(r"[#>*_`\[\]()-]", " ", self.body_md)
            plain = WS_RE.sub(" ", plain).strip()
            text = plain.split(". ")[0]
        text = WS_RE.sub(" ", text).strip()
        if len(text) > 220:
            text = text[:217].rsplit(" ", 1)[0] + "..."
        return text

    def sidecar_paths(self) -> list[pathlib.Path]:
        """Return every .md path this page should be written to."""
        if not self.rel_dir:  # root index.html
            return [REPO / "index.md"]
        return [
            REPO / f"{self.rel_dir}.md",
            REPO / self.rel_dir / "index.md",
        ]

    def sidecar_markdown(self) -> str:
        head = f"# {self.label}\n"
        if self.description:
            head += f"\n> {self.description}\n"
        return f"{head}\n{self.body_md}\n"

    def full_entry(self) -> str:
        return f"# {self.label}\nURL: {self.url}\n\n{self.body_md}\n\n---\n"

    def shippable_text(self) -> str:
        """All text that would be written for this page (for the gate)."""
        return "\n".join([self.label, self.description, self.summary, self.body_md])


def _iter_jsonld(data):
    """Yield every dict node from a JSON-LD blob (handles @graph and lists)."""
    if isinstance(data, dict):
        if "@graph" in data and isinstance(data["@graph"], list):
            for item in data["@graph"]:
                yield from _iter_jsonld(item)
        yield data
    elif isinstance(data, list):
        for item in data:
            yield from _iter_jsonld(item)


def _clean_markdown(markdown: str) -> str:
    # Absolutize root-relative links and images for AI ingestion.
    markdown = re.sub(r"\]\(/(?!/)", f"]({SITE}/", markdown)
    # Brand: drop em dashes and icon/emoji glyphs (newlines preserved).
    markdown = _strip_glyphs(markdown)
    # Collapse intra-line double spaces left by glyph removal while keeping
    # markdown list indentation and blank lines intact.
    lines = []
    for line in markdown.splitlines():
        body = line.lstrip(" \t")
        indent = line[: len(line) - len(body)]
        lines.append((indent + re.sub(r"[ \t]{2,}", " ", body)).rstrip())
    markdown = MULTI_BLANK_RE.sub("\n\n", "\n".join(lines))
    return markdown.strip()


def discover_pages() -> list[Page]:
    pages: list[Page] = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        rel_root = os.path.relpath(root, REPO)
        rel_root = "" if rel_root == "." else rel_root.replace(os.sep, "/")
        if "index.html" in files:
            pages.append(Page(pathlib.Path(root) / "index.html"))
        if rel_root in FLAT_HTML_DIRS:
            for name in sorted(files):
                if name.endswith(".html") and name != "index.html":
                    pages.append(Page(pathlib.Path(root) / name))
    return pages


def scan_forbidden(pages: list[Page]) -> list[tuple]:
    """Return (html_path, matched, pattern, context) for every forbidden hit."""
    violations: list[tuple] = []
    for page in pages:
        text = page.shippable_text()
        for rx in FORBIDDEN_RE:
            for m in rx.finditer(text):
                start = max(0, m.start() - 80)
                end = min(len(text), m.end() + 80)
                context = " ".join(text[start:end].split())
                violations.append((page.html_path, m.group(0), rx.pattern, context))
    return violations


def write_sidecars(pages: list[Page]) -> int:
    count = 0
    for page in pages:
        content = page.sidecar_markdown()
        for path in page.sidecar_paths():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            count += 1
    return count


def build_llms_txt(pages: list[Page]) -> str:
    by_kind: dict[str, list[Page]] = {}
    for page in pages:
        by_kind.setdefault(page.kind, []).append(page)

    home = next((p for p in pages if p.kind == "home"), None)
    tagline = (
        home.description
        if home and home.description
        else "A simple, thoughtful way for businesses to hear from their customers after every service."
    )

    lines = [
        "# MyBusinessFeedback",
        f"> {tagline}",
        "",
    ]

    def emit(heading: str, items: list[Page]) -> None:
        if not items:
            return
        lines.append(f"## {heading}")
        for page in items:
            lines.append(f"- [{page.label}]({page.url}): {page.summary}")
        lines.append("")

    def ordered(kind: str, order: list[str]) -> list[Page]:
        items = by_kind.get(kind, [])
        return sorted(
            items,
            key=lambda p: (
                order.index(p.slug) if p.slug in order else len(order),
                p.label.lower(),
            ),
        )

    emit("Product", ordered("product", PRODUCT_ORDER))
    emit(
        "Use cases",
        sorted(by_kind.get("usecases", []), key=lambda p: p.label.lower()),
    )
    emit(
        "Locations",
        sorted(by_kind.get("locations", []), key=lambda p: p.url),
    )
    emit("Company", ordered("company", COMPANY_ORDER))
    emit(
        "Blog",
        sorted(
            by_kind.get("blog", []),
            key=lambda p: (p.date or "0000-00-00", p.label),
            reverse=True,
        ),
    )

    return "\n".join(lines).rstrip() + "\n"


def build_llms_full_txt(pages: list[Page]) -> str:
    order = {
        "home": 0,
        "product": 1,
        "usecases": 2,
        "locations-index": 3,
        "locations": 4,
        "company": 5,
        "blog-index": 6,
        "blog": 7,
    }

    def sort_key(page: Page):
        if page.kind == "blog":
            return (order.get(page.kind, 99), "", _neg_date(page.date), page.label)
        return (order.get(page.kind, 99), page.url, "", "")

    ordered = sorted(pages, key=sort_key)
    header = (
        "# MyBusinessFeedback: full content export\n"
        f"URL: {SITE}/\n\n"
        "Every public page in one file for AI retrieval. Sections are divided "
        "by a horizontal rule.\n\n---\n"
    )
    return header + "".join(page.full_entry() for page in ordered)


def _neg_date(date: str) -> str:
    """Sort newer dates first inside an ascending sort."""
    if not date or not re.match(r"\d{4}-\d{2}-\d{2}", date):
        return "9999-99-99"
    y, m, d = date[:10].split("-")
    return f"{9999 - int(y):04d}-{99 - int(m):02d}-{99 - int(d):02d}"


HEADERS_BEGIN = "# === llms / markdown sidecars (managed by scripts/generate_llms.py) ==="
HEADERS_END = "# === end llms ==="
HEADERS_BLOCK = f"""{HEADERS_BEGIN}
/*.md
  Content-Type: text/markdown; charset=utf-8
  X-Robots-Tag: index, follow

/llms.txt
  Content-Type: text/markdown; charset=utf-8

/llms-full.txt
  Content-Type: text/markdown; charset=utf-8
{HEADERS_END}"""


def update_headers() -> None:
    path = REPO / "_headers"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if HEADERS_BEGIN in existing and HEADERS_END in existing:
        pattern = re.compile(
            re.escape(HEADERS_BEGIN) + r".*?" + re.escape(HEADERS_END), re.DOTALL
        )
        updated = pattern.sub(HEADERS_BLOCK, existing)
    else:
        sep = "" if existing.endswith("\n\n") or not existing else (
            "\n" if existing.endswith("\n") else "\n\n"
        )
        updated = existing + sep + "\n" + HEADERS_BLOCK + "\n"
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    pages = discover_pages()
    if not pages:
        sys.stderr.write("No pages found.\n")
        sys.exit(1)

    violations = scan_forbidden(pages)
    if violations:
        sys.stderr.write(
            "\nERROR: forbidden public-positioning language detected in "
            f"{len(violations)} place(s). No output files were written.\n"
            "mybusinessfeedback.com must be framed as a customer satisfaction "
            "and communication tool, never as review gating or negative-review "
            "suppression.\n"
        )
        for html_path, matched, pattern, context in violations:
            rel = html_path.relative_to(REPO)
            sys.stderr.write(
                f"\n  FILE:    {rel}\n"
                f"  MATCH:   {matched!r}\n"
                f"  PATTERN: {pattern}\n"
                f"  CONTEXT: ...{context}...\n"
            )
        sys.stderr.write(
            "\nFix the source HTML in the files listed above so the public "
            "copy reflects customer satisfaction and communication framing, "
            "then re-run scripts/generate_llms.py.\n"
        )
        sys.exit(1)

    sidecar_count = write_sidecars(pages)
    (REPO / "llms.txt").write_text(build_llms_txt(pages), encoding="utf-8")
    (REPO / "llms-full.txt").write_text(build_llms_full_txt(pages), encoding="utf-8")
    update_headers()

    print(
        f"Forbidden-phrase gate passed. Processed {len(pages)} pages -> "
        f"{sidecar_count} .md sidecars, llms.txt, llms-full.txt, _headers updated."
    )


if __name__ == "__main__":
    main()
