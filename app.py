from flask import Flask, render_template
from os import getenv
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import src.routes.authentication
import src.routes.dashboard


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


if __name__ == '__main__':
    app.run()
