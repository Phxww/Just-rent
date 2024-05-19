from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Car, User, Reservation, Location
from app.utilities.helpers import is_valid_email
from sqlalchemy import and_, or_
import re
import requests
from app.utilities.helpers import car_spec_api

api = Blueprint('api', __name__)


@api.route("/profile", methods=['GET', 'POST'])
@login_required
def api_profile():
    if request.method == 'GET':
        return jsonify({
            'username': current_user.username,
            'email': current_user.email,
            'phone_number': current_user.phone_number
        })

    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        if not username or not email or not phone_number:
            flash('Missing username, email, or phone number.', 'error')
            return redirect(url_for('main.profile'))

        if not is_valid_email(email):
            flash('Invalid email format.', 'error')
            return redirect(url_for('main.profile'))

        if not re.match(r'^09\d{8}$', phone_number):
            flash("Phone number must start with '09' and be 10 digits long.", 'error')
            return redirect(url_for('main.profile'))

        user = User.query.filter_by(username=username).first()
        if user is not None and user.username != current_user.username:
            flash('Username already taken.', 'error')
            return redirect(url_for('main.profile'))

        current_user.username = username
        current_user.email = email
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('main.profile'))


@api.route("/cars")
def cars():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    brand = request.args.get('brand')
    doors = request.args.get('doors')
    seats = request.args.get('seats')
    power_type = request.args.get('powerType')
    displacement = request.args.get('displacement')
    price = request.args.get('price')

    query = Car.query
    if brand:
        query = query.filter(Car.brand == brand)
    if doors:
        query = query.filter(Car.door == doors)
    if seats:
        query = query.filter(Car.seat == seats)
    if power_type:
        query = query.filter(Car.power_type == power_type)
    if displacement:
        query = query.filter(Car.displacement == displacement)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    cars = pagination.items

    cars_list = [
        {"id": car.id,
         "name": car.name,
         "brand": car.brand,
         "year": car.year,
         "model": car.model,
         'price': car.price,
         "isLiked": car in current_user.liked_cars if current_user.is_authenticated else None
         } for car in cars
    ]
    response = {
        "cars": cars_list,
        "isAuthenticated": current_user.is_authenticated,
        "total_pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_num": pagination.next_num,
        "prev_num": pagination.prev_num
    }
    return jsonify(response)


@api.route("/cars/pop")
def pop():
    cars = Car.query.order_by(Car.year.desc()).limit(3).all()
    cars_list = [{
        'id': car.id,
        'name': car.name,
        'brand': car.brand,
        'year': car.year,
        'model': car.model,
        'seat': car.seat,
        'door': car.door,
        'body': car.body,
        'price': car.price,
        'original_price': round(3*(car.price)),
        'discount_price': round(3*(car.price)*0.95)
    } for car in cars]

    return jsonify(cars_list)


@api.route('/cars/<int:car_id>')
def get_car_spec(car_id):
    return car_spec_api(car_id)


@api.route('/brand')
def get_brands():
    brands = Car.query.with_entities(Car.brand).distinct().all()
    return jsonify([brand[0] for brand in brands])


@api.route('/seat')
def get_seat():
    seats = Car.query.with_entities(Car.seat).distinct().all()
    return jsonify([seat[0] for seat in seats])


@api.route('/door')
def get_door():
    doors = Car.query.with_entities(Car.door).distinct().all()
    return jsonify([door[0] for door in doors])


@api.route('/power')
def get_power():
    powers = Car.query.with_entities(Car.power_type).distinct().all()
    return jsonify([power[0] for power in powers])


@api.route('/like_car/<int:car_id>', methods=['POST'])
@login_required
def like_car(car_id):
    user_id = current_user.id
    user = User.query.get(user_id)
    car = Car.query.get(car_id)

    if not user or not car:
        return jsonify({"error": "User or Car not found"}), 404

    if car in user.liked_cars:
        return jsonify({"message": "Car already liked by user"}), 400

    user.liked_cars.append(car)
    db.session.commit()
    return jsonify({"message": "Car liked successfully"}), 200


