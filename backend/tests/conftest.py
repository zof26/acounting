import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.core.config import settings

@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def initialized_app():
    yield app

@pytest.fixture
async def client(initialized_app):
    transport = ASGITransport(app=initialized_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c

@pytest.fixture
async def admin_token(client):
    response = await client.post(
        f"{settings.API_PREFIX}/auth/token",
        data={
            "username": settings.DEFAULT_ADMIN_EMAIL,
            "password": settings.DEFAULT_ADMIN_PASSWORD
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200, f"Auth failed: {response.text}"
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }