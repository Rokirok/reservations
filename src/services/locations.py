from flask import render_template, Request, redirect
from src.helpers.context_generator import dashboard_context
from src.database.entities.user import User
from src.database.repositories.location_repository import list_locations, create_location, delete_location
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request
from urllib.parse import urlparse


def view_manage_locations(user: User):
    locations = list_locations()
    return render_template('dashboard/locations/manage_locations.html', dashboard_context=dashboard_context(user),
                           locations=locations)


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