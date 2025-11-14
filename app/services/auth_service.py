from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.profile import Profile
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_repository import UserRepository

user_repo = UserRepository()
profile_repo = ProfileRepository()


class AuthService:
    async def register_user(self, session: AsyncSession, username: str, password: str) -> User:
        existing_user = await user_repo.get_by_username(session, username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = User(username=username, password=hash_password(password))
        created_user = await user_repo.add(session, user)

        profile = Profile(user_id=created_user.id)
        await profile_repo.add(session, profile)
        return created_user

    async def authenticate_user(self, session: AsyncSession, username: str, password: str):
        user = await user_repo.get_by_username(session, username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    async def change_password(
        self, session: AsyncSession, user: User, old_password: str, new_password: str
    ):
        if not verify_password(old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
            )

        user.password = hash_password(new_password)
        session.add(user)
        await session.commit()
        return {"message": "Password updated successfully"}
