from typing import Any, Optional

from fastapi import Request
from fastapi.responses import UJSONResponse
from starlette.templating import Jinja2Templates

from globals import CONSTANTS_YML

# Constants
STATUS_KEY_PRIORITY = ["phrase", "description", "spec", "spec_link"]
DEFAULT_DETAILS = {
    1: "Information",
    2: "Success",
    3: "Redirect",
    4: "Client Error",
    5: "Server Error",
    7: "Developer Error",
}
DEFAULT_MESSAGE = {
    4: "The client has erred.",
    5: "The server has erred.",
    7: "Thy underpaid yet overworked developer hath erred.",
}
DEFAULT_ERROR = {
    1: False,
    2: False,
    3: False,
    4: True,
    5: True,
    7: True,
}


def fetch_flash(request: Request):
    return request.session.pop("_messages") if "_messages" in request.session else []


TEMPLATES = Jinja2Templates(directory="src/api/templates")
TEMPLATES.env.globals["fetch_flash"] = fetch_flash


class CustomResponse:
    @staticmethod
    def pretty_json(  # noqa: C901 # type: ignore[no-untyped-def]
        status_code: int,
        detail: str | None = None,
        message: str | None = None,
        error: bool | None = None,
    ):
        code_group = int(str(status_code)[0])

        if error is None:
            error = DEFAULT_ERROR.get(code_group, False)

        if rci := CONSTANTS_YML.dir(f"http/code/{status_code}", None):
            rci = rci.copy()
            ci = {}
            for i in STATUS_KEY_PRIORITY:
                if (rcip := rci.pop(i, "U2VDckV0")) and (rcip != "U2VDckV0"):
                    ci[i] = rcip

            gi = {}
            rgi = CONSTANTS_YML.dir(f"http/group/{code_group}").copy()
            for i in STATUS_KEY_PRIORITY:
                if (rgip := rgi.pop(i, "U2VDckV0")) and (rgip != "U2VDckV0"):
                    gi[i] = rgip
            if (rgis := rgi.pop("subgroup", "U2VDckV0")) and (rgis != "U2VDckV0"):
                rgis = rgis.copy()
                if (rgisc := rgis.pop(str(status_code)[1], "U2VDckV0")) and (
                    rgisc != "U2VDckV0"
                ):
                    gi["subgroup"] = rgisc

            status = {"code": status_code, **ci, **rci, "group": {**gi, **rgi}}
        else:
            status = {"code": status_code}

        if code_group == 1:
            status_code = 200
        elif code_group == 7:
            status_code = 500

        content: dict[str, Any] = {}

        if detail := (detail or DEFAULT_DETAILS.get(code_group, None)):
            content["detail"] = detail

        if message := (message or DEFAULT_MESSAGE.get(code_group, None)):
            content["message"] = message

        content["error"] = DEFAULT_ERROR.get(code_group, False) if error is None else error

        return [status_code, content, status]

    @staticmethod
    def json(  # type: ignore[no-untyped-def]
        status_code: int,
        detail: str | None = None,
        message: str | None = None,
        error: bool | None = None,
        json: dict[str, Any] | None = None,
        *args,
        **kwargs,
    ) -> UJSONResponse:
        if json is None:
            json = {}

        status_code, content, status = CustomResponse.pretty_json(
            status_code,
            detail,
            message,
            error,
        ).copy()

        return UJSONResponse(  # type: ignore[misc]
            *args,
            status_code=status_code,
            content={
                **content,
                **json,
                "status": status,
            },
            **kwargs,
        )

    # @staticmethod
    # def tpl(
    #     request: Request,
    #     tpl: str,
    # ) -> Callable[[str, str], TEMPLATES.TemplateResponse]:
    #     def inner(
    #         message: str,
    #         category: str = "primary",
    #         *args,
    #         **kwargs,
    #     ) -> TEMPLATES.TemplateResponse:
    #         if "_messages" not in request.session:
    #             request.session["_messages"] = []
    #         request.session["_messages"].append(
    #             {"message": message, "category": category},
    #         )
    #         return TEMPLATES.TemplateResponse(
    #             tpl,
    #             {"request": request},
    #             *args,
    #             **kwargs,
    #             status_code=status_code,
    #             content={
    #                 **content,
    #                 **json,
    #                 "status": status,
    #             },
    #         )

    #     return inner

