from flask import render_template, Request, redirect
from src.helpers.context_generator import dashboard_context
from src.database.entities.user import User
from src.database.repositories.location_repository import list_locations, get_location_by_id
from src.database.repositories.service_repository import list_services, get_service_by_id
from src.database.repositories.user_repository import list_employees, get_user_by_id
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request
from datetime import datetime
from src.helpers.generic_validators import is_uuid
from src.database.repositories.reservable_times_repository import create_reservable_time as db_create_reservable_time


def view_reservable_times(user: User):
    locations = list_locations()
    services = list_services()
    employees = list_employees()
    return render_template('dashboard/manage_reservable_times.html', dashboard_context=dashboard_context(user),
                           locations=locations, employees=employees, services=services)


def view_customer_reservable_times(location_id: str, employee_id: str):
    return render_template('customer/create_reservation.html')


def _validate_create_reservable_time(req: Request):
    form_body = req.form
    required_fields = {"location", "date", "time", "employee", "service"}

    if not required_fields.issubset(form_body.keys()):
        raise ValidationException(
            "Request form doesn't have 'location', 'date', 'time', 'employee' and 'service' parameters")

    try:
        datetime.strptime(req.form['date'], '%d.%m.%Y')
        datetime.strptime(req.form['time'], '%H.%M')
    except ValueError:
        raise ValidationException(
            "Date or time is not in the proper format. Date should be DD.MM.YYYY and time as HH.MM")

    if not is_uuid(req.form['employee']):
        raise ValidationException('Employee is not an UUID')

    if not is_uuid(req.form['service']):
        raise ValidationException('Service is not an UUID')

    if not is_uuid(req.form['location']):
        raise ValidationException('Location is not an UUID')


def create_reservable_time(user: User, request: Request):
    try:
        validate_request(_validate_create_reservable_time, request)
    except ValidationException as e:
        print('validation exception')
        print(e)
        # TODO: Return error message to frontend
        return redirect('/dashboard/manage-reservable-times/', code=302)
    location = get_location_by_id(request.form['location'])
    service = get_service_by_id(request.form['service'])
    employee = get_user_by_id(request.form['employee'])

    if not location or not service or not employee:
        return redirect('/dashboard/manage-reservable-times/', code=302)

    parsed_time = datetime.strptime(str(request.form['time']), '%H.%M').time()
    parsed_date = datetime.strptime(str(request.form['date']), '%d.%m.%Y').date()
    parsed_datetime = datetime.combine(parsed_date, parsed_time)

    db_create_reservable_time(parsed_datetime, user, service, location)

    return redirect('/dashboard/manage-reservable-times/', code=302)


def delete_reservable_time(user: User, request: Request):
    return redirect('/dashboard/manage-reservable-times/', code=302)
