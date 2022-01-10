from typing import List

from databases.core import Database as DB
from fastapi import APIRouter, Depends

from app.cruds import user as crud
from app.db.connect import get_db
from app.schemas import user as schema

router = APIRouter()


@router.get("/", response_model=List[schema.User])
async def read_user_list(offset: int = 0, limit=100, db: DB = Depends(get_db)):
    user = await crud.get_user_list(db, offset=offset, limit=limit)
    return user


@router.get("/{email}", response_model=schema.User)
async def read_user(email: str, db: DB = Depends(get_db)):
    user = await crud.get_user(db, email)
    return user


@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserIn, db: DB = Depends(get_db)):
    return await crud.create_user(db=db, user=user)
