from flask import Request, render_template, redirect
from src.helpers.ValidationException import ValidationException
from src.helpers.EntityExistsException import EntityExistsException
from src.helpers.request_validator import validate_request
from src.database.repositories.user_repository import register_user as create_new_user, get_user_with_password_by_email
from src.helpers.InvalidCredentialsException import InvalidCredentialsException
from src.helpers.InternalException import InternalException
from werkzeug.security import check_password_hash
import re


RFC_5322_EMAIL_REGEX = ('(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:['
                        'a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5['
                        '0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])')


def _validate_email(request: Request) -> None:
    if not request.form['email']:
        raise ValidationException('Sähköpostia ei ole syötetty!')

    if not re.match(RFC_5322_EMAIL_REGEX, request.form['email']):
        raise ValidationException('Sähköposti ei ole oikeassa muodossa. Muodon tulisi olla: käyttäjä@example.com')


def _validate_password(request: Request) -> None:
    if not request.form['password']:
        raise ValidationException('Salasanaa ei ole syötetty!')

    if len(request.form['password']) < 8:
        raise ValidationException('Salasanassa tulee olla vähintään 8 merkkiä!')

    if str(request.form['password']).isalpha():
        raise ValidationException('Salasanassa tulee olla myös numeroita tai erikoismerkkejä!')


def _validate_register(request: Request):
    if not request.form['name'] or len(request.form['name']) < 1:
        raise ValidationException('Nimeä ei ole syötetty!')

    _validate_email(request)
    _validate_password(request)


def register_user(request: Request):
    try:
        validate_request(_validate_register, request)
    except ValidationException as e:
        return render_template('customer/register.html', error_message=str(e))
    try:
        user = create_new_user(request.form['name'], request.form['email'], request.form['password'])
        if user.role == 'admin':
            return redirect('/successful_registration?created_as_admin=yes')
        else:
            return redirect('/successful_registration')
    except EntityExistsException as e:
        return render_template('customer/register.html', error_message=str(e))


def _validate_login(request: Request) -> None:
    _validate_email(request)
    _validate_password(request)


def login_user(request: Request, session):
    try:
        validate_request(_validate_login, request)
    except ValidationException as e:
        return render_template('customer/login.html', error_message=str(e))

    try:
        result = get_user_with_password_by_email(request.form['email'])
        user = result[0]
        password_hash = result[1]
        if check_password_hash(password_hash, request.form['password']):
            session['user_id'] = user.user_id
            return redirect('/dashboard')
        else:
            raise InvalidCredentialsException()
    except InvalidCredentialsException:
        return render_template('customer/login.html', error_message="Väärä sähköposti tai salasana!")
    except InternalException as e:
        return render_template('customer/login.html', error_message=str(e))
