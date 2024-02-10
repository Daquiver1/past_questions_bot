"""Config file for the project"""

import os

import dotenv

dotenv.load_dotenv()
TOKEN = os.environ["TOKEN"]
BASE_URL = os.environ["BASE_URL"]
ADMIN_TELEGRAM_ID = os.environ["ADMIN_TELEGRAM_ID"]
SENTRY_DSN_BOT = os.environ["SENTRY_DSN_BOT"]
ENVIRONMENT = os.environ.get("ENVIRONMENT", "DEVELOPMENT")
