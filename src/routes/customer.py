from app import app
from flask import request, render_template
from src.services.locations import view_customer_locations, view_reservable_locations
from src.services.services import view_reservable_services
from src.services.reservable_times import view_customer_reservable_times
from src.services.reservations import create_reservation, search_for_reservation, show_edit_reservation, \
    save_edited_reservation


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


@app.route('/successful-reservation/')
def successful_reservation():
    return render_template('customer/successful_reservation.html', pin=request.args.get('pin', 'N/A'))


@app.route('/search-reservation/')
def view_search_reservation():
    return render_template('customer/search_reservation.html')


@app.route('/search-reservation/', methods=['POST'])
def search_reservation():
    return search_for_reservation(request)


@app.route('/edit-reservation/<reservation_id>')
def edit_reservation(reservation_id: str):
    return show_edit_reservation(request, reservation_id)


@app.route('/edit-reservation/<reservation_id>', methods=['POST'])
def save_edit_reservation(reservation_id: str):
    return save_edited_reservation(request, reservation_id)
