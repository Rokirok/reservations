from app import app
from src.services.locations import view_customer_locations, view_reservable_locations
from src.services.services import view_reservable_services
from src.services.reservable_times import view_customer_reservable_times


@app.route('/locations/')
def list_locations():
    return view_customer_locations()


@app.route('/reserve/')
def select_service():
    return view_reservable_services()


@app.route('/reserve/<service_id>/')
def select_location(service_id: str):
    return view_reservable_locations(service_id)


@app.route('/reserve/<service_id>/<location_id>/')
def finish_reservation(service_id: str, location_id: str):
    return view_customer_reservable_times(service_id, location_id)
