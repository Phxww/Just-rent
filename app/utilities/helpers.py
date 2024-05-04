import re
def clean_input(value):
    """Strips the string and checks if it is not just empty or spaces. Passes integers unchanged."""
    if isinstance(value, str):  # Check if the input is a string
        trimmed = value.strip()  # Remove leading/trailing whitespace
        if trimmed:  # Check if the result is non-empty
            return trimmed
    elif isinstance(value, int):  # Directly return integers without modification
        return value
    return None  # Return None for all other cases or if checks fail


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
