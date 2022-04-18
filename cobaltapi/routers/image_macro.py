import asyncio
from functools import partial
from io import BytesIO

from aiohttp import ClientSession
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from PIL import UnidentifiedImageError
from base64 import b64encode

from cobaltapi.functions import gen_image_macro

IMAGE_MACRO_ROUTER = APIRouter(prefix='/image_macro')


@IMAGE_MACRO_ROUTER.get("/", tags=["Image"])
async def generate_image_macro(image_url: str, top_text: str, bottom_text: str = None):
    """
    Classic image macro generator using the Impact font  
    `image_url`: string - required parameter - the background image URL to use  
    `top_text`: string - required parameter - the top text to use  
    `bottom_text`: string - optional parameter - the bottom text to use  
    """

    loop = asyncio.get_event_loop()

    async with ClientSession(loop=loop) as cs:
        try:
            async with cs.get(image_url) as r:
                img_bytes = BytesIO(await r.read())
                fmt = r.headers["Content-Type"]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to obtain image from URL - {type(e).__name__}: {e}")

    try:
        out = await loop.run_in_executor(
            None, partial(gen_image_macro, img_bytes, top_text, bottom_text, font_path="cobaltapi/files/fonts/impact.ttf")
        )
    except UnidentifiedImageError as e:
        raise HTTPException(status_code=400, detail="Failed to identify image, maybe the format is invalid?") from e
    return {
        "b64_data": f"data:{fmt};base64,{b64encode(out.read()).decode('utf-8')}",
    }