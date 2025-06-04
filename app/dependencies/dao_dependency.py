from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.database import async_session_maker

from loguru import logger

async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            logger.debug("Starting a new database session")
            yield session
            logger.debug("Committing the database session")
            await session.commit()
        except Exception as e:
            logger.error(f"An error occurred during the database session: {e}, rolling back")
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            logger.debug("Starting a new database session without commit")
            yield session
        except Exception as e:
            logger.error(f"An error occurred during the database session: {e}, rolling back")
            await session.rollback()
            raise
        finally:
            await session.close()