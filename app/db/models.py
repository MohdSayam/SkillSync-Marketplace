from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Enum
)

from sqlalchemy.orm import relationship

from .base import Base
from .enums import UserRole, GigStatus, ApplicationStatus

# ___User____ model

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    client_profile = relationship(
        "ClientProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    applications = relationship(
        "Application",
        back_populates="freelancer"
    )

# _________ CLient profile ---
class ClientProfile(Base):
    __tablename__="client_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    company_name = Column(String(150), nullable=False)
    industry = Column(String(150))
    description = Column(Text)
    approval_status = Column(String(20), default="Pending")

    user = relationship("User", back_populates="client_profile")

    gigs = relationship(
        "Gig",
        back_populates="client",
        cascade="all, delete-orphan"
    )

# _____________Gig_________________
class Gig(Base):
    __tablename__="gigs"

    id = Column(Integer, primary_key=True)
    client_id= Column(Integer, ForeignKey("client_profiles.id"), nullable=False ) 

    title = Column(String(200), nullable=False)
    description= Column(Text)
    budget = Column(Integer)
    status = Column(Enum(GigStatus), default=GigStatus.ACTIVE)

    client = relationship("ClientProfile", back_populates="gigs")

    applications = relationship(
        "Application",
        back_populates="gig",
        cascade="all, delete-orphan"
    )

# _________Application_________
class Application(Base):
    __tablename__="applications"

    id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    gig_id = Column(Integer, ForeignKey("gigs.id"), nullable=False)

    proposal_text=Column(Text, nullable=False)
    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED
    )  

    freelancer = relationship("User", back_populates="applications")
    gig = relationship("Gig", back_populates="applications")    