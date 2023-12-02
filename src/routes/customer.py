from app import app
from src.services.locations import view_customer_locations, view_reservable_locations
from src.services.users import view_reservable_employees
from src.services.reservable_times import view_customer_reservable_times


@app.route('/locations/')
def list_locations():
    return view_customer_locations()


@app.route('/reserve/')
def select_location():
    return view_reservable_locations()


@app.route('/reserve/<location_id>/')
def select_employee(location_id: str):
    return view_reservable_employees(location_id)


@app.route('/reserve/<location_id>/<employee_id>/')
def finish_reservation(location_id: str, employee_id: str):
    return view_customer_reservable_times(location_id, employee_id)
