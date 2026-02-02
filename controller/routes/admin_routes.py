from flask import Blueprint, render_template, url_for, request, flash, redirect
from controller.models import User, Client, Gig, Application
from controller.database import db
import re
from werkzeug.security import generate_password_hash


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/clients")
def clients():
    return render_template("admin/clients.html")

@admin_bp.route("/create_clients", methods = ["GET", "POST"])
def create_clients():
    if request.method == "GET":
        return render_template("admin/create_clients.html")
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    industry = request.form.get("industry")
    company = request.form.get("company")
    description = request.form.get("description")

    if not username or not email or not password or not industry or not company or not description:
        flash("All details should be there no field should be empty")
        return redirect(url_for("admin.create_clients"))
    
    if len(password) < 6:
        flash("Password length should be atleast 6.")
        return redirect(url_for("admin.create_clients"))
    
    email_pattern = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(email_pattern, email):
        flash("Please enter a valid email address", "danger")
        return redirect(url_for("admin.create_clients"))
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("user already exists with this email in db")
        return redirect(url_for("admin.create_clients"))
    
    hashed_password = generate_password_hash(password)

    new_User = User(
        username = username,
        email = email, 
        password = hashed_password,
        role = "Client"
    )

    new_client = Client(
        user = new_User,
        company_name = company,
        industry = industry,
        description = description
    )
    db.session.add_all([new_User, new_client])

    db.session.commit()
    flash("client successfully created")
    return redirect(url_for("admin.clients"))

@admin_bp.route("/freelancers")
def freelancers():
    return render_template("admin/freelancers.html")


@admin_bp.route("/gigs")
def gigs():
    return render_template("admin/gigs.html")


@admin_bp.route("/applications")
def applications():
    return render_template("admin/applications.html")