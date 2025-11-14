import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, obj_id: uuid.UUID) -> ModelType | None:
        """Get user by ID with profile eagerly loaded"""
        result = await session.execute(
            select(self.model)
            .options(selectinload(self.model.profile))
            .where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def add(self, session: AsyncSession, obj: ModelType) -> ModelType:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, obj: ModelType):
        await session.delete(obj)
        await session.commit()
