from functools import wraps
from flask import session, redirect, url_for, flash, abort

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to access this page", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to access this page", "warning")
            return redirect(url_for("auth.login"))
        if session.get("user_role") != "Admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def client_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to access this page", "warning")
            return redirect(url_for("auth.login"))
        if session.get("user_role") != "Client":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def freelancer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to access this page", "warning")
            return redirect(url_for("auth.login"))
        if session.get("user_role") != "Freelancer":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
