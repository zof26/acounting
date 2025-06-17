import os
import importlib.util
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

models_dir = Path(__file__).parent
base_package = __name__  # 'app.models'

for file in os.listdir(models_dir):
    if file.startswith("_") or not file.endswith(".py"):
        continue

    module_name = file.removesuffix(".py")
    full_module = f"{base_package}.{module_name}"

    try:
        spec = importlib.util.find_spec(full_module)
        if spec:
            importlib.import_module(full_module)
            logger.info(f"Loaded model module: {full_module}")
    except Exception as e:
        logger.warning(f"Failed to import model module '{full_module}': {e}")

from sqlmodel import SQLModel
logger.info(f"Registered tables: {list(SQLModel.metadata.tables.keys())}")
