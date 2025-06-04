import pytest

USER1 = {"username": "user1", "password": "pass1"}
USER2 = {"username": "user2", "password": "pass2"}

async def register_and_login(client, username, password):
    await client.post("/api/auth/register", json={"username": username, "password": password})
    resp = await client.post("/api/auth/login", data={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["access_token"]

async def create_short_link(client, token, orig_url):
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post("/api/links/create", json={"orig_url": orig_url}, headers=headers)
    assert resp.status_code == 201
    return resp.json()

async def deactivate_link(client, token, short_code):
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.post(f"/api/links/{short_code}/deactivate", headers=headers)
    return resp

async def get_links(client, token, **params):
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/links/list", headers=headers, params=params)
    assert resp.status_code == 200
    return resp.json()

async def get_stats(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/api/links/stats", headers=headers)
    assert resp.status_code == 200
    return resp.json()

async def redirect(client, short_code):
    resp = await client.get(f"/{short_code}", follow_redirects=False)
    return resp


import uuid

@pytest.mark.anyio
async def test_create_and_list_links(async_client):
    username = f"linkuser_{uuid.uuid4().hex}"
    password = "linkpass"
    token = await register_and_login(async_client, username, password)
    headers = {"Authorization": f"Bearer {token}"}
    resp1 = await async_client.post("/api/links/create", json={"orig_url": "https://a.com"}, headers=headers)
    resp2 = await async_client.post("/api/links/create", json={"orig_url": "https://b.com"}, headers=headers)
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    resp = await async_client.get("/api/links/list", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    print("DATA:", data)
    assert any(l["orig_url"] == "https://a.com/" for l in data)
    assert any(l["orig_url"] == "https://b.com/" for l in data)

@pytest.mark.anyio
async def test_redirect_link(async_client):
    token = await register_and_login(async_client, "rediruser", "redirpass")
    link = await create_short_link(async_client, token, "https://fastapi.tiangolo.com/")
    short_code = link["short_code"]
    resp = await redirect(async_client, short_code)
    assert resp.status_code == 307
    assert resp.headers["location"] == "https://fastapi.tiangolo.com/"

@pytest.mark.anyio
async def test_deactivate_and_forbid_redirect(async_client):
    token = await register_and_login(async_client, "deactuser", "deactpass")
    link = await create_short_link(async_client, token, "https://deactivate.me/")
    short_code = link["short_code"]
    resp = await deactivate_link(async_client, token, short_code)
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False
    resp = await redirect(async_client, short_code)
    assert resp.status_code == 410

@pytest.mark.anyio
async def test_stats(async_client):
    token = await register_and_login(async_client, "statuser", "statpass")
    await create_short_link(async_client, token, "https://stat1.com/")
    await create_short_link(async_client, token, "https://stat2.com/")
    stats = await get_stats(async_client, token)
    assert isinstance(stats, list)
    assert all("link" in s for s in stats)

@pytest.mark.anyio
async def test_privacy(async_client):
    token1 = await register_and_login(async_client, "privuser1", "privpass1")
    token2 = await register_and_login(async_client, "privuser2", "privpass2")
    link1 = await create_short_link(async_client, token1, "https://private1.com/")
    link2 = await create_short_link(async_client, token2, "https://private2.com/")
    links1 = await get_links(async_client, token1)
    links2 = await get_links(async_client, token2)
    print("links1:", links1)
    print("link1:", link1)
    assert any(l["short_code"] == link1["short_code"] for l in links1)
    assert not any(l["short_code"] == link2["short_code"] for l in links1)
    assert any(l["short_code"] == link2["short_code"] for l in links2)
    assert not any(l["short_code"] == link1["short_code"] for l in links2)

@pytest.mark.anyio
async def test_errors(async_client):
    resp = await async_client.get("/api/links/list")
    assert resp.status_code == 401
    resp = await redirect(async_client, "notexist123")
    assert resp.status_code in (404, 410)

@pytest.mark.anyio
async def test_create_link_invalid_url(async_client):
    await async_client.post("/api/auth/register", json={"username": "badurl", "password": "badurl"})
    resp = await async_client.post("/api/auth/login", data={"username": "badurl", "password": "badurl"})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = await async_client.post("/api/links/create", json={"orig_url": "not_a_url"}, headers=headers)
    assert resp.status_code == 422

@pytest.mark.anyio
async def test_deactivate_foreign_link(async_client):
    await async_client.post("/api/auth/register", json={"username": "owner", "password": "owner"})
    resp = await async_client.post("/api/auth/login", data={"username": "owner", "password": "owner"})
    token1 = resp.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    resp = await async_client.post("/api/links/create", json={"orig_url": "https://onlyowner.com/"}, headers=headers1)
    short_code = resp.json()["short_code"]
    await async_client.post("/api/auth/register", json={"username": "other", "password": "other"})
    resp = await async_client.post("/api/auth/login", data={"username": "other", "password": "other"})
    token2 = resp.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    resp = await async_client.post(f"/api/links/{short_code}/deactivate", headers=headers2)
    assert resp.status_code == 403

@pytest.mark.anyio
async def test_redirect_not_found(async_client):
    resp = await async_client.get("/notexist123", follow_redirects=False)
    assert resp.status_code in (404, 410)