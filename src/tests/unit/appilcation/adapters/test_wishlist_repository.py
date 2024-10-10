import pytest
from unittest.mock import patch, MagicMock
from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.application.adapters.wishlist_repository import SQLAlchemyWishlistRepository
from api.application.persistency.tables import Wishlist as WishlistTable


def test_create(app):
    name = 'John Wick 007'
    email = 'johnwick007@example.com'
    client = SQLAlchemyClientRepository.persist_client(name, email)
    wishlist = SQLAlchemyWishlistRepository.create(client)
    assert type(wishlist) is WishlistTable
    assert wishlist.client_id == client.id


def test_get_by_id(app):
    name = 'John Wick 008'
    email = 'johnwick008@example.com'
    client = SQLAlchemyClientRepository.persist_client(name, email)
    wishlist = SQLAlchemyWishlistRepository.create(client)
    result = SQLAlchemyWishlistRepository.get_by_id(wishlist.id)

    assert type(result) is WishlistTable


def test_get_by_id_not_found(app):
    wishlist = SQLAlchemyWishlistRepository.get_by_id("53fcf979-c508-450c-8fe2-911ce7bd49d1")

    assert wishlist is None


def test_add_product(add_producs_db, app):
    name = 'John Wick 009'
    email = 'johnwick009@example.com'
    client = SQLAlchemyClientRepository.persist_client(name, email)
    wishlist = SQLAlchemyWishlistRepository.create(client)
    SQLAlchemyWishlistRepository.add_product(wishlist, add_producs_db[0])
    assert len(wishlist.products) == 1

    SQLAlchemyWishlistRepository.add_product(wishlist, add_producs_db[1])
    assert len(wishlist.products) == 2