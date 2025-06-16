from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.logging import init_logging
from app.core.exceptions import register_exception_handlers
from app.routes import autoload_routes


def create_app() -> FastAPI:
    init_logging()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url=f"{settings.API_PREFIX}/docs",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        redoc_url=None,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    autoload_routes(app)

    # Register global exception handlers
    register_exception_handlers(app)

    return app


app = create_app()
