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


class ClothingCategory(BaseModel):
    weather: Literal['fall', 'winter', 'summer', 'spring']
    sex: Literal['male', 'female']

from pydantic import HttpUrl
class ClothingModel(BaseModel):
    category: ClothingCategory
    color: str
    size: str
    image: HttpUrl

class Offer(BaseModel):
    cloth: ClothingModel
    price: float
    discount: float

# Annotated[, Body(title="Weather", description="What is the recommended weather to use the Cloth")]
@app.post('/offer/')
def post_offer(
    offer:Annotated[Offer, Body(description="Your offer")]
    ):
    print(offer)
    for offe in offer:
        print(offe)
    return offer
    
### Declare Request Example Data
class House(BaseModel):
    country: str 
    state: str 
    street: str 
    number: int | str 

@app.put("/body-example/")
def body_example(
    house: Annotated[
        House,
        Body(openapi_examples={
            "normal" : {
                "summary" : "Expected example",
                "description" : "Example that will work correctly",
                "value" : {
                        
                    "country" : "Brazil",
                    "state": "São Paulo",
                    "street": "Rua das Araucárias",
                    "number": 1
                }
            },
            "error" : {
                "summary" : "Wrong example",
                "description" : "Example that will not work",
                "value" : {
                    "country" : "Argentina",
                    "street": "Buena vista",
                    "number": 1
                }
            },
        })
    ]
    ):
    return house

from uuid import UUID
from datetime import time, datetime, timedelta
from time import sleep

@app.put("/other-types/{id}/")
def other_types(
    id: UUID, # Example: 6d6a21de-0736-4c0e-9a3c-a3a1493fa6ad
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()], # Example: P3D --> 3 days
    repeat_at: Annotated[time | None, Body()]
    ):
    start_process = start_datetime + process_after
    duration  = end_datetime - start_process
    return {
        "id" : id,
        "start_datetime" : start_datetime,
        "end_datetime" : end_datetime,
        "process_after" : process_after,
        "repeat_at" : repeat_at,
        "start_process" : start_process,
        "duration " : duration ,
    }

from fastapi import Cookie
@app.get('/cookie/')
def get_cookie(
    cookie_id: Annotated[str | None, Cookie()]
    ):
    return {"cookie_id":cookie_id} # It must have cookie_id on browser cookies

from fastapi import Header
@app.get('/headers/')
def get_header(
    header_param: Annotated[list[str], Header()]
    ):
    return {"header" : header_param} # Example: "header": ["Foo,Bar,Get"]


class CookieModel(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get('/cookie-model-1/')
def get_cookie_1(
    cookies: Annotated[CookieModel, Cookie()]
    ):
    return cookies

@app.get('/cookie-model-2/')
def get_cookie_1(
    cookies: Annotated[CookieModel, Cookie()]
    ):
    return {**cookies.dict(), "other-response": 2}


class HeaderModel(BaseModel):
    host: str
    save_data: bool = False
    x_tag: list[str] = []

@app.get('/header-model-1/')
def get_header_1(
    headers: Annotated[HeaderModel, Header()]
    ):
    return headers

from pydantic import EmailStr
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

@app.post('/users/')
async def create_user(user:Annotated[UserIn, Body(openapi_examples={
    "right" : {
        "summary" : "Expected body",
        "description" : "Body correctly formatted",
        "value" : {
            "username" : "username",
            "password" : "your_password",
            "email" : "email@host.com",
            "full_name" : "optional: Your Full Name"
        }
    },
    "wrong" : {
        "summary" : "Not Expected body",
        "description" : "Body incorrectly formatted",
        "value" : {
            "username" : 1,
            "password" : "your_password",
            "email" : "Lorem",
            "full_name" : 123
        }
    }
})]) -> UserIn:
    return user # Problem: I want to send all data but password

    
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn2(BaseUser):
    password: str

from fastapi import status

@app.post('/users-formated-response/', response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED)
async def create_user_formated(user:UserIn2) -> BaseUser:
    return user # It will return only username, email and full_name


from fastapi import Form

class BaseModelForm(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post("/login/")
async def login_user(data: Annotated[BaseModelForm, Form()]):
    return {"data": data}