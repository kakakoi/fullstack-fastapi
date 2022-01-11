from datetime import datetime
from typing import Any, Dict, List, Union

from app.models.user import user as model
from app.schemas import user as schema
from databases.core import Database
from fastapi.encoders import jsonable_encoder


class CRUDUser:
    async def get_user(self, db: Database, email: str) -> schema.User:
        query = model.select().where(model.columns.user_email == email)
        user = await db.fetch_one(query)
        return user

    async def update(
        self, db: Database, db_obj: dict, obj_in: Union[schema.User, Dict[str, Any]]
    ) -> schema.User:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        query = (
            model.update()
            .where(model.columns.user_email == obj_in.user_email)
            .values(obj_in.dict())
        )
        return await db.execute(query)

    async def get_user_list(
        self, db: Database, offset: int = 0, limit: int = 100
    ) -> List[schema.User]:
        query = model.select().offset(offset).limit(limit)
        return await db.fetch_all(query)

    async def create_user(self, user: schema.User, db: Database):
        query = model.insert().values(
            user_email=user.user_email,
            user_name=user.user_name,
        )
        await db.execute(query)
        return {**user.dict(), "created_at": datetime.now().isoformat()}  # 仮


user = CRUDUser()
