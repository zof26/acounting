import os
import importlib.util
import logging
from fastapi import FastAPI, APIRouter
from app.core.config import settings

logger = logging.getLogger(__name__)


def autoload_routes(app: FastAPI):
    router = APIRouter()
    base_path = os.path.dirname(__file__)
    base_package = __name__  # 'app.routes'

    for root, _, files in os.walk(base_path):
        for file in files:
            if not file.endswith(".py") or file.startswith("_"):
                continue

            rel_path = os.path.relpath(os.path.join(root, file), base_path)
            module_path = rel_path.replace(os.sep, ".").removesuffix(".py")
            full_module_name = f"{base_package}.{module_path}"

            try:
                spec = importlib.util.find_spec(full_module_name)
                if spec is None:
                    continue
                module = importlib.import_module(full_module_name)
                if hasattr(module, "router"):
                    router.include_router(getattr(module, "router"))
                    logger.info(f"Loaded router from: {full_module_name}")
            except Exception as e:
                logger.warning(f"Failed to load router '{full_module_name}': {e}")

    app.include_router(router, prefix=settings.API_PREFIX)
