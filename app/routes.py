from app import app
from flask import render_template
from app.models import User


@app.route('/')
def home():
    # 撈出所有cars的資料
    return render_template('index.html')

@app.route('/cars')
def cars():
    # 撈出所有cars的資料
    return render_template('cars.html')


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
