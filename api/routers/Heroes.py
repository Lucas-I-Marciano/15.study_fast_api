from fastapi import APIRouter, Depends, Path, Body
from typing import Annotated
from api.db.Heroes import PublicHero, BaseHero, HeroCreate, HeroUpdate, Heroes

router = APIRouter(
    prefix="/heroes",
    tags=["Heroes"]
)

from api.db.Heroes import PublicHero, BaseHero, HeroCreate, HeroUpdate, Heroes

from api.db import get_session
from sqlmodel import Session, select

session_dependency = Annotated[Session, Depends(get_session)] # Help on database management


@router.post("", response_model=PublicHero)
def create_hero(hero: HeroCreate, session: session_dependency):
    db_hero = Heroes.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("", response_model=list[PublicHero])
def get_list_heroes(session: session_dependency):
    heroes = session.exec(select(Heroes)).all()
    return heroes

@router.get("/{hero_id}", response_model=PublicHero)
def get_one_hero(
    session: session_dependency,
    hero_id: Annotated[int, Path()],
    ):
    hero = session.get(Heroes, hero_id)
    print(hero)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not founded")
    return hero

@router.delete("/{hero_id}")
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

@router.patch("/{hero_id}", response_model=PublicHero)
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
