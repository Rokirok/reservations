import re
from uuid import UUID


def is_uuid(uuid_string: str) -> bool:
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


RFC_5322_EMAIL_REGEX = ('(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:['
                        'a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5['
                        '0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:['
                        '\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\['
                        '\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])')


def is_email(input: str) -> bool:
    if re.match(RFC_5322_EMAIL_REGEX, input):
        return True
    return False
