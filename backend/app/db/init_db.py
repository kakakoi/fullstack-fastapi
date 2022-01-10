from fastapi.applications import FastAPI

from app.db.connect import DB, ENGINE, metadata


def init_db(app: FastAPI):
    try:
        metadata.create_all(ENGINE)

    except AttributeError as e:
        print(f"EXCEPTION: {e}")
        setattr(app, "state_message", "Failed to Load: INIT DB 😢")
