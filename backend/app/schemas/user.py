import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserIn(BaseModel):
    user_email: Optional[EmailStr] = Field(None)
    user_name: str = Field(max_length=100)


class UserUpdate(UserIn):
    pass


class User(UserIn):
    created_at: datetime.datetime
