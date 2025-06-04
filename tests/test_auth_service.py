import pytest
from app.auth.user_service import AuthService
from app.auth.schemas import UserRegister
from fastapi import HTTPException

class FakeSession:
    async def execute(self, query):
        class Result:
            def scalar_one_or_none(self):
                return type("User", (), {"username": "user", "password_hash": "hash"})()
        return Result()
    async def commit(self): pass
    async def refresh(self, obj): pass

@pytest.mark.asyncio
async def test_register_duplicate():
    session = FakeSession()
    with pytest.raises(HTTPException) as excinfo:
        await AuthService.register(session, UserRegister(username="user", password="123"))
    assert excinfo.value.status_code == 409