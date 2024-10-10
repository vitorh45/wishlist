import mock
import pytest
from datetime import datetime
import freezegun

from api.application.persistency.tables import Client as ClientTable
from api.presentation.mappings import (
    CreateClientRequestMapping,
    UpdateClientRequestMapping
)
from api.application.use_cases import (
    ClientsUseCase,
    ClientNotFound
)


@mock.patch.object(ClientsUseCase, "create_client")
def test_client_creation_success(create_client_mock, create_jwt_user, app):
    create_client_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com",
        insert_at=datetime.now(),
        update_at=datetime.now()
    )
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    payload = {"name": "John Wick 123", "email": "johnwick123@example.com"}
    response = app.post(
        "/api/v1/clients",
        json=payload,
        headers=headers
    )
    
    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.json["name"] == "John Wick 123"
    assert response.json["email"] == "johnwick123@example.com"
    assert response.status_code == 201
    create_client_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "create_client")
def test_client_creation_error(create_client_mock, create_jwt_user, app):
    create_client_mock.side_effect = Exception("Something went wrong")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    payload = {"name": "John Wick 123", "email": "johnwick123@example.com"}
    response = app.post(
        "/api/v1/clients",
        json=payload,
        headers=headers
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    create_client_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "update_by_email")
def test_client_patch_success(update_by_email_mock, create_jwt_user, app):
    update_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 1234",
        email="johnwick123@example.com",
        insert_at=datetime.now(),
        update_at=datetime.now()
    )
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    payload = {"name": "John Wick 1234"}
    response = app.patch(
        "/api/v1/clients?email=johnwick123@example.com",
        json=payload,
        headers=headers
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.json["name"] == "John Wick 1234"
    assert response.json["email"] == "johnwick123@example.com"
    assert response.status_code == 200
    update_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "update_by_email")
def test_client_patch_client_not_found_error(update_by_email_mock, create_jwt_user, app):
    update_by_email_mock.side_effect = ClientNotFound("Client not found")

    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    payload = {"name": "John Wick 1234"}
    response = app.patch(
        "/api/v1/clients?email=johnwick123@example.com",
        json=payload,
        headers=headers
    )
    
    assert response.json["message"] == "Client not found"
    assert response.status_code == 404
    update_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "update_by_email")
def test_client_patch_error(update_by_email_mock, create_jwt_user, app):
    update_by_email_mock.side_effect = Exception("Something went wrong")

    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    payload = {"name": "John Wick 1234"}
    response = app.patch(
        "/api/v1/clients?email=johnwick123@example.com",
        json=payload,
        headers=headers
    )
    
    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400


@mock.patch.object(ClientsUseCase, "get_by_email")
def test_client_get_success(get_by_email_mock, create_jwt_user, app):
    get_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 1234",
        email="johnwick123@example.com",
        insert_at=datetime.now(),
        update_at=datetime.now()
    )
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/clients?email=johnwick1234@example.com",
        headers=headers
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.json["name"] == "John Wick 1234"
    assert response.json["email"] == "johnwick123@example.com"
    assert response.status_code == 200
    get_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "get_by_email")
def test_client_get_not_found_error(get_by_email_mock, create_jwt_user, app):
    get_by_email_mock.side_effect = ClientNotFound("Client not found")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/clients?email=johnwick1234@example.com",
        headers=headers
    )

    assert response.json["message"] == "Client not found"
    assert response.status_code == 404
    get_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "delete_by_email")
def test_client_delete_success(delete_by_email_mock, create_jwt_user, app):
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.delete(
        "/api/v1/clients?email=johnwick1234@example.com",
        headers=headers
    )
    
    assert response.status_code == 200
    delete_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "delete_by_email")
def test_client_delete_not_found_error(delete_by_email_mock, create_jwt_user, app):
    delete_by_email_mock.side_effect = ClientNotFound("Client not found")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.delete(
        "/api/v1/clients?email=johnwick1234@example.com",
        headers=headers
    )
    
    assert response.json["message"] == "Client not found"
    assert response.status_code == 404
    delete_by_email_mock.assert_called_once()


@mock.patch.object(ClientsUseCase, "delete_by_email")
def test_client_delete_error(delete_by_email_mock, create_jwt_user, app):
    delete_by_email_mock.side_effect = Exception("Something went wrong")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.delete(
        "/api/v1/clients?email=johnwick1234@example.com",
        headers=headers
    )
    
    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    delete_by_email_mock.assert_called_once()
