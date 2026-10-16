"""src/api/routers/pages.py - Router for all public collection and content pages.

Enforces the Auto-Hide rule: empty collections return 404 and are omitted from nav.
"""

from typing import Any
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import Response

from src.api.config.content_loader import load_all_content
from src.api.utils import TEMPLATES

router = APIRouter()


def get_catalog():
    """Load fresh catalog from content/ directory."""
    return load_all_content()


# 1. Projects
@router.get("/projects", response_class=Response)
async def projects_index(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_projects:
        raise HTTPException(status_code=404, detail="Projects collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="projects/index.html",
        context={"content": ctx, "projects": catalog.public_projects},
    )


@router.get("/projects/{slug}", response_class=Response)
async def project_detail(request: Request, slug: str) -> Any:
    catalog = get_catalog()
    matching = [p for p in catalog.public_projects if p.slug == slug]
    if not matching:
        raise HTTPException(status_code=404, detail=f"Project '{slug}' not found")
    project = matching[0]
    ctx = catalog.to_template_context()
    body_html = ""
    if project.body:
        from src.api.config.content_loader import get_markdown_renderer
        body_html = get_markdown_renderer("blog").render(project.body)

    return TEMPLATES.TemplateResponse(
        request=request,
        name="projects/detail.html",
        context={"content": ctx, "project": project, "body_html": body_html},
    )


# 2. Writing Hub & Subcollections
@router.get("/writing", response_class=Response)
async def writing_hub(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_writing:
        raise HTTPException(status_code=404, detail="Writing collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="writing/index.html",
        context=ctx,
    )


@router.get("/writing/poems", response_class=Response)
async def poems_index(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_poems:
        raise HTTPException(status_code=404, detail="Poems collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="writing/collection.html",
        context={
            "content": ctx,
            "title": "Poems",
            "description": "Heartfelt stanzas written under neon glow and terminal screens :3",
            "base_url": "/writing/poems",
            "items": catalog.public_poems,
        },
    )


@router.get("/writing/poems/{slug}", response_class=Response)
async def poem_detail(request: Request, slug: str) -> Any:
    catalog = get_catalog()
    matching = [p for p in catalog.public_poems if p.slug == slug]
    if not matching:
        raise HTTPException(status_code=404, detail=f"Poem '{slug}' not found")
    poem = matching[0]
    ctx = catalog.to_template_context()
    body_html = catalog.render_post_html(poem)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="writing/detail.html",
        context={
            "content": ctx,
            "post": poem,
            "body_html": body_html,
            "back_url": "/writing/poems",
            "back_label": "Poems",
        },
    )


@router.get("/writing/song-analysis", response_class=Response)
async def song_analysis_index(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_song_analysis:
        raise HTTPException(status_code=404, detail="Song analysis collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="writing/collection.html",
        context={
            "content": ctx,
            "title": "Song Analysis",
            "description": "Dissecting music, lyrics, and emotional resonance line by line :3",
            "base_url": "/writing/song-analysis",
            "items": catalog.public_song_analysis,
        },
    )


@router.get("/writing/song-analysis/{slug}", response_class=Response)
async def song_analysis_detail(request: Request, slug: str) -> Any:
    catalog = get_catalog()
    matching = [p for p in catalog.public_song_analysis if p.slug == slug]
    if not matching:
        raise HTTPException(status_code=404, detail=f"Song analysis '{slug}' not found")
    post = matching[0]
    ctx = catalog.to_template_context()
    body_html = catalog.render_post_html(post)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="writing/detail.html",
        context={
            "content": ctx,
            "post": post,
            "body_html": body_html,
            "back_url": "/writing/song-analysis",
            "back_label": "Song Analysis",
        },
    )


# 3. Blog
@router.get("/blog", response_class=Response)
async def blog_index(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_blog:
        raise HTTPException(status_code=404, detail="Blog collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="blog/index.html",
        context={"content": ctx, "blog": catalog.public_blog},
    )


@router.get("/blog/{slug}", response_class=Response)
async def blog_detail(request: Request, slug: str) -> Any:
    catalog = get_catalog()
    matching = [p for p in catalog.public_blog if p.slug == slug]
    if not matching:
        raise HTTPException(status_code=404, detail=f"Post '{slug}' not found")
    post = matching[0]
    ctx = catalog.to_template_context()
    body_html = catalog.render_post_html(post)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="blog/detail.html",
        context={"content": ctx, "post": post, "body_html": body_html},
    )


@router.get("/blog/rss.xml", response_class=Response)
async def blog_rss(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_blog:
        raise HTTPException(status_code=404, detail="Blog collection is empty")
    site = catalog.site
    posts = catalog.public_blog

    items_xml = []
    for p in posts:
        items_xml.append(f"""    <item>
      <title><![CDATA[{p.title}]]></title>
      <link>{site.url}/blog/{p.slug}</link>
      <guid>{site.url}/blog/{p.slug}</guid>
      <pubDate>{p.date}</pubDate>
      <description><![CDATA[{p.summary or ""}]]></description>
    </item>""")

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title><![CDATA[{site.title} - Blog]]></title>
    <link>{site.url}/blog</link>
    <description><![CDATA[{site.description}]]></description>
    <language>en</language>
{"\n".join(items_xml)}
  </channel>
</rss>"""
    return Response(content=rss_content, media_type="application/xml")


# 4. Resume & CV (Canonical /resume)
@router.get("/resume", response_class=Response)
async def resume_page(request: Request) -> Any:
    catalog = get_catalog()
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="resume/index.html",
        context={"content": ctx, "resume": catalog.resume},
    )


@router.get("/cv", response_class=Response)
async def cv_page(request: Request) -> Any:
    # Identical to /resume, canonical points to /resume
    return await resume_page(request)


# 5. Contacts
@router.get("/contacts", response_class=Response)
async def contacts_page(request: Request) -> Any:
    catalog = get_catalog()
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="contacts/index.html",
        context={"content": ctx, "site": catalog.site},
    )


# 6. Talks & Slides
@router.get("/talks", response_class=Response)
async def talks_page(request: Request) -> Any:
    catalog = get_catalog()
    if not catalog.has_talks:
        raise HTTPException(status_code=404, detail="Talks collection is empty")
    ctx = catalog.to_template_context()
    return TEMPLATES.TemplateResponse(
        request=request,
        name="talks/index.html",
        context={"content": ctx, "talks": catalog.public_talks},
    )
