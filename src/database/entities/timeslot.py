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
