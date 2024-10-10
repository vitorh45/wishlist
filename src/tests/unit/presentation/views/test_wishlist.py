import mock
import pytest
from datetime import datetime
import freezegun

from api.application.persistency.tables import Product as ProductTable
from api.application.persistency.tables import Wishlist as WishlistTable
from api.application.use_cases import (
    ClientNotFound,
    WishlistAlreadyExists,
    WishlistUseCase,
    WishlistNotFound,
    WishlistAlreadyContainsThisProduct
)


@mock.patch.object(WishlistUseCase, "create_wishlist")
def test_post(create_wishlist_mock, create_jwt_user, app):
    create_wishlist_mock.return_value = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        client_id="53fcf979-c508-450c-8fe2-911ce7bd49d2"
    )
    payload = {"client_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.post(
        "/api/v1/wishlists",
        headers=headers,
        json=payload
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.status_code == 201
    create_wishlist_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "create_wishlist")
def test_post_client_found(create_wishlist_mock, create_jwt_user, app):
    create_wishlist_mock.side_effect = ClientNotFound("Client not found")
    payload = {"client_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.post(
        "/api/v1/wishlists",
        headers=headers,
        json=payload
    )

    assert response.json["message"] == "Client not found"
    assert response.status_code == 404
    create_wishlist_mock.assert_called_once()

@mock.patch.object(WishlistUseCase, "create_wishlist")
def test_post_already_existis(create_wishlist_mock, create_jwt_user, app):
    create_wishlist_mock.side_effect = WishlistAlreadyExists("Wishlist already exists")
    payload = {"client_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.post(
        "/api/v1/wishlists",
        headers=headers,
        json=payload
    )

    assert response.json["message"] == "Wishlist already exists"
    assert response.status_code == 409
    create_wishlist_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "create_wishlist")
def test_post_error(create_wishlist_mock, create_jwt_user, app):
    create_wishlist_mock.side_effect = Exception("Something went wrong")
    payload = {"client_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.post(
        "/api/v1/wishlists",
        headers=headers,
        json=payload
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    create_wishlist_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "get_by_id")
def test_get(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.return_value = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        client_id="53fcf979-c508-450c-8fe2-911ce7bd49d2"
    )
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.status_code == 200
    get_by_id_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "get_by_id")
def test_get_not_found(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.side_effect = WishlistNotFound("Wishlist not found")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["message"] == "Wishlist not found"
    assert response.status_code == 404
    get_by_id_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "get_by_id")
def test_get_error(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.side_effect = Exception("Something went wrong")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    get_by_id_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "add_product")
def test_put_success(add_product_mock, create_jwt_user, app):
    add_product_mock.return_value = WishlistTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        client_id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        products=[ProductTable(
            id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
            title="Les Paul 69 cherry sunburst",
            brand="Gibson",
            price="2500000",
            image="src/products/product_01.jpg"
        )]
    )
    payload = {"product_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.put(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers,
        json=payload
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.json["products"][0]["brand"] == "Gibson"
    assert response.status_code == 200
    add_product_mock.assert_called_once()
    

@mock.patch.object(WishlistUseCase, "add_product")
def test_put_duplicate_product_error(add_product_mock, create_jwt_user, app):
    add_product_mock.side_effect = WishlistAlreadyContainsThisProduct("Wishlist already has product")
    payload = {"product_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.put(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers,
        json=payload
    )

    assert response.json["message"] == "Wishlist already has product"
    assert response.status_code == 400
    add_product_mock.assert_called_once()


@mock.patch.object(WishlistUseCase, "add_product")
def test_put_error(add_product_mock, create_jwt_user, app):
    add_product_mock.side_effect = Exception("Something went wrong")
    payload = {"product_id": "53fcf979-c508-450c-8fe2-911ce7bd49d2"}
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.put(
        "/api/v1/wishlists/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers,
        json=payload
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    add_product_mock.assert_called_once()