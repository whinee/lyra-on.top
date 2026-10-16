import hashlib
import hmac
import os
import subprocess
import time
import traceback
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from src.api.config.content import get_slot
from src.api.config.content_loader import load_all_content
from src.api.models.settings import settings
from src.api.routers import pages
from src.api.utils import TEMPLATES, CustomResponse

description = """
Lyra Phasma's Website and Blog :3
"""

security = HTTPBasic()

middleware = [
    Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET),  # type: ignore
]
app = FastAPI(
    title="Lyra-on.top",
    description=description,
    version="1.0.0",
    contact={
        "name": "Lyra Phasma",
        "url": "https://lyra-on.top",
        "email": "lyraphasma@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://choosealicense.com/licenses/mit/",
    },
    docs_url=None,
    redoc_url=None,
    middleware=middleware,
)

# Load content and inject global template helpers
catalog = load_all_content()
content = catalog.to_template_context()
TEMPLATES.env.globals["content"] = content
TEMPLATES.env.globals["get_slot"] = lambda slot_name: get_slot(content, slot_name)

app.include_router(pages.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next) -> Any:  # type: ignore[no-untyped-def]
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        if response.status_code == 404 and not request.url.path.startswith("/api"):
            return TEMPLATES.TemplateResponse(
                request=request,
                name="404.html",
                context={"content": content, "get_slot": lambda name: get_slot(content, name)},
                status_code=404,
            )
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception:  # noqa: BLE001
        return CustomResponse.json(
            status_code=500,
            message="Error occurred",
            json={"traceback": traceback.format_exc()},
        )


@app.get("/", response_class=Response)
async def index_get(request: Request) -> Any:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html",
        context={"content": content, "get_slot": lambda name: get_slot(content, name)},
    )


@app.get("/404.html", response_class=Response)
async def not_found_page(request: Request) -> Any:
    return TEMPLATES.TemplateResponse(
        request=request,
        name="404.html",
        context={"content": content, "get_slot": lambda name: get_slot(content, name)},
        status_code=404,
    )


@app.get("/docs", include_in_schema=False, status_code=200)
async def docs(response: Response) -> Any:  # type: ignore[no-untyped-def]
    response.status_code = 200
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore[arg-type]
        title=app.title + " - Docs",
        swagger_css_url="/static/stylesheets/docs.css",
    )


@app.get("/code/{code}")
async def code_get(request: Request, code: int) -> Any:  # type: ignore[no-untyped-def]
    status_code, resp_content, status = CustomResponse.raw_json(status_code=code)
    return TEMPLATES.TemplateResponse(
        name="code.j2.html",
        context={
            "request": request,
            "content": resp_content,
            "status": {"code": status_code, **status.copy()},
        },
        status_code=status_code,
    )


@app.post("/code/{code}")
async def code_post(code: int) -> Any:  # type: ignore[no-untyped-def]
    return CustomResponse.json(status_code=code)


@app.post("/webhook")
async def handle_webhook(request: Request) -> Any:  # type: ignore[no-untyped-def]
    payload = await request.body()
    secret = settings.WEBHOOK_SECRET
    signature = request.headers.get("X-Hub-Signature-256")
    exp_signature = "sha256=" + hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(exp_signature, signature or ""):  # type: ignore[type-var]
        raise HTTPException(status_code=403, detail="Invalid signature")
    subprocess.Popen(f"kill -9 {os.getpid()}", shell=True)  # noqa: S602
    return {"message": "Webhook received successfully!"}


app.mount("/static", StaticFiles(directory="src/api/static"), name="static")
