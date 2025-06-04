from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.links.models import Link
from app.links.utils import generate_short_code

from loguru import logger


class LinksDAO(BaseDAO):
    model = Link

    async def create_link(self, orig_url: str, owner_id: int):
        logger.info(f"Creating link for URL: {orig_url} with owner ID: {owner_id}")
        try:
            short_code = generate_short_code()
            expires_at = datetime.now() + timedelta(days=1)
            link = Link(
                short_code=short_code,
                orig_url=str(orig_url),
                is_active=True,
                created_at=datetime.now(),
                expires_at=expires_at,
                click_count=0,
                owner_id=owner_id
            )
            self._session.add(link)
            await self._session.commit()
            await self._session.refresh(link)
            log_message = f"Link created with short code: {short_code} for owner ID: {owner_id}"
            logger.info(log_message)
            return link
        except SQLAlchemyError as e:
            logger.error(f"Error creating link: {e}")
            await self._session.rollback()
            raise

    async def get_by_short_code(self, short_code: str):
        try:
            query = select(self.model).where(self.model.short_code == short_code)
            result = await self._session.execute(query)
            log_message = f"Retrieving link by short code: {short_code}"
            logger.info(log_message)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving link by short code {short_code}: {e}")
            raise

    async def get_links_for_user(self, owner_id: int, is_active: bool | None = None, skip: int = 0,
                                 limit: int = 10):
        try:
            query = select(self.model).where(self.model.owner_id == owner_id)
            if is_active is not None:
                query = query.where(self.model.is_active == is_active)
            query = query.offset(skip).limit(limit)
            result = await self._session.execute(query)
            log_message = f"Retrieving links for user ID: {owner_id}, active: {is_active}, skip: {skip}, limit: {limit}"
            logger.info(log_message)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving links for user {owner_id}: {e}")
            raise

    async def deactivate_link(self, link: Link):
        try:
            link.is_active = False
            await self._session.commit()
            await self._session.refresh(link)
            log_message = f"Link {link.short_code} deactivated successfully."
            logger.info(log_message)
            return link
        except SQLAlchemyError as e:
            logger.error(f"Error deactivating link {link.short_code}: {e}")
            await self._session.rollback()
            raise

    async def get_link_stats(self, user_id: int):
        try:
            query = select(
                self.model.short_code,
                self.model.orig_url,
                self.model.click_count,
                self.model.created_at,
                self.model.expires_at
            ).where(self.model.owner_id == user_id)
            result = await self._session.execute(query)
            log_message = f"Retrieving link stats for user ID: {user_id}"
            logger.info(log_message)
            return result.all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving link stats for user {user_id}: {e}")
            raise

    async def increment_click(self, short_code: str):
        try:
            link = await self.find_one_or_none_by_field(short_code=short_code)
            if link:
                link.click_count += 1
                await self._session.commit()
                await self._session.refresh(link)
                return link
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error incrementing click for link {short_code}: {e}")
            await self._session.rollback()
            raise

    async def find_one_or_none_by_field(self, **kwargs):
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self._session.execute(query)
            item = result.scalars().first()
            log_message = f"Finding link by field {kwargs}: {'found' if item else 'not found'}"
            logger.info(log_message)
            return item
        except SQLAlchemyError as e:
            logger.error(f"Error finding link by field {kwargs}: {e}")
            raise
