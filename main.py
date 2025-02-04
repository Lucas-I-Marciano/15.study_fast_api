from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

from typing import Annotated
from fastapi import Header, Depends
def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "secret-pass" : # Remember that even declaring x_token, on header (by default) will be x-token
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden url - Invalid token")

def get_key_header(x_key: Annotated[str, Header()]):
    if x_key != "secret-key": # Remember that even declaring x_key, on header (by default) will be x-key
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden url - Invalid key")
    return x_key
# app = FastAPI(dependencies=[Depends(get_token_header), Depends(get_key_header)])

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

class TagsEnum(Enum):
    user = "users"
    item = "items"
    dependency = "Dependency"
    security = "Security"
    hero = "Hero"

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

@app.get("/items/query_p_enum/{item_id}", tags=[TagsEnum.item])
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

@app.post("/items/", tags=[TagsEnum.item])
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

@app.put('/body/', tags=[TagsEnum.user])
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
@app.post('/offer/', tags=[TagsEnum.item])
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

@app.post('/users/', tags=[TagsEnum.user])
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

@app.post('/users-formated-response/', response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED, tags=[TagsEnum.user])
async def create_user_formated(user:UserIn2) -> BaseUser:
    return user # It will return only username, email and full_name


from fastapi import Form

class BaseModelForm(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}

@app.post("/login/", tags=[TagsEnum.user])
async def login_user(data: Annotated[BaseModelForm, Form()]):
    return {"data": data}

from fastapi import File, UploadFile

@app.post("/files/")
async def create_file(file: Annotated[UploadFile, File()]):
    return {"filename":file.filename, "content_type":file.content_type}

from fastapi import HTTPException, Request

from fastapi.responses import JSONResponse

class ErrorItem3(Exception):
    def __init__(self, id_number:int):
        self.id_number = id_number

@app.exception_handler(ErrorItem3)
def whathever_name_I_want(request:Request, exc: ErrorItem3):
    return JSONResponse({
        "status" : status.HTTP_406_NOT_ACCEPTABLE,
        "message" : f'{exc.id_number} is not an acceptable value'
    })

from fastapi.exceptions import RequestValidationError
# @app.exception_handler(RequestValidationError)
# def the_name_is_not_important(request:Request, exc:RequestValidationError):
#     return JSONResponse({
#         "exeption" : str(exc),
#         "custom_exception": True,
#         "status code": status.HTTP_400_BAD_REQUEST,
#         "body" : exc.body
#     })

from starlette.exceptions import HTTPException as StarletteHTTPException 
# @app.exception_handler(StarletteHTTPException)
# def name_of_function(req: Request, exc:StarletteHTTPException):
#     return JSONResponse({
#         "exeption" : str(exc.detail),
#         "custom_exception": True,
#         "status code": status.HTTP_418_IM_A_TEAPOT,
#         "custom_starlette" : True
#     })

@app.get('/error/{item_id}')
def handling_error(item_id: Annotated[int, Path()]):
    """<h1>Error Handling</h1>

    **Args**:
        item_id (Annotated[int, Path): ID of item

    **Raises**:
        ErrorItem3: Model to handle with error in this function
        HTTPException: Default Exception raising that is modified

    **Returns**:
        item: Item ID
    """
    if item_id == 3:
        raise ErrorItem3(item_id)
    if item_id == 4:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="4 is not a good number")
    return {"item": item_id}

from fastapi.encoders import jsonable_encoder

@app.put('/error_two/', summary="Error handling", description="Another way of handling errors", response_description="Error or Item")
def handling_error2(item: Annotated[Item, Body()]):
    item_jsonable_encoder = jsonable_encoder(item) # Maybe I want to return not a complex type
    return item_jsonable_encoder


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

@app.patch('/items/{item_id}/', tags=[TagsEnum.item])
def update_path(item_id:str, item:ItemUpdate):
    try :
        saved_item = items[item_id]
    except :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not founded")
    instance_saved_item_model = ItemUpdate(**saved_item)
    body_data = item.model_dump(exclude_unset=True)

    new_data = instance_saved_item_model.model_copy(update=body_data)
    jsonable_encoder_new_data = jsonable_encoder(new_data)
    items[item_id] = jsonable_encoder_new_data
    print(items)
    return jsonable_encoder_new_data

class CommomDependencies:
    def __init__(self, a:str, b:int, c:bool):
        self.a = a
        self.b = b
        self.c = c

from fastapi import Depends

commom_annotated = Annotated[CommomDependencies, Depends()]

@app.get('/dependent-1/', tags=[TagsEnum.dependency])
def dependent_function(commom:commom_annotated):
    return commom

@app.get('/dependent-2/', tags=[TagsEnum.dependency])
def dependent_function(commom:commom_annotated):
    return commom

def sub_dependency(
        commom:Annotated[CommomDependencies, Depends()],
        another_field:str | None = None
    ):
    if another_field:
        return{"commom" : commom, "another":another_field}
    return {"commom":commom}

@app.get('/dependent-3/', tags=[TagsEnum.dependency])
def sub_dependencies(dependency:Annotated[any, Depends(sub_dependency)]):
    return dependency



@app.get('/path-dependency/', tags=[TagsEnum.dependency], dependencies=[Depends(get_token_header), Depends(get_key_header)])
def path_dependency():
    return {"Allow to see page" : True}


from fastapi.security import OAuth2PasswordBearer

