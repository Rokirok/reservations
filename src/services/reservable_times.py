from flask import render_template, Request, redirect, flash
from src.helpers.context_generator import dashboard_context
from src.database.entities.user import User
from src.database.repositories.location_repository import list_locations, get_location_by_id
from src.database.repositories.service_repository import list_services, get_service_by_id
from src.database.repositories.user_repository import list_employees, get_user_by_id
from src.database.repositories.reservable_times_repository import get_reservable_times, get_reservable_time_by_id
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request
from datetime import datetime
from src.helpers.generic_validators import is_uuid
from src.database.repositories.reservable_times_repository import create_reservable_time as db_create_reservable_time, \
    list_reservable_times, delete_reservable_time as db_delete_reservable_time


def view_reservable_times(user: User):
    reservable_times = list_reservable_times()
    locations = list_locations()
    services = list_services()
    employees = list_employees()
    return render_template('dashboard/manage_reservable_times.html', dashboard_context=dashboard_context(user),
                           locations=locations, employees=employees, services=services,
                           reservable_times=reservable_times[0], reserved_ids=reservable_times[1])


def view_customer_reservable_times(service_id: str, location_id: str):
    if not is_uuid(service_id):
        return redirect('/reserve/', code=302)
    if not is_uuid(location_id):
        return redirect(f'/reserve/${service_id}', code=302)
    service = get_service_by_id(service_id)
    location = get_location_by_id(location_id)
    if not service:
        return redirect('/reserve/', code=302)
    if not location:
        return redirect(f'/reserve/${service_id}', code=302)
    reservable_times = get_reservable_times(service, location)
    return render_template('customer/create_reservation.html', location=location, service=service,
                           reservable_times=reservable_times)


def _validate_create_reservable_time(req: Request):
    form_body = req.form
    required_fields = {"location", "date", "time", "employee", "service"}

    if not required_fields.issubset(form_body.keys()):
        raise ValidationException("Täytäthän kaikki kentät!")

    try:
        datetime.strptime(req.form['date'], '%d.%m.%Y')
    except ValueError:
        raise ValidationException(
            "Päivän tulisi olla muodossa DD.MM.YYYY Esim. 22.12.2023")
    try:
        datetime.strptime(req.form['time'], '%H.%M')
    except ValueError:
        raise ValidationException("Ajan tulisi olla muodossa HH.MM Esim. 10.15")

    if not is_uuid(req.form['employee']):
        raise ValidationException('Työntekijä-kenttä ei saa olla tyhjä!')

    if not is_uuid(req.form['service']):
        raise ValidationException('Palvelu-kenttä ei saa olla tyhjä!')

    if not is_uuid(req.form['location']):
        raise ValidationException('Toimipiste-kenttä ei saa olla tyhjä!')


def create_reservable_time(user: User, request: Request):
    try:
        validate_request(_validate_create_reservable_time, request)
    except ValidationException as e:
        flash(str(e), 'error')
        return redirect('/dashboard/manage-reservable-times/', code=302)
    location = get_location_by_id(request.form['location'])
    service = get_service_by_id(request.form['service'])
    employee = get_user_by_id(request.form['employee'])

    if not location or not service or not employee:
        return redirect('/dashboard/manage-reservable-times/', code=302)

    parsed_time = datetime.strptime(str(request.form['time']), '%H.%M').time()
    parsed_date = datetime.strptime(str(request.form['date']), '%d.%m.%Y').date()
    parsed_datetime = datetime.combine(parsed_date, parsed_time)

    db_create_reservable_time(parsed_datetime, employee, service, location)

    return redirect('/dashboard/manage-reservable-times/', code=302)


def delete_reservable_time(user: User, request: Request):
    timeslot_id = request.form.get('timeslot_id', '')
    if not is_uuid(timeslot_id):
        return redirect('/dashboard/manage-reservable-times/', code=302)
    timeslot = get_reservable_time_by_id(timeslot_id)
    if not timeslot:
        return redirect('/dashboard/manage-reservable-times/', code=302)
    db_delete_reservable_time(timeslot)
    return redirect('/dashboard/manage-reservable-times/', code=302)
