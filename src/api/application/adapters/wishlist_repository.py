import logging
from typing import Union, Optional
from uuid import UUID

from api.app import db
from api.application.persistency.tables import Wishlist as WishlistTable
from api.application.persistency.tables import Product as ProductTable
from api.domain.models.wishlist import Wishlist
from api.domain.ports.wishlist import WishlistRepository
from api.domain.models.client import Client

logger = logging.getLogger("wishlist")


class SQLAlchemyWishlistRepository(WishlistRepository):
    @staticmethod
    def _build_wishlist(wishlist) -> Client:
        return Wishlist(
            id=wishlist.id,
            client_id=wishlist.client.id,
            insert_at=wishlist.insert_at,
            update_at=wishlist.update_at,
        )

    @classmethod
    def create(
        cls,
        client: Client
    ) -> "Wishlist":
        logger.info(
            "Creating a new wishlist.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "create",
                    "client_id": str(client.id)
                }
            },
        )
        try:
            wishlist = WishlistTable(client=client)
            db.session.add(wishlist)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create a new wishlist.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "create",
                        "client_id": str(client.id)
                    }
                },
            )
            raise e

        return wishlist
    

    @classmethod
    def get_by_id(cls, wishlist_id: str) -> Optional["Wishlist"]:
        logger.info(
            "Getting wishlist by id.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "wishlist_id": str(wishlist_id),
                }
            },
        )
        try:
            wishlist = WishlistTable.query.filter_by(id=wishlist_id).first()
        except Exception as e:
            logger.exception(
                "Error while trying to get wishlist by id.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "wishlist_id": str(wishlist_id),
                    }
                },
            )
            raise e

        if wishlist:
            logger.info(
                "Wishlist found.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "wishlist_id": str(wishlist_id),
                    }
                },
            )

            return wishlist

        logger.info(
            "Wishlist not found.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "wishlist_id": str(wishlist_id),
                }
            },
        )
        return None
    
    @classmethod
    def add_product(cls, wishlist: "Wishlist", product: "Product") -> Optional["Wishlist"]:
        logger.info(
            "Add a product to a wishlist",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "add_product",
                    "wishlist_id": str(wishlist.id),
                    "product_id": str(product.id),
                }
            },
        )
        try:
            wishlist.products.append(product)
            db.session.commit()
        except Exception as e:
            logger.exception(
                "Error while trying to add a product to a wishlist.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "add_product",
                        "wishlist_id": str(wishlist.id),
                        "product_id": str(product.id),
                    }
                },
            )
            raise e

        return wishlist
  
  