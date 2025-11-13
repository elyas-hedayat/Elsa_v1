from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.auth import (
    ChangePasswordRequest,
    ChangePasswordResponse,
    LoginRequest,
    RegisterRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register")
async def register(
    data: RegisterRequest, session: Annotated[AsyncSession, Depends(get_session)]
):
    user = await auth_service.register_user(session, data.username, data.password)
    return {"message": "User created", "user_id": user.id}


@router.post("/login")
async def login(
    data: LoginRequest, session: Annotated[AsyncSession, Depends(get_session)]
):
    return await auth_service.authenticate_user(session, data.username, data.password)


@router.post(
    "/change-password",
    response_model=ChangePasswordResponse,
    summary="Change current user password",
    description="Requires valid Bearer token. User must provide old and new password.",
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    result = await auth_service.change_password(
        session,
        current_user,
        data.old_password,
        data.new_password,
    )
    return result
