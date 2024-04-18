from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for
from app.models import User, Car
from app.utilities.helpers import clean_input

# 前端渲染


@app.route("/")
def home():
    return render_template("index.html")

# 汽車頁面


@app.route("/cars")
def view_cars():
    return render_template("cars.html")

# 單一汽車頁面


@app.route('/cars/<int:car_id>')
def view_spec_car(car_id):
    return render_template('car-single.html', car_id=car_id)


# 使用者登入


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('email and password are required!')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')


# 使用者註冊
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash('Username, email, and password are required!')
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

        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

# 個人自我介紹
@app.route("/profile")
def profile():
    return render_template('profile.html',template='_profile.html')


@app.route("/profile/orders")
def orders():
    return render_template('profile.html', template='_orders.html')


@app.route("/profile/favorites")
def favorites():
    return render_template('profile.html', template='_favorites.html')


# ==== api ====

# 瀏覽所有汽車


@app.route("/api/cars")
def cars():
    brand = request.args.get("brand")
    if brand:
        # 從資料庫撈出指定的廠牌
        cars = Car.query.filter_by(brand=brand).all()
    else:
        # 如果沒有指定廠牌，就撈出所有資料
        cars = Car.query.all()

    # 以字典返回資料
    cars_list = [
        {"id": car.id,
         "name": car.name,
         "brand": car.brand,
         "year": car.year,
         "model": car.model}
        for car in cars
    ]

    # 以 JSON 格式回傳
    return jsonify(cars_list)


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
        'body': car.body
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
        'body': car.body
    }

    return jsonify(car_data)


# ==== admin ====
# 瀏覽汽車
@app.route('/admin', methods=['GET'])
def home_car():
    return redirect(url_for('admin_cars'))


@app.route('/admin/cars')
def admin_cars():
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)


# 編輯汽車
@app.route('/admin/cars/<int:id>', methods=['GET', 'POST'])
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
            'door': request.form.get('door')
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
def admin_users():
    return render_template('admin/users.html')


# test database
@app.route("/test_db")
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"
