from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.utilities.rbac import user_only
from app.utilities.helpers import car_spec_api
from app.models import User, Reservation
import json

main = Blueprint('main', __name__)


@main.route("/")
@user_only
def home():
    return render_template("index.html", user=current_user)


@main.route("/cars")
@user_only
def view_cars():
    return render_template('cars.html', user=current_user)


@main.route('/cars/<int:car_id>')
@user_only
def view_spec_car(car_id):
    response = car_spec_api(car_id)
    if response.status_code != 200:
        return "Car not found", 404
    car_details = json.loads(response.get_data(as_text=True))
    return render_template('car-single.html', car_id=car_id, car=car_details, user=current_user)


@main.route("/profile/")
@login_required
@user_only
def profile():
    return render_template('profile.html', template='_profile.html', user=current_user)


@main.route("/profile/orders")
@login_required
@user_only
def orders():
    return render_template('profile.html', template='_orders.html', user=current_user)


@main.route("/profile/favorites")
@login_required
@user_only
def favorites():
    return render_template('profile.html', template='_favorites.html', user=current_user)


@main.route("/payment")
@login_required
def payment():
    user_id = current_user.id
    reservation_id = request.args.get('reservationId', None)

    if not reservation_id:
        flash("No reservation specified.", "error")
        return redirect(url_for('main.view_cars'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('main.view_cars'))

    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if not reservation:
        flash("Reservation not found.", "error")
        return redirect(url_for('main.view_cars'))

    rental_days = (reservation.end_date - reservation.start_date).days + 1
    total_amount = rental_days * reservation.car.price

    if rental_days >= 3:
        discount = round(total_amount * 0.095)
        total_amount -= discount

    total_amount = round(total_amount)

    return render_template('payment.html', user=user, reservation=reservation, rental_days=rental_days, total_amount=total_amount)
