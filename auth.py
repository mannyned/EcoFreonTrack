"""
Authentication and Authorization Module
Handles user login, logout, session management, and role-based permissions
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request
from models import User, db


def login_required(f):
    """Decorator to require user login for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission):
    """Decorator to require specific permission for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login', next=request.url))

            user = User.query.get(session['user_id'])
            if not user or not user.is_active:
                flash('Your account is not active.', 'danger')
                return redirect(url_for('login'))

            if not user.has_permission(permission):
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(*roles):
    """Decorator to require specific role(s) for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login', next=request.url))

            user = User.query.get(session['user_id'])
            if not user or not user.is_active:
                flash('Your account is not active.', 'danger')
                return redirect(url_for('login'))

            if user.role not in roles:
                flash(f'This page is only accessible to: {", ".join(roles)}', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """Get the currently logged-in user object"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def is_authenticated():
    """Check if a user is currently logged in"""
    return 'user_id' in session


def has_role(*roles):
    """Check if current user has one of the specified roles"""
    user = get_current_user()
    return user and user.role in roles


def has_permission(permission):
    """Check if current user has a specific permission"""
    user = get_current_user()
    return user and user.has_permission(permission)
