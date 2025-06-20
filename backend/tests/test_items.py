import pytest
from decimal import Decimal
from uuid import UUID

BASE_URL = "/api/v1/items"


@pytest.mark.anyio
async def test_create_item_minimal(client, auth_headers):
    payload = {
        "name": "Basic Service",
        "unit_price": 100,
        "vat_rate": 19,
    }
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Basic Service"
    assert Decimal(data["unit_price"]) == Decimal("100")
    return data["id"]


@pytest.mark.anyio
async def test_create_item_full(client, auth_headers):
    payload = {
        "name": "Design Package",
        "description": "A full design sprint",
        "type": "bundle",
        "unit": "package",
        "unit_price": "999.99",
        "cost_price": "400.50",
        "vat_rate": "7.0",
        "external_id": "SKU-1234",
        "is_active": True,
    }
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert data["type"] == "bundle"
    assert Decimal(data["unit_price"]) == Decimal("999.99")
    assert data["unit"] == "package"


@pytest.mark.anyio
async def test_create_item_invalid_payload(client, auth_headers):
    payload = {
        "unit_price": -5,
        "vat_rate": 200
    }
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 422


@pytest.mark.anyio
async def test_list_items_pagination(client, auth_headers):
    r = await client.get(BASE_URL + "?skip=0&limit=5", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.anyio
async def test_get_item_valid(client, auth_headers):
    item_id = await test_create_item_minimal(client, auth_headers)
    r = await client.get(f"{BASE_URL}/{item_id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == item_id


@pytest.mark.anyio
async def test_get_item_invalid(client, auth_headers):
    r = await client.get(f"{BASE_URL}/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.anyio
async def test_update_item_partial(client, auth_headers):
    item_id = await test_create_item_minimal(client, auth_headers)
    patch = await client.patch(f"{BASE_URL}/{item_id}", json={"description": "Updated"}, headers=auth_headers)
    assert patch.status_code == 200
    assert patch.json()["description"] == "Updated"


@pytest.mark.anyio
async def test_update_item_full_overwrite(client, auth_headers):
    item_id = await test_create_item_minimal(client, auth_headers)
    payload = {
        "name": "Overwritten",
        "type": "product",
        "unit": "unit",
        "unit_price": 300,
        "cost_price": 150,
        "vat_rate": 0,
        "external_id": "SKU-NEW",
        "is_active": False,
    }
    r = await client.patch(f"{BASE_URL}/{item_id}", json=payload, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Overwritten"
    assert not data["is_active"]
    assert Decimal(data["vat_rate"]) == Decimal("0")


@pytest.mark.anyio
async def test_update_item_invalid_id(client, auth_headers):
    r = await client.patch(f"{BASE_URL}/00000000-0000-0000-0000-000000000000", json={"name": "Nope"}, headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.anyio
async def test_delete_item_valid(client, auth_headers):
    item_id = await test_create_item_minimal(client, auth_headers)
    d = await client.delete(f"{BASE_URL}/{item_id}", headers=auth_headers)
    assert d.status_code == 204

    # Ensure it’s actually gone
    r = await client.get(f"{BASE_URL}/{item_id}", headers=auth_headers)
    assert r.status_code == 404


@pytest.mark.anyio
async def test_delete_item_invalid(client, auth_headers):
    r = await client.delete(f"{BASE_URL}/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert r.status_code == 404
