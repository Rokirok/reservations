from src.database.entities.user import User


def dashboard_context(user: User) -> { "is_admin": bool, "user": User }:
    return {
        "is_admin": user.role == 'admin',
        "user": user
    }
