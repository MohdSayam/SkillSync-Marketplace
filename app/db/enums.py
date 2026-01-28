import enum

class UserRole(enum.Enum):
    ADMIN="Admin"
    CLIENT="Client"
    FREELANCER="Freelancer"

class GigStatus(enum.Enum):
    ACTIVE="Active"
    CLOSED="Closed"

class ApplicationStatus(enum.Enum):
    APPLIED="Applied"
    SHORTLISTED="Shortlisted"
    REJECTED="Rejected"
    HIRED="Hired"        