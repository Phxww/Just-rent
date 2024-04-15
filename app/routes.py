from app import app, db
from flask import render_template, request, jsonify, flash, redirect, url_for
from app.models import User, Car
from app.utilities.helpers import clean_input

# 前端渲染


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars")
def carss():
    return render_template("cars.html")


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
        {"name": car.name,
         "brand": car.brand,
         "year": car.year,
         "model": car.model}
        for car in cars
    ]

    # 以 JSON 格式回傳
    return jsonify(cars_list)


@app.route("/api/cars/pop")
def pop():
    cars = Car.query.order_by(Car.year.desc()).limit(5).all()
    # print(cars[0].items())
    cars_list = [{
        'id': car.id,
        'name': car.name,
        'brand': car.brand,
        'year': car.year
    } for car in cars]

    # return jsonify(cars_list)
    return cars_list

# @app.route('/cars/:car_id')
# def cars():
#     # 撈出單一汽車規格的資訊
#     return render_template('car-single.html')


# ==== admin ====
@app.route('/admin/cars')
def admin_cars():
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)


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
