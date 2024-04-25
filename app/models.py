from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum, unique


@unique
class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

# an association table to link users and cars.
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), primary_key=True),
    db.Column('liked_at', db.DateTime, default=db.func.current_timestamp())
)

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)
    liked_cars = db.relationship('Car', secondary=likes,
                                 backref=db.backref('liked_by', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, id):
        return f'https://i.pravatar.cc/300?img={id}'

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default="Unknown")
    brand = db.Column(db.String(255), nullable=False, default="Unknown")
    year = db.Column(db.Integer, nullable=False, default=0)
    model = db.Column(db.String(255), nullable=False, default="Unknown")
    body = db.Column(db.String(255), nullable=False, default="Unknown")
    door = db.Column(db.String(255), nullable=False, default="Unknown")
    displacement = db.Column(db.String(255), nullable=False, default="Unknown")
    seat = db.Column(db.String(255), nullable=False, default="Unknown")
    car_length = db.Column(db.String(255), nullable=False, default="Unknown")
    wheelbase = db.Column(db.String(255), nullable=False, default="Unknown")
    power_type = db.Column(db.String(255), nullable=False, default="Unknown")
