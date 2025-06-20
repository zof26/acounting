from datetime import datetime, timezone
from typing import NamedTuple
import asyncio
import logging
import time

from zeep import Client
from zeep.exceptions import Fault, TransportError
from app.core.config import settings

logger = logging.getLogger(__name__)


class VATValidationResult(NamedTuple):
    valid: bool
    name: str
    address: str
    checked_at: datetime


def _sync_check_vat(vat_id: str, retries: int = 3, delay: float = 1.5) -> VATValidationResult:
    country_code = vat_id[:2].upper()
    vat_number = vat_id[2:].replace(" ", "").strip()
    checked_at = datetime.now(timezone.utc)

    client = Client(wsdl=settings.VIES_WSDL_URL)
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            result = client.service.checkVat(
                countryCode=country_code,
                vatNumber=vat_number
            )
            return VATValidationResult(
                valid=result["valid"],
                name=result.get("name", "").strip(),
                address=result.get("address", "").strip(),
                checked_at=checked_at,
            )
        except (Fault, TransportError, Exception) as e:
            last_error = e
            if settings.DEBUG:
                logger.warning(f"[VIES {type(e).__name__}] attempt {attempt}: {e}")

            # Only retry for temporary service faults
            if isinstance(e, Fault) and "MS_UNAVAILABLE" not in str(e).upper():
                break  # Permanent fault, no retry

            time.sleep(delay)

    if settings.DEBUG:
        logger.error(f"[VIES Failure] All {retries} attempts failed: {last_error}")
    return VATValidationResult(False, "", "", checked_at)


async def validate_vat_id(vat_id: str) -> VATValidationResult:
    if not vat_id or len(vat_id) < 3:
        return VATValidationResult(False, "", "", datetime.now(timezone.utc))

    return await asyncio.to_thread(_sync_check_vat, vat_id)
