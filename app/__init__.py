from fastapi import FastAPI

app = FastAPI()

with open(
    "app/files/facts.txt", "r"
) as factfile:  # facts list from https://github.com/assaf/dailyhi/blob/master/facts.txt
    app.facts = [fact.strip() for fact in factfile.readlines()]

from app import views
