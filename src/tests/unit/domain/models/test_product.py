import mock
import pytest

from api.application.adapters.product_repository import SQLAlchemyProductRepository
from api.domain.models.product import Product
from api.application.persistency.tables import Product as ProductTable


@mock.patch.object(SQLAlchemyProductRepository, "get_by_filters")
def test_get_by_filters(get_by_filters_mock, app):
    get_by_filters_mock.return_value = [ProductTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )]
    
    products = Product.get_by_filters(
        limit=1,
        offset=0,
        using_repository=SQLAlchemyProductRepository
    )
    
    assert products[0].brand == "Gibson"
    assert products[0].title == "Les Paul 69 cherry sunburst"
    get_by_filters_mock.assert_called_once_with(limit=1, offset=0)


@mock.patch.object(SQLAlchemyProductRepository, "get_by_id")
def test_get_by_id(get_by_id_mock, app):
    get_by_id_mock.return_value = ProductTable(
        id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        title="Les Paul 69 cherry sunburst",
        brand="Gibson",
        price="2500000",
        image="src/products/product_01.jpg"
    )
    
    product = Product.get_by_id(
        product_id="53fcf979-c508-450c-8fe2-911ce7bd49d2",
        using_repository=SQLAlchemyProductRepository
    )
    
    assert product.brand == "Gibson"
    assert product.title == "Les Paul 69 cherry sunburst"
    get_by_id_mock.assert_called_once_with(product_id="53fcf979-c508-450c-8fe2-911ce7bd49d2")