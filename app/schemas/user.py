import uuid
from datetime import date

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    job: str | None = None
    birthday: date | None = None
    address: str | None = None
    thumbnail: str | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    profile: ProfileResponse | None = None

    class Config:
        from_attributes = True
