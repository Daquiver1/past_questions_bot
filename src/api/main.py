"""Server Setup."""

# Third party imports
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.routes.user import router as user_router
from src.api.routes.past_question import router as past_question_router
from src.api.routes.download import router as download_router
from src.api.routes.help_ticket import router as help_ticket_router
from src.api.routes.paystack import router as paystack_router
from src.core import config, tasks


def get_application() -> FastAPI:
    """Server configs."""
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # event handlers
    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    @app.get("/", name="index")
    async def index() -> str:
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."

    @app.get("/sentry-debug")
    async def trigger_error():
        division_by_zero = 1 / 0

    app.include_router(user_router, prefix="/user", tags=["user"])
    app.include_router(
        past_question_router, prefix="/past_question", tags=["past_question"]
    )
    app.include_router(paystack_router, prefix="/paystack", tags=["paystack"])
    app.include_router(download_router, prefix="/download", tags=["download"])
    app.include_router(help_ticket_router, prefix="/help_ticket", tags=["help_ticket"])

    return app


app = get_application()
