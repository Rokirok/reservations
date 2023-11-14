from timeslot import Timeslot


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
