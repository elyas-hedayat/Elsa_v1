import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    job: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None
    thumbnail: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    profile: Optional[ProfileResponse] = None

    class Config:
        from_attributes = True
