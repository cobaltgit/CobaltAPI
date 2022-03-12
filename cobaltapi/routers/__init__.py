import typing as t

from fastapi import APIRouter

from cobaltapi.routers.facts import FACTS_ROUTER
from cobaltapi.routers.strings import STRINGS_ROUTER
from cobaltapi.routers.eight_ball import EIGHT_BALL_ROUTER


ALL_API_ROUTERS: t.Type[APIRouter] = [
    FACTS_ROUTER,
    STRINGS_ROUTER,
    EIGHT_BALL_ROUTER
]
