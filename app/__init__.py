import tomli
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

with open("pyproject.toml", "rb") as pyproject:
    info = tomli.load(pyproject)["tool"]["poetry"]

app = FastAPI()
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=info["name"],
        version=info["version"],
        description=info["description"],
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
