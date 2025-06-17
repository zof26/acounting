from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.logging import init_logging
from app.core.exceptions import register_exception_handlers
from app.routes import autoload_routes

from app.models.enums import RoleEnum
from app.models.enums import LanguageEnum
from app.models.enums import CurrencyEnum
from app.schemas.user import UserCreate
from app.db.session import async_session
from app.crud.user import get_user_by_email, create_user

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === Startup ===
    init_logging()
    async with async_session() as db:
        existing = await get_user_by_email(db, settings.DEFAULT_ADMIN_EMAIL)
        if not existing:
            user_in = UserCreate(
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                first_name=settings.DEFAULT_ADMIN_FIRST_NAME,
                last_name=settings.DEFAULT_ADMIN_LAST_NAME,
                preferred_language=LanguageEnum.en,
                preferred_currency=CurrencyEnum.EUR,
                role=RoleEnum.Admin,
                is_active=True,
            )
            await create_user(db, user_in)
            logger.info(f"Default admin created: {user_in.email}")
        else:
            logger.info(f"ℹDefault admin already exists: {existing.email}")
    yield
    # === Shutdown ===
    # We don't really need to do any teardown here

def create_app() -> FastAPI:
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
        lifespan=lifespan,
    )

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