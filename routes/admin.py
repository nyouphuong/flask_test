from flask import Blueprint, session, flash, redirect, url_for
from functools import wraps

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Chỉ admin mới được phép truy cập!", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/admin")
@admin_required
def admin_panel():
    return "<h1>Chào Admin!</h1>"