o_auth_pass_bearer = OAuth2PasswordBearer(tokenUrl="token") # relative URL: https://example.com/ --> https://example.com/token

@app.get('/security', dependencies=[Depends(o_auth_pass_bearer)], tags=[TagsEnum.security])
def testing_security(token: Annotated[str, Depends(o_auth_pass_bearer)]):
    return {"token" : token}


def get_current_user_encrypted(token: Annotated[str, Depends(o_auth_pass_bearer)]):
    return UserIn2(username=token + " " + "Lucas", email="l@l.com", full_name="", password="asad")


@app.get('/user/me', tags=[TagsEnum.security])
def get_current_user(current_user: Annotated[UserIn2, Depends(get_current_user_encrypted)]):
    return current_user

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "$2b$12$zCOUSOkVRRU1JPE1mV7OR.OKUvA7COgC0pnCQ/EJI1aSCq4aqHA6i",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "password": "$2b$12$Sn9pgTKvFTln6eqHGjriwOmwa0m35bD25bKqiNQEyLUHXVRtaqVYi",
        "disabled": True,
    },
}



from fastapi.security import OAuth2PasswordRequestForm

### Just to remember
# class BaseUser(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserIn2(BaseUser):
#     password: str

def fake_hash_password(password:str):
    return f'hash...{password}'

import jwt
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

import os 
from dotenv import load_dotenv
load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create_hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

def create_token(data):
    payload = data.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration = str(int(expiration.timestamp()))
    payload.update({"exp" : expiration})
    print("payload", payload)
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

@app.post("/url_to_connect_with_RequestForm", tags=[TagsEnum.security])
def login_user(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]): # It
    user_from_db = fake_users_db.get(form_data.username)
    if not user_from_db :
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_instance = UserIn2(**user_from_db)
    if not verify_password(form_data.password, user_instance.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token" : create_token({"sub":str(user_instance.username)}), "token_type": "bearer"}

o_auth_RequestForm = OAuth2PasswordBearer(tokenUrl="url_to_connect_with_RequestForm")

def capturing_user(token: Annotated[str, Depends(o_auth_RequestForm)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_data = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_dict = fake_users_db[decoded_data['sub']]
    except:
        raise credentials_exception
    if not user_dict :
        raise credentials_exception
    user_instance = UserIn(**user_dict)
    return user_instance
    

@app.get("/current/user", tags=[TagsEnum.security])
def retrive_current_user(current_user:Annotated[BaseUser, Depends(capturing_user)]):
    return current_user # Now as is returning a user as capturing_user() is returning a user instance

from fastapi import Request
import time as time_2

@app.middleware("http")
async def time_in_header(req: Request, call_next):
    start_time = time_2.perf_counter()
    print(req.headers)
    response = await call_next(req)
    elapsed_time = time_2.perf_counter() - start_time
    response.headers["X-time-elapsed"] = str(elapsed_time)
    return response

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from sqlmodel import SQLModel, Field, create_engine, Session, select

class BaseHero(SQLModel):
    name: str = Field(index=True)
    age: int = Field(default=0, index=True)

class Heroes(BaseHero, table=True):
    id: int|None = Field(default=None, primary_key=True)
    secret_name: str 

class PublicHero(BaseHero):
    id:int

class HeroCreate(BaseHero):
    secret_name: str

class HeroUpdate(BaseHero):
    """
    Because all the fields actually change (the type now includes None and they now have a default value of None), we need to re-declare them
    """
    name: str|None = Field(default=None, index=True)
    age: int|None = Field(default=None, index=True)
    secret_name: str = Field(default=None)

database_name = "database.db"
database_url = f"sqlite:///{database_name}"
connect_args = {"check_same_thread":False}
engine = create_engine(
    database_url, 
    connect_args=connect_args
)

def create_all_table_and_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def creating_on_startup():
    create_all_table_and_db()

def get_session():
    with Session(engine) as session:
        yield session # It will provide a new Session for each request. This is what ensures that we use a single session per request

session_dependency = Annotated[Session, Depends(get_session)] # Help on database management

@app.post("/heroes", tags=[TagsEnum.hero], response_model=PublicHero)
def create_hero(hero: HeroCreate, session: session_dependency):
    db_hero = Heroes.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes", tags=[TagsEnum.hero], response_model=list[PublicHero])
def get_list_heroes(session: session_dependency):
    heroes = session.exec(select(Heroes)).all()
    return heroes

@app.get("/heroes/{hero_id}", tags=[TagsEnum.hero], response_model=PublicHero)
def get_one_hero(
    session: session_dependency,
    hero_id: Annotated[int, Path()],
    ):
    hero = session.get(Heroes, hero_id)
    print(hero)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not founded")
    return hero

@app.delete("/heroes/{hero_id}", tags=[TagsEnum.hero])
def delete_hero(
    session: session_dependency,
    hero_id: Annotated[int, Path()]
    ):
    hero = session.get(Heroes, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not founded")
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted"}

@app.patch("/heroes/{hero_id}", tags=[TagsEnum.hero], response_model=PublicHero)
def update_hero(
    session: session_dependency,
    hero_id: Annotated[int, Path()],
    hero_data: Annotated[HeroUpdate, Body()]
    ):
    hero_db = session.get(Heroes, hero_id)
    if not hero_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not founded")

    hero_body = hero_data.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_body)

    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db
