from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.models import User, Client, Gig, Application
from controller.database import db
from controller.utils import client_required

client_bp = Blueprint(
    "client",
    __name__,
    url_prefix="/client"
)

@client_bp.route("/dashboard")
@client_required
def dashboard():
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    
    total_gigs = len(client.gigs) if client else 0
    active_gigs = Gig.query.filter_by(client_id=client.id, status="Active").count() if client else 0
    
    total_applications = 0
    if client:
        for gig in client.gigs:
            total_applications += len(gig.applications)
    
    return render_template(
        "client/dashboard.html",
        user=user,
        client=client,
        total_gigs=total_gigs,
        active_gigs=active_gigs,
        total_applications=total_applications
    )

@client_bp.route("/gigs")
@client_required
def gigs():
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    gigs = client.gigs if client else []
    return render_template("client/gigs.html", gigs=gigs, client=client)

@client_bp.route("/gigs/create", methods=["GET", "POST"])
@client_required
def create_gig():
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        budget = request.form.get("budget")
        
        if not title or not description or not budget:
            flash("All fields are required", "danger")
            return redirect(url_for("client.create_gig"))
        
        new_gig = Gig(
            client_id=client.id,
            title=title,
            description=description,
            budget=int(budget),
            status="Active"
        )
        db.session.add(new_gig)
        db.session.commit()
        flash("Gig created successfully", "success")
        return redirect(url_for("client.gigs"))
    
    return render_template("client/create_gig.html", client=client)

@client_bp.route("/gigs/<int:gig_id>/edit", methods=["GET", "POST"])
@client_required
def edit_gig(gig_id):
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    gig = Gig.query.get_or_404(gig_id)
    
    if gig.client_id != client.id:
        flash("You can only edit your own gigs", "danger")
        return redirect(url_for("client.gigs"))
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        budget = request.form.get("budget")
        status = request.form.get("status")
        
        if not title or not description or not budget or not status:
            flash("All fields are required", "danger")
            return redirect(url_for("client.edit_gig", gig_id=gig.id))
        
        gig.title = title
        gig.description = description
        gig.budget = int(budget)
        gig.status = status
        
        db.session.commit()
        flash("Gig updated successfully", "success")
        return redirect(url_for("client.gigs"))
    
    return render_template("client/edit_gig.html", gig=gig, client=client)

@client_bp.route("/gigs/<int:gig_id>/delete", methods=["POST"])
@client_required
def delete_gig(gig_id):
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    gig = Gig.query.get_or_404(gig_id)
    
    if gig.client_id != client.id:
        flash("You can only delete your own gigs", "danger")
        return redirect(url_for("client.gigs"))
    
    db.session.delete(gig)
    db.session.commit()
    flash("Gig deleted successfully", "success")
    return redirect(url_for("client.gigs"))

@client_bp.route("/applications")
@client_required
def applications():
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    
    all_applications = []
    if client:
        for gig in client.gigs:
            for app in gig.applications:
                all_applications.append(app)
    
    return render_template("client/applications.html", applications=all_applications, client=client)

@client_bp.route("/applications/<int:app_id>/update", methods=["POST"])
@client_required
def update_application(app_id):
    user = User.query.get(session["user_id"])
    client = Client.query.filter_by(user_id=user.id).first()
    application = Application.query.get_or_404(app_id)
    
    if application.gig.client_id != client.id:
        flash("You can only update applications for your gigs", "danger")
        return redirect(url_for("client.applications"))
    
    new_status = request.form.get("status")
    if new_status in ["Applied", "Shortlisted", "Rejected", "Hired"]:
        application.status = new_status
        db.session.commit()
        flash(f"Application status updated to {new_status}", "success")
    
    return redirect(url_for("client.applications"))