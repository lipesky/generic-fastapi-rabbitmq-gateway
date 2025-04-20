from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    port: int | None = None
    circuitbreaker_failure_threshold: int | None = 5
    circuitbreaker_recovery_timeout: int | None = 30
    rabbitmq_url: str
    environment: str = 'DEV'
    root_path: str | None = None
    broker_project_name: str | None = ''
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '.env'), frozen=True, extra='ignore')

@lru_cache
def get_settings():
    return Settings()

if __name__ == '__main__':
    print(get_settings())