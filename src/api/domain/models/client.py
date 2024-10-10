from dataclasses import dataclass
from datetime import datetime
from typing import Union, Type, Optional, Callable
from uuid import UUID

from api.domain.ports.client import ClientRepository


@dataclass
class Client:
    id: UUID
    name: str = None
    email: str = None
    insert_at: datetime = None 
    update_at: datetime = None

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        using_repository: Type["ClientRepository"]
    ):
        client_data = {
            "name": name,
            "email": email
        }

        return using_repository.persist_client(**client_data)
    
    @classmethod
    def get_by_email(
        cls,
        email: str,
        using_repository: Type["ClientRepository"]
    ):
        return using_repository.get_by_email(email=email)
    
    @classmethod
    def get_by_id(
        cls,
        client_id: UUID,
        using_repository: Type["ClientRepository"]
    ):
        return using_repository.get_by_id(client_id=client_id)
    
    @classmethod
    def delete_by_email(
        cls,
        email: str,
        using_repository: Type["ClientRepository"]
    ):
        return using_repository.delete_by_email(email=email)
    
    @classmethod
    def update_by_email(
        cls,
        email: str,
        name: str,
        using_repository: Type["ClientRepository"]
    ):
        return using_repository.update_by_email(email=email, name=name)