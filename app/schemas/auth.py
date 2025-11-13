from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., example="oldPassword123")
    new_password: str = Field(..., example="newStrongPassword456")


class ChangePasswordResponse(BaseModel):
    message: str = Field(..., example="Password updated successfully")
