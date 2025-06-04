import pytest
from app.links.dao import LinksDAO

@pytest.mark.asyncio
async def test_increment_click_not_found():
    class FakeSession:
        async def execute(self, query):
            class Result:
                def scalars(self):
                    class Scalars:
                        def first(self):
                            return None
                    return Scalars()
            return Result()
    dao = LinksDAO(FakeSession())
    result = await dao.increment_click("notfound")
    assert result is None 