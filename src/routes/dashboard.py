from flask import render_template, redirect, url_for, session
from src.decorators.require_authorization import login_required
from app import app
from src.helpers.context_generator import dashboard_context


@app.route('/dashboard/')
@login_required('user')
def dashboard(user):
    return render_template('dashboard/dashboard.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/manage-services/')
@login_required('admin')
def manage_services(user):
    return render_template('dashboard/manage_services.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/reservations/reservationId')
@login_required('user')
def manage_reservation(user):
    return render_template('dashboard/manage_reservation.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/manage-reservable-times/')
@login_required('admin')
def manage_reservable_times(user):
    return render_template('dashboard/manage_reservable_times.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/users/manage-users/')
@login_required('admin')
def manage_users(user):
    return render_template('dashboard/users/manage_users.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/users/user-details/')
@login_required('user')
def user_details(user):
    return render_template('dashboard/users/user_details.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/locations/manage-locations/')
@login_required('admin')
def manage_locations(user):
    return render_template('dashboard/locations/manage_locations.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/locations/edit-location/')
@login_required('admin')
def edit_location(user):
    return render_template('dashboard/locations/edit_location.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/logout/')
def logout():
    del session['user_id']
    return redirect(url_for('index'), code=302)
