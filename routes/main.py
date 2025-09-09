from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from datetime import datetime
from functools import wraps

main_bp = Blueprint("main", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Bạn cần đăng nhập trước!", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route("/")
@login_required
def home():
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template(
        "base.html",
        email=session["email"],
        role=session["role"],
        user_ip=user_ip,
        current_time=current_time
    )


