from typing import Any, List

from app.cruds import user as crud
from app.db.connect import get_db
from app.schemas import user as schema
from databases.core import Database as DB
from fastapi import APIRouter, Depends
from fastapi.responses import Response

router = APIRouter()


@router.get("/", response_model=List[schema.User])
async def read_user_list(offset: int = 0, limit=100, db: DB = Depends(get_db)):
    user = await crud.user.get_user_list(db, offset=offset, limit=limit)
    return user


@router.get("/{email}", response_model=schema.User)
async def read_user(email: str, db: DB = Depends(get_db)):
    user = await crud.user.get_user(db, email)
    return user


@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserIn, db: DB = Depends(get_db)):
    return await crud.user.create_user(db=db, user=user)


@router.patch("/{email}", response_model=schema.User)
async def update_user_me(
    email: str,
    user: schema.UserUpdate,
    db: DB = Depends(get_db),
) -> Any:
    """
    Update user.

    """
    current_user = await crud.user.get_user(db=db, email=email)
    if current_user is None:
        return Response(
            status_code=404,
        )

    current_user_obj = schema.User(**current_user)
    update_data = user.dict(exclude_unset=True)
    update_item = current_user_obj.copy(update=update_data, exclude={"created_at"})
    current_user_data = current_user_obj.dict(exclude={"created_at"})

    if current_user_data == update_item:
        return Response(
            status_code=202,
        )

    await crud.user.update(db, db_obj=current_user_obj, obj_in=update_item)
    user_after = await crud.user.get_user(db=db, email=email)
    return user_after
