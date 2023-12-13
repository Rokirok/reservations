from flask import Request, redirect

from src.database.repositories.reservable_times_repository import get_reservable_time_by_id
from src.helpers.ValidationException import ValidationException
from src.helpers.generic_validators import is_uuid, is_email
from src.helpers.request_validator import validate_request
from src.database.repositories.reservation_repository import create_reservation as db_create_reservation


def _validate_create_location(request: Request) -> None:
    # Validate that timeslot, customer_name and customer_number is set on req.form
    form_body = request.form
    required_fields = {"timeslot", "customer_name", "customer_number", "customer_email", "message"}
    if not required_fields.issubset(form_body.keys()):
        raise ValidationException(
            "Request form doesn't have 'timeslot', 'customer_name', 'customer_number', 'customer_email' and 'message' parameters")

    if not is_uuid(request.form['timeslot']):
        raise ValidationException("Viallinen aika varattuna, timeslot is not uuid")

    if not is_email(request.form['customer_email']):
        raise ValidationException("Sähköposti ei ole muotoa test@example.com")

    return None


def create_reservation(req: Request):
    try:
        validate_request(_validate_create_location, req)
    except ValidationException:
        # TODO: Virheviestit varaukseen nätisti!
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
