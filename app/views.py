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
    """Get random facts from a list of 3,090 facts"""
    if count > len(app.facts):
        raise HTTPException(status_code=400, detail=f"Attempted to request more than {len(app.facts)} facts")
    return {"response": sample(app.facts, count)}
