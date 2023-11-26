from flask import render_template, redirect, url_for, session, request
from src.decorators.require_authorization import login_required
from app import app
from src.helpers.context_generator import dashboard_context
from src.services.users import update_user_details as service_update_user_details


@app.route('/dashboard/')
@login_required('user')
def dashboard(user):
    return render_template('dashboard/dashboard.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/reservations/reservationId')
@login_required('user')
def manage_reservation(user):
    return render_template('dashboard/manage_reservation.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/users/user-details/')
@login_required('user')
def user_details(user):
    return render_template('dashboard/users/user_details.html', dashboard_context=dashboard_context(user), user=user)


@app.route('/dashboard/users/user-details/update/', methods=['POST'])
@login_required('user')
def update_user_details(user):
    return service_update_user_details(user, request)


@app.route('/dashboard/logout/')
def logout():
    del session['user_id']
    return redirect(url_for('index'), code=302)
