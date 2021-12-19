from fastapi import FastAPI

import os
import json
from typing import Optional  #

import databases
import sqlalchemy

app = FastAPI()


SECRET_NAME = 'APICLUSTER_SECRET'
SECRET_JSON = json.loads(os.environ[SECRET_NAME])
DATABASE = 'postgresql'
USER = SECRET_JSON['username']
PASSWORD = SECRET_JSON['password']
HOST = SECRET_JSON['host']
PORT = SECRET_JSON['port']
DB_NAME = SECRET_JSON['dbname']
DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

DB = databases.Database(
    DATABASE_URL,
    min_size=0,
    max_size=50
)

ENGINE = sqlalchemy.create_engine(
    DATABASE_URL
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
