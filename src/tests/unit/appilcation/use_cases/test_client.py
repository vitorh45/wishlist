import pytest
import mock

from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.application.persistency.tables import Client as ClientTable
from api.domain.models.client import Client
from api.application.use_cases import (
    ClientsUseCase,
    ClientNotFound,
    ClientAlreadyRegistered
)


@mock.patch.object(Client, "get_by_email")
@mock.patch.object(Client, "create")
def test_create_client_success(create_mock, get_by_email_mock, create_client_mapping, app):
    get_by_email_mock.return_value = None
    create_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    client = ClientsUseCase.create_client(
        create_client_mapping
    )
    
    assert client.name == "John Wick 123"
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)
    

@mock.patch.object(Client, "get_by_email")
def test_create_client_already_registered_error(get_by_email_mock, create_client_mapping, app):
    get_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    with pytest.raises(ClientAlreadyRegistered):
        ClientsUseCase.create_client(
            create_client_mapping
        )
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
def test_get_by_email_success(get_by_email_mock, app):
    get_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    client = ClientsUseCase.get_by_email(
        email="johnwick123@example.com"
    )
    
    assert client.name == "John Wick 123"
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
def test_get_by_email_not_found(get_by_email_mock, app):
    get_by_email_mock.return_value = None
    with pytest.raises(ClientNotFound):
        ClientsUseCase.get_by_email(
            email="johnwick123@example.com"
        )
    
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
@mock.patch.object(Client, "delete_by_email")
def test_delete_by_email_success(delete_by_email_mock, get_by_email_mock, app):
    get_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    client = ClientsUseCase.delete_by_email(
        email="johnwick123@example.com"
    )
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)
    delete_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
def test_delete_by_email_not_found(get_by_email_mock, app):
    get_by_email_mock.return_value = None
    with pytest.raises(ClientNotFound):
        ClientsUseCase.get_by_email(
            email="johnwick123@example.com"
        )
    
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
@mock.patch.object(Client, "update_by_email")
def test_update_by_email_success(update_by_email_mock, get_by_email_mock, update_client_mapping, app):
    get_by_email_mock.return_value = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    client = ClientsUseCase.update_by_email(
        data=update_client_mapping,
        email="johnwick123@example.com"
    )
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)
    update_by_email_mock.assert_called_once_with(email="johnwick123@example.com", 
                                                 name=update_client_mapping.name, 
                                                 using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_email")
def test_update_by_email_not_found(get_by_email_mock, app):
    get_by_email_mock.return_value = None
    with pytest.raises(ClientNotFound):
        ClientsUseCase.get_by_email(
            email="johnwick123@example.com"
        )
    
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com", using_repository=SQLAlchemyClientRepository)