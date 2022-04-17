import asyncio
from functools import partial
from io import BytesIO
from random import sample

import aiohttp
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse

from app import app
from PIL import UnidentifiedImageError
from .functions import gen_image_macro


@app.get("/utils/ping", response_class=ORJSONResponse, tags=["Utilities"])
async def ping():
    """Returns a simple "Pong!" response, showing that the API is online"""
    return {"response": "Pong!"}


@app.get("/random/facts", response_class=ORJSONResponse, tags=["Random"])
async def get_fact(count: int = 1):
    """Get \<count\> random facts from a list of 3,090 facts  
    `count`: integer - optional parameter - the number of facts to retrieve - can be anywhere between 1 and 3090 (default: 1)
    """
    if count > len(app.facts):
        raise HTTPException(status_code=400, detail=f"Attempted to request more than {len(app.facts)} facts")
    elif count < 1:
        raise HTTPException(status_code=400, detail=f"Count must be at least 1, got {count}")
    samp = sample(app.facts, count)
    return {"response": samp[0] if count == 1 else samp}


@app.get("/fun/memegen", tags=["Fun"])
async def generate_image_macro(image_url: str, top_text: str, bottom_text: str):
    """
    Classic image macro generator using the Impact font

    `image_url`: string - required parameter - the background image URL to use  
    `top_text`: string - required parameter - the top text to use  
    `bottom_text`: string - required parameter - the bottom text to use  
    """

    loop = asyncio.get_event_loop()

    async with aiohttp.ClientSession(loop=loop) as cs:
        try:
            async with cs.get(image_url) as r:
                img_bytes = BytesIO(await r.read())
                fmt = r.headers["Content-Type"]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to obtain image from URL - {type(e).__name__}: {e}")

    try:
        out = await loop.run_in_executor(
            None, partial(gen_image_macro, img_bytes, top_text, bottom_text, font_path="app/files/fonts/impact.ttf")
        )
    except UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="Failed to identify image, maybe the format is invalid?") from e
    return StreamingResponse(out, media_type=fmt)