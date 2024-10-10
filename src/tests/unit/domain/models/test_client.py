import mock
import pytest

from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.domain.models.client import Client
from api.application.persistency.tables import Client as ClientTable


@mock.patch.object(SQLAlchemyClientRepository, "persist_client")
def test_create(persist_client_mock, create_client_mapping, app):
    client = Client.create(
        name=create_client_mapping.name,
        email=create_client_mapping.email,
        using_repository=SQLAlchemyClientRepository
    )
    
    persist_client_mock.assert_called_once_with(name=create_client_mapping.name, email=create_client_mapping.email)


@mock.patch.object(SQLAlchemyClientRepository, "get_by_email")
def test_get_by_email(get_by_email_mock, app):
    get_by_email_mock.return_value = ClientTable(
        id="0075dad8-8f89-44e1-8c26-94e1ccbf1422",
        name="John Wick",
        email="johnwick123@example.com"
    )
    client = Client.get_by_email(
        email="johnwick123@example.com",
        using_repository=SQLAlchemyClientRepository
    )
    
    assert client.name == "John Wick"
    get_by_email_mock.assert_called_once_with(email="johnwick123@example.com")


@mock.patch.object(SQLAlchemyClientRepository, "get_by_id")
def test_get_by_id(get_by_id_mock, app):
    get_by_id_mock.return_value = ClientTable(
        id="0075dad8-8f89-44e1-8c26-94e1ccbf1422",
        name="John Wick",
        email="johnwick123@example.com"
    )
    client = Client.get_by_id(
        client_id="0075dad8-8f89-44e1-8c26-94e1ccbf1422",
        using_repository=SQLAlchemyClientRepository
    )

    assert client.name == "John Wick"
    assert client.email == "johnwick123@example.com"
    get_by_id_mock.assert_called_once_with(client_id="0075dad8-8f89-44e1-8c26-94e1ccbf1422")


@mock.patch.object(SQLAlchemyClientRepository, "delete_by_email")
def test_delete_by_email(delete_by_email_mock, app):
    Client.delete_by_email(
        email="johnwick123@example.com",
        using_repository=SQLAlchemyClientRepository
    )
    
    delete_by_email_mock.assert_called_once_with(email="johnwick123@example.com")


@mock.patch.object(SQLAlchemyClientRepository, "update_by_email")
def test_delete_by_email(update_by_email_mock, app):
    client = Client.update_by_email(
        email="johnwick123@example.com",
        name="John Wick",
        using_repository=SQLAlchemyClientRepository
    )
    
    update_by_email_mock.assert_called_once_with(email="johnwick123@example.com", name="John Wick")