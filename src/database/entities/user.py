from __future__ import annotations
from uuid import uuid4


class User:
    def __init__(self, user_id: str, name: str, email: str, role: str, allowed_access: bool):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.allow_access = allowed_access

    def __str__(self):
        return (f"id: {self.user_id}, name: {self.name}, email: {self.email}, role: {self.role}, "
                f"allowed: {self.allow_access}")

    @classmethod
    def new_user(cls, name: str, email: str) -> User:
        new_user_id = str(uuid4())
        return cls(new_user_id, name, email, "user", False)