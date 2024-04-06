from app import app
from flask import render_template


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
