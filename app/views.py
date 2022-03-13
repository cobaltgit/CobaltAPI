from random import sample

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from app import app


@app.get("/ping", response_class=ORJSONResponse, tags=["Utilities"])
async def ping():
    """Ping the API"""
    return {"response": "Pong!"}


@app.get("/facts", response_class=ORJSONResponse, tags=["Random"])
async def get_fact(count: int = 1):
    """Get <count> random facts from a list of 3,090 facts"""
    if count > len(app.facts):
        raise HTTPException(status_code=400, detail=f"Attempted to request more than {len(app.facts)} facts")
    else:
        samp = sample(app.facts, count)
        if count == 1:
            return {"response": samp[0]}
        else:
            return {"response": samp}
