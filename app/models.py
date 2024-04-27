from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum, unique
from sqlalchemy.orm import relationship

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
    price = db.Column(db.Integer, nullable=False, default=0)
    # Relationship indicating that a car can have multiple reservations
    reservations = db.relationship('Reservation', back_populates='car')
    


class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    # FOREIGN KEY (car_id) REFERENCES Car(id)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    # FOREIGN KEY (user_id) REFERENCES User(id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    pick_up_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    drop_off_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    status = db.Column(db.String(255), nullable=False, default='Pending')

    # Relationships linking back to the Car, User, and Location
    # 使用 back_populates 來確保兩邊資料的修改能同步更新
    car = db.relationship('Car', back_populates='reservations')
    # backref 只需要在一邊設置，SQLAlchemy 會自動處理反向關聯的建立
    user = db.relationship('User', backref='reservations')
    pick_up_location = db.relationship("Location", foreign_keys=[pick_up_location_id])
    drop_off_location = db.relationship("Location", foreign_keys=[drop_off_location_id])


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