@api.route('/unlike_car/<int:car_id>', methods=['POST'])
@login_required
def unlike_car(car_id):
    user_id = current_user.id
    user = User.query.get(user_id)
    car = Car.query.get(car_id)

    if not user or not car:
        return jsonify({"error": "User or Car not found"}), 404

    if car not in user.liked_cars:
        return jsonify({"message": "Car not liked by user"}), 400

    user.liked_cars.remove(car)
    db.session.commit()
    return jsonify({"message": "Car unliked successfully"}), 200


@api.route('/favorites', methods=['GET'])
@login_required
def user_favorites():
    user_id = current_user.id
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    liked_cars = user.liked_cars
    cars_list = [
        {'id': car.id, 'name': car.name, 'price': car.price}
        for car in liked_cars
    ]
    return jsonify(cars_list)


@api.route('/reservations', methods=['GET'])
@login_required
def user_reservations():
    user_id = current_user.id
    reservations = Reservation.query.filter_by(
        user_id=user_id).order_by(Reservation.start_date.asc()).all()
    bookingList = []
    try:
        for reservation in reservations:
            bookingList.append({
                "id": reservation.id,
                "car_name": reservation.car.name,
                "pick_up_date": reservation.start_date.isoformat(),
                "return_date": reservation.end_date.isoformat(),
                "pick_up_location": reservation.pick_up_location.name if reservation.pick_up_location_id is not None else None,
                "drop_off_location": reservation.drop_off_location.name if reservation.pick_up_location_id is not None else None,
                "status": reservation.status,
                "created_at": reservation.created_at.isoformat() if reservation.created_at else None
            })
        return jsonify(bookingList)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/check-availability', methods=['POST'])
@login_required
def check_availability():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    pick_up_loc = data['pickUpLocation']
    return_loc = data['dropOffLocation']
    pick_up_date = data['pickUpDate']
    return_date = data['returnDate']
    car_id = data['carId']

    if pick_up_date > return_date:
        return jsonify({'error': 'Pick-up date must not be later than the return date.'}), 400

    result = Reservation.query.filter(
        Reservation.car_id == car_id,
        or_(
            and_(Reservation.start_date <= pick_up_date,
                 Reservation.end_date >= pick_up_date),
            and_(Reservation.start_date <= return_date,
                 Reservation.end_date >= return_date),
            and_(Reservation.start_date >= pick_up_date,
                 Reservation.end_date <= return_date)
        )
    ).first()

    if result:
        return jsonify({'available': False}), 200

    new_reservation = Reservation(
        car_id=car_id,
        user_id=current_user.id,
        start_date=pick_up_date,
        end_date=return_date,
        pick_up_location_id=pick_up_loc,
        drop_off_location_id=return_loc,
        status='Pending'
    )
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({'available': True, 'reservationId': new_reservation.id}), 200


@api.route('/locations')
def locations_api():
    locations = Location.query.all()
    location_data = [
        {'id': location.id, 'name': location.name, 'city': location.city}
        for location in locations
    ]
    return jsonify(location_data)




@api.route('/tappaysdk/pay-by-prime', methods=['POST'])
@login_required
def proxy_payment():
    tappay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
    incoming_data = request.get_json()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "partner_KOO8dhjMg4V7bifJUKXcuDXiYW0lK78oFvICgoeREFyh6Hp31fuu306X"
    }
    response = requests.post(tappay_url, headers=headers, json=incoming_data)
    return jsonify(response.json()), response.status_code


@api.route('/update-payment-status', methods=['POST'])
@login_required
def update_reservation_status():
    data = request.get_json()
    reservation_id = data.get('reservationId')
    new_status = data.get('status')
    auth_code = data.get('auth_code')

    if not reservation_id or new_status != 'Success':
        return jsonify({'error': 'Invalid request'}), 400

    try:
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if reservation:
            reservation.status = new_status
            reservation.auth_code = auth_code
            db.session.add(reservation)
            db.session.commit()
            return jsonify({'message': 'Reservation status updated successfully'}), 200
        else:
            return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
