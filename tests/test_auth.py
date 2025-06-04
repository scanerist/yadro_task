import pytest

USER = {"username": "testuser", "password": "testpass"}

@pytest.mark.anyio
async def test_register_and_login(async_client):
    resp = await async_client.post("/api/auth/register", json=USER)
    assert resp.status_code in (200, 201, 409)
    resp = await async_client.post("/api/auth/login", data=USER)
    assert resp.status_code == 200
    assert "access_token" in resp.json()

@pytest.mark.anyio
async def test_login_wrong_password(async_client):
    await async_client.post("/api/auth/register", json={"username": "user2", "password": "pass2"})
    resp = await async_client.post("/api/auth/login", data={"username": "user2", "password": "wrong"})
    assert resp.status_code in (400, 401) 