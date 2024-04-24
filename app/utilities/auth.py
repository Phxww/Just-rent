

# role-based access control (RBAC)

# 1. Role Assignment in the User Model: Ensure that your User model includes a role attribute.
# 2. Login and Role Check: Implement a login function that checks the user's role upon successful login and redirects accordingly.
# 3. Route Protection: Protect routes by ensuring that users can only access routes appropriate to their role.

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from app.models import UserRole


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and if they are an admin
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            flash('You do not have permission to view this page.', 'warning')
            return redirect(url_for('view_cars'))  # Redirect to a safe page
        return f(*args, **kwargs)  # Run the actual route function
    return decorated_function
