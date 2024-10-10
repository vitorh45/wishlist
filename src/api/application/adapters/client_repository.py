import logging
from typing import Union, Optional
from uuid import UUID

from api.app import db
from api.application.persistency.tables import Client as ClientTable
from api.domain.models.client import Client
from api.domain.ports.client import ClientRepository

logger = logging.getLogger("wishlist")


class SQLAlchemyClientRepository(ClientRepository):
    @staticmethod
    def _build_client(row) -> Client:
        return Client(
            name=row.name,
            email=row.email,
            id=row.id,
            insert_at=row.insert_at,
            update_at=row.update_at,
        )

    @classmethod
    def persist_client(
        cls,
        name: str,
        email: str
    ) -> "Client":
        logger.info(
            "Creating a new client.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "create_client",
                    "name": name,
                    "email": email
                }
            },
        )
        try:
            client = ClientTable(name=name, email=email)
            db.session.add(client)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create a new client.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "create_client",
                        "name": name,
                        "email": email
                    }
                },
            )
            raise e

        return cls.get_by_email(email=email)
    

    @classmethod
    def get_by_email(cls, email: str) -> Optional["Client"]:
        logger.info(
            "Getting client by email.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_email",
                    "email": email,
                }
            },
        )
        try:
            client = ClientTable.query.filter_by(email=email).first()
        except Exception as e:
            logger.exception(
                "Error while trying to get client by email.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_email",
                        "email": email,
                    }
                },
            )
            raise e

        if client:
            logger.info(
                "Client found.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_email",
                        "email": email,
                    }
                },
            )

            # return cls._build_client(client)
            return client

        logger.info(
            "Client not found.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_email",
                    "email": email,
                }
            },
        )
        return None
    
    @classmethod
    def get_by_id(cls, client_id: UUID) -> Optional["Client"]:
        logger.info(
            "Getting client by client_id.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "client_id": client_id,
                }
            },
        )
        try:
            client = ClientTable.query.filter_by(id=client_id).first()
        except Exception as e:
            logger.exception(
                "Error while trying to get client by id.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "client_id": client_id,
                    }
                },
            )
            raise e

        if client:
            logger.info(
                "Client found.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_id",
                        "client_id": client_id,
                    }
                },
            )

            # return cls._build_client(client)
            return client

        logger.info(
            "Client not found.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_id",
                    "client_id": client_id,
                }
            },
        )
        return None

    @classmethod
    def delete_by_email(
        cls,
        email: str
    ) -> "Client":
        logger.info(
            "Deleting a client.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "delete_by_email",
                    "email": email
                }
            },
        )
        try:
            client = ClientTable.query.filter_by(email=email).first()
            if client:
                db.session.delete(client)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to delete a client.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "delete_by_email",
                        "email": email
                    }
                },
            )
            raise e

        return None
    
    @classmethod
    def update_by_email(
        cls,
        email: str,
        name: str
    ) -> "Client":
        logger.info(
            "Updating a client.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "update_by_email",
                    "email": email,
                    "name": name,
                }
            },
        )
        try:
            client = ClientTable.query.filter_by(email=email).first()
            if client:
                client.name = name
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to update a client.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "update_by_email",
                        "email": email,
                        "name": name,
                    }
                },
            )
            raise e

        # return cls.get_by_email(email=email)
        return client