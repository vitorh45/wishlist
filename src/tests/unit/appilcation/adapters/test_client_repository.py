import pytest
from unittest.mock import patch, MagicMock
from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.application.persistency.tables import Client as ClientTable


def test_persist_client_success(app):
    name = 'John Wick'
    email = 'johnwick@example.com'

    client = SQLAlchemyClientRepository.persist_client(name, email)
    assert type(client) is ClientTable


def test_get_by_email_success(app):
    name = 'John Wick2'
    email = 'johnwick2@example.com'

    SQLAlchemyClientRepository.persist_client(name, email)
    client = SQLAlchemyClientRepository.get_by_email(email)
    
    assert client.email == email


def test_get_by_email_not_found(app):
    email = 'not_found@example.com'
    client = SQLAlchemyClientRepository.get_by_email(email)
    
    assert client is None
    

def test_get_by_id_success(app):
    name = 'John Wick3'
    email = 'johnwick3@example.com'

    result = SQLAlchemyClientRepository.persist_client(name, email)
    client = SQLAlchemyClientRepository.get_by_id(result.id)
    
    assert client.email == email


def test_get_by_id_not_found(app):
    client_id = '02324861-cc01-451d-9b5a-f076c866dfed'
    client = SQLAlchemyClientRepository.get_by_id(client_id)
    
    assert client is None


def test_delete_by_email_success(app):
    name = 'John Wick4'
    email = 'johnwick4@example.com'

    result = SQLAlchemyClientRepository.persist_client(name, email)
    SQLAlchemyClientRepository.delete_by_email(result.email)
    client = SQLAlchemyClientRepository.get_by_email(email)
    
    assert client is None