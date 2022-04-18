import typing as t

from fastapi import APIRouter

from cobaltapi.routers.fun import FUN_ROUTER
from cobaltapi.routers.rand import RANDOM_ROUTER
from cobaltapi.routers.images import IMAGE_ROUTER
from cobaltapi.routers.strings import STRINGS_ROUTER

ALL_API_ROUTERS: t.Type[APIRouter] = [RANDOM_ROUTER, STRINGS_ROUTER, FUN_ROUTER, IMAGE_ROUTER]
