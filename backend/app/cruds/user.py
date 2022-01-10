from datetime import datetime
from typing import List

from databases.core import Database

from app.models.user import user as model
from app.schemas import user as schema


async def get_user(db: Database, email: str) -> schema.User:
    query = model.select().where(model.columns.user_email == email)
    user = await db.fetch_one(query)
    return user


async def get_user_list(
    db: Database, offset: int = 0, limit: int = 100
) -> List[schema.User]:
    query = model.select().offset(offset).limit(limit)
    return await db.fetch_all(query)


async def create_user(user: schema.User, db: Database):
    query = model.insert().values(
        user_email=user.user_email,
        user_name=user.user_name,
    )
    await db.execute(query)
    return {**user.dict(), "created_at": datetime.now().isoformat()}  # 仮
