from datetime import datetime
from src.database.entities.reservation import Timeslot
from src.database.entities.user import User
from src.database.entities.service import Service
from src.database.entities.location import Location
from src.database.db_connection import db
from sqlalchemy.sql import text


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
