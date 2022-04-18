import typing as t
from random import choice

from fastapi import APIRouter

EIGHT_BALL_ROUTER = APIRouter(prefix="/8ball")
ANSWERS = (
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes, definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
)


@EIGHT_BALL_ROUTER.get("/", tags=["Fun"])
async def get_answer(question: t.Optional[str] = None):
    """
    Get random answer.
    """

    return {"question": question or "something dumb", "answer": choice(ANSWERS)}
