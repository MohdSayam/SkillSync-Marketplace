from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.models import User, Gig, Application
from controller.database import db
from controller.utils import freelancer_required

freelancer_bp = Blueprint(
    "freelancer",
    __name__,
    url_prefix="/freelancer"
)

@freelancer_bp.route("/dashboard")
@freelancer_required
def dashboard():
    user = User.query.get(session["user_id"])
    
    total_applications = Application.query.filter_by(freelancer_id=user.id).count()
    shortlisted = Application.query.filter_by(freelancer_id=user.id, status="Shortlisted").count()
    hired = Application.query.filter_by(freelancer_id=user.id, status="Hired").count()
    
    return render_template(
        "freelancer/dashboard.html",
        user=user,
        total_applications=total_applications,
        shortlisted=shortlisted,
        hired=hired
    )

@freelancer_bp.route("/gigs")
@freelancer_required
def gigs():
    user = User.query.get(session["user_id"])
    active_gigs = Gig.query.filter_by(status="Active").all()
    
    applied_gig_ids = [app.gig_id for app in user.applications]
    
    return render_template(
        "freelancer/gigs.html",
        gigs=active_gigs,
        applied_gig_ids=applied_gig_ids,
        user=user
    )

@freelancer_bp.route("/gigs/<int:gig_id>/apply", methods=["GET", "POST"])
@freelancer_required
def apply_to_gig(gig_id):
    user = User.query.get(session["user_id"])
    gig = Gig.query.get_or_404(gig_id)
    
    existing_application = Application.query.filter_by(
        freelancer_id=user.id,
        gig_id=gig.id
    ).first()
    
    if existing_application:
        flash("You have already applied to this gig", "warning")
        return redirect(url_for("freelancer.gigs"))
    
    if request.method == "POST":
        proposal_text = request.form.get("proposal_text")
        
        if not proposal_text:
            flash("Proposal text is required", "danger")
            return redirect(url_for("freelancer.apply_to_gig", gig_id=gig.id))
        
        new_application = Application(
            freelancer_id=user.id,
            gig_id=gig.id,
            proposal_text=proposal_text,
            status="Applied"
        )
        db.session.add(new_application)
        db.session.commit()
        flash("Application submitted successfully", "success")
        return redirect(url_for("freelancer.my_applications"))
    
    return render_template("freelancer/apply.html", gig=gig, user=user)

@freelancer_bp.route("/my-applications")
@freelancer_required
def my_applications():
    user = User.query.get(session["user_id"])
    applications = Application.query.filter_by(freelancer_id=user.id).all()
    
    return render_template(
        "freelancer/my_applications.html",
        applications=applications,
        user=user
    )