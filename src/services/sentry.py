"""Sentry class"""
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


class SentryInitializer:
    """Sentry initializer."""

    def __init__(self, dsn: str, environment: str) -> None:
        """Initialize Sentry."""
        sentry_sdk.init(
            dsn=dsn,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                StarletteIntegration(transaction_style="endpoint"),
            ],
            environment=environment,
            traces_sample_rate=0.1,
        )
