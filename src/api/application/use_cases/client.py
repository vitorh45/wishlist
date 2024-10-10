from api.domain.models.client import Client
from api.application.adapters.client_repository import SQLAlchemyClientRepository


class ClientAlreadyRegistered(Exception):
    pass


class ClientNotFound(Exception):
    pass


class ClientsUseCase:
    @classmethod
    def create_client(cls, data: "PayloadMapping"):
        
        client = Client.get_by_email(
            email=data.email,
            using_repository=SQLAlchemyClientRepository
        )
        if client:
            raise ClientAlreadyRegistered(f"Client with email {data.email} already exists")


        client = Client.create(
            name=data.name,
            email=data.email,
            using_repository=SQLAlchemyClientRepository
        )

        return client
    
    @classmethod
    def get_by_email(cls, email: str):
        
        client = Client.get_by_email(
            email=email,
            using_repository=SQLAlchemyClientRepository
        )
        if not client:
            raise ClientNotFound(f"Client with email {email} not found")

        return client

    @classmethod
    def delete_by_email(cls, email: str):
        
        client = Client.get_by_email(
            email=email,
            using_repository=SQLAlchemyClientRepository
        )
        if not client:
            raise ClientNotFound(f"Client with email {email} not found")

        Client.delete_by_email(
            email=email,
            using_repository=SQLAlchemyClientRepository
        )
        
        return client
    
    @classmethod
    def update_by_email(cls, data: "PayloadMapping", email: str):
        
        client = Client.get_by_email(
            email=email,
            using_repository=SQLAlchemyClientRepository
        )
        if not client:
            raise ClientNotFound(f"Client with email {email} not found")

        return Client.update_by_email(
            email=email,
            name=data.name,
            using_repository=SQLAlchemyClientRepository
        )
