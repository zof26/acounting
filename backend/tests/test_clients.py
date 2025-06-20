import pytest
from uuid import UUID

BASE_URL = "/api/v1/clients"

# ---- CLIENT TESTS ----

@pytest.mark.anyio
async def test_create_client_minimal(client, auth_headers):
    payload = {"name": "Basic Client", "type": "Client"}
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "Basic Client"


@pytest.mark.anyio
async def test_create_client_with_contacts(client, auth_headers):
    payload = {
        "name": "Client With Contacts",
        "type": "Client",
        "contacts": [
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com",
                "phone": "123",
                "mobile": "321",
                "position": "CEO",
                "notes": "Main",
                "is_main_contact": True,
            }
        ]
    }
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 201
    data = r.json()
    assert len(data["contacts"]) == 1
    return data["id"], data["contacts"][0]["id"]


@pytest.mark.anyio
async def test_create_client_invalid_contact(client, auth_headers):
    payload = {
        "name": "Broken Client",
        "type": "Client",
        "contacts": [
            {
                "first_name": "John"
                # missing last_name, email, etc.
            }
        ]
    }
    r = await client.post(BASE_URL + "/", json=payload, headers=auth_headers)
    assert r.status_code == 422


@pytest.mark.anyio
async def test_get_client_valid(client, auth_headers):
    resp = await client.post(BASE_URL + "/", json={"name": "GetTest", "type": "Client"}, headers=auth_headers)
    client_id = resp.json()["id"]
    get = await client.get(f"{BASE_URL}/{client_id}", headers=auth_headers)
    assert get.status_code == 200
    assert get.json()["id"] == client_id


@pytest.mark.anyio
async def test_get_client_invalid_id(client, auth_headers):
    resp = await client.get(f"{BASE_URL}/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_list_clients_paginated(client, auth_headers):
    r = await client.get(BASE_URL + "?skip=0&limit=10", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.anyio
async def test_update_client_valid(client, auth_headers):
    r = await client.post(BASE_URL + "/", json={"name": "UpdateMe", "type": "Client"}, headers=auth_headers)
    client_id = r.json()["id"]
    patch = await client.patch(f"{BASE_URL}/{client_id}", json={"notes": "updated"}, headers=auth_headers)
    assert patch.status_code == 200
    assert patch.json()["notes"] == "updated"


@pytest.mark.anyio
async def test_update_client_invalid_id(client, auth_headers):
    r = await client.patch(f"{BASE_URL}/00000000-0000-0000-0000-000000000000", json={"notes": "fail"}, headers=auth_headers)
    assert r.status_code == 404


# ---- CONTACT TESTS ----

@pytest.mark.anyio
async def test_add_list_update_delete_contact(client, auth_headers):
    # Create base client
    r = await client.post(BASE_URL + "/", json={"name": "ContactBase", "type": "Client"}, headers=auth_headers)
    client_id = r.json()["id"]

    # Add contact
    contact = {
        "first_name": "Rick",
        "last_name": "Sanchez",
        "email": "rick@example.com",
        "phone": "42",
        "mobile": "666",
        "position": "Scientist",
        "notes": "Mad",
        "is_main_contact": True
    }
    c = await client.post(f"{BASE_URL}/{client_id}/contacts", json=contact, headers=auth_headers)
    assert c.status_code == 201
    contact_id = c.json()["id"]

    # List
    lst = await client.get(f"{BASE_URL}/{client_id}/contacts", headers=auth_headers)
    assert lst.status_code == 200
    assert any(ct["id"] == contact_id for ct in lst.json())

    # Update
    u = await client.patch(f"{BASE_URL}/contacts/{contact_id}", json={"notes": "Updated"}, headers=auth_headers)
    assert u.status_code == 200
    assert u.json()["notes"] == "Updated"

    # Delete
    d = await client.delete(f"{BASE_URL}/contacts/{contact_id}", headers=auth_headers)
    assert d.status_code == 204


@pytest.mark.anyio
async def test_delete_contact_invalid_id(client, auth_headers):
    r = await client.delete(f"{BASE_URL}/contacts/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert r.status_code == 404


# ---- ATTACHMENT TESTS ----

@pytest.mark.anyio
async def test_attachment_flow(client, auth_headers):
    # Create client
    c = await client.post(BASE_URL + "/", json={"name": "Attachy", "type": "Client"}, headers=auth_headers)
    client_id = c.json()["id"]

    # Add attachment
    attachment = {
    "file_name": "contract.pdf",
    "file_url": "https://example.com/contract.pdf",
    "file_type": "application/pdf",
    "notes": "Client contract",
    "uploaded_by": "Rick"
}
    a = await client.post(f"{BASE_URL}/{client_id}/attachments", json=attachment, headers=auth_headers)
    assert a.status_code == 201
    attachment_id = a.json()["id"]

    # Get by ID
    g = await client.get(f"{BASE_URL}/attachments/{attachment_id}", headers=auth_headers)
    assert g.status_code == 200
    assert g.json()["file_name"] == "contract.pdf"

    # List all
    l = await client.get(f"{BASE_URL}/{client_id}/attachments", headers=auth_headers)
    assert l.status_code == 200
    assert any(a["id"] == attachment_id for a in l.json())

    # Delete
    d = await client.delete(f"{BASE_URL}/attachments/{attachment_id}", headers=auth_headers)
    assert d.status_code == 204


@pytest.mark.anyio
async def test_attachment_invalid_id(client, auth_headers):
    r = await client.get(f"{BASE_URL}/attachments/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert r.status_code == 404

    d = await client.delete(f"{BASE_URL}/attachments/00000000-0000-0000-0000-000000000000", headers=auth_headers)
    assert d.status_code == 404
