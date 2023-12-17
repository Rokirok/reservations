from flask import render_template, Request, redirect
from src.helpers.context_generator import dashboard_context
from src.database.entities.user import User
from src.database.repositories.location_repository import list_locations, create_location, delete_location, get_reservable_locations
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request
from urllib.parse import urlparse
from src.helpers.generic_validators import is_uuid
from src.database.repositories.service_repository import get_service_by_id


def view_manage_locations(user: User):
    locations = list_locations()
    return render_template('dashboard/locations/manage_locations.html', dashboard_context=dashboard_context(user),
                           locations=locations)


def view_customer_locations():
    locations = list_locations()
    return render_template('customer/locations.html', locations=locations)


def view_reservable_locations(service_id: str):
    if not is_uuid(service_id):
        return redirect('/reserve/', code=302)
    service = get_service_by_id(service_id)
    if not service:
        return redirect('/reserve/', code=302)
    locations = get_reservable_locations(service)
    return render_template('customer/select_location.html', locations=locations, service=service)


def _validate_create_location(request: Request) -> None:
    if not request.form['location_name']:
        raise ValidationException('Pyynnöstä puuttuu location_name parametri')

    if len(request.form['location_name']) < 1:
        raise ValidationException('location_name on tyhjä')

    if not request.form['location_address']:
        raise ValidationException('Pyynnöstä puuttuu location_address parametri')

    if len(request.form['location_address']) < 1:
        raise ValidationException('location_address on tyhjä')

    if request.form['location_cover_image']:
        parsed_url = urlparse(request.form['location_cover_image'])
        if not parsed_url.scheme == 'https':
            raise ValidationException('location_cover_image ei ole https:// alkuinen URL')


def add_location(executor: User, request: Request):
    try:
        validate_request(_validate_create_location, request)
    except ValidationException:
        return redirect('/dashboard/locations/manage-locations/', code=302)
    location_name = request.form['location_name']
    location_address = request.form['location_address']
    cover_image = request.form['location_cover_image']
    if len(cover_image) == 0:
        cover_image = None
    create_location(location_name, location_address, cover_image)
    return redirect('/dashboard/locations/manage-locations/', code=302)


def _validate_location_id(request: Request) -> None:
    if not request.form['location_id']:
        raise ValidationException('Pyynnöstä puuttuu location_id parametri')

    if len(request.form['location_id']) < 2:
        raise ValidationException('location_id ei ole UUID')


def remove_location(executor: User, request: Request):
    try:
        validate_request(_validate_location_id, request)
    except ValidationException:
        return redirect('/dashboard/locations/manage-locations/', code=302)
    location_id = request.form['location_id']
    delete_location(location_id)
    return redirect('/dashboard/locations/manage-locations/', code=302)