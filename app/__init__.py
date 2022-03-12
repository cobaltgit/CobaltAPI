import re

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

with open("pyproject.toml", "r") as pyproject:
    if ver := re.search("^version.*$", pyproject.read(), re.MULTILINE):
        __version__ = ver.group().split("=")[-1].strip().replace('"', "")

app = FastAPI()
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cobalt API",
        version=__version__,
        description="A general purpose API with many endpoints - IN DEVELOPMENT",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "/assets/cobaltapi_logo.svg"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

with open(
    "app/files/facts.txt", "r"
) as factfile:  # facts list from https://github.com/assaf/dailyhi/blob/master/facts.txt
    app.facts = [fact.strip() for fact in factfile.readlines()]

from app import views
