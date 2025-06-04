from fastapi import Depends, Query

from app.links.dao import LinksDAO
from app.dependencies.dao_dependency import get_session_with_commit
from app.dependencies.auth_dependency import get_current_user
from app.exceptions import ForbiddenException, LinkNotFoundException

from loguru import logger

def get_pagination_params(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)) -> tuple[int, int]:

    return skip, limit

async def get_link_by_code(short_code: str, session=Depends(get_session_with_commit)) -> LinksDAO:
    dao = LinksDAO(session)
    logger.debug(f"Fetching link with short code: {short_code}")
    link = await dao.find_one_or_none_by_field(short_code=short_code)
    if not link:
        raise LinkNotFoundException
    return link

async def get_owned_link(short_code: str, current_user=Depends(get_current_user), session=Depends(get_session_with_commit)) -> LinksDAO:
    link = await get_link_by_code(short_code, session)
    logger.debug(f"Checking ownership of link {link.short_code} for user {current_user.id}")
    if link.owner_id != current_user.id:
        raise ForbiddenException
    return link