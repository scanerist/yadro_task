import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
# trouble with PATH, you can remove it if it works without any troubles
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app



@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_datetime_now(monkeypatch):
    import datetime as dt
    class MockedDatetime(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return dt.datetime(2025, 1, 1, 12, 0, 0, tzinfo=tz)
    import app.links.link_service as ls
    monkeypatch.setattr(ls, "datetime", MockedDatetime)
    yield
    monkeypatch.undo()