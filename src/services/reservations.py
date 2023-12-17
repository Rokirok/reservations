from flask import Request, redirect, render_template, flash

from src.database.entities.user import User
from src.database.repositories.reservable_times_repository import get_reservable_time_by_id
from src.helpers.ValidationException import ValidationException
from src.helpers.context_generator import dashboard_context
from src.helpers.generic_validators import is_uuid, is_email
from src.helpers.request_validator import validate_request
from src.database.repositories.reservation_repository import create_reservation as db_create_reservation, \
    search_reservation, get_reservation_by_id, save_updated_reservation, get_all_reservations, \
    delete_reservation as db_delete_reservation, set_complete_status as db_set_completed_status


def _validate_create_location(request: Request) -> None:
    form_body = request.form
    required_fields = {"timeslot", "customer_name", "customer_number", "customer_email", "message"}
    if not required_fields.issubset(form_body.keys()):
        raise ValidationException("Täytäthän kaikki kentät!")

    if not is_uuid(request.form['timeslot']):
        raise ValidationException("Viallinen aika varattuna, timeslot is not uuid")

    if not is_email(request.form['customer_email']):
        raise ValidationException("Sähköposti ei ole muotoa test@example.com")

    return None


def create_reservation(req: Request):
    try:
        validate_request(_validate_create_location, req)
    except ValidationException as error:
        flash(str(error), 'error')
        service_id = req.args.get('service', '')
        location_id = req.args.get('location', '')
        if is_uuid(service_id) and is_uuid(location_id):
            return redirect(f'/reserve/{service_id}/{location_id}', code=302)
        return redirect('/reserve', code=302)
    timeslot_id = req.form['timeslot']
    timeslot = get_reservable_time_by_id(timeslot_id)
    if not timeslot:
        return redirect('/reserve', code=302)
    customer_name = req.form['customer_name']
    customer_mobile = req.form['customer_number']
    customer_email = req.form['customer_email']
    message = req.form['message']
    reservation = db_create_reservation(timeslot, customer_name, customer_mobile, customer_email, message)
    return redirect(f'/successful-reservation?pin={reservation.pin}', code=302)


def _validate_search_reservation(request: Request) -> None:
    form_body = request.form
    required_fields = {"customer_email", "reservation_pin"}
    if not required_fields.issubset(form_body.keys()):
        raise ValidationException("Täytä molemmat kentät!")

    if not request.form['reservation_pin'].isdigit() or len(request.form['reservation_pin']) != 4:
        raise ValidationException("Varauksen PIN tulisi olla neljä numeroa!")

    if not is_email(request.form['customer_email']):
        raise ValidationException("Sähköposti ei ole muotoa test@example.com")
    return None


def search_for_reservation(request: Request):
    try:
        validate_request(_validate_search_reservation, request)
    except ValidationException as e:
        return render_template('customer/search_reservation.html', error=e)
    email = request.form['customer_email']
    pin = request.form['reservation_pin']
    reservation = search_reservation(email, pin)
    if not reservation:
        return render_template('customer/search_reservation.html', error="Varausta ei ole")
    return redirect(f'/edit-reservation/{reservation.reservation_id}', code=302)


def show_edit_reservation(request: Request, reservation_id: str):
    if not is_uuid(reservation_id):
        return redirect('/search-reservation/', code=302)
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return redirect('/search-reservation/', code=302)
    return render_template('customer/edit_reservation.html', reservation=reservation)


def _validate_save_edit(request: Request):
    form_body = request.form
    required_fields = {"customer_email", "customer_name", "customer_mobile"}
    if not required_fields.issubset(form_body.keys()):
        raise ValidationException("Täytäthän nimesi, sähköpostisi ja puhelinnumerosi!")

    if not is_email(request.form['customer_email']):
        raise ValidationException("Sähköposti ei ole muotoa test@example.com")


def save_edited_reservation(request: Request, reservation_id: str):
    if not is_uuid(reservation_id):
        return redirect('/search-reservation/', code=302)
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return redirect('/search-reservation/', code=302)
    try:
        validate_request(_validate_save_edit, request)
    except ValidationException as e:
        return render_template('customer/edit_reservation.html', reservation=reservation, error=e)
    reservation.customer_email = request.form['customer_email']
    reservation.customer_mobile = request.form['customer_mobile']
    reservation.customer_name = request.form['customer_name']
    reservation.message = request.form.get('message', None)
    save_updated_reservation(reservation)
    return redirect(f'/edit-reservation/{reservation.reservation_id}', code=302)


def view_reservations(user: User, request: Request):
    reservations = get_all_reservations()
    return render_template('dashboard/dashboard.html', dashboard_context=dashboard_context(user),
                           reservations=reservations)


def view_reservation(user: User, reservation_id: str):
    if not is_uuid(reservation_id):
        return redirect('/dashboard/', code=302)
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return redirect('/dashboard/', code=302)
    return render_template('dashboard/manage_reservation.html', dashboard_context=dashboard_context(user),
                           reservation=reservation)


def set_complete_status(user: User, request: Request, completed: bool):
    reservation_id = request.form.get('reservation_id', '')
    if not is_uuid(reservation_id):
        return redirect('/dashboard/', code=302)
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return redirect('/dashboard/', code=302)
    db_set_completed_status(reservation, completed)
    return redirect(f'/dashboard/reservations/{reservation.reservation_id}/', code=302)


def delete_reservation(user: User, request: Request):
    reservation_id = request.form.get('reservation_id', '')
    if not is_uuid(reservation_id):
        return redirect('/dashboard/', code=302)
    reservation = get_reservation_by_id(reservation_id)
    if not reservation:
        return redirect('/dashboard/', code=302)
    db_delete_reservation(reservation)
    return redirect('/dashboard/', code=302)
