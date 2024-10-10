from dataclasses import dataclass
from datetime import datetime
from typing import Union, Type, Optional, Callable
from uuid import UUID

from api.domain.models.client import Client
from api.domain.ports.wishlist import WishlistRepository


@dataclass
class Wishlist:
    id: UUID
    client_id: str = None
    insert_at: datetime = None 
    update_at: datetime = None

    @classmethod
    def create(
        cls,
        client: Client,
        using_repository: Type["WishlistRepository"]
    ):

        return using_repository.create(client)
    
    @classmethod
    def get_by_id(
        cls,
        wishlist_id: UUID,
        using_repository: Type["WishlistRepository"]
    ):
        return using_repository.get_by_id(wishlist_id=wishlist_id)
    
    @classmethod
    def add_product(
        cls,
        wishlist: "Wishlist",
        product: "Product",
        using_repository: Type["WishlistRepository"]
    ):
        return using_repository.add_product(wishlist=wishlist, product=product)
