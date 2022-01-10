import os

import sqlalchemy
from app.core.config import settings
from databases import Database
from fastapi import HTTPException, status


def remove_sqlite_file():
    db_file_path = "./database.db"
    if os.path.exists(db_file_path):
        os.remove(db_file_path)


try:
    if settings.TESTING:
        remove_sqlite_file()
        DB = Database(settings.SQLALCHEMY_DATABASE_URI)
    else:
        DB = Database(settings.SQLALCHEMY_DATABASE_URI, min_size=0, max_size=50)

    ENGINE = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)
    metadata = sqlalchemy.MetaData()

except AttributeError as e:
    print(f"EXCEPTION: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Could not validate credentials",
    )
except sqlalchemy.exc.OperationalError as e:
    print(f"EXCEPTION: {e}")


async def get_db():
    yield DB
