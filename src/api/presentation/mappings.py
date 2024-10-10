from typing import Optional, Literal


class PayloadMapping:
    def __init__(self, *, payload: dict) -> None:
        self.payload = payload
        

class CreateClientRequestMapping(PayloadMapping):
    @property
    def name(self) -> str:
        return self.payload.get("name")

    @property
    def email(self) -> str:
        return self.payload.get("email")
    

class UpdateClientRequestMapping(PayloadMapping):
    @property
    def name(self) -> str:
        return self.payload.get("name")


class UserLoginRequestMapping(PayloadMapping):
    @property
    def username(self) -> str:
        return self.payload.get("username")

    @property
    def password(self) -> str:
        return self.payload.get("password")


class CreateWishlistRequestMapping(PayloadMapping):
    @property
    def client_id(self) -> str:
        return self.payload.get("client_id")


class AddProductWishlistRequestMapping(PayloadMapping):
    @property
    def product_id(self) -> str:
        return self.payload.get("product_id")