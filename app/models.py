from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default='Unknown')
    brand = db.Column(db.String(255))
    year = db.Column(db.String(255), nullable=False, default='Unknown')
    model = db.Column(db.String(255))
    door = db.Column(db.Integer, nullable=False, default=0)
    body = db.Column(db.String(255), nullable=False, default='Unknown')
    displacement = db.Column(db.String(255), nullable=False, default='Unknown')
    seat = db.Column(db.Integer, nullable=False, default=0)
    car_length = db.Column(db.String(255), nullable=False, default='Unknown')
    wheelbase = db.Column(db.String(255), nullable=False, default='Unknown')
    power_type = db.Column(db.String(255), nullable=False, default='Unknown')
    