import os
import secrets
import warnings
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class ENV(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


ENVIRONMENT = ENV(os.getenv("ENV", ENV.PRODUCTION.value))


def _get_jwt_secret() -> str:
    """Return the JWT secret from the environment.

    Falls back to a cryptographically random 32-byte hex string when the env
    var is absent (acceptable only in development/testing). Logs a warning so
    operators cannot miss the misconfiguration in production.
    """
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        secret = secrets.token_hex(32)
        warnings.warn(
            "JWT_SECRET_KEY is not set. A random key has been generated for this "
            "process. Tokens will be invalidated on restart. Set JWT_SECRET_KEY "
            "to a strong, stable secret in production.",
            stacklevel=2,
        )
    return secret


class Settings:
    JWT_SECRET_KEY = _get_jwt_secret()
    CHEF_USERNAME = os.getenv("CHEF_USERNAME", "chef")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "restaurant")

    TITLE: str = "Damn Vulnerable RESTaurant"
    DESCRIPTION: str = (
        "An intentionally vulnerable API service designed for learning and training purposes for ethical hackers, security engineers"
        ", and developers."
    )
    VERSION: str = "1.0.0"

    # Allow switching between Postgres (default) and in-memory SQLite.
    # This keeps Postgres as the default behavior while enabling
    # self-contained in-memory runs when DB_BACKEND=memory is set.
    DB_BACKEND: str = os.getenv("DB_BACKEND", "postgres")

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_BACKEND == "memory":
            return "sqlite://"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def SERVER_URL(self) -> str:
        return "http://localhost:8091/"

    @property
    def SERVERS(self) -> list[dict]:
        return [{"url": self.SERVER_URL, "description": self.SERVER_DESCRIPTION}]

    @property
    def ROOT_PATH(self) -> str:
        return ""

    @property
    def SERVER_DESCRIPTION(self) -> str:
        return "Local API server"


settings = Settings()
