import random

from sqlalchemy import text

from src.database.db_connection import db
from src.database.entities.reservation import Reservation
from src.database.entities.timeslot import Timeslot


def generate_pin():
    pin = ''
    for i in range(4):
        pin += str(random.randint(0, 9))
    return pin


def create_reservation(timeslot: Timeslot, customer_name: str, customer_mobile: str, customer_email: str, message: str):
    reservation = Reservation.new_reservation(generate_pin(), timeslot, customer_name, customer_mobile, customer_email, message, False)
    insert_query = "INSERT INTO reservations (id, pin, timeslot, customer_name, customer_email, customer_mobile, message, completed) VALUES (:id, :pin, :timeslot, :customer_name, :customer_email, :customer_mobile, :message, :completed)"
    db.session.execute(text(insert_query), {
        "id": reservation.reservation_id,
        "pin": reservation.pin,
        "timeslot": reservation.timeslot.timeslot_id,
        "customer_name": reservation.customer_name,
        "customer_email": reservation.customer_email,
        "customer_mobile": reservation.customer_mobile,
        "message": reservation.message,
        "completed": reservation.completed
    })
    db.session.commit()
    return reservation
