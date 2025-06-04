from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base

from loguru import logger

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self._session = session
        if self.model is None:
            raise ValueError("Model must be specified in the child class.")

    async def find_one_or_none_by_id(self, data_id: int):
        try:
            query = select(self.model).filter_by(id=data_id)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Record {self.model.__name__} with ID {data_id} {'found' if record else 'not found'}."
            logger.info(log_message)
            return record
        except SQLAlchemyError as e:
            logger.error(f"Error finding record with ID {data_id}: {e}")
            raise

    async def find_one_or_none(self, filters: BaseModel):
        filter_dict = dict(filters)
        logger.info(f"find_one_or_none {self.model.__name__} by filters: {filter_dict}")
        try:
            query = select(self.model).filter_by(**filter_dict)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            log_message = f"Record {'found' if record else 'not found'} by filters: {filter_dict}"
            logger.info(log_message)
            return record
        except SQLAlchemyError as e:
            logger.error(f"Error finding record by filters {filter_dict}: {e}")
            raise

    async def add(self, values: BaseModel):
        values_dict = dict(values)
        logger.info(f"add new record {self.model.__name__} with values: {values_dict}")
        try:
            new_instance = self.model(**values_dict)
            self._session.add(new_instance)
            logger.info(f"Record {self.model.__name__} added.")
            await self._session.flush()
            return new_instance
        except SQLAlchemyError as e:
            logger.error(f"Error adding record: {e}")
            raise




