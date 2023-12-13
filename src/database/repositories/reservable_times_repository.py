from datetime import datetime
from src.database.entities.reservation import Timeslot
from src.database.entities.user import User
from src.database.entities.service import Service
from src.database.entities.location import Location
from src.database.db_connection import db
from sqlalchemy.sql import text
from src.database.repositories.service_repository import get_service_by_id
from src.database.repositories.location_repository import get_location_by_id
from src.database.repositories.user_repository import get_user_by_id


def create_reservable_time(time: datetime, user: User, service: Service, location: Location) -> Timeslot:
    timeslot = Timeslot.new_timeslot(time, location, user, service)
    insert_query = "INSERT INTO reservable_timeslots (id, timestamp, location, employee, service) VALUES (:id, :timestamp, :location, :employee, :service)"
    db.session.execute(text(insert_query), {
        "id": timeslot.timeslot_id,
        "timestamp": timeslot.timestamp,
        "location": timeslot.location.location_id,
        "employee": timeslot.employee.user_id,
        "service": timeslot.service.service_id
    })
    db.session.commit()
    return timeslot


def list_reservable_times() -> (list[Timeslot], list[str]):
    result = db.session.execute(text(
        "SELECT rt.id, rt.timestamp, rt.location, rt.employee, rt.service, reservations.id IS NOT NULL as reserved FROM reservable_timeslots rt LEFT JOIN reservations ON reservations.timeslot = rt.id ORDER BY rt.timestamp DESC"))
    raw_reservable_times_array = result.fetchall()
    reservable_times_array = []
    reserved_ids = []
    for rt_data in raw_reservable_times_array:
        rt_id = rt_data[0]
        rt_timestamp = rt_data[1]
        rt_location_id = rt_data[2]
        rt_employee_id = rt_data[3]
        rt_service_id = rt_data[4]
        rt_reserved_status = rt_data[5]
        rt_location = get_location_by_id(rt_location_id)
        rt_employee = get_user_by_id(rt_employee_id)
        rt_service = get_service_by_id(rt_service_id)
        reservable_time = Timeslot(rt_id, rt_timestamp, rt_location, rt_employee, rt_service)
        reservable_times_array.append(reservable_time)
        if rt_reserved_status:
            reserved_ids.append(rt_id)
    return reservable_times_array, reserved_ids


def get_reservable_times(service_filter: Service, location_filter: Location):
    select_query = 'SELECT rt.id, rt.timestamp, rt.location, rt.employee, rt.service FROM reservable_timeslots rt WHERE NOT EXISTS (SELECT FROM reservations WHERE timeslot = rt.id) AND rt.location = :location_id AND rt.service = :service_id ORDER BY rt.timestamp DESC'
    result = db.session.execute(text(select_query),
                                {"service_id": service_filter.service_id, "location_id": location_filter.location_id})
    raw_reservable_times_array = result.fetchall()
    reservable_times_array = []
    for rt_data in raw_reservable_times_array:
        rt_id = rt_data[0]
        rt_timestamp = rt_data[1]
        rt_location_id = rt_data[2]
        rt_employee_id = rt_data[3]
        rt_service_id = rt_data[4]
        rt_location = get_location_by_id(rt_location_id)
        rt_employee = get_user_by_id(rt_employee_id)
        rt_service = get_service_by_id(rt_service_id)
        reservable_time = Timeslot(rt_id, rt_timestamp, rt_location, rt_employee, rt_service)
        reservable_times_array.append(reservable_time)
    return reservable_times_array


def get_reservable_time_by_id(rt_id: str):
    select_query = 'SELECT rt.id, rt.timestamp, rt.location, rt.employee, rt.service FROM reservable_timeslots rt WHERE rt.id = :id'
    result = db.session.execute(text(select_query), {"id": rt_id})
    raw_rt_array = result.fetchall()
    if len(raw_rt_array) == 0:
        return None
    rt_data = raw_rt_array[0]
    rt_id = rt_data[0]
    rt_timestamp = rt_data[1]
    rt_location_id = rt_data[2]
    rt_employee_id = rt_data[3]
    rt_service_id = rt_data[4]
    rt_location = get_location_by_id(rt_location_id)
    rt_employee = get_user_by_id(rt_employee_id)
    rt_service = get_service_by_id(rt_service_id)
    return Timeslot(rt_id, rt_timestamp, rt_location, rt_employee, rt_service)
