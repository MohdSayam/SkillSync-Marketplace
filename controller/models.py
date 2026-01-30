from controller.database import db

# User Model 
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(
        db.Enum("Admin", "Freelancer", "Client", name="user_roles"),
        default="Freelancer",
        nullable=False
    )

    client_profile = db.relationship(
        "Client",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    applications = db.relationship(
        "Application",
        back_populates="freelancer",
        cascade = "all, delete-orphan"
    )

# client model
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    company_name  = db.Column(db.String(150), nullable=False)
    industry  = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    approval_status = db.Column(
        db.Enum("pending", "approved", name="client_status"),
        default="pending",
        nullable=False
    )

    user = db.relationship("User", back_populates="client_profile")
    gigs = db.relationship(
        "Gig",
        back_populates="client",
        cascade="all, delete-orphan"
    )

# gigs model
class Gig(db.Model):
    __tablename__ = "gigs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.Integer)

    status = db.Column(
        db.Enum("Active", "Closed", name="gig_status"),
        default="Active"
    )

    client = db.relationship("Client", back_populates="gigs")
    applications = db.relationship(
        "Application",
        back_populates="gig",
        cascade="all, delete-orphan"
    )


# application model
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    gig_id = db.Column(db.Integer, db.ForeignKey("gigs.id"), nullable=False)
    proposal_text = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("Applied", "Shortlisted", "Rejected", "Hired", name="application_status"),
        default="Applied"
    )   

    freelancer = db.relationship("User", back_populates="applications")
    gig = db.relationship("Gig", back_populates="applications")
