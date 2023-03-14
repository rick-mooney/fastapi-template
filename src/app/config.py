import os

APP_SECRET = os.environ.get("APP_SECRET")  # openssl rand -hex 32
AUTH_COOKIE_ID = 'test-token'
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
API_NAME = 'Test API'

ORIGINS = ["http://localhost:3000"]

class Scopes:
    ADMIN = "admin"
    USER = "user"


AUTH_SCOPES = {
    Scopes.ADMIN: "for admins",
    Scopes.USER: "for app users"
}

SENTRY_URL = os.environ.get('SENTRY_URL')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')


POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT: str = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB: str = os.getenv("POSTGRES_DB")
DB_CONNECTION_STR = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
TEST_DB_CONNECTION_STR = f"{DB_CONNECTION_STR}_testrun"