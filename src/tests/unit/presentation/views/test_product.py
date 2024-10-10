import mock
import pytest
from datetime import datetime
import freezegun

from api.application.persistency.tables import Product as ProductTable
from api.application.use_cases import (
    ProductUseCase,
    ProductNotFound
)


@mock.patch.object(ProductUseCase, "get_by_filters")
def test_product_get_filters_success(get_by_filters_mock, create_jwt_user, app):
    get_by_filters_mock.return_value = [ProductTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )]
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/products?limit=1&offset=0",
        headers=headers
    )

    assert response.json[0]["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.status_code == 200
    get_by_filters_mock.assert_called_once()


@mock.patch.object(ProductUseCase, "get_by_filters")
def test_product_get_filters_error(get_by_filters_mock, create_jwt_user, app):
    get_by_filters_mock.side_effect = Exception("Something went wrong")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/products?limit=1&offset=1",
        headers=headers
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    get_by_filters_mock.assert_called_once()


@mock.patch.object(ProductUseCase, "get_by_id")
def test_product_get_by_id_success(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.return_value = ProductTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/products/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["id"] == "53fcf979-c508-450c-8fe2-911ce7bd49d2"
    assert response.json["brand"] == "Gibson"
    assert response.status_code == 200
    get_by_id_mock.assert_called_once()


@mock.patch.object(ProductUseCase, "get_by_id")
def test_product_get_by_id_not_found(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.side_effect = ProductNotFound("Product not found")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/products/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["message"] == "Product not found"
    assert response.status_code == 404
    get_by_id_mock.assert_called_once()


@mock.patch.object(ProductUseCase, "get_by_id")
def test_product_get_by_id_error(get_by_id_mock, create_jwt_user, app):
    get_by_id_mock.side_effect = Exception("Something went wrong")
    headers = {"Authorization": f"Bearer {create_jwt_user}"}
    response = app.get(
        "/api/v1/products/53fcf979-c508-450c-8fe2-911ce7bd49d2",
        headers=headers
    )

    assert response.json["message"] == "Something went wrong"
    assert response.status_code == 400
    get_by_id_mock.assert_called_once()
