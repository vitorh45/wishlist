from uuid import UUID

from api.domain.models.client import Client
from api.domain.models.product import Product
from api.domain.models.wishlist import Wishlist
from api.application.adapters.client_repository import SQLAlchemyClientRepository
from api.application.adapters.wishlist_repository import SQLAlchemyWishlistRepository
from api.application.adapters.product_repository import SQLAlchemyProductRepository
from api.application.use_cases import ClientNotFound

class WishlistNotFound(Exception):
    pass


class WishlistAlreadyExists(Exception):
    pass


class WishlistAlreadyContainsThisProduct(Exception):
    pass


class WishlistUseCase:
    @classmethod
    def create_wishlist(cls, data: "PayloadMapping"):
        
        client = Client.get_by_id(
            client_id=data.client_id,
            using_repository=SQLAlchemyClientRepository
        )
        if not client:
            raise ClientNotFound(f"Client with id {data.client_id} not found")

        if client.wishlist:
            raise WishlistAlreadyExists(f"Wishlist already exists for this user {client.id}")

        wishlist = Wishlist.create(
            client=client,
            using_repository=SQLAlchemyWishlistRepository
        )

        return wishlist
    
    @classmethod
    def get_by_id(cls, wishlist_id: str):
        wishlist = Wishlist.get_by_id(
            wishlist_id=wishlist_id,
            using_repository=SQLAlchemyWishlistRepository
        )
        if not wishlist:
            raise WishlistNotFound(f"Wishlist with id {wishlist_id} not found")

        return wishlist
    
    @classmethod
    def add_product(cls, wishlist_id: UUID, data: "PayloadMapping"):
        
        wishlist = Wishlist.get_by_id(
            wishlist_id=wishlist_id,
            using_repository=SQLAlchemyWishlistRepository
        )
        product = Product.get_by_id(
            product_id=data.product_id,
            using_repository=SQLAlchemyProductRepository
        )

        if product in wishlist.products:
            raise WishlistAlreadyContainsThisProduct("Wishlist already contains this product")
            
            
        Wishlist.add_product(
            wishlist=wishlist,
            product=product,
            using_repository=SQLAlchemyWishlistRepository
        )
        return wishlist