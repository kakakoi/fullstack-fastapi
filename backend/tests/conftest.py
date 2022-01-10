import pytest
from app.main import app
from httpx import AsyncClient


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
