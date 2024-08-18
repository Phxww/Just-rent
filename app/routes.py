from app import app, db, login
from flask import render_template, request, jsonify, flash, redirect, url_for
from app.models import User, Car, Reservation, Location
from app.utilities.helpers import clean_input, is_valid_email
from app.utilities.auth import admin_required, user_only
from flask_login import login_user, logout_user, current_user, login_required
from enum import Enum, unique
from sqlalchemy import and_, or_
import requests
import re
from datetime import datetime


@unique
class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


@login.user_loader
def user_loader(id):
    return db.session.get(User, int(id))


# 前端渲染

@app.route("/")
@user_only
def home():
    return render_template("index.html", user=current_user)

# 汽車頁面


@app.route("/cars")
@user_only
def view_cars():
    return render_template('cars.html', user=current_user)

# 單一汽車頁面


@app.route('/cars/<int:car_id>')
@user_only
def view_spec_car(car_id):
    return render_template('car-single.html', car_id=car_id, user=current_user)


# 使用者登入


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view_cars'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('email and password are required!')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # 驗證完成之後，透過login_user來記錄user_id
            login_user(user)
            if current_user.role.value == UserRole.ADMIN.value:
                # Redirect admins to the admin dashboard
                return redirect(url_for('admin_cars'))
            else:
                # Redirect regular users to the user dashboard
                # print(current_user.role)
                # print(UserRole.USER.value)
                return redirect(url_for('view_cars'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

# 使用者登出


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# 使用者註冊


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # phone_number = request.form.get('phone_number')
        confirm_password = request.form.get('confirm_password')
        if not all([username, email,password, confirm_password]):
            flash('All fields are required!')
            return redirect(url_for('signup'))
        
        # Check password confirmation
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))


        if User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already in use')
            return redirect(url_for('signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# 個人資訊


@app.route("/profile/")
@login_required
@user_only
def profile():
    return render_template('profile.html', template='_profile.html', user=current_user)


@app.route("/profile/orders")
@login_required
@user_only
def orders():
    return render_template('profile.html', template='_orders.html', user=current_user)


@app.route("/profile/favorites")
@login_required
@user_only
def favorites():
    return render_template('profile.html', template='_favorites.html', user=current_user)


# ==== api ====

@app.route("/api/profile", methods=['GET', 'POST'])
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
            return redirect(url_for('profile'))

        if not is_valid_email(email):
            flash('Invalid email format.', 'error')
            return redirect(url_for('profile'))

        if not re.match(r'^09\d{8}$', phone_number):
            flash("Phone number must start with '09' and be 10 digits long.", 'error')
            return redirect(url_for('profile'))

        user = User.query.filter_by(username=username).first()
        if user is not None and user.username != current_user.username:
            flash('Username already taken.', 'error')
            return redirect(url_for('profile'))

        current_user.username = username
        current_user.email = email
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))


# 所有汽車
@app.route("/api/cars")
# `/api/cars?page=${page}`
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
    if power_type:
        query = query.filter(Car.power_type == power_type)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    cars = pagination.items  # Access the paginated items

    # cars = Car.query.all()

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

    # 以 JSON 格式回傳
    return jsonify(response)


@app.route("/api/cars/pop")
def pop():
    cars = Car.query.order_by(Car.year.desc()).limit(3).all()
    # print(cars[0].items())
    cars_list = [{
        'id': car.id,
        'name': car.name,
        'brand': car.brand,
        'year': car.year,
        'model': car.model,
        'seat': car.seat,
        'door': car.door,
        'body': car.body,
        'price':car.price,
        'original_price': round(3*(car.price)),
        'discount_price':round(3*(car.price)*0.95)
    } for car in cars]

    return jsonify(cars_list)

# 汽車詳細規格


@app.route('/api/cars/<int:car_id>')
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
        'displacement':car.displacement,
        'wheelbase': car.wheelbase,
        'power_type': car.power_type,
        
    }

    return jsonify(car_data)


# 過濾條件
@app.route('/api/brand')
def get_brands():
    brands = Car.query.with_entities(Car.brand).distinct().all()
    return jsonify([brand[0] for brand in brands])


@app.route('/api/seat')
def get_seat():
    seats = Car.query.with_entities(Car.seat).distinct().all()
    return jsonify([seat[0] for seat in seats])


@app.route('/api/door')
def get_door():
    doors = Car.query.with_entities(Car.door).distinct().all()
    return jsonify([door[0] for door in doors])


@app.route('/api/power')
def get_power():
    powers = Car.query.with_entities(Car.power_type).distinct().all()
    return jsonify([power[0] for power in powers])


# 喜歡汽車


@app.route('/api/like_car/<int:car_id>', methods=['POST'])
@login_required
def like_car(car_id):
    user_id = current_user.id
    user = User.query.get(user_id)
    print(user.liked_cars)
    car = Car.query.get(car_id)
    print(car)

    if not user or not car:
        return jsonify({"error": "User or Car not found"}), 404

    if car in user.liked_cars:
        return jsonify({"message": "Car already liked by user"}), 400

    user.liked_cars.append(car)
    db.session.commit()
    return jsonify({"message": "Car liked successfully"}), 200

