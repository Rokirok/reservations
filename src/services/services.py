from flask import render_template, Request, redirect
from src.database.repositories.service_repository import list_services, create_service, delete_service
from src.database.entities.user import User
from src.helpers.context_generator import dashboard_context
from src.helpers.ValidationException import ValidationException
from src.helpers.request_validator import validate_request


def show_services(user: User):
    services = list_services()
    return render_template('dashboard/manage_services.html', dashboard_context=dashboard_context(user),
                           services=services)


def _validate_create_service(request: Request) -> None:
    if not request.form['service_name']:
        raise ValidationException('Pyynnöstä puuttuu service_name parametri')

    if len(request.form['service_name']) < 1:
        raise ValidationException('service_name on tyhjä')

    if not request.form['service_price']:
        raise ValidationException('Pyynnöstä puuttuu service_price parametri')

    if not str(request.form['service_price']).isnumeric():
        raise ValidationException('service_price ei ole numero')

    if int(request.form['service_price']) < 0:
        raise ValidationException('service_price ei saa olla alle 0')


def add_service(executor: User, request: Request):
    try:
        validate_request(_validate_create_service, request)
    except ValidationException:
        return redirect('/dashboard/manage-services/', code=302)
    name = request.form['service_name']
    price = int(request.form['service_price'])
    create_service(name, price)
    return redirect('/dashboard/manage-services/', code=302)


def _validate_service_id(request: Request) -> None:
    if not request.form['service_id']:
        raise ValidationException('Pyynnöstä puuttuu service_id parametri')

    if len(request.form['service_id']) < 2:
        raise ValidationException('service_id ei ole UUID')


def remove_service(executor: User, request: Request):
    try:
        validate_request(_validate_service_id, request)
    except ValidationException:
        return redirect('/dashboard/manage-services/', code=302)
    service_id = request.form['service_id']
    delete_service(service_id)
    return redirect('/dashboard/manage-services/', code=302)