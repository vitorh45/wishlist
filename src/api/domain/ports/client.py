from abc import ABC
from typing import Optional, Union
from uuid import UUID


class ClientRepository(ABC):
    @classmethod
    def create_client(cls, email: str, name: str) -> "Client":
        raise NotImplementedError

    @classmethod
    def get_by_email(cls, email: str) -> "Client":
        raise NotImplementedError
    
    @classmethod
    def get_by_id(cls, client_id: str) -> "Client":
        raise NotImplementedError

    @classmethod
    def delete_by_email(cls, email: str) -> "Client":
        raise NotImplementedError
    
    @classmethod
    def update_by_email(cls, email: str) -> "Client":
        raise NotImplementedError