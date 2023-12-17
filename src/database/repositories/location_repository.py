from src.database.entities.location import Location
from src.database.entities.service import Service
from src.database.db_connection import db
from sqlalchemy.sql import text


def create_location(name: str, address: str, cover_image: str or None) -> Location:
    location = Location.new_location(name, address, cover_image)
    insert_query = "INSERT INTO locations (id, name, address, cover_image) VALUES (:id, :name, :address, :cover_image)"
    db.session.execute(text(insert_query), {
        "id": location.location_id,
        "name": location.name,
        "address": location.address,
        "cover_image": location.cover_image
    })
    db.session.commit()
    return location


def get_location_by_id(id: str) -> Location or None:
    result = db.session.execute(text("SELECT id, name, address, cover_image FROM locations WHERE id = :id"), {"id": id})
    locations_array = result.fetchall()
    if len(locations_array) == 0:
        return None
    location_data = locations_array[0]
    location_id = location_data[0]
    location_name = location_data[1]
    location_address = location_data[2]
    location_cover_image = location_data[3]
    location = Location(location_id=location_id, name=location_name, address=location_address,
                        cover_image=location_cover_image)
    return location


def list_locations() -> list[Location]:
    result = db.session.execute(text("SELECT id, name, address, cover_image FROM locations"))
    raw_locations_array = result.fetchall()
    locations_array = []
    for location_data in raw_locations_array:
        location_id = location_data[0]
        location_name = location_data[1]
        location_address = location_data[2]
        location_cover_image = location_data[3]
        location = Location(location_id=location_id, name=location_name, address=location_address,
                            cover_image=location_cover_image)
        locations_array.append(location)
    return locations_array


def get_deletable_location_ids() -> list[str]:
    result = db.session.execute(text("SELECT locations.id, rt.id IS NULL as can_be_deleted FROM locations LEFT JOIN reservable_timeslots rt ON locations.id = rt.location"))
    raw_results_array = result.fetchall()
    deletable_location_ids = []
    for row in raw_results_array:
        if row[1] is True:
            deletable_location_ids.append(row[0])
    return deletable_location_ids


def delete_location(id: str):
    delete_query = "DELETE FROM locations WHERE id = :id"
    db.session.execute(text(delete_query), {"id": id})
    db.session.commit()


def get_reservable_locations(service_filter: Service) -> list[Location]:
    select_query = 'SELECT l.id, l.name, l.address, l.cover_image FROM reservable_timeslots JOIN locations l ON location = l.id WHERE NOT EXISTS (SELECT FROM reservations WHERE timeslot = reservable_timeslots.id) AND reservable_timeslots.service = :service_filter_id GROUP BY l.id'
    result = db.session.execute(text(select_query), {"service_filter_id": service_filter.service_id})
    raw_locations_array = result.fetchall()
    locations_array = []
    for location_data in raw_locations_array:
        location_id = location_data[0]
        location_name = location_data[1]
        location_address = location_data[2]
        location_cover_image = location_data[3]
        location = Location(location_id=location_id, name=location_name, address=location_address,
                            cover_image=location_cover_image)
        locations_array.append(location)
    return locations_array
