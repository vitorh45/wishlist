import pytest
import mock

from api.domain.models.client import Client
from api.domain.models.product import Product
from api.domain.models.wishlist import Wishlist
from api.application.use_cases import (
    ClientNotFound,
    WishlistUseCase,
    WishlistNotFound,
    WishlistAlreadyExists,
    WishlistAlreadyContainsThisProduct
)
from api.application.persistency.tables import Client as ClientTable
from api.application.persistency.tables import Product as ProductTable
from api.application.persistency.tables import Wishlist as WishlistTable
from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.application.adapters.product_repository import SQLAlchemyProductRepository
from api.application.adapters.wishlist_repository import SQLAlchemyWishlistRepository


@mock.patch.object(Client, "get_by_id")
@mock.patch.object(Wishlist, "create")
def test_create_wishlist_success(create_mock, get_by_id_mock, create_wishlist_mapping, app):
    client = ClientTable(
        id=create_wishlist_mapping.client_id,
        name="John Wick 123",
        email="johnwick123@example.com"
    )
    get_by_id_mock.return_value = client
    create_mock.return_value = Wishlist(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
    )
    wishlist = WishlistUseCase.create_wishlist(
        data=create_wishlist_mapping
    )
    
    assert wishlist.id == "53fcf979-c508-450c-8fe2-911ce7bd44a3"
    get_by_id_mock.assert_called_once_with(client_id=create_wishlist_mapping.client_id, 
                                           using_repository=SQLAlchemyClientRepository)
    create_mock.assert_called_once_with(client=client, using_repository=SQLAlchemyWishlistRepository)


@mock.patch.object(Client, "get_by_id")
def test_create_wishlist_client_not_found_error(get_by_id_mock, create_wishlist_mapping, app):
    get_by_id_mock.return_value = None

    with pytest.raises(ClientNotFound):
        WishlistUseCase.create_wishlist(
            data=create_wishlist_mapping
        )
    
    get_by_id_mock.assert_called_once_with(client_id=create_wishlist_mapping.client_id, 
                                           using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Client, "get_by_id")
def test_create_wishlist_client_with_existing_wishlist(get_by_id_mock, create_wishlist_mapping, app):
    client = ClientTable(
        id=create_wishlist_mapping.client_id,
        name="John Wick 123",
        email="johnwick123@example.com",
        wishlist=[WishlistTable(
            id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
            client_id=create_wishlist_mapping.client_id,
        )]
    )
    get_by_id_mock.return_value = client
    
    with pytest.raises(WishlistAlreadyExists):
        WishlistUseCase.create_wishlist(
            data=create_wishlist_mapping
        )
    
    get_by_id_mock.assert_called_once_with(client_id=create_wishlist_mapping.client_id, 
                                           using_repository=SQLAlchemyClientRepository)


@mock.patch.object(Wishlist, "get_by_id")
def test_get_by_id_success(get_by_id_mock, app):
    get_by_id_mock.return_value = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="111cf979-c508-450c-8fe2-911ce7bd4222"
    )
    
    wishlist = WishlistUseCase.get_by_id(
        wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3"
    )
    
    get_by_id_mock.assert_called_once_with(wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3", 
                                           using_repository=SQLAlchemyWishlistRepository)


@mock.patch.object(Wishlist, "get_by_id")
def test_get_by_id_not_found_error(get_by_id_mock, app):
    get_by_id_mock.return_value = None
    
    with pytest.raises(WishlistNotFound):
        WishlistUseCase.get_by_id(
            wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3"
        )
    
    get_by_id_mock.assert_called_once_with(wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3", 
                                           using_repository=SQLAlchemyWishlistRepository)


@mock.patch.object(Wishlist, "get_by_id")
@mock.patch.object(Product, "get_by_id")
@mock.patch.object(Wishlist, "add_product")
def test_add_product_success(add_product_mock, product_get_by_id_mock, wishlist_get_by_id_mock, add_product_mapping, app):
    wishlist = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="111cf979-c508-450c-8fe2-911ce7bd4222"
    )
    wishlist_get_by_id_mock.return_value = wishlist
    product = ProductTable(
        id=add_product_mapping.product_id,
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )
    product_get_by_id_mock.return_value = product
    WishlistUseCase.add_product(
        wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        data=add_product_mapping
    )
    
    wishlist_get_by_id_mock.assert_called_once_with(wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3", 
                                                    using_repository=SQLAlchemyWishlistRepository)
    product_get_by_id_mock.assert_called_once_with(product_id=add_product_mapping.product_id, 
                                                    using_repository=SQLAlchemyProductRepository)
    add_product_mock.assert_called_once_with(wishlist=wishlist, product=product,
                                             using_repository=SQLAlchemyWishlistRepository)


@mock.patch.object(Wishlist, "get_by_id")
@mock.patch.object(Product, "get_by_id")
def test_add_product_product_already_existis(product_get_by_id_mock, wishlist_get_by_id_mock, add_product_mapping, app):
    product = ProductTable(
        id=add_product_mapping.product_id,
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )
    wishlist = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
        client_id="111cf979-c508-450c-8fe2-911ce7bd4222",
        products=[product]
    )
    wishlist_get_by_id_mock.return_value = wishlist
    product_get_by_id_mock.return_value = product
    
    with pytest.raises(WishlistAlreadyContainsThisProduct):
        WishlistUseCase.add_product(
            wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3",
            data=add_product_mapping
        )
    
    wishlist_get_by_id_mock.assert_called_once_with(wishlist_id="53fcf979-c508-450c-8fe2-911ce7bd44a3", 
                                                    using_repository=SQLAlchemyWishlistRepository)
    product_get_by_id_mock.assert_called_once_with(product_id=add_product_mapping.product_id, 
                                                    using_repository=SQLAlchemyProductRepository)
