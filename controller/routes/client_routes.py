from flask import Blueprint, render_template

client_bp = Blueprint(
    "client",
    __name__,
    url_prefix="/client"
)

@client_bp.route("/dashboard")
def dashboard():
    return render_template("client/dashboard.html")