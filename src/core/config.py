"""Setting up configs."""

# Third party imports
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


PROJECT_NAME = "past_questions_bot"
VERSION = "1.0"
API_PREFIX = "/api"

# Postgres
POSTGRES_USERNAME = config("POSTGRES_USERNAME", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str)
POSTGRES_DB = config("POSTGRES_DB", cast=str)
POSTGRES_PORT = config("POSTGRES_PORT", cast=str)
DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)

# Redis
REDIS_HOST = config("REDIS_HOST", cast=str)
REDIS_PORT = config("REDIS_PORT", cast=str)
REDIS_URL = config(
    "REDIS_URL",
    cast=str,
    default=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)

# s3
S3_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str)
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID", cast=str)
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY", cast=Secret)
S3_REGION = config("S3_REGION", cast=str)
