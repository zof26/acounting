import pytest
from app.services.vat_validation import validate_vat_id

@pytest.mark.anyio
async def test_validate_vat_id_real():
    # Known valid German VAT ID: SAP SE
    vat_id = "DE811193231"
    result = await validate_vat_id(vat_id)

    assert result.valid is True
    assert "SAP" in result.name.upper()
    assert result.address != ""
