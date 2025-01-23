from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
async def read_item(item_id:int, q:str | None = None):
    return {
        "item_id" : item_id,
        "q" : q
    }

@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    return {
        "item_name": item.name,
        "item_price": item.price,
        "item_id": item_id
    }


@app.get("/users/{user_id}")
def read_user(user_id :str):
    return {"user_id": user_id}

@app.get("/users/me")
def read_user_me():
    return {"user_id": "the current user"}