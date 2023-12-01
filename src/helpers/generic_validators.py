from uuid import UUID


def is_uuid(uuid_string: str) -> bool:
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False
