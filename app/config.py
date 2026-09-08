from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    admin_ids: str
    database_url: str = "sqlite+aiosqlite:///./diagnostic_bot.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def admin_id_list(self) -> list[int]:
        return [
            int(admin_id.strip())
            for admin_id in self.admin_ids.split(",")
            if admin_id.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()