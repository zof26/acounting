from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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
        contact={
            "name": "Acounting Support",
            "email": settings.EMAIL_FROM,
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Log user-agent and IP on each request (for observability)
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("uvicorn.access")
        ua = request.headers.get("user-agent", "-")
        ip = request.client.host if request.client else "unknown"
        logger.info(f"Incoming request: {request.method} {request.url.path} from {ip} - UA: {ua}")
        return await call_next(request)

    # Register all routers dynamically
    autoload_routes(app)

    # Register global exception handlers
    register_exception_handlers(app)

    return app


app = create_app()
