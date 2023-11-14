from flask import Flask, render_template, url_for, redirect
from os import getenv
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import src.routes.authentication
from src.helpers.require_authorization import login_required


@app.route('/')
def index():
    return render_template('customer/landing_page.html')


@app.route('/locations/')
def list_locations():
    return render_template('customer/locations.html')


@app.route('/reserve/')
def select_location():
    return render_template('customer/select_location.html')


@app.route('/reserve/locationId/')
def select_employee():
    return render_template('customer/select_employee.html')


@app.route('/reserve/locationId/employeeId/')
def finish_reservation():
    return render_template('customer/create_reservation.html')


@app.route('/search-reservation')
def search_reservation():
    return render_template('customer/search_reservation.html')


@app.route('/edit-reservation')
def edit_reservation():
    return render_template('customer/edit_reservation.html')


@app.route('/dashboard/')
@login_required('user')
def dashboard(user):
    return render_template('dashboard/dashboard.html')


@app.route('/dashboard/manage-services/')
def manage_services():
    return render_template('dashboard/manage_services.html')


@app.route('/dashboard/reservations/reservationId')
def manage_reservation():
    return render_template('dashboard/manage_reservation.html')


@app.route('/dashboard/manage-reservable-times/')
def manage_reservable_times():
    return render_template('dashboard/manage_reservable_times.html')


@app.route('/dashboard/users/manage-users/')
def manage_users():
    return render_template('dashboard/users/manage_users.html')


@app.route('/dashboard/users/user-details/')
def user_details():
    return render_template('dashboard/users/user_details.html')


@app.route('/dashboard/locations/manage-locations/')
def manage_locations():
    return render_template('dashboard/locations/manage_locations.html')


@app.route('/dashboard/locations/edit-location/')
def edit_location():
    return render_template('dashboard/locations/edit_location.html')


@app.route('/dashboard/logout/')
def logout():
    return redirect(url_for('index'), code=302)


if __name__ == '__main__':
    app.run()
