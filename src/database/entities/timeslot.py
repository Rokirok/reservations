from __future__ import annotations
from uuid import uuid4
from location import Location
from user import User
from service import Service


class Timeslot:
    def __init__(self, timeslot_id: str, timestamp: int, location: Location, employee: User, service: Service):
        self.timeslot_id = timeslot_id
        self.timestamp = timestamp
        self.location = location
        self.employee = employee
        self.service = service

    @classmethod
    def new_timeslot(cls, timestamp: int, location: Location, employee: User, service: Service) -> Timeslot:
        new_timeslot_id = str(uuid4())
        return cls(new_timeslot_id, timestamp, location, employee, service)
