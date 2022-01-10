import pytest
import starlette.status
from app.core.config import settings
from tests.validate import validate_iso8601


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post(
        f"{settings.API_V1_STR}/user/",
        json={"user_email": "user@example.com", "user_name": "テスト名前"},
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["user_email"] == "user@example.com"
    assert response_obj["user_name"] == "テスト名前"

    response = await async_client.get(f"{settings.API_V1_STR}/user/")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["user_name"] == "テスト名前"
    assert response_obj[0]["user_email"] == "user@example.com"
    assert validate_iso8601(response_obj[0]["created_at"])
