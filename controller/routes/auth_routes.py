from flask import Blueprint, render_template,request,url_for,redirect,flash, session
from controller.models import User
from controller.database import db
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        passwd = request.form.get("password")
        conf_passwd = request.form.get("confirm_password")

        if not username or not email or not passwd or not conf_passwd:
            flash("All fields are required", "danger")
            return redirect(url_for("auth.signup"))
        
        if len(passwd) < 6:
            flash("Password length should be more than 6", "danger")
            return redirect(url_for("auth.signup"))
        
        if passwd != conf_passwd:
            flash("Both passwords should match each other", "warning")
            return redirect(url_for("auth.signup"))
        
        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"

        if not re.match(email_pattern, email):
            flash("Please enter a valid email address", "danger")
            return redirect(url_for("auth.signup"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already exists with this email", "danger")
            return redirect(url_for("auth.signup"))
        
        password = generate_password_hash(passwd)

        new_user = User(
            username=username,
            email=email,
            password=password,
            role = "Freelancer"
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful. Please login", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html")

@auth_bp.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("All fields required", "danger")
            return redirect(url_for("auth.login"))


        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            flash("User not present with this credentials", "warning")
            return redirect(url_for("auth.login"))
        
        check_password = check_password_hash(existing_user.password, password)
        if not check_password:
            flash("password is wrong", "danger")
            return redirect(url_for("auth.login"))
        
        session["user_id"]=existing_user.id
        session["user_role"]=existing_user.role
        
        if existing_user.role == "Admin":
            flash("Welcome to the admin dashboard", "success")
            return redirect(url_for("admin.dashboard"))
        elif existing_user.role == "Client":
            flash("Welcome to the client dashboard", "success")
            return redirect(url_for("client.dashboard"))
        else:
            flash("welcome to the freelancer dashboard")
            return redirect(url_for("freelancer.dashboard"))

    return render_template("auth/login.html")

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id",None)
    session.pop("user_role",None)
    flash("You have been logged out", "info")
    return redirect(url_for("auth.login"))