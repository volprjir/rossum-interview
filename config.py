import logging
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    def __init__(self, env_file: str = ".env"):
        self.model_config["env_file"] = env_file
        super().__init__()

    rossum_api: str = os.getenv("ROSSUM_API")
    rossum_username: str = os.getenv("ROSSUM_USERNAME")
    rossum_password: SecretStr = os.getenv("ROSSUM_PASSWORD")
    postbin_url: str = os.getenv("POSTBIN_URL")
    basic_auth_username: str = os.getenv("BASIC_AUTH_USERNAME")
    basic_auth_password: SecretStr = os.getenv("BASIC_AUTH_PASSWORD")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    server_port: int = int(os.getenv("SERVER_PORT", 8000))

    model_config = SettingsConfigDict()

settings = Settings()

