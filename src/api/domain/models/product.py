from dataclasses import dataclass
from datetime import datetime
from typing import Union, Type, Optional, Callable
from uuid import UUID

from api.domain.ports.product import ProductRepository


@dataclass
class Product:
    id: UUID
    brand: str = None
    title: str = None
    price: int = None
    image: str = None
    insert_at: datetime = None 
    update_at: datetime = None
    
    @classmethod
    def get_by_filters(
        cls,
        limit: str,
        offset: str,
        using_repository: Type["ProductRepository"]
    ):
        return using_repository.get_by_filters(limit=limit, offset=offset)
    
    
    @classmethod
    def get_by_id(
        cls,
        product_id: UUID,
        using_repository: Type["ProductRepository"]
    ):
        return using_repository.get_by_id(product_id=product_id)