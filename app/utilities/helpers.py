import re
from flask import jsonify
from app.models import Car

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


def car_spec_api(car_id):
    car = Car.query.get_or_404(car_id)
    car_data = {
        'id': car.id,
        'name': car.name,
        'brand': car.brand,
        'year': car.year,
        'model': car.model,
        'seat': car.seat,
        'door': car.door,
        'body': car.body,
        'price': car.price,
        'displacement': car.displacement,
        'wheelbase': car.wheelbase,
        'power_type': car.power_type,
    }
    return jsonify(car_data)
