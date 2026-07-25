from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    APP_ENV: str = "dev"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"
    ALLOWED_HOSTS: str = "*"

    # Database
    # SQLite（默认）: sqlite+aiosqlite:///./myweb.db
    # PostgreSQL:      postgresql+asyncpg://user:pass@host/db
    # MySQL:           mysql+aiomysql://user:pass@host/db
    DATABASE_URL: str = "sqlite+aiosqlite:///./myweb.db"

    # Redis（可选，本地开发可留空使用内存存储）
    REDIS_URL: str | None = None

    # JWT
    JWT_SECRET_KEY: str = "change-me"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Upload
    UPLOAD_DIR: Path = Path("./uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # API
    API_V1_PREFIX: str = "/api/v1"
    API_VERSION: str = "v1"

    # Cache
    CATEGORY_CACHE_TTL: int = 300  # 5 minutes

    @property
    def is_dev(self) -> bool:
        return self.APP_ENV == "dev"

    @property
    def is_prod(self) -> bool:
        return self.APP_ENV == "prod"

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_URL.startswith("postgresql")

    @property
    def is_mysql(self) -> bool:
        return self.DATABASE_URL.startswith("mysql")

    @property
    def has_redis(self) -> bool:
        return bool(self.REDIS_URL)

    @property
    def database_url_async(self) -> str:
        return self.DATABASE_URL

    # ClassVar to hold singleton
    _instance: ClassVar["Settings | None"] = None

    @classmethod
    def get(cls) -> Settings:
        if cls._instance is None:
            cls._instance = cls()  # type: ignore[call-arg]
        return cls._instance  # type: ignore[return-value]


settings = Settings.get()
