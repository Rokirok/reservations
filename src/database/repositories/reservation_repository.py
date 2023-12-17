import random

from sqlalchemy import text

from src.database.db_connection import db
from src.database.entities.reservation import Reservation
from src.database.entities.timeslot import Timeslot
from src.database.repositories.reservable_times_repository import get_reservable_time_by_id


def generate_pin():
    pin = ''
    for i in range(4):
        pin += str(random.randint(0, 9))
    return pin


def create_reservation(timeslot: Timeslot, customer_name: str, customer_mobile: str, customer_email: str, message: str):
    reservation = Reservation.new_reservation(generate_pin(), timeslot, customer_name, customer_mobile, customer_email,
                                              message, False)
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


def search_reservation(email: str, pin: str) -> Reservation or None:
    select_query = 'SELECT id, pin, timeslot, customer_name, customer_email, customer_mobile, message, completed FROM reservations WHERE customer_email = :email AND pin = :pin'
    result = db.session.execute(text(select_query), {"email": email, "pin": pin})
    reservation_data = result.fetchone()
    if reservation_data is None:
        return None
    id = reservation_data[0]
    pin = reservation_data[1]
    timeslot_id = reservation_data[2]
    customer_name = reservation_data[3]
    customer_email = reservation_data[4]
    customer_mobile = reservation_data[5]
    message = reservation_data[6]
    completed = reservation_data[7]
    timeslot = get_reservable_time_by_id(timeslot_id)
    return Reservation(id, pin, timeslot, customer_name, customer_mobile, customer_email, message, completed)


def get_reservation_by_id(reservation_id: str) -> Reservation or None:
    select_query = 'SELECT id, pin, timeslot, customer_name, customer_email, customer_mobile, message, completed FROM reservations WHERE :id = id'
    result = db.session.execute(text(select_query), {"id": reservation_id})
    reservation_data = result.fetchone()
    if reservation_data is None:
        return None
    id = reservation_data[0]
    pin = reservation_data[1]
    timeslot_id = reservation_data[2]
    customer_name = reservation_data[3]
    customer_email = reservation_data[4]
    customer_mobile = reservation_data[5]
    message = reservation_data[6]
    completed = reservation_data[7]
    timeslot = get_reservable_time_by_id(timeslot_id)
    return Reservation(id, pin, timeslot, customer_name, customer_mobile, customer_email, message, completed)


def save_updated_reservation(reservation: Reservation) -> Reservation:
    update_query = 'UPDATE reservations SET customer_name = :customer_name, customer_email = :customer_email, customer_mobile = :customer_mobile, message = :message WHERE id = :id'
    db.session.execute(text(update_query), {
        "id": reservation.reservation_id,
        "customer_name": reservation.customer_name,
        "customer_email": reservation.customer_email,
        "customer_mobile": reservation.customer_mobile,
        "message": reservation.message
    })
    db.session.commit()
    return reservation

def get_all_reservations() -> list[Reservation]:
    select_query = 'SELECT id, pin, timeslot, customer_name, customer_email, customer_mobile, message, completed FROM reservations'
    result = db.session.execute(text(select_query))
    raw_reservations_array = result.fetchall()
    reservations = []
    for reservation_data in raw_reservations_array:
        id = reservation_data[0]
        pin = reservation_data[1]
        timeslot_id = reservation_data[2]
        customer_name = reservation_data[3]
        customer_email = reservation_data[4]
        customer_mobile = reservation_data[5]
        message = reservation_data[6]
        completed = reservation_data[7]
        timeslot = get_reservable_time_by_id(timeslot_id)
        reservation = Reservation(id, pin, timeslot, customer_name, customer_mobile, customer_email, message, completed)
        reservations.append(reservation)
    return reservations


def set_complete_status(reservation: Reservation, completed: bool) -> Reservation:
    reservation.completed = completed
    update_query = 'UPDATE reservations SET completed = :completed WHERE id = :id'
    db.session.execute(text(update_query), {
        "id": reservation.reservation_id,
        "completed": reservation.completed
    })
    db.session.commit()
    return reservation


def delete_reservation(reservation: Reservation):
    delete_query = 'DELETE FROM reservations WHERE id = :id'
    db.session.execute(text(delete_query), {
        "id": reservation.reservation_id
    })
    db.session.commit()
