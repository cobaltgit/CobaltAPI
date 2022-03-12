import tomli
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

with open("pyproject.toml", "rb") as pyproject:
    info = tomli.load(pyproject)["tool"]["poetry"]

__version__ = info["version"]

tags = [
    {"name": "Utilities", "description": "API-related utilities"},
    {"name": "Random", "description": "Random things (facts and more to come)"},
]

app = FastAPI(
    title=info["name"],
    description=info["description"],
    version=__version__,
    license_info={
        "name": "MPL 2.0",
        "url": "https://www.mozilla.org/en-US/MPL/2.0/",
    },
    openapi_tags=tags,
    docs_url="/",
    redoc_url=None,
)


with open(
    "app/files/facts.txt", "r"
) as factfile:  # facts list from https://github.com/assaf/dailyhi/blob/master/facts.txt
    app.facts = [fact.strip() for fact in factfile.readlines()]

from app import views
