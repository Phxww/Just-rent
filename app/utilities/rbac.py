# role-based access control (RBAC)

# 1. Role Assignment in the User Model: Ensure that your User model includes a role attribute.
# 2. Login and Role Check: Implement a login function that checks the user's role upon successful login and redirects accordingly.
# 3. Route Protection: Protect routes by ensuring that users can only access routes appropriate to their role.

from app import db, login
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from app.models import UserRole, User


@login.user_loader
def user_loader(id):
    return db.session.get(User, int(id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and if they are an admin
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            # flash('You do not have permission to view this page.', 'warning')
            return redirect(url_for('main.view_cars'))  # Redirect to a safe page
        return f(*args, **kwargs)  # Run the actual route function
    return decorated_function

def user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and if they are an admin
        if current_user.is_authenticated and current_user.role == UserRole.ADMIN:
            # Optional: flash a message if you want to inform the user
            # flash('Admins do not have access to this page.', 'warning')
            # Redirect admins to an admin-specific page
            return redirect(url_for('admin.admin_cars'))
        return f(*args, **kwargs)  # Run the actual route function for non-admins
    return decorated_function
