from flask import render_template, request
from src.decorators.require_authorization import login_required
from app import app
from src.helpers.context_generator import dashboard_context
from src.services.users import view_manage_users, set_user_role, set_admin_role, allow_user_login, disallow_user_login
from src.services.services import show_services, add_service, remove_service


@app.route('/dashboard/manage-services/')
@login_required('admin')
def manage_services(user):
    return show_services(user)


@app.route('/dashboard/manage-services/create/', methods=['POST'])
@login_required('admin')
def create_service(user):
    return add_service(user, request)


@app.route('/dashboard/manage-services/delete/', methods=['POST'])
@login_required('admin')
def delete_service(user):
    return remove_service(user, request)


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