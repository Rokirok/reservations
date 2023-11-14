from collections.abc import Callable
from flask import Request

from src.helpers.ValidationException import ValidationException


def is_valid_request(request: Request) -> bool:
    if not request.form:
        return False

    return True


def validate_request(validator: Callable[[Request], None], request: Request) -> None:
    if not is_valid_request(request):
        raise ValidationException('Vääränlainen pyyntö lähetetty palvelimelle')
    validator(request)
