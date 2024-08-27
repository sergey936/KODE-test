from dataclasses import dataclass

from httpx import AsyncClient

from logic.exceptions.yandex import YandexServiceIntegrationException
from settings.config import Config


@dataclass
class YandexService:
    config: Config
    http_client: AsyncClient

    async def validate_text(self, text: str) -> list[dict] | None:
        response = await self.http_client.post(
            url=self.config.YANDEX_SPELLER_API_URL, data={"text": text}
        )
        if response.status_code != 200:
            raise YandexServiceIntegrationException()

        return response.json()
