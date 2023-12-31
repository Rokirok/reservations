from flask import render_template, redirect, url_for, session, request
from src.decorators.require_authorization import login_required
from app import app
from src.helpers.context_generator import dashboard_context
from src.services.reservations import view_reservations, view_reservation, set_complete_status, \
    delete_reservation as service_delete_reservation
from src.services.users import update_user_details as service_update_user_details


@app.route('/dashboard/')
@login_required('user')
def dashboard(user):
    return view_reservations(user, request)


@app.route('/dashboard/reservations/<reservation_id>/')
@login_required('user')
def manage_reservation(user, reservation_id):
    return view_reservation(user, reservation_id)


@app.route('/dashboard/complete-reservation/', methods=['POST'])
@login_required('user')
def complete_reservation(user):
    return set_complete_status(user, request, True)


@app.route('/dashboard/uncomplete-reservation/', methods=['POST'])
@login_required('user')
def uncomplete_reservation(user):
    return set_complete_status(user, request, False)


@app.route('/dashboard/delete-reservation/', methods=['POST'])
@login_required('user')
def delete_reservation(user):
    return service_delete_reservation(user, request)


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
