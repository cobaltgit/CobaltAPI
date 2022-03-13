import tomli
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

with open("pyproject.toml", "rb") as pyproject:
    info = tomli.load(pyproject)["tool"]["poetry"]

__version__ = info["version"]
__license__ = "MPL-2.0"
__author__ = "Cobalt"
__author_contact__ = {"discord": {"name": "cobalt#9144", "id": 700661710696087562}}

tags = [
    {"name": "Utilities", "description": "API-related utilities"},
    {"name": "Random", "description": "Random things (facts, numbers, more)"},
    {"name": "Fun", "description": "Fun stuff, you get the gist"},
]
app = FastAPI(
    title=info["name"],
    description=f"""{info['description']}\n
Discord - [`{__author_contact__['discord']['name']}`](https://discord.com/users/{__author_contact__['discord']['id']})""",
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
