import logging
from typing import Union, Optional, List
from uuid import UUID

from api.app import db
from api.application.persistency.tables import Product as ProductTable
from api.domain.models.product import Product
from api.domain.ports.product import ProductRepository

logger = logging.getLogger("wishlist")


class SQLAlchemyProductRepository(ProductRepository):
    
    @staticmethod
    def _build_products(rows) -> List[Product]:
        return [Product(
            title=row.title,
            brand=row.brand,
            id=row.id,
            price=row.price,
            image=row.image,
            insert_at=row.insert_at,
            update_at=row.update_at,
        ) for row in rows]
        
    @staticmethod
    def _build_product(row) -> Product:
        
        return Product(
            title=row.title,
            brand=row.brand,
            id=row.id,
            price=row.price,
            image=row.image,
            insert_at=row.insert_at,
            update_at=row.update_at,
        )
    

    @classmethod
    def get_by_id(cls, product_id: str) -> Optional["Product"]:
        logger.info(
            "Getting product by id.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "product_id": product_id,
                }
            },
        )

        try:
            product = ProductTable.query.filter_by(id=product_id).first()
        except Exception as e:
            logger.exception(
                "Error while trying to get product by id.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "product_id": product_id,
                    }
                },
            )
            raise e

        if product:
            logger.info(
                "Product found.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "product_id": product_id,
                    }
                },
            )

            return product

        logger.info(
            "Product not found.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "product_id": product_id,
                }
            },
        )
        return None
    
    @classmethod
    def get_by_filters(cls, limit: int, offset: int) -> Optional["Product"]:
        logger.info(
            "Getting products with limit and offset.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_filters",
                    "limit": limit,
                    "offset": offset
                }
            },
        )
        try:
            products = ProductTable.query.limit(limit).offset(offset).all()
        except Exception as e:
            logger.exception(
                "Error while trying to get products with limit and offset.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_filters",
                        "limit": limit,
                        "offset": offset
                    }
                },
            )
            raise e

        if products:
            logger.info(
                "Products found.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_filters",
                        "limit": limit,
                        "offset": offset
                    }
                },
            )
            return products

        logger.info(
            "Products not found.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_filters",
                    "limit": limit,
                    "offset": offset
                }
            },
        )
        return None