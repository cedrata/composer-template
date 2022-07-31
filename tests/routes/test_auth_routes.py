import json

import pytest
from httpx import AsyncClient
from src.routes.auth import login
from tests import build_db_client, fastapi_app, BASE_URL


@pytest.mark.asyncio
async def test_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admin",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    assert response.status_code == 200
    response_json: dict = json.loads(response.text)
    assert "access_token" in response_json.keys()
    assert "refresh_token" in response_json.keys()
    assert "token_type" in response_json.keys()


@pytest.mark.asyncio
async def test_bad_username_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admon",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_bad_password_login():
    await build_db_client()
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admin",
                "password": "admon",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh():
    await build_db_client()

    # Generate a valid token.
    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        login_response = await ac.post(
            "/auth/login",
            data={
                "grant_type": "",
                "username": "admin",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh",
            headers={"Refresh-Token": json.loads(login_response.text)["refresh_token"]},
        )

    assert response.status_code == 200
    response_json: dict = json.loads(response.text)
    assert "access_token" in response_json.keys()
    assert "refresh_token" in response_json.keys()
    assert "token_type" in response_json.keys()


@pytest.mark.asyncio
async def test_expired_token_refresh():
    await build_db_client()

    # Add any expired token.
    # If this test is givin you issues, just create a new token with the key you are using and let it expire, then run again the test.
    expired_refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlcyI6W10sImV4cCI6MTY1OTIxOTgyNywiaXNfcmVmcmVzaCI6dHJ1ZX0.39q63PmDMVLe837vPMWPW37Wq0nRaEz0YRqlNpZUHtA"

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh", headers={"Refresh-Token": expired_refresh_token}
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_token_refresh():
    await build_db_client()

    # Add any invalid token.
    invalid_refresh_token = "pippo"

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh", headers={"Refresh-Token": invalid_refresh_token}
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_token_structure_refresh():
    await build_db_client()

    invalid_refresh_token = "eyJhbGciOiJIUzI1NiJ9.eyJpbnZhbGlkLWZpZWxkcyI6ImEgcmFuZG9tIHZhbHVlIn0.lEk4w_k3Sc-IzVeEWj0qIABdY2Nt5zClJPeLFN5FchA"

    async with AsyncClient(app=fastapi_app, base_url=BASE_URL) as ac:
        response = await ac.post(
            "/auth/refresh", headers={"Refresh-Token": invalid_refresh_token}
        )

    assert response.status_code == 403


# Maybe a test for bad payload ca be added, but it would be too much of a time effort.
