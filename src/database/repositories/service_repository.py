from src.database.entities.service import Service
from src.database.db_connection import db
from sqlalchemy.sql import text


def create_service(name: str, price: int) -> Service:
    service = Service.new_service(name, price)
    insert_query = "INSERT INTO services (id, name, price_snt) VALUES (:id, :name, :price)"
    db.session.execute(text(insert_query), {"id": service.service_id, "name": service.name, "price": service.price})
    db.session.commit()
    return service


def get_service_by_id(id: str) -> Service or None:
    result = db.session.execute(text("SELECT id, name, price_snt FROM services WHERE id = :id"), {"id": id})
    services_array = result.fetchall()
    if len(services_array) == 0:
        return None
    service_data = services_array[0]
    service_id = service_data[0]
    service_name = service_data[1]
    service_price = service_data[2]
    service = Service(service_id=service_id, name=service_name, price=service_price)
    return service


def list_services() -> list[Service]:
    result = db.session.execute(text("SELECT id, name, price_snt FROM services"))
    raw_services_array = result.fetchall()
    services_array = []
    for service_data in raw_services_array:
        service_id = service_data[0]
        service_name = service_data[1]
        service_price = service_data[2]
        service = Service(service_id=service_id, name=service_name, price=service_price)
        services_array.append(service)
    return services_array


def get_deletable_service_ids() -> list[str]:
    result = db.session.execute(text("SELECT services.id, rt.id IS NULL as can_be_deleted FROM services LEFT JOIN reservable_timeslots rt ON services.id = rt.service"))
    raw_results_array = result.fetchall()
    deletable_service_ids = []
    for row in raw_results_array:
        if row[1] is True:
            deletable_service_ids.append(row[0])
    return deletable_service_ids


def delete_service(id: str):
    delete_query = "DELETE FROM services WHERE id = :id"
    db.session.execute(text(delete_query), {"id": id})
    db.session.commit()


def get_reservable_services() -> list[Service]:
    select_query = 'SELECT s.id, s.name, s.price_snt FROM reservable_timeslots JOIN services s ON service = s.id WHERE NOT EXISTS (SELECT FROM reservations WHERE timeslot = reservable_timeslots.id) GROUP BY s.id'
    result = db.session.execute(text(select_query))
    raw_services_array = result.fetchall()
    services_array = []
    for service_data in raw_services_array:
        service_id = service_data[0]
        service_name = service_data[1]
        service_price = service_data[2]
        service = Service(service_id=service_id, name=service_name, price=service_price)
        services_array.append(service)
    return services_array
