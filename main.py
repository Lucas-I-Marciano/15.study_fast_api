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
def read_query(q: Annotated[str|None, Query(max_length=50, min_length=5, pattern="_admin$")]):
    results = {"items" : [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

from fastapi import Path
@app.get('/query_list/{size}/')
def read_query_list(
    *,
    q: 
        Annotated[None | list[str], Query(
            title="Query parameters as list", 
            description="Deprecated function, use XPTO to get use of query to handle with list of query parameter",
            alias="q-item", # alias for my 'q' parameter --> http://127.0.0.1:8000/query_list/?q-item=foo&q-item=bar
            deprecated=True
        )] = ['foo', 'bar'],
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
    size: Annotated[float, Path(le=20.5, ge=0, title="Size of list", description="Variable to handle with # of items")],
    ):
    result = {"q" : q}
    if size>0 :
        result.update({"size":size})
    return result

from pydantic import Field
from typing import Literal

class QueryParamValidator(BaseModel):
    model_config = {"extra":"forbid"} # It will forbid: http://127.0.0.1:8000/query-params-validator2/?limit=100&off_set=0&order_by=created_at&tool=hammer, because of tool=hammer
    limit: int = Field(default=100, le=100, ge=0)
    off_set: int = Field(default=0, le=10, ge=0)
    tags: list[str] = []
    order_by: Literal["tags", "created_at"] = "created_at" 

@app.get('/query-params-validator/')
def query_params_validator(
    query: Annotated[QueryParamValidator, Query()]
):
    return query

@app.get('/query-params-validator2/')
def query_params_validator2(
    query2: Annotated[QueryParamValidator, Query()]
):
    return query2


from fastapi import Body
class UserModel(BaseModel):
    name: str = Field(title="Your name", max_digits=30, description="Your first name to fullfill our database")
    last_name: str | None = None

@app.put('/body/')
def study_body(
    user: Annotated[UserModel, Body(title="User requesting", embed=True)],
    item : Annotated[ItemName, Body()],
    importance : Annotated[Literal['h', 'm', 'l'], Body()],
    q: Annotated[str, Query(alias="q-param")]
    ):
    results = {"q":q , "user" : user}
    return results