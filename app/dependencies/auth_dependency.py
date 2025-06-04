from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.dependencies.dao_dependency import get_session_with_commit
from app.auth.token_service import TokenService
from app.exceptions import InvalidTokenException, UserNotFoundException

from loguru import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session_with_commit)):
    payload = TokenService.decode_token(token)
    logger.debug(f"Decoded token payload: {payload}")
    if not payload or "sub" not in payload:
        logger.error("Invalid token payload or missing 'sub' field")
        raise InvalidTokenException
    user_id = int(payload["sub"])
    dao = UsersDAO(session)
    logger.debug(f"Fetching user with ID: {user_id}")
    user = await dao.find_one_or_none(filters={"id": user_id})
    if not user:
        raise UserNotFoundException
    return user


