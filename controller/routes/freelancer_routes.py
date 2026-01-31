from flask import Blueprint, render_template

freelancer_bp = Blueprint(
    "freelancer",
    __name__,
    url_prefix="/freelancer"
)

@freelancer_bp.route("/dashboard")
def dashboard():
    return render_template("freelancer/dashboard.html")