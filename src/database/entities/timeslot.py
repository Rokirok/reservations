from __future__ import annotations
from uuid import uuid4
from src.database.entities.location import Location
from src.database.entities.user import User
from src.database.entities.service import Service
from datetime import datetime


class Timeslot:
    def __init__(self, timeslot_id: str, timestamp: datetime, location: Location, employee: User, service: Service):
        self.timeslot_id = timeslot_id
        self.timestamp = timestamp
        self.location = location
        self.employee = employee
        self.service = service

    @classmethod
    def new_timeslot(cls, timestamp: datetime, location: Location, employee: User, service: Service) -> Timeslot:
        new_timeslot_id = str(uuid4())
        return cls(new_timeslot_id, timestamp, location, employee, service)
