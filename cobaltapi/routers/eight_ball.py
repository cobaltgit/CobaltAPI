import typing as t

from fastapi import APIRouter
from random import choice


EIGHT_BALL_ROUTER = APIRouter(prefix='/8ball')
ANSWERS = ['Yes.', 'No.', 'Maybe.', 'Certainly.', 'Absolutely not.', 'Try asking again.', 'I do not know.']



@EIGHT_BALL_ROUTER.get('/')
async def get_answer(question: t.Optional[str] = None):
    """
        Get random answer.
    """

    return {
        "question": question or 'something dumb',
        "answer": choice(ANSWERS)
    }
