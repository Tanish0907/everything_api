from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class item(BaseModel):
    name: str
    genre: str


inventory = {
    1: {
        "name": "muck",
        "genre": "rogue like"
    },
    2: {
        "name": "hitman",
        "genre": "stealth"
    }
}


@app.get("/")
def home():
    return {"idk": "test"}


@app.get("/about")
def about():
    return {1: "jkrowling"}


@app.get("/games/{game_id}")
def get_game(game_id: int):
    return inventory[game_id]


@app.get("/search")
def get_game(name: Optional[str] = None):
    for id in inventory:
        if inventory[id].name == name:
            return inventory[id]
    return {"Data": 'notfound'}


@app.post("/add_game/{id}")
def add(id: int, item: item):
    if id in inventory:
        return {"error": "id already exists"}
    inventory[id] = item
    return {"sucess": "item added to inventory"}
