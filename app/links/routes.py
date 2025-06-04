from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from app.links.schemas import LinkCreate, LinkRead, LinkStats
from app.links.link_service import LinkService
from app.dependencies.links_dependency import get_owned_link, get_pagination_params
from app.dependencies.dao_dependency import get_session_with_commit
from app.dependencies.auth_dependency import get_current_user

from loguru import logger

public_router = APIRouter()
private_router = APIRouter(tags=["private"])


@private_router.post("/create",
                     response_model=LinkRead,
                     status_code=status.HTTP_201_CREATED,
                     summary="Create a short link",
                     description="Creates a short link for the provided original URL. The link will be active for 24 hours by default.",
                     responses={
                         201: {"description": "Short link created successfully"},
                         400: {"description": "Invalid URL or other validation errors"},
                     })
async def create_short_link(
        link: LinkCreate,
        session=Depends(get_session_with_commit),
        current_user=Depends(get_current_user)
):
    logger.info(f"Creating short link for user {current_user.id} with URL: {link.orig_url}")
    link = await LinkService.create_link(session, link.orig_url, current_user.id)
    logger.info(f"Short link created: {link.short_code} for user {current_user.id}")
    return link


@private_router.get("/list",
                    response_model=list[LinkRead],
                    summary="Liст all links for the user",
                    description="Retrieves a list of all short links created by the user. You can filter by active status and paginate results.",
                    responses={
                        200: {"description": "List of links retrieved successfully"},
                        404: {"description": "No links found for the user"},
                        400: {"description": "Invalid parameters for filtering or pagination"}
                    }
                    )
async def list_links(
        session=Depends(get_session_with_commit),
        current_user=Depends(get_current_user),
        pagination: tuple[int, int] = Depends(get_pagination_params),
        is_active: bool | None = None,
) -> list[LinkRead]:
    skip, limit = pagination
    logger.info(
        f"Listing links for user {current_user.id} with active status: {is_active}, skip: {skip}, limit: {limit}")
    user_list_links = await LinkService.list_links(session, current_user.id, is_active, skip, limit)
    logger.info(f"Links listed for user {current_user.id}: {len(user_list_links)} links found")
    return user_list_links


@private_router.post("/{short_code}/deactivate",
                     response_model=LinkRead,
                     summary="Deactivate a short link",
                     description="Deactivates a short link, making it no longer accessible. The link will not be deleted, but its status will be set to inactive.",
                     responses={
                         200: {"description": "Short link deactivated successfully"},
                         404: {"description": "Link not found or you do not have permission to access this link"},
                     })
async def deactivate_short_link(
        link=Depends(get_owned_link),
        session=Depends(get_session_with_commit),
        current_user=Depends(get_current_user)
) -> LinkRead:
    logger.info(f"Deactivating link {link.short_code} for user {current_user.id}")
    deactivating = await LinkService.deactivate_link(session, link)
    logger.info(f"Link {link.short_code} deactivated for user {current_user.id}")
    return deactivating


@private_router.get("/stats",
                    response_model=list[LinkStats],
                    summary="Get link statistics",
                    description="Retrieves statistics for all links created by the user, including click counts and creation dates.",
                    responses={
                        200: {"description": "Link statistics retrieved successfully"},
                        404: {"description": "No links found for the user"}
                    })
async def stats(
        session=Depends(get_session_with_commit),
        current_user=Depends(get_current_user)
) -> list[LinkStats]:
    logger.info(f"Retrieving link statistics for user {current_user.id}")
    links_stats = await LinkService.get_link_stats(session, current_user.id)
    logger.info(f"Link statistics retrieved for user {current_user.id}")
    return links_stats


@public_router.get("/{short_code}",
                   summary="Redirect to original URL",
                   description="Redirects to the original URL associated with the short link. If the link is expired or not found, an error will be raised.",
                   responses={
                       302: {"description": "Redirected to the original URL"},
                       404: {"description": "Link not found or expired"},
                   }
                   )
async def redirect_link(
        short_code: str,
        session=Depends(get_session_with_commit),
) -> RedirectResponse:
    logger.info(f"Redirecting short code: {short_code}")
    link = await LinkService.redirect_link(session, short_code)
    logger.info(f"Link found: {link.short_code} with original URL: {link.orig_url}, incrementing click count")
    return RedirectResponse(url=link.orig_url)
