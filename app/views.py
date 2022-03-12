from random import sample

from fastapi import HTTPException
from fastapi.responses import ORJSONResponse, RedirectResponse

from app import app


@app.get("/")
async def redirect_to_docs():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs", status_code=303)


@app.get("/facts", response_class=ORJSONResponse)
async def get_fact(count: int = 1) -> dict[str, str | list[str]]:
    """Get random facts from a list of 3,090 facts"""
    if count > len(app.facts):
        raise HTTPException(status_code=400, detail=f"Attempted to request more than {len(app.facts)} facts")
    return {"response": sample(app.facts, count)}
