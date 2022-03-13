from random import randint, sample
from sys import maxsize

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from app import app


@app.get("/ping", response_class=ORJSONResponse, tags=["Utilities"])
async def ping():
    """Ping the API"""
    return {"response": "Pong!"}


@app.get("/facts", response_class=ORJSONResponse, tags=["Random"])
async def get_fact(count: int = 1):
    """Get \<count\> random facts from a list of 3,090 facts"""
    if count > len(app.facts):
        raise HTTPException(status_code=400, detail=f"Attempted to request more than {len(app.facts)} facts")
    elif count < 1:
        raise HTTPException(status_code=400, detail=f"Count must be at least 1, got {count}")
    samp = sample(app.facts, count)
    return {"response": samp[0] if count == 1 else samp}


@app.get("/randint", response_class=ORJSONResponse, tags=["Random"])
async def random_int(floor: int = 0, ceil: int = 25, count: int = 1):
    """Get \<count\> random integers between \<floor\> and \<ceil\>"""
    if floor < -maxsize:
        raise HTTPException(status_code=400, detail=f"Floor integer must be more than {-maxsize}")
    elif -maxsize + 1 > ceil or ceil > maxsize:
        raise HTTPException(status_code=400, detail=f"Ceiling integer must be between {-maxsize+1} and {maxsize}")
    elif count > maxsize:
        raise HTTPException(status_code=400, detail=f"Cannot generate more than {maxsize} random integers")
    elif floor > ceil:
        raise HTTPException(status_code=400, detail="Floor integer must be less than ceiling integer")
    elif count < 1:
        raise HTTPException(status_code=400, detail=f"Count must be at least 1, got {count}")

    return {"response": randint(floor, ceil) if count == 1 else [randint(floor, ceil) for _ in range(count)]}