# 不喜歡汽車


@app.route('/api/unlike_car/<int:car_id>', methods=['POST'])
@login_required
def unlike_car(car_id):
    user_id = current_user.id
    print(user_id)
    user = User.query.get(user_id)
    car = Car.query.get(car_id)

    if not user or not car:
        return jsonify({"error": "User or Car not found"}), 404

    if car not in user.liked_cars:
        return jsonify({"message": "Car not liked by user"}), 400

    user.liked_cars.remove(car)
    db.session.commit()
    return jsonify({"message": "Car unliked successfully"}), 200


# 使用者喜歡的汽車
@app.route('/api/favorites', methods=['GET'])
@login_required
def user_favorites():
    user_id = current_user.id
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    liked_cars = user.liked_cars
    print(liked_cars)
    cars_list = [
        {'id': car.id, 'name': car.name, 'price':car.price}
        for car in liked_cars
    ]
    return jsonify(cars_list)


# 使用者的訂單

@app.route('/api/reservations', methods=['GET'])
@login_required
def user_reservations():
    user_id = current_user.id
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.start_date.asc()).all()
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

# ============================
# ========== admin ===========
# ============================

@app.route('/admin')
@app.route('/admin/cars', methods=['GET'])
@login_required
@admin_required
def admin_cars():
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)


