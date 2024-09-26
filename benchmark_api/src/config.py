from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    API_KEY: str
    LOG_FILE: str = "benchmarking_api_service.log"
    CONSOLE_LOGGING: bool = False
    CACHE_EXPIRATION: int = 3600
    REDIS_HOST: str
    REDIS_PORT: int

    def get_database_url(self, db_name: str) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"

    @property
    def DATABASE_URL(self) -> str:
        return self.get_database_url(self.POSTGRES_DB)

    class Config:
        extra = "ignore"
        env_file = ".env"
        case_sensitive = False


settings = Settings()
