from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Car, User
from app.utilities.rbac import admin_required
from app.utilities.helpers import clean_input

admin = Blueprint('admin', __name__)


@admin.route('/cars', methods=['GET'])
@login_required
@admin_required
def admin_cars():
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)


@admin.route('/cars/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_car(id):
    car = Car.query.get_or_404(id)
    if request.method == "POST":
        fields = {
            'name': request.form.get('name'),
            'model': request.form.get('model'),
            'year': request.form.get('year', type=int),
            'seat': request.form.get('seat'),
            'body': request.form.get('body'),
            'displacement': request.form.get('displacement'),
            'car_length': request.form.get('car_length'),
            'wheelbase': request.form.get('wheelbase'),
            'power_type': request.form.get('power_type'),
            'brand': request.form.get('brand'),
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
                return redirect(url_for('admin.admin_cars', open_modal=id))
        if all_inputs_valid:
            db.session.commit()
            flash('Car details updated successfully!', 'success')
            return redirect(url_for('admin.admin_cars'))
    return render_template('admin/cars.html')


@admin.route('/cars/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_car():
    if request.method == 'POST':
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

        if not name or not brand or not model or not year:
            flash('Name, brand, model, and year are required.', 'error')
            return render_template('admin/new_car.html')

        new_car = Car(name=name, model=model, year=year, body=body, seat=seat,
                      brand=brand, door=door,
                      displacement=displacement, car_length=car_length, wheelbase=wheelbase,
                      power_type=power_type)

        db.session.add(new_car)
        try:
            db.session.commit()
            flash('New car added successfully!', 'success')
            return redirect(url_for('admin.admin_cars'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding car: {str(e)}', 'error')

    return render_template('admin/new_car.html')


@admin.route('/cars/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_car(id):
    car = Car.query.get_or_404(id)

    try:
        db.session.delete(car)
        db.session.commit()
        flash('Car deleted successfully!', 'success')
        return redirect(url_for('admin.admin_cars'))
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete car. Error: {}'.format(str(e)), 'error')
        return redirect(url_for('admin.admin_cars'))


@admin.route('/users')
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)
