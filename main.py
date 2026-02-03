from flask import Flask, render_template
from controller.database import db
from controller.config import Config

from controller.routes import (auth_bp, client_bp, freelancer_bp, admin_bp)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# routes registering
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)
app.register_blueprint(freelancer_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)