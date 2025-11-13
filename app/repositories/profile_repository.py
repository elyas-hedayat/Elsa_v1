import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self):
        super().__init__(Profile)

    async def create(self, session: AsyncSession, user_id: uuid.UUID) -> Profile:
        profile = Profile(user_id=user_id)
        return await self.add(session, profile)
