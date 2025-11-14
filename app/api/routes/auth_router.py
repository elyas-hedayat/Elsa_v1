import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
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
    """
    List all users.
    """
    return await user_service.user_list(session)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the currently authenticated user's info.
    """
    return current_user


@router.get("/{pk}", response_model=UserResponse)
async def get_user(pk: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]):
    """
    Get a user by their UUID.
    """
    user_instance = await user_service.get_user_by_id(session=session, pk=pk)
    if not user_instance:
        return {"error": "User not found"}  # Or raise HTTPException(status_code=404)
    return user_instance


@router.delete("/{pk}/delete", status_code=204)
async def delete_user(pk: uuid.UUID, session: Annotated[AsyncSession, Depends(get_session)]):
    """
    Delete a user by their UUID.
    """
    await user_service.delete_user(session=session, pk=pk)
