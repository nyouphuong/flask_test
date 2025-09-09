from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form.get("role", "user")
        if User.query.filter_by(email=email).first():
            flash("Email đã tồn tại!", "error")
        else:
            new_user = User(email=email, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["email"] = user.email
            session["role"] = user.role
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Sai email hoặc password!", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Đăng xuất thành công!", "success")
    return redirect(url_for("auth.login"))
