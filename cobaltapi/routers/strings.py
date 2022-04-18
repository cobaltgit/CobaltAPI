from difflib import SequenceMatcher

from fastapi import APIRouter, HTTPException

STRINGS_ROUTER = APIRouter(prefix="/strings")


@STRINGS_ROUTER.get("/upper", tags=["Strings"])
@STRINGS_ROUTER.get("/uppercase", tags=["Strings"])
async def uppercase(string: str):
    """
    Converts string to uppercase.
    """

    return string.upper()


@STRINGS_ROUTER.get("/lower", tags=["Strings"])
@STRINGS_ROUTER.get("/lowercase", tags=["Strings"])
async def lowercase(string: str):
    """
    Converts string to lowercase.
    """

    return string.lower()


@STRINGS_ROUTER.get("/similarity", tags=["Strings"])
async def similarity(original: str, edited: str):
    """
    Calculates similarity between two strings
    and returns similarity in %.

    Uses `difflib`'s `SequenceMatcher` class.
    """

    return {"original": original, "edited": edited, "similarity": SequenceMatcher(None, original, edited).ratio() * 100}


@STRINGS_ROUTER.get("/replace", tags=["Strings"])
async def replace(string: str, find: str, replace_with: str):
    """
    Replaces all occurrences of `find` with `replace_with` in `string`.
    """

    total_length = len(string) + len(find) + len(replace_with)

    # TODO: Still clogs things up.
    # The app should be run behind another server, so
    # the upstream server can handle abnormal requests.
    # But that's a thing for the future, when the app expands
    # Note: I recommend Caddy: https://caddyserver.com/v2
    if total_length > 10000:
        raise HTTPException(status_code=400, detail="String length must be less than 10000.")

    return {"original": string, "new": string.replace(find, replace_with)}


@STRINGS_ROUTER.get("/split", tags=["Strings"])
async def split(string: str, separator: str = " ", max_split: int = -1, strip: bool = True):
    """
    Splits `string` into list of strings.
    """

    return {
        "original": string,
        "split": string.split(separator, max_split)
        if not strip
        else [s.strip() for s in string.split(separator, max_split)],
    }
