from flask import render_template, Request, redirect, url_for
from src.database.entities.user import User
from src.helpers.context_generator import dashboard_context
from src.database.repositories.user_repository import get_all_users, get_user_by_id, set_user_role as set_role, \
    set_allow_status, update_details, get_reservable_employees
from src.database.repositories.location_repository import get_location_by_id
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request
from src.helpers.generic_validators import is_uuid
import re

RFC_5322_EMAIL_REGEX = ('(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:['
                        'a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5['
                        '0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])')


def view_manage_users(user: User):
    # Decorator in the route handler handles the role checking
    users = get_all_users()
    return render_template('dashboard/users/manage_users.html', dashboard_context=dashboard_context(user), users=users)


def view_reservable_employees(location_id: str):
    if not is_uuid(location_id):
        return redirect('/reserve/', code=302)
    location = get_location_by_id(location_id)
    if not location:
        return redirect('/reserve/', code=302)
    employees = get_reservable_employees()
    return render_template('customer/select_employee.html', employees=employees, location_id=location_id)


def _validate_user_id(request: Request) -> None:
    if not request.form['user_id']:
        raise ValidationException('Pyynnöstä puuttuu user_id parametri')

    if len(request.form['user_id']) < 2:
        raise ValidationException('user_id ei ole UUID')


def allow_user_login(executor: User, request: Request):
    try:
        validate_request(_validate_user_id, request)
    except ValidationException:
        return redirect('/dashboard/users/manage-users/', code=302)
    user_id = request.form['user_id']
    user = get_user_by_id(user_id)
    if not user:
        return redirect('/dashboard/users/manage-users/', code=302)
    set_allow_status(user, True)
    return redirect('/dashboard/users/manage-users/', code=302)


def disallow_user_login(executor: User, request: Request):
    try:
        validate_request(_validate_user_id, request)
    except ValidationException:
        return redirect('/dashboard/users/manage-users/', code=302)
    user_id = request.form['user_id']
    user = get_user_by_id(user_id)
    if not user:
        return redirect('/dashboard/users/manage-users/', code=302)
    set_allow_status(user, False)
    return redirect('/dashboard/users/manage-users/', code=302)


def set_admin_role(executor: User, request: Request):
    try:
        validate_request(_validate_user_id, request)
    except ValidationException:
        return redirect('/dashboard/users/manage-users/', code=302)
    user_id = request.form['user_id']
    user = get_user_by_id(user_id)
    if not user:
        return redirect('/dashboard/users/manage-users/', code=302)
    set_role(user, 'admin')
    return redirect('/dashboard/users/manage-users/', code=302)


def set_user_role(executor: User, request: Request):
    try:
        validate_request(_validate_user_id, request)
    except ValidationException:
        return redirect('/dashboard/users/manage-users/', code=302)
    user_id = request.form['user_id']
    user = get_user_by_id(user_id)
    if not user:
        return redirect('/dashboard/users/manage-users/', code=302)
    set_role(user, 'user')
    return redirect('/dashboard/users/manage-users/', code=302)


def _validate_user_details_update(request: Request):
    if not request.form['user_name']:
        raise ValidationException('Pyynnöstä puuttuu user_name parametri')

    if len(request.form['user_name']) < 2:
        raise ValidationException('user_name on tyhjä')

    if not request.form['user_email']:
        raise ValidationException('Pyynnöstä puuttuu user_email parametri')

    if not re.match(RFC_5322_EMAIL_REGEX, request.form['user_email']):
        raise ValidationException('Sähköposti ei ole oikeassa muodossa. Muodon tulisi olla: käyttäjä@example.com')


def update_user_details(executor: User, request: Request):
    try:
        validate_request(_validate_user_details_update, request)
    except ValidationException:
        return redirect('/dashboard/users/user-details/', code=302)
    new_user_name = request.form['user_name']
    new_user_email = request.form['user_email']
    update_details(executor, new_user_name, new_user_email)
    return redirect('/dashboard/users/user-details/', code=302)
