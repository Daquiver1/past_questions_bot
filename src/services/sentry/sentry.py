import sentry_sdk


class SentryClass:
    def __init__(
        self,
    ):
        sentry_sdk.init(
            dsn="https://6544a59a7d5f4587837a28b4e9cbbaf4@o4505263376171008.ingest.sentry.io/4505263390523392",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
        )
