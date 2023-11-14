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


def delete_service(id: str):
    delete_query = "DELETE FROM services WHERE id = :id"
    db.session.execute(text(delete_query), {"id": id})
    db.session.commit()
