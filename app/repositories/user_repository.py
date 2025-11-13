from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def list_with_profile(self, session: AsyncSession):
        stmt = select(User).options(selectinload(User.profile))
        result = await session.execute(stmt)
        return result.scalars().unique().all()

    async def add(self, session: AsyncSession, obj: User) -> User:
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def get_by_username(self, session: AsyncSession, username: str):
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
