import typing as t
import settings as s

import random

from fastapi import APIRouter, HTTPException


FACTS_ROUTER = APIRouter(prefix='/facts')

with open(s.FACTS_PATH, 'r') as facts:
    FACTS = [fact.strip() for fact in facts.readlines()]
    """Cached list of all facts"""



@FACTS_ROUTER.get('/')
async def get_fact(count: t.Optional[int] = None):
    """
        Get random facts.
    """

    facts_count = len(FACTS)

    if count is None or count >= facts_count:
        return {
            "facts": FACTS,
            "total": facts_count
        }

    elif count <= 0:
        raise HTTPException(status_code=400, detail="Requested fact count must be greater than 0.")


    return {
        "facts": random.sample(FACTS, count),
        "total": facts_count
    }
