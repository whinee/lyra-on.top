"""src/api/models/content.py - Pydantic models for site content engine."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Social(BaseModel):
    kind: str
    label: str
    url: str | None = None
    handle: str | None = None
    visibility: Literal["public", "private"] = "public"


class EmailConfig(BaseModel):
    address: str
    obfuscate: bool = True


class Site(BaseModel):
    title: str = "Lyra Phasma | lyra-on.top"
    tagline: str = "neko dev. weird hardware. FOSS or bust."
    description: str = "Lyra Phasma's portfolio: Software developer, cyberdeck builder, and FOSS advocate! :3"
    url: str = "https://lyra-on.top"
    author_display_name: str = "Lyra Phasma"
    blog_signature_intro: str = "Nyahallo! Your favorite kittygirl hacker here :3"
    blog_signature_outro: str = "Paws off the keyboard for now. I'm Lyra: your local kittygirl hacker :3"
    nav: list[str] = Field(default_factory=lambda: ["projects", "writing", "blog", "resume", "contacts", "talks"])
    socials: list[Social] = Field(default_factory=list)
    email: EmailConfig = Field(default_factory=lambda: EmailConfig(address="hi@lyra-on.top", obfuscate=True))
    availability: str | None = None
    hero_variant: Literal["a", "b", "c"] = "a"
    features: dict[str, bool] = Field(
        default_factory=lambda: {
            "cat_cursor": True,
            "lite_motion": True,
            "image_lock": True,
        },
    )


class Project(BaseModel):
    slug: str
    title: str
    summary: str = Field(..., max_length=200)
    repo_url: str
    homepage_url: str | None = None
    tags: list[str] = Field(default_factory=list)
    language: str | None = None
    status: Literal["active", "maintained", "archived", "idea"] = "active"
    featured: bool = False
    year: str | int | None = None
    highlights: list[str] = Field(default_factory=list)
    body: str | None = None
    visibility: Literal["public", "private"] = "public"

    @field_validator("repo_url")
    @classmethod
    def validate_repo_url(cls, v: str) -> str:
        if not v.startswith(("https://github.com/", "http://github.com/")):
            raise ValueError(f"Project repo_url must be a GitHub URL, got: {v}")
        return v


class Achievement(BaseModel):
    title: str
    year: str | int | None = None
    detail: str | None = None
    link: str | None = None
    visibility: Literal["public", "private"] = "private"


class Speaking(BaseModel):
    title: str
    event: str
    date: str
    link: str | None = None
    visibility: Literal["public", "private"] = "public"


class Education(BaseModel):
    degree: str
    institution: str
    year: str | int | None = None
    visibility: Literal["public", "private"] = "private"


class Resume(BaseModel):
    headline: str
    summary: str
    achievements: list[Achievement] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    speaking: list[Speaking] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    email_note: str = (
        "if u want my personal CV with my dead/government name in it, "
        "just email me here, and ask for it. we can talk more there as well :3"
    )
    cta: str = "Say Hello (=^･ω･^=)"


class Talk(BaseModel):
    slug: str
    title: str
    event: str
    date: str
    venue: str | None = None
    slides_url: str = "TODO(lyra)"
    description: str | None = None
    featured: bool = False


class Post(BaseModel):
    slug: str
    title: str
    date: str
    summary: str | None = None
    updated: str | None = None
    tags: list[str] = Field(default_factory=list)
    draft: bool = False
    cover: str | None = None
    cover_alt: str | None = None
    content_type: Literal["blog", "poem", "song-analysis"] = "blog"
    body: str = ""

    @field_validator("cover_alt")
    @classmethod
    def validate_cover_alt(cls, v: str | None, info) -> str | None:
        if info.data.get("cover") and not v:
            raise ValueError("cover_alt is required when cover is provided")
        return v
