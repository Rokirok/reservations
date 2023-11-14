from __future__ import annotations
from uuid import uuid4


class Service:
    def __init__(self, service_id: str, name: str, price: int):
        self.service_id = service_id
        self.name = name
        self.price = price

    @classmethod
    def new_service(cls, name: str, price: int) -> Service:
        new_service_id = str(uuid4())
        return cls(new_service_id, name, price)
