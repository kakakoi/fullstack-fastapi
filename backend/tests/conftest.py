import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
