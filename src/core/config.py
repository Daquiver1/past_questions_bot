"""Setting up configs."""

# Third party imports
from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


PROJECT_NAME = "past_questions_bot"
VERSION = "1.0"
API_PREFIX = "/api"

# Environment
ENV = config("ENV", cast=str, default="development")

# Telegram
ADMIN_TELEGRAM_ID = config("ADMIN_TELEGRAM_ID", cast=int)
# Database[Sqlite3]
if ENV == "development":
    DATABASE_URL = config(
        "DATABASE_URL",
        cast=DatabaseURL,
        default="sqlite:///./past_questions_bot.db",
    )
else:
    DATABASE_URL = config(
        "TEST_DATABASE_URL",
        cast=DatabaseURL,
        default="sqlite:///./past_questions_bot_test.db",
    )


# Redis
REDIS_HOST = config("REDIS_HOST", cast=str)
REDIS_PORT = config("REDIS_PORT", cast=str)
REDIS_URL = config(
    "REDIS_URL",
    cast=str,
    default=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)

# S3
S3_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str)
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID", cast=str)
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY", cast=Secret)
S3_REGION = config("S3_REGION", cast=str)

# Sentry
SENTRY_DSN = config("SENTRY_DSN", cast=str, default=None)
SENTRY_ENVIRONMENT = config("SENTRY_ENVIRONMENT", cast=str, default=None)

# Paystack
PAYSTACK_BASE_URL = config("PAYSTACK_BASE_URL", cast=str)
if ENV == "development":
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_TEST_PUBLIC_KEY")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_TEST_SECRET_KEY")
else:
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_LIVE_PUBLIC_KEY")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_LIVE_SECRET_KEY")
