from pydantic import BaseModel, ConfigDict

from src.api.config.constants import STRINGS
from src.api.config.env import optional, require
from src.api.config.loader import load_environment
from src.api.models.strings import Strings


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Meta
    ENV: str

    # Secrets
    JWT_SECRET: str
    WEBHOOK_SECRET: str

    # Optional config
    DEBUG: bool = False

    # Constants
    STRINGS: Strings = STRINGS


def load_settings() -> Settings:
    env = load_environment()
    default_secret = "dev-secret-not-for-production" if env != "production" else None
    jwt_secret = optional("JWT_SECRET", default_secret) or require("JWT_SECRET")
    webhook_secret = optional("WEBHOOK_SECRET", default_secret) or optional("JWT_SECRET", default_secret) or "dev-webhook-secret"

    return Settings(
        ENV=env,
        JWT_SECRET=jwt_secret,
        WEBHOOK_SECRET=webhook_secret,
        DEBUG=optional("DEBUG", "false").lower() == "true",
        STRINGS=STRINGS,
    )


settings = load_settings()
