from uuid import UUID
from typing import Union, Optional

from api.domain.models.product import Product
from api.application.adapters.product_repository import SQLAlchemyProductRepository


class ProductNotFound(Exception):
    pass


class ProductUseCase:
    @classmethod
    def get_by_filters(cls, limit: int, offset: int) -> Optional["Product"]:
        
        products = Product.get_by_filters(
            limit=limit,
            offset=offset,
            using_repository=SQLAlchemyProductRepository
        )

        return products


    @classmethod
    def get_by_id(cls, product_id: UUID) -> "Product":

        product = Product.get_by_id(
            product_id=product_id,
            using_repository=SQLAlchemyProductRepository
        )

        if not product:
            raise ProductNotFound(f"Product with id {product_id} not found")

        return product
