from flask import render_template, request, session
from app import app
from src.services.authentication import register_user, login_user


@app.route('/login/', methods=['GET'])
def view_login():
    return render_template('customer/login.html')


@app.route('/login/', methods=['POST'])
def handle_login():
    return login_user(request, session)


@app.route('/register/', methods=['GET'])
def view_register():
    return render_template('customer/register.html')


@app.route('/register/', methods=['POST'])
def handle_register():
    return register_user(request)


@app.route('/successful_registration/', methods=['GET'])
def view_successful_register():
    created_as_admin = request.args.get('created_as_admin', False) == 'yes'
    return render_template('customer/successful_registration.html', created_as_admin=created_as_admin)
