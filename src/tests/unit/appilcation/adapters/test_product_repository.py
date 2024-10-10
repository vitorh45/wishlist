import pytest
from unittest.mock import patch, MagicMock
from api.application.adapters.product_repository import SQLAlchemyProductRepository
from api.application.persistency.tables import Product as ProductTable


def test_get_by_id(add_producs_db, app):
    prod_1, prod_2 = add_producs_db

    product_1 = SQLAlchemyProductRepository.get_by_id(prod_1.id)
    product_2 = SQLAlchemyProductRepository.get_by_id(prod_2.id)
    
    assert product_1.id == prod_1.id
    assert product_2.id == prod_2.id


def test_get_by_id_not_found(add_producs_db, app):
    product = SQLAlchemyProductRepository.get_by_id("7c35dad8-8f89-44e1-8c26-94e1ccbf14e1")
    
    assert product is None


def test_get_by_filters(add_producs_db, app):
    products_1 = SQLAlchemyProductRepository.get_by_filters(limit=2, offset=0)
    products_2 = SQLAlchemyProductRepository.get_by_filters(limit=1, offset=0)
    products_3 = SQLAlchemyProductRepository.get_by_filters(limit=10, offset=1)
    
    assert len(products_1) == 2
    assert len(products_2) == 1
    assert len(products_3) == 5
