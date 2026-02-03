from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from controller.models import User, Client, Gig, Application
from controller.database import db
from controller.utils import admin_required
import re
from werkzeug.security import generate_password_hash


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    user = User.query.get(session["user_id"])
    return render_template("admin/dashboard.html", user = user)

@admin_bp.route("/clients")
@admin_required
def clients():
    clients = Client.query.all()
    return render_template("admin/clients.html", clients=clients)

@admin_bp.route("/create_clients", methods = ["GET", "POST"])
@admin_required
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

@admin_bp.route("/clients/<int:client_id>/edit", methods=["GET","POST"])
@admin_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == "POST":
        company_name = request.form.get("company")
        industry = request.form.get("industry")
        description = request.form.get("description")
        user_name = request.form.get("username")
        user_email = request.form.get("email")

        if not company_name or not industry or not description or not user_email or not user_name:
            flash("all fields should be filled", "warning")
            return redirect(url_for("admin.edit_client"))
        
        client.company_name = company_name
        client.industry = industry
        client.description = description

        client.user.username = user_name
        client.user.email = user_email

        db.session.commit()
        flash("Client updated successfully", "success")
        return redirect(url_for("admin.clients"))
    
    return render_template("admin/edit_client.html",client=client)

@admin_bp.route("/clients/<int:client_id>/delete", methods=["POST"])
@admin_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)

    db.session.delete(client.user)  # cascade deletes client + gigs
    db.session.commit()

    flash("Client deleted successfully", "success")
    return redirect(url_for("admin.clients"))


@admin_bp.route("/freelancers")
@admin_required
def freelancers():
    users = User.query.filter_by(role="Freelancer").all()
    return render_template("admin/freelancers.html", users = users)


@admin_bp.route("/gigs")
@admin_required
def gigs():
    gigs = Gig.query.all()
    return render_template("admin/gigs.html", gigs = gigs)

@admin_bp.route("/gigs/<int:gig_id>/delete", methods=["POST"])
@admin_required
def delete_gig(gig_id):
    gig = Gig.query.get_or_404(gig_id)
    db.session.delete(gig)
    db.session.commit()

    flash("Gig deleted successfully", "success")
    return redirect(url_for("admin.gigs"))

@admin_bp.route("/gigs/<int:gig_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_gig(gig_id):
    gig = Gig.query.get_or_404(gig_id)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        budget = request.form.get("budget")
        status = request.form.get("status")

        if not title or not description or not budget or not status:
            flash("All fields are required", "danger")
            return redirect(url_for("admin.edit_gig", gig_id=gig.id))

        gig.title = title
        gig.description = description
        gig.budget = int(budget)
        gig.status = status

        db.session.commit()
        flash("Gig updated successfully", "success")
        return redirect(url_for("admin.gigs"))

    return render_template("admin/edit_gig.html", gig=gig)


@admin_bp.route("/applications")
@admin_required
def applications():
    applications = Application.query.all()
    return render_template("admin/applications.html", applications=applications)