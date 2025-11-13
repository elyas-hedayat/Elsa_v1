import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository

user_repo = UserRepository()


class UserService:
    async def user_list(
        self,
        session: AsyncSession,
    ) -> list[User]:
        return await user_repo.list_with_profile(session)

    async def get_user_by_id(self, pk: uuid.UUID, session: AsyncSession) -> User:
        return await user_repo.get_by_id(session, obj_id=pk)

    async def delete_user(self, session: AsyncSession, pk: uuid.UUID) -> None:
        user_instance = await self.get_user_by_id(session=session, pk=pk)
        if not user_instance:
            raise HTTPException(status_code=404, detail="User not found")
        await user_repo.delete(session=session, obj=user_instance)
