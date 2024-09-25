from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_MODELS_STR: str = (
        "GPT-4o,Llama 3.1 405,Claude 3.5 Sonnet,Gemini 1.5 Pro,\
        GPT-4o mini,Llama 3.1 70B,amba 1.5Large,Mixtral 8x22B,\
        Gemini 1.5Flash,Claude 3 Haiku,Llama 3.1 8B"
    )

    SIMULATION_INTERVAL: int = 3600
    NUM_DATA_POINTS: int = 100
    RANDOM_SEED: int = 42
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "llm_db"
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672
    RABBITMQ_QUEUE: str = "benchmarking_service"
    LOG_FILE: str = "simulation_service.log"
    CONSOLE_LOGGING: bool = True

    @property
    def LLM_MODELS(self) -> list[str]:
        return self.LLM_MODELS_STR.split(",")

    def get_database_url(self, db_name: str) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{db_name}"

    @property
    def DATABASE_URL(self) -> str:
        return self.get_database_url(self.POSTGRES_DB)

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    class Config:
        extra = "ignore"
        env_file = ".env"
        case_sensitive = False


settings = Settings()
