from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    algorithm: str = Field(alias="ALGORITHM")
    secret_key: str = Field(alias="SECRET_KEY")
    token_expire_min: int = Field(alias="TOKEN_EXPIRE_TIME")

    DB_NAME: str = Field(alias="DATABASE_NAME")
    DB_PASS: str = Field(alias="DATABASE_PASS")
    DB_USER: str = Field(alias="DATABASE_USER")
    DB_HOST: str = Field(alias="DATABASE_HOST")
    DB_PORT: str = Field(alias="DATABASE_PORT")

    TEST_DB_NAME: str = Field(alias="TEST_DATABASE_NAME")
    TEST_DB_PASS: str = Field(alias="TEST_DATABASE_PASS")
    TEST_DB_USER: str = Field(alias="TEST_DATABASE_USER")
    TEST_DB_HOST: str = Field(alias="TEST_DATABASE_HOST")
    TEST_DB_PORT: str = Field(alias="TEST_DATABASE_PORT")

    YANDEX_SPELLER_API_URL: str = Field(
        default="https://speller.yandex.net/services/spellservice.json/checkText"
    )

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"

    @property
    def test_database_url(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
