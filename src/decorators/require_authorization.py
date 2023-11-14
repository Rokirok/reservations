from flask import session, redirect
from functools import wraps
from src.database.repositories.user_repository import get_user_by_id
from src.helpers.InvalidCredentialsException import InvalidCredentialsException
from src.helpers.InternalException import InternalException


def login_required(required_role):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/login')
            user_id = session['user_id']
            try:
                user = get_user_by_id(user_id)
                if not user.allow_access:
                    return redirect('/login/')
                if required_role == 'admin':
                    if user.role != 'admin':
                        return redirect('/dashboard/')
                return func(user, *args, **kwargs)
            except InvalidCredentialsException:
                del session['user_id']
                return redirect('/login/')
            except InternalException:
                del session['user_id']
                return redirect('/login/')
        return authorize
    return decorator
