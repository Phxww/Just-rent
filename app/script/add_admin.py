import sys
sys.path.insert(0, '/Users/annachu/mento3/Just-rent')

from app import app, db
from app.models import User
from enum import Enum, unique

@unique
class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


def create_admin():
    with app.app_context():
        admin = User(username='admin', email='admin@ex.com',
                     role=UserRole.ADMIN.value)
        admin.set_password('strongpassword123')
        db.session.add(admin)
        db.session.commit()
        db.session.close()

if __name__ == "__main__":
    create_admin()
