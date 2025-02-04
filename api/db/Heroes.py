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