from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "Name example"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id" : "12",
    "signup_ts": "1999-01-07",
    "friends" : [1, "2", br"3"],
}

user = User(**external_data)
print(user) #id=12 name='Name example' signup_ts=datetime.datetime(1999, 1, 7, 0, 0) friends=[1, 2, 3]