from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases import get_session
from app.core.jwt import decode_access_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = HTTPBearer()
user_repo = UserRepository()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    token = credentials.credentials
    username = decode_access_token(token)
    print(username)
    user = await user_repo.get_by_username(session, username.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