# 編輯汽車
@app.route('/admin/cars/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_car(id):
    car = Car.query.get_or_404(id)
    if request.method == "POST":
        fields = {
            'name': request.form.get('name'),
            'model': request.form.get('model'),
            # Handling integer conversion
            'year': request.form.get('year', type=int),
            'seat': request.form.get('seat'),
            'body': request.form.get('body'),
            'displacement': request.form.get('displacement'),
            'car_length': request.form.get('car_length'),
            'wheelbase': request.form.get('wheelbase'),
            'power_type': request.form.get('power_type'),
            'brand': request.form.get('brand'),
            # Handling integer conversion
            'door': request.form.get('door'),
            'price': request.form.get('price')
        }
        all_inputs_valid = True
        for key, value in fields.items():
            cleaned_value = clean_input(value)
            if cleaned_value is not None:
                setattr(car, key, cleaned_value)
            else:
                flash(f'Invalid input for {key}', 'error')
                all_inputs_valid = False
                return redirect(url_for('admin_cars', open_modal=id))
        if all_inputs_valid:
            db.session.commit()
            flash('Car details updated successfully!', 'success')
            return redirect(url_for('admin_cars'))
    return render_template('admin/cars.html')

# 新增汽車


@app.route('/admin/cars/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_car():
    if request.method == 'POST':
        # Extract information from form
        name = request.form.get('name')
        brand = request.form.get('brand')
        model = request.form.get('model')
        year = request.form.get('year')
        body = request.form.get('body')
        door = request.form.get('door')
        seat = request.form.get('seat')
        displacement = request.form.get('displacement')
        car_length = request.form.get('car_length')
        wheelbase = request.form.get('wheelbase')
        power_type = request.form.get('power_type')

        # Validate the input
        if not name or not brand or not model or not year:
            flash('Name, brand, model, and year are required.', 'error')
            return render_template('admin/new_car.html')

        # Create a new Car instance
        new_car = Car(name=name, model=model, year=year, body=body, seat=seat,
                      brand=brand, door=door,
                      displacement=displacement, car_length=car_length, wheelbase=wheelbase,
                      power_type=power_type)

        # Add to the database
        db.session.add(new_car)
        try:
            db.session.commit()
            flash('New car added successfully!', 'success')
            return redirect(url_for('admin_cars'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding car: {str(e)}', 'error')

    # Show the form if GET request
    return render_template('admin/new_car.html')

# 刪除汽車


# Change to POST if using forms
@app.route('/admin/cars/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_car(id):
    car = Car.query.get_or_404(id)

    try:
        db.session.delete(car)  # Perform the delete operation
        db.session.commit()  # Commit the transaction
        flash('Car deleted successfully!', 'success')  # Provide user feedback
        # Redirect to the car listing page
        return redirect(url_for('admin_cars'))
    except Exception as e:
        db.session.rollback()  # Roll back the transaction in case of error
        flash('Failed to delete car. Error: {}'.format(
            str(e)), 'error')  # Provide error message
        # Optionally redirect back to the same page or error page
        return redirect(url_for('admin_cars'))


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


# test database
@app.route("/test_db")
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"


# ============================
# ========== 租賃付款 =========
# ============================


# Check-car-availability

@app.route('/api/check-availability',  methods=['POST'])
@login_required
def check_availability():

    try:
        # Access the JSON data sent with the POST request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        # Extract dates from the JSON data
        print(data)
        pick_up_loc = data['pickUpLocation']
        return_loc = data['dropOffLocation']
        pick_up_date = data['pickUpDate']
        return_date = data['returnDate']
        car_id = data['carId']

        if pick_up_date > return_date:
            return jsonify({'error': 'Pick-up date must not be later than the return date.'}), 400

        # 暫時註解，為了已預定，但交易那邊尚未成功的時候測試用，就不會遇到已預訂但未交易的情況方昇

        # result = Reservation.query.filter(
        #     Reservation.car_id == car_id,
        #     # or_(...)用來包含多個條件
        #     or_(
        #         # 假設我的 Pick Up Date: 2023-04-15 , Return Date: 2023-04-20
        #         # start_date <= '2023-04-15' AND end_date >= '2023-04-15'
        #         # 檢查任何已存在的預訂是否覆蓋了取車日期
        #         and_(Reservation.start_date <= pick_up_date,
        #             Reservation.end_date >= pick_up_date),
        #         # 檢查任何已存在的預訂是否覆蓋還車日期
        #         and_(Reservation.start_date <= return_date,
        #             Reservation.end_date >= return_date),
        #         # 檢查是否有預訂的完整時段位於請求的日期範圍內
        #         and_(Reservation.start_date >= pick_up_date,
        #             Reservation.end_date <= return_date)
        #     )
        # ).first()

        # if result:
        #     return jsonify({'available': False}), 200

        # # Car is available, create a new reservation
        # new_reservation = Reservation(
        #     car_id=car_id,
        #     user_id=current_user.id,
        #     start_date=datetime.strptime(pick_up_date, '%Y-%m-%d').date(),
        #     end_date= datetime.strptime(return_date, '%Y-%m-%d').date(),
        #     pick_up_location_id=pick_up_loc,
        #     drop_off_location_id=return_loc,
        #     status='Pending'  # Initial reservation status
        # )
        # db.session.add(new_reservation)
        # db.session.commit()

        # 暫時註解，為了已預定，但交易那邊尚未成功的時候測試用，就不會遇到已預訂但未交易的情況發生。
        # return jsonify({'available': True, 'reservationId': new_reservation.id}), 200
        # 暫時寫死 id 為 1
        return jsonify({'available': True, 'reservationId': 1}), 200                
    except Exception as e:
        print('Error:',e)

@app.route('/api/locations')
def locations_api():
    locations = Location.query.all()  # Fetch all locations
    location_data = [
        {'id': location.id, 'name': location.name, 'city': location.city}
        for location in locations
    ]
    return jsonify(location_data)

# Tappay-getyprime


@app.route("/payment")
@login_required
def payment():
    user_id = current_user.id
    # Get reservation ID or None if not provided
    reservation_id = request.args.get('reservationId', None)

    if not reservation_id:
        flash("No reservation specified.", "error")
        # Assuming 'index' is a safe redirect target
        return redirect(url_for('cars'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('cars'))

    reservation = Reservation.query.filter_by(id=reservation_id).first()

    # Calculate rental days and total amount, add 1 to include the start day
    # Depend on biz logic. ex, 5/1 pick and 5/2 return -> 1 day
    rental_days = (reservation.end_date - reservation.start_date).days + 1
    total_amount = rental_days * reservation.car.price

    # Apply a 9.5% discount if the rental period is more than 3 days
    if rental_days >= 3:
        # Calculate 9.5% of the total amount
        discount = round(total_amount * 0.095)
        total_amount -= discount

    total_amount = round(total_amount)

    return render_template('payment.html', user=user, reservation=reservation, rental_days=rental_days, total_amount=total_amount)

# Tappay-paybyprime


@app.route('/api/tappaysdk/pay-by-prime', methods=['POST'])
@login_required
def proxy_payment():
    tappay_url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
    # Extract the JSON body from the incoming Flask request
    incoming_data = request.get_json()
    # Headers for TapPay request
    headers = {
        "Content-Type": "application/json",
        # "x-api-key": "partner_KOO8dhjMg4V7bifJUKXcuDXiYW0lK78oFvICgoeREFyh6Hp31fuu306X"
        "x-api-key": "partner_GVQwt2gIZgnvl8Q4joIDNTOqwD4r7D99ZCcaf630kIqFqbyBbjGGaSyF"
    }
    # Forward the request to TapPay
    response = requests.post(tappay_url, headers=headers, json=incoming_data)
    return jsonify(response.json()), response.status_code

# Update Reservation Status


@app.route('/api/update-payment-status', methods=['POST'])
@login_required
def update_reservation_status():
    data = request.get_json()
    reservation_id = data.get('reservationId')
    new_status = data.get('status')
    auth_code = data.get('auth_code')

    if not reservation_id or new_status != 'Success':
        return jsonify({'error': 'Invalid request'}), 400

    try:
        # Begin a transaction
        reservation = Reservation.query.filter_by(id=reservation_id).first()
        if reservation:
            reservation.status = new_status
            reservation.auth_code = auth_code
            # Not needed unless you're adding a new record
            db.session.add(reservation)
            db.session.commit()  # Commit the transaction
            return jsonify({'message': 'Reservation status updated successfully'}), 200
        else:
            return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        db.session.rollback()  # Roll back the transaction on error
        return jsonify({'error': str(e)}), 500
