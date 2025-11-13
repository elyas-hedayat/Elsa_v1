import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases import get_session
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


@router.get("/", response_model=list[UserResponse])
async def list_users(session: Annotated[AsyncSession, Depends(get_session)]):
    return await user_service.user_list(session)


@router.get(
    "/me",
)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/{pk}", response_model=UserResponse)
async def get_user(
    pk: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    user_instance = await user_service.get_user_by_id(session=session, pk=pk)
    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")
    return user_instance


@router.delete("/{pk}/delete", status_code=204)
async def delete_user(
    pk: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]
):
    await user_service.delete_user(session=session, pk=pk)
    return {"message": "User deleted"}
