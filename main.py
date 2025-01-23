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

@app.get("/users/me")
def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
def read_user(user_id :str):
    return {"user_id": user_id}

from enum import Enum

class ModelName(str, Enum):
    #<name> = <value>
    alexnet = "Alexnet"
    resnet = "Resnet"
    lenet = "Lenet"

print(ModelName.alexnet.name)  # -> alexnet
print(ModelName.alexnet.value) # -> Alexnet

@app.get("/models/{model_name}")
async def get_model(model_name : ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "Lenet": 
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
def get_file(file_path:str):
    return {"path" : file_path}

@app.get("/items/query_p_enum/{item_id}")
async def read_user_item(
    item_id: str, needy: ModelName, skip: int = 0, limit: int | None = None
): # needy has to be the values of eNum, not name --> 'http://127.0.0.1:8000/items/query_p_enum/AN1322?needy=Alexnet&skip=0'
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

class ItemName(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item:ItemName): # Declaring as a type of ItemName class that inherits from BaseModel, FastAPI will Read the body of the request as JSON|Validate the data|
    return {**item.model_dump(exclude=['tax']), "price_with_tax":item.price + item.tax} # model_dump() is a modernized method of .dict()

## Query Parameters and String Validations

from fastapi import Query
from typing import Annotated

@app.get('/query_validator/')
def read_query(q: Annotated[str|None, Query(max_length=50, min_length=5, pattern="_admin$")] = None):
    results = {"items" : [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
