from abc import ABC
from typing import Optional, Union
from uuid import UUID


class ProductRepository(ABC):
    @classmethod
    def create_product(cls, cpf: str) -> "Client":
        raise NotImplementedError

    @classmethod
    def get_by_filters(cls, cpf: str) -> "Client":
        raise NotImplementedError

    @classmethod
    def get_by_id(cls, cpf: str) -> "Client":
        raise NotImplementedError
    