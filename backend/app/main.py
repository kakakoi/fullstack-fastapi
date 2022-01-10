from databases import Database
from fastapi import FastAPI
from fastapi.logger import logger

from app.api.api_v1.api import api_router
from app.api.root import root_router
from app.core.config import settings
from app.db.connect import DB, ENGINE, metadata

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=settings.DESCRIPTION_TXT,
)


try:
    # root_router is state_message
    app.include_router(root_router)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    metadata.create_all(ENGINE)

except Exception as e:
    logger.error(f"EXCEPTION: {e}")
    setattr(root_router, "state_message", "Exception: Init server process")

else:
    logger.info(f"Finished: Init server process ")
    setattr(root_router, "state_message", "running")


@app.on_event("startup")
async def startup():
    if type(DB) is Database:
        try:
            await DB.connect()
        except Exception as e:
            logger.error(f"EXCEPTION: {e}")
            setattr(root_router, "state_message", "Failed to Load: Startup event")
