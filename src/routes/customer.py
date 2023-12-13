from app import app
from flask import request, render_template
from src.services.locations import view_customer_locations, view_reservable_locations
from src.services.services import view_reservable_services
from src.services.reservable_times import view_customer_reservable_times
from src.services.reservations import create_reservation


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


@app.route('/reserve/create-reservation/', methods=['POST'])
def post_create_reservation():
    return create_reservation(request)


@app.route('/successful-reservation')
def successful_reservation():
    return render_template('customer/successful_reservation.html', pin=request.args.get('pin', 'N/A'))
