import mock
import pytest

from api.application.adapters.wishlist_repository import SQLAlchemyWishlistRepository
from api.domain.models.wishlist import Wishlist
from api.application.persistency.tables import Client as ClientTable
from api.application.persistency.tables import Product as ProductTable
from api.application.persistency.tables import Wishlist as WishlistTable


@mock.patch.object(SQLAlchemyWishlistRepository, "create")
def test_create(create_mock, app):
    client = ClientTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    wishlist = Wishlist.create(
        client=client,
        using_repository=SQLAlchemyWishlistRepository
    )
    
    create_mock.assert_called_once_with(client)
    

@mock.patch.object(SQLAlchemyWishlistRepository, "get_by_id")
def test_get_by_ud(get_by_id_mock, app):
    get_by_id_mock.return_value = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="111cf979-c508-450c-8fe2-911ce7bd4222",
        products=[]
    )
    wishlist = Wishlist.get_by_id(
        wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        using_repository=SQLAlchemyWishlistRepository
    )
    
    assert wishlist.id == "53fcf979-c508-450c-8fe2-911ce7bd44a3"
    get_by_id_mock.assert_called_once_with(wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3")
    

@mock.patch.object(SQLAlchemyWishlistRepository, "add_product")
def test_add_product(add_product_mock, app):
    wishlist = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="111cf979-c508-450c-8fe2-911ce7bd4222",
        products=[]
    )
    product = ProductTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )
    
    result = Wishlist.add_product(wishlist=wishlist, product=product, using_repository=SQLAlchemyWishlistRepository)
    
    add_product_mock.assert_called_once_with(wishlist=wishlist, product=product)