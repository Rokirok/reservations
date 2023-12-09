from src.database.entities.user import User
from werkzeug.security import generate_password_hash
from src.database.db_connection import db
from sqlalchemy.sql import text
from src.helpers.EntityExistsException import EntityExistsException
from src.helpers.InvalidCredentialsException import InvalidCredentialsException
from src.helpers.InternalException import InternalException


def is_email_in_use(email: str) -> bool:
    result = db.session.execute(text('SELECT email FROM users WHERE email = :email'), {
        "email": email
    })
    emails = result.fetchall()
    print(emails)
    return len(emails) != 0


def register_user(name: str, email: str, raw_password: str) -> User:
    email_in_use = is_email_in_use(email)
    if email_in_use:
        raise EntityExistsException('Sähköpostiosoite on jo käytössä')
    user = User.new_user(name, email)
    password_hash = generate_password_hash(raw_password)
    insert_query = ("INSERT INTO users (id, name, email, password_hash, allowed_access, role) VALUES ("
                    ":id, :name, :email, :password_hash, :allowed_access, :role)")
    db.session.execute(text(insert_query), {
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "password_hash": password_hash,
        "allowed_access": False,
        "role": 'user'
    })
    db.session.commit()
    return user


def get_user_with_password_by_email(email: str) -> (User, str):
    result = db.session.execute(text("SELECT id, email, name, allowed_access, role, password_hash FROM users WHERE "
                                     "email = :email"), {"email": email})
    users_array = result.fetchall()
    if len(users_array) == 0:
        raise InvalidCredentialsException()
    if len(users_array) > 1:
        raise InternalException('Tapahtui odottamaton virhe!')
    user_data = users_array[0]
    user_id = user_data[0]
    user_email = user_data[1]
    user_name = user_data[2]
    user_allowed_access = user_data[3]
    user_role = user_data[4]
    password_hash = user_data[5]
    user = User(user_id=user_id, name=user_name, email=user_email, role=user_role, allowed_access=user_allowed_access)
    return user, password_hash


def get_user_by_id(id: str) -> User:
    result = db.session.execute(text("SELECT id, email, name, allowed_access, role FROM users WHERE "
                                     "id = :id"), {"id": id})
    users_array = result.fetchall()
    if len(users_array) == 0:
        raise InvalidCredentialsException()
    if len(users_array) > 1:
        raise InternalException()
    user_data = users_array[0]
    user_id = user_data[0]
    user_email = user_data[1]
    user_name = user_data[2]
    user_allowed_access = user_data[3]
    user_role = user_data[4]
    user = User(user_id=user_id, name=user_name, email=user_email, role=user_role, allowed_access=user_allowed_access)
    return user


def get_all_users():
    result = db.session.execute(text("SELECT id, email, name, allowed_access, role FROM users"))
    raw_users_array = result.fetchall()
    users_array = []
    for user_data in raw_users_array:
        user_id = user_data[0]
        user_email = user_data[1]
        user_name = user_data[2]
        user_allowed_access = user_data[3]
        user_role = user_data[4]
        user = User(user_id=user_id, name=user_name, email=user_email, role=user_role,
                    allowed_access=user_allowed_access)
        users_array.append(user)
    return users_array


def set_allow_status(user: User, allow: bool):
    insert_query = 'UPDATE users SET allowed_access = :allow WHERE id = :id'
    db.session.execute(text(insert_query), {
        "id": user.user_id,
        "allow": allow
    })
    db.session.commit()


def set_user_role(user: User, role: str):
    insert_query = 'UPDATE users SET role = :role WHERE id = :id'
    db.session.execute(text(insert_query), {
        "id": user.user_id,
        "role": role
    })
    db.session.commit()


def update_details(user: User, user_name: str, user_email: str):
    insert_query = 'UPDATE users SET name = :name, email = :email WHERE id = :id'
    db.session.execute(text(insert_query), {
        "id": user.user_id,
        "name": user_name,
        "email": user_email
    })
    db.session.commit()


def list_employees():
    result = db.session.execute(text("SELECT id, email, name, allowed_access, role FROM users WHERE allowed_access = TRUE"))
    raw_users_array = result.fetchall()
    users_array = []
    for user_data in raw_users_array:
        user_id = user_data[0]
        user_email = user_data[1]
        user_name = user_data[2]
        user_allowed_access = user_data[3]
        user_role = user_data[4]
        user = User(user_id=user_id, name=user_name, email=user_email, role=user_role,
                    allowed_access=user_allowed_access)
        users_array.append(user)
    return users_array
