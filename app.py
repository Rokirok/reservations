from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('customer/landing_page.html')


@app.route('/locations')
def list_locations():
    return render_template('customer/locations.html')


@app.route('/reserve')
def select_location():
    return render_template('customer/select_location.html')

@app.route('/reserve/locationId')
def select_employee():
    return render_template('customer/select_employee.html')


@app.route('/reserve/locationId/employeeId')
def finish_reservation():
    return render_template('customer/create_reservation.html')


@app.route('/login')
def login():
    return render_template('customer/login.html')


@app.route('/register')
def register():
    return render_template('customer/register.html')

if __name__ == '__main__':
    app.run()
