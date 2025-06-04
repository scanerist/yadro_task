from typing import Any

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings
from loguru import logger

class TokenService:
    @staticmethod
    def create_access_token(data: dict) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=settings.JWT_EXP_MINUTES)
        payload = data.copy()
        payload.update({"exp": expire, "type": "access"})
        logger.debug(f"Creating access token with payload: {payload}")
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            logger.debug(f"Decoded token payload: {payload}")
            return payload
        except JWTError:
            return None 