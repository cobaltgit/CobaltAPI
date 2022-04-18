import json
import typing as t

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

import settings as s
from cobaltapi.routers import ALL_API_ROUTERS


class JSONResponse(ORJSONResponse):
    """
    A subclass of `fastapi.responses.ORJSONResponse` that
    injects a project-wide, standarized JSON response data.
    """

    def render(self, content: t.Any) -> str:
        """
        Renders the JSON data.
        """

        errors = content.pop("errors", None) if isinstance(content, dict) else None

        _content = {"success": errors is None, "errors": errors, "data": None if errors else content}

        return json.dumps(
            _content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


COBALTAPI = FastAPI(
    title="CobaltAPI",
    version="2.0",
    description="A general purpose API with many endpoints - IN DEVELOPMENT",
    docs_url="/",
    default_response_class=JSONResponse,
)

COBALTAPI.mount("/assets", StaticFiles(directory=s.ROOT_PATH / "cobaltapi" / "assets"), name="assets")


@COBALTAPI.exception_handler(RequestValidationError)
@COBALTAPI.exception_handler(HTTPException)
async def validation_exception_handler(_, exception: t.Union[HTTPException, RequestValidationError]):
    """
    Overwrites the default exception handler to return
    a standarized JSON error response, for consistency.
    """

    return JSONResponse(
        {"errors": [exception.detail] if isinstance(exception, HTTPException) else exception.errors()},
        status_code=exception.status_code,
    )


@COBALTAPI.get("/echo", tags=["Utilities"])
@COBALTAPI.get("/ping", tags=["Utilities"])
async def ping(message: str = "Pong!"):
    """
    Pings the API.
    """

    return message


for router in ALL_API_ROUTERS:
    COBALTAPI.include_router(router)


COBALTAPI.openapi()
COBALTAPI.openapi_schema["info"]["x-logo"] = {"url": "/assets/cobaltapi_logo.svg"}
