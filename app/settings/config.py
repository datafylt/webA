import os
import typing
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class Settings(BaseSettings):
    VERSION: str = "1.0.0"
    APP_TITLE: str = 'Formation Électro API'
    PROJECT_NAME: str = "Formation Électro"
    APP_DESCRIPTION: str = "Système de gestion de formation"

    CORS_ORIGINS: typing.List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "3488a63e1765035d386f05409663f55c83bfae3b3c61a932744b20ad14244dcf")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # ═══════════════════════════════════════════════════════════════════════
    # SMTP EMAIL - IONOS Configuration
    # ═══════════════════════════════════════════════════════════════════════
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.ionos.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "administration@formationelectro.com")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "administration@formationelectro.com")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Formation Électro")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "false").lower() == "true"
    SMTP_USE_SSL: bool = os.getenv("SMTP_USE_SSL", "true").lower() == "true"
    EMAIL_TEST_MODE: bool = os.getenv("EMAIL_TEST_MODE", "false").lower() == "true"
    
    TORTOISE_ORM: dict = {
        "connections": {
            "sqlite": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {"file_path": f"{BASE_DIR}/db_website_a.sqlite3"},
            },
        },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "sqlite",
            },
        },
        "use_tz": False,
        "timezone": "America/Montreal",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


settings = Settings()


# ═══════════════════════════════════════════════════════════════════════════
# SMTP PROVIDER PRESETS
# ═══════════════════════════════════════════════════════════════════════════

SMTP_PROVIDERS = {
    "ionos": {
        "host": "smtp.ionos.com",
        "port": 465,
        "use_tls": True,
        "use_ssl": False,
    },
    "gmail": {
        "host": "smtp.gmail.com",
        "port": 587,
        "use_tls": True,
        "use_ssl": False,
    },
    "outlook": {
        "host": "smtp.office365.com",
        "port": 587,
        "use_tls": True,
        "use_ssl": False,
    },
    "sendgrid": {
        "host": "smtp.sendgrid.net",
        "port": 587,
        "use_tls": True,
        "use_ssl": False,
    },
}
