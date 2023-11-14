from __future__ import annotations
from uuid import uuid4


class Location:
    def __init__(self, location_id: str, name: str, address: str, cover_image: str or None):
        self.location_id = location_id
        self.name = name
        self.address = address
        self.cover_image = cover_image

    @classmethod
    def new_location(cls, name: str, address: str, cover_image: str or None) -> Location:
        new_location_id = str(uuid4())
        return cls(new_location_id, name, address, cover_image)
