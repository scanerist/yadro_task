from app.exceptions import LinkNotFoundException
from app.links.dao import LinksDAO
from app.links.models import Link
from app.links.schemas import LinkStats


class LinkService:
    @staticmethod
    async def create_link(session, orig_url: str, owner_id: int) -> Link:
        dao = LinksDAO(session)
        return await dao.create_link(orig_url=orig_url, owner_id=owner_id)

    @staticmethod
    async def get_link_by_code(session, short_code: str):
        dao = LinksDAO(session)
        return await dao.find_one_or_none_by_field(short_code=short_code)

    @staticmethod
    async def list_links(session, owner_id: int, is_active=None, skip=0, limit=10):
        dao = LinksDAO(session)
        return await dao.get_links_for_user(owner_id=owner_id, is_active=is_active, skip=skip, limit=limit)

    @staticmethod
    async def deactivate_link(session, link: Link):
        dao = LinksDAO(session)
        return await dao.deactivate_link(link)

    @staticmethod
    async def increment_click(session, short_code: str):
        dao = LinksDAO(session)
        return await dao.increment_click(short_code)

    @staticmethod
    async def get_link_stats(session, owner_id: int):
        dao = LinksDAO(session)
        raw_stats = await dao.get_link_stats(owner_id)
        stats = []
        for row in raw_stats:
            stats.append(LinkStats(
                link=row[0],
                orig_link=row[1],
                last_hour_clicks=row[2] if len(row) > 2 else 0,
                last_day_clicks=row[2] if len(row) > 2 else 0,
            ))
        return stats

    @staticmethod
    async def redirect_link(session, short_code: str):
        link = await LinkService.get_link_by_code(session, short_code)
        if not link or not link.is_active:
            raise LinkNotFoundException
        await LinkService.increment_click(session, short_code)
        return link
