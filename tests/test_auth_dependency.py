import pytest
from app.dependencies.auth_dependency import get_current_user
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    class FakeSession: pass
    with pytest.raises(HTTPException):
        await get_current_user(token="badtoken", session=FakeSession()) 