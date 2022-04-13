import asyncio
from functools import partial
from io import BytesIO
from random import randint, sample
from sys import maxsize

import aiohttp
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse

from app import app
from PIL import UnidentifiedImageError
from .functions import gen_image_macro, screenshot_webpage


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


@app.get("/random/numbers", response_class=ORJSONResponse, tags=["Random"])
async def random_int(floor: int = 0, ceil: int = 25, count: int = 1):
    """
    Get \<count\> random integers between \<floor\> and \<ceil\>  
    `count`: integer - optional parameter - the number of integers to retrieve - can be anywhere between 1 and 1000 (default: 1)  
    `floor`: integer - optional parameter - the minimum integer in the range - must be at least `-sys.maxsize`\* (default: 0)  
    `ceil`: integer - optional parameter - the maximum integer in the range - can be anywhere between `-sys.maxsize + 1`\* and `sys.maxsize`\*, must be greater than `floor` (default: 25)  

    \* `sys.maxsize` is 9223372036854775807 on a 64-bit system - the maximum value of a 64-bit signed integer, or on a 32-bit system, 2147483647
    """
    if floor < -maxsize:
        raise HTTPException(status_code=400, detail=f"Floor integer must be more than {-maxsize}")
    elif -maxsize + 1 > ceil or ceil > maxsize:
        raise HTTPException(status_code=400, detail=f"Ceiling integer must be between {-maxsize+1} and {maxsize}")
    elif count > 1000:
        raise HTTPException(
            status_code=400,
            detail="Cannot generate more than 100,000 random integers",
        )
    elif floor > ceil:
        raise HTTPException(status_code=400, detail="Floor integer must be less than ceiling integer")
    elif count < 1:
        raise HTTPException(status_code=400, detail=f"Count must be at least 1, got {count}")

    return {"response": randint(floor, ceil) if count == 1 else [randint(floor, ceil) for _ in range(count)]}


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

@app.get("/utils/screenshot", tags=["Utilities"])
async def screenshot(url: str, resolution: str = "1280x720"):
    """
    Screenshot a webpage and return the image

    `url`: string - required parameter - the webpage to screenshot
    """
    if tuple(map(int, resolution.split("x"))) > (3840, 2160):
        raise HTTPException(status_code=400, detail="Resolution must be 3840x2160 or less")
    loop = asyncio.get_event_loop()
    fn = partial(screenshot_webpage, url, resolution=resolution)
    screenshot = await loop.run_in_executor(None, fn)
    return StreamingResponse(screenshot, media_type='image/png')