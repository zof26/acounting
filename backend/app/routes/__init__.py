import importlib
import pkgutil
from fastapi import FastAPI, APIRouter
from app.core.config import settings


def autoload_routes(app: FastAPI):
    router = APIRouter()
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{__name__}.{module_name}")
        if hasattr(module, "router"):
            router.include_router(getattr(module, "router"))
    app.include_router(router, prefix=settings.API_PREFIX)
