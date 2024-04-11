from app import app
from flask import render_template, request, jsonify
from app.models import User, Car


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cars')
def carss():
    return render_template('cars.html')

@app.route('/api/cars')
def cars():
    brand = request.args.get('brand')
    if brand:
        # 從資料庫撈出指定的廠牌
        cars = Car.query.filter_by(brand=brand).all()
    else:
        # 如果沒有指定廠牌，就撈出所有資料
        cars = Car.query.all()

    # 以字典返回資料
    cars_list = [{
        'name': car.name,
        'brand': car.brand,
        'year': car.year,
        'model': car.model
    } for car in cars]

    # 以 JSON 格式回傳
    return jsonify(cars_list)


# @app.route('/cars/:car_id')
# def cars():
#     # 撈出單一汽車規格的資訊
#     return render_template('car-single.html')


# test database
@app.route('/test_db')
def test_db():
    try:
        user_count = User.query.count()
        return f"資料庫連線成功，用戶數量為：{user_count}"
    except Exception as e:
        return f"資料庫連線失敗，錯問訊息：{e}"
