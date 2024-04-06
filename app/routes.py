from app import app
from flask import render_template


@app.route('/cars')
def cars():
    return render_template('cars.html')
