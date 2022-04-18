import random
import typing as t

from fastapi import APIRouter, HTTPException

import settings as s

RANDOM_ROUTER = APIRouter(prefix="/random")

with open(s.FACTS_PATH, "r") as facts:
    FACTS = [fact.strip() for fact in facts.readlines()]
    """Cached list of all facts"""


@RANDOM_ROUTER.get("/facts", tags=["Random"])
async def get_fact(count: t.Optional[int] = None):
    """
    Get random facts.
    """

    facts_count = len(FACTS)

    if count is None or count >= facts_count:
        return {"facts": FACTS, "total": facts_count}

    elif count <= 0:
        raise HTTPException(status_code=400, detail="Requested fact count must be greater than 0.")

    return {"facts": random.sample(FACTS, count), "total": facts_count}
