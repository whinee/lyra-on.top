"""
src/api/config/content_loader.py - Content loading, parsing, and validation engine.

Loads YAML and Markdown content, validates against Pydantic models,
enforces auto-hide rules, and provides human-readable errors.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml
from markdown_it import MarkdownIt
from pydantic import ValidationError
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

from src.api.models.content import Post, Project, Resume, Site, Talk


@dataclass
class ContentError:
    file_path: str
    field: str
    issue: str
    fix: str

    def __str__(self) -> str:
        return (
            f"FILE:  {self.file_path}\n"
            f"FIELD: {self.field}\n"
            f"ISSUE: {self.issue}\n"
            f"FIX:   {self.fix}"
        )


def _highlight_code(code: str, lang: str | None, attrs: Any) -> str:
    """Highlight code snippets using Pygments."""
    try:
        lexer = get_lexer_by_name(lang) if lang else TextLexer()
    except Exception:  # noqa: BLE001
        lexer = TextLexer()
    formatter = HtmlFormatter(nowrap=True)
    return highlight(code, lexer, formatter)


def get_markdown_renderer(content_type: str = "blog") -> MarkdownIt:
    """Return configured markdown-it-py renderer with pygments and HTML passthrough OFF."""
    options: dict[str, Any] = {
        "html": False,  # HTML passthrough strictly OFF
        "highlight": _highlight_code,
    }
    if content_type == "poem":
        options["breaks"] = True  # Preserved line breaks for poems
    return MarkdownIt("commonmark", options)


def parse_markdown_with_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract frontmatter and body from markdown content."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].lstrip("\r\n")
            data = yaml.safe_load(fm_text)
            return (data if isinstance(data, dict) else {}), body
    return {}, text


def suggest_fix(field: str, err_msg: str, file_name: str) -> str:
    """Generate human-readable fix suggestion."""
    if "repo_url" in field:
        return "Must be a valid GitHub URL starting with 'https://github.com/'"
    if "summary" in field and "at most 200" in err_msg:
        return "Shorten summary to 200 characters or fewer"
    if "cover_alt" in field:
        return "Provide descriptive cover_alt text when cover image is specified"
    if "visibility" in field:
        return "Set visibility to either 'public' or 'private'"
    return f"Correct '{field}' in {file_name}: {err_msg}"


@dataclass
class ContentCatalog:
    site: Site
    projects: list[Project]
    resume: Resume
    talks: list[Talk]
    blog: list[Post]
    poems: list[Post]
    song_analysis: list[Post]
    legacy_content: dict[str, Any]

    @property
    def public_projects(self) -> list[Project]:
        return [p for p in self.projects if p.visibility == "public"]

    @property
    def public_blog(self) -> list[Post]:
        return [p for p in self.blog if not p.draft]

    @property
    def public_poems(self) -> list[Post]:
        return [p for p in self.poems if not p.draft]

    @property
    def public_song_analysis(self) -> list[Post]:
        return [p for p in self.song_analysis if not p.draft]

    @property
    def public_talks(self) -> list[Talk]:
        return self.talks

    # Auto-Hide rule evaluations
    @property
    def has_projects(self) -> bool:
        return len(self.public_projects) > 0

    @property
    def has_blog(self) -> bool:
        return len(self.public_blog) > 0

    @property
    def has_poems(self) -> bool:
        return len(self.public_poems) > 0

    @property
    def has_song_analysis(self) -> bool:
        return len(self.public_song_analysis) > 0

    @property
    def has_writing(self) -> bool:
        return self.has_poems or self.has_song_analysis or self.has_blog

    @property
    def has_talks(self) -> bool:
        return len(self.public_talks) > 0

    @property
    def active_nav(self) -> list[dict[str, str]]:
        """Return active nav links honoring the Auto-Hide rule."""
        checks = {
            "projects": self.has_projects,
            "writing": self.has_writing,
            "blog": self.has_blog,
            "resume": True,
            "contacts": True,
            "talks": self.has_talks,
        }
        labels = {
            "projects": "Projects",
            "writing": "Writing",
            "blog": "Blog",
            "resume": "Resume",
            "contacts": "Contacts",
            "talks": "Talks",
        }
        return [
            {"slug": k, "label": labels[k], "href": f"/{k}"}
            for k in self.site.nav
            if checks.get(k, False)
        ]

    def render_post_html(self, post: Post) -> str:
        """Render post body to HTML with signature styling and poem line-preservation."""
        md = get_markdown_renderer(post.content_type)
        html = md.render(post.body)

        # Style signature intro & outro without modifying text
        intro = self.site.blog_signature_intro.strip()
        outro = self.site.blog_signature_outro.strip()

        if intro and intro in html:
            html = html.replace(
                f"<p>{intro}</p>",
                f'<aside class="blog-signature-intro" aria-label="Greeting">'
                f'<span class="bubble-sparkle">✧</span> {intro} <span class="bubble-sparkle">✧</span>'
                f"</aside>",
                1,
            )

        if outro and outro in html:
            html = html.replace(
                f"<p>{outro}</p>",
                f'<aside class="blog-signature-outro" aria-label="Sign-off">'
                f'<span class="paw-icon">🐾</span> {outro}'
                f"</aside>",
                1,
            )

        if post.content_type == "poem":
            html = f'<div class="poem-wrapper">{html}</div>'

        return html

    def to_template_context(self) -> dict[str, Any]:
        """Convert into a dictionary suitable for Jinja template context."""
        ctx = dict(self.legacy_content)
        ctx.update({
            "site": self.site,
            "meta": {
                "title": self.site.title,
                "description": self.site.description,
                "canonical_url": self.site.url,
                "og_image": self.legacy_content.get("meta", {}).get(
                    "og_image", "/static/assets/images/meta/og-card.png",
                ),
            },
            "active_nav": self.active_nav,
            "projects": self.public_projects,
            "resume": self.resume,
            "talks": self.public_talks,
            "blog": self.public_blog,
            "poems": self.public_poems,
            "song_analysis": self.public_song_analysis,
            "has_projects": self.has_projects,
            "has_blog": self.has_blog,
            "has_poems": self.has_poems,
            "has_song_analysis": self.has_song_analysis,
            "has_writing": self.has_writing,
            "has_talks": self.has_talks,
        })
        return ctx


def _validate_site_file(site_file: Path) -> list[ContentError]:
    errors = []
    if not site_file.exists():
        return [ContentError(str(site_file), "file", "site.yaml missing", "Create content/site.yaml")]
    try:
        with open(site_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        Site(**(data or {}))
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            errors.append(ContentError(str(site_file), field, err["msg"], suggest_fix(field, err["msg"], "site.yaml")))
    except Exception as e:  # noqa: BLE001
        errors.append(ContentError(str(site_file), "syntax", str(e), "Fix YAML syntax in site.yaml"))
    return errors


def _check_project_item(item: dict, idx: int, p_file: Path, seen: set[str]) -> list[ContentError]:
    errs = []
    try:
        proj = Project(**item)
        if proj.slug in seen:
            errs.append(ContentError(str(p_file), f"projects[{idx}].slug", f"Duplicate slug: {proj.slug}", "Ensure slug is unique"))
        seen.add(proj.slug)
    except ValidationError as e:
        for err in e.errors():
            field = f"projects[{idx}]." + ".".join(str(p) for p in err["loc"])
            errs.append(ContentError(str(p_file), field, err["msg"], suggest_fix(field, err["msg"], "projects.yaml")))
    return errs


def _validate_projects_file(projects_file: Path) -> list[ContentError]:
    if not projects_file.exists():
        return [ContentError(str(projects_file), "file", "projects.yaml missing", "Create content/projects.yaml")]
    try:
        with open(projects_file, encoding="utf-8") as f:
            p_data = yaml.safe_load(f) or {}
        items = p_data.get("projects", [])
        seen_slugs = set()
        errors = []
        for idx, item in enumerate(items):
            errors.extend(_check_project_item(item, idx, projects_file, seen_slugs))
        return errors
    except Exception as e:  # noqa: BLE001
        return [ContentError(str(projects_file), "syntax", str(e), "Fix YAML syntax in projects.yaml")]


def _validate_resume_file(resume_file: Path) -> list[ContentError]:
    errors = []
    if not resume_file.exists():
        return [ContentError(str(resume_file), "file", "resume.yaml missing", "Create content/resume.yaml")]
    try:
        with open(resume_file, encoding="utf-8") as f:
            r_data = yaml.safe_load(f) or {}
        Resume(**r_data)
    except ValidationError as e:
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            errors.append(ContentError(str(resume_file), field, err["msg"], suggest_fix(field, err["msg"], "resume.yaml")))
    except Exception as e:  # noqa: BLE001
        errors.append(ContentError(str(resume_file), "syntax", str(e), "Fix YAML syntax in resume.yaml"))
    return errors


def _check_talk_item(item: dict, idx: int, t_file: Path, seen: set[str]) -> list[ContentError]:
    errs = []
    try:
        talk = Talk(**item)
        if talk.slug in seen:
            errs.append(ContentError(str(t_file), f"talks[{idx}].slug", f"Duplicate slug: {talk.slug}", "Ensure slug is unique"))
        seen.add(talk.slug)
    except ValidationError as e:
        for err in e.errors():
            field = f"talks[{idx}]." + ".".join(str(p) for p in err["loc"])
            errs.append(ContentError(str(t_file), field, err["msg"], suggest_fix(field, err["msg"], "talks.yaml")))
    return errs


def _validate_talks_file(talks_file: Path) -> list[ContentError]:
    if not talks_file.exists():
        return [ContentError(str(talks_file), "file", "talks.yaml missing", "Create content/talks.yaml")]
    try:
        with open(talks_file, encoding="utf-8") as f:
            t_data = yaml.safe_load(f) or {}
        items = t_data.get("talks", [])
        seen_slugs = set()
        errors = []
        for idx, item in enumerate(items):
            errors.extend(_check_talk_item(item, idx, talks_file, seen_slugs))
        return errors
    except Exception as e:  # noqa: BLE001
        return [ContentError(str(talks_file), "syntax", str(e), "Fix YAML syntax in talks.yaml")]


def _check_lyrics_length(md_path: Path, body: str) -> list[ContentError]:
    errors = []
    lines = body.splitlines()
    consecutive_quotes = 0
    for line in lines:
        if line.strip().startswith(">"):
            consecutive_quotes += 1
            if consecutive_quotes > 6:
                errors.append(ContentError(
                    str(md_path), "lyrics_policy",
                    "Song analysis contains > 6 continuous lyrics lines",
                    "Break lyrics into 1-2 lines paired with your commentary",
                ))
                break
        else:
            consecutive_quotes = 0
    return errors


def _validate_post_model(meta: dict, md_path: Path, c_type: str, body: str) -> list[ContentError]:
    try:
        Post(**meta)
        if c_type == "song-analysis":
            return _check_lyrics_length(md_path, body)
    except ValidationError as e:
        errors = []
        for err in e.errors():
            field = ".".join(str(p) for p in err["loc"])
            errors.append(ContentError(str(md_path), field, err["msg"], suggest_fix(field, err["msg"], md_path.name)))
        return errors
    return []


def _validate_md_file(md_path: Path, c_type: str) -> list[ContentError]:
    try:
        text = md_path.read_text(encoding="utf-8")
        meta, body = parse_markdown_with_frontmatter(text)
        if not meta:
            return [ContentError(str(md_path), "frontmatter", "Missing frontmatter ('---')", "Add YAML frontmatter")]
        if "slug" not in meta:
            meta["slug"] = md_path.stem
        meta["content_type"] = c_type
        meta["body"] = body
        return _validate_post_model(meta, md_path, c_type, body)
    except Exception as e:  # noqa: BLE001
        return [ContentError(str(md_path), "format", str(e), f"Fix syntax in {md_path.name}")]


def validate_content(content_dir: Path | None = None) -> list[ContentError]:
    """Validate all content in content_dir against models and rules."""
    if content_dir is None:
        content_dir = Path("content").resolve()

    errors = []
    errors.extend(_validate_site_file(content_dir / "site.yaml"))
    errors.extend(_validate_projects_file(content_dir / "projects.yaml"))
    errors.extend(_validate_resume_file(content_dir / "resume.yaml"))
    errors.extend(_validate_talks_file(content_dir / "talks.yaml"))

    collections = [
        ("blog", content_dir / "blog"),
        ("poem", content_dir / "poems"),
        ("song-analysis", content_dir / "song-analysis"),
    ]
    for c_type, c_dir in collections:
        if c_dir.exists():
            for md_path in c_dir.glob("*.md"):
                errors.extend(_validate_md_file(md_path, c_type))

    return errors


def _load_posts(folder: Path, content_type: Literal["blog", "poem", "song-analysis"]) -> list[Post]:
    posts = []
    if folder.exists():
        for p in sorted(folder.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            meta, body = parse_markdown_with_frontmatter(text)
            if "slug" not in meta:
                meta["slug"] = p.stem
            meta["content_type"] = content_type
            meta["body"] = body
            posts.append(Post(**meta))
    return posts


def load_all_content(content_dir: Path | None = None) -> ContentCatalog:
    """Load all site content into a ContentCatalog. Raises RuntimeError on validation failure."""
    if content_dir is None:
        content_dir = Path("content").resolve()

    errors = validate_content(content_dir)
    if errors:
        err_msg = "\n\n".join(str(e) for e in errors)
        raise RuntimeError(f"Content validation failed with {len(errors)} error(s):\n\n{err_msg}")

    with open(content_dir / "site.yaml", encoding="utf-8") as f:
        site = Site(**(yaml.safe_load(f) or {}))
    with open(content_dir / "projects.yaml", encoding="utf-8") as f:
        projects = [Project(**item) for item in (yaml.safe_load(f) or {}).get("projects", [])]
    with open(content_dir / "resume.yaml", encoding="utf-8") as f:
        resume = Resume(**(yaml.safe_load(f) or {}))
    with open(content_dir / "talks.yaml", encoding="utf-8") as f:
        talks = [Talk(**item) for item in (yaml.safe_load(f) or {}).get("talks", [])]

    legacy_file = Path("src/api/config/values/content.yml")
    legacy = {}
    if legacy_file.exists():
        with open(legacy_file, encoding="utf-8") as f:
            legacy = yaml.safe_load(f) or {}

    return ContentCatalog(
        site=site,
        projects=projects,
        resume=resume,
        talks=talks,
        blog=_load_posts(content_dir / "blog", "blog"),
        poems=_load_posts(content_dir / "poems", "poem"),
        song_analysis=_load_posts(content_dir / "song-analysis", "song-analysis"),
        legacy_content=legacy,
    )
