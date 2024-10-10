from abc import ABC
from typing import Optional, Union
from uuid import UUID


class WishlistRepository(ABC):
    @classmethod
    def create(cls, client: str) -> "Wishlist":
        raise NotImplementedError

    @classmethod
    def get_by_id(cls, id: str) -> "Wishlist":
        raise NotImplementedError

    @classmethod
    def add_product(cls, wishlist: "Wishlist", product: "Product") -> "Wishlist":
        raise NotImplementedError
