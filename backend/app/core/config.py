import json
import os
from typing import Any, Dict, Optional

from fastapi.logger import logger
from pydantic import BaseSettings, PostgresDsn, validator

TESTING = os.getenv("TESTING", "False") == "True"


class Settings(BaseSettings):
    TESTING: bool = False
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "project"
    DESCRIPTION_TXT: str = "detail"

    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings: Settings
DB_SECRET_NAME = "APICLUSTER_SECRET"  # nosec
try:
    DB_SECRET_JSON = json.loads(os.environ[DB_SECRET_NAME])

    if not TESTING:
        settings = Settings(
            POSTGRES_USER=DB_SECRET_JSON["username"],
            POSTGRES_SERVER=DB_SECRET_JSON["host"],
            POSTGRES_PASSWORD=DB_SECRET_JSON["password"],
            POSTGRES_DB=DB_SECRET_JSON["dbname"],
        )
    else:
        settings = Settings(
            TESTING=TESTING, SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
        )
except KeyError as e:
    logger.error(f"EXCEPTION : {e}")
    # status.set_message("Failed to Load: NO ENV KEY 😢")
