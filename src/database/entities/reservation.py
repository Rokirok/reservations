from __future__ import annotations
from uuid import uuid4
from src.database.entities.timeslot import Timeslot


class Reservation:
    def __init__(self, reservation_id: str, pin: str, timeslot: Timeslot, customer_name: str, customer_mobile: str,
                 customer_email: str, message: str, completed: bool):
        self.reservation_id = reservation_id
        self.pin = pin
        self.timeslot = timeslot
        self.customer_name = customer_name
        self.customer_mobile = customer_mobile
        self.customer_email = customer_email
        self.message = message
        self.completed = completed

    @classmethod
    def new_reservation(cls, pin: str, timeslot: Timeslot, customer_name: str, customer_mobile: str,
                        customer_email: str, message: str, completed: bool) -> Reservation:
        new_reservation_id = str(uuid4())
        return cls(new_reservation_id, pin, timeslot, customer_name, customer_mobile, customer_email, message,
                   completed)
