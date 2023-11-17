from flask import render_template, request
from src.decorators.require_authorization import login_required
from app import app
from src.helpers.context_generator import dashboard_context
from src.services.users import view_manage_users, set_user_role, set_admin_role, allow_user_login, disallow_user_login


@app.route('/dashboard/manage-services/')
@login_required('admin')
def manage_services(user):
    return render_template('dashboard/manage_services.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/manage-reservable-times/')
@login_required('admin')
def manage_reservable_times(user):
    return render_template('dashboard/manage_reservable_times.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/users/manage-users/')
@login_required('admin')
def manage_users(user):
    return view_manage_users(user)


@app.route('/dashboard/users/manage-users/allow/', methods=['POST'])
@login_required('admin')
def route_allow_user_login(user):
    return allow_user_login(user, request)


@app.route('/dashboard/users/manage-users/disallow/', methods=['POST'])
@login_required('admin')
def route_disallow_user_login(user):
    return disallow_user_login(user, request)


@app.route('/dashboard/users/manage-users/make_admin/', methods=['POST'])
@login_required('admin')
def route_set_admin_role(user):
    return set_admin_role(user, request)


@app.route('/dashboard/users/manage-users/make_user/', methods=['POST'])
@login_required('admin')
def route_set_user_role(user):
    return set_user_role(user, request)


@app.route('/dashboard/locations/edit-location/')
@login_required('admin')
def edit_location(user):
    return render_template('dashboard/locations/edit_location.html', dashboard_context=dashboard_context(user))


@app.route('/dashboard/locations/manage-locations/')
@login_required('admin')
def manage_locations(user):
    return render_template('dashboard/locations/manage_locations.html', dashboard_context=dashboard_context(user))