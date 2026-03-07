from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)
    role=db.Column(db.String(20), nullable=False)
    is_active=db.Column(db.Boolean, default=True)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    student_profile=db.relationship("Student", backref="user", uselist=False)
    company_profile=db.relationship("Company", backref="user", uselist=False)

    def set_password(self, password):
        self.password=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Student(db.Model):
    __tablename__ = "students"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    branch=db.Column(db.String(50))
    cgpa=db.Column(db.Float)
    year=db.Column(db.Integer)
    phone = db.Column(db.String(20))
    skills = db.Column(db.String(300))
    bio = db.Column(db.Text)
    resume_link = db.Column(db.String(200))
    placement_history = db.relationship("Application", backref="student", lazy=True)

class Company(db.Model):
    __tablename__ = "companies"

    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_name=db.Column(db.String(150), nullable=False)
    hr_contact=db.Column(db.String(100))
    website=db.Column(db.String(150))
    approval_status=db.Column(db.String(20), default="Pending")
    drives=db.relationship("PlacementDrive", backref="company", lazy=True)

class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"
    id=db.Column(db.Integer, primary_key=True)
    company_id=db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    job_title=db.Column(db.String(100), nullable=False)
    job_description=db.Column(db.Text)
    branch_eligibility=db.Column(db.String(100))
    cgpa_eligibility=db.Column(db.Float)
    year_eligibility=db.Column(db.Integer)
    application_deadline=db.Column(db.DateTime)
    status=db.Column(db.String(20), default="Pending")
    applications=db.relationship("Application", backref="drive", lazy=True)

class Application(db.Model):
    __tablename__ = "applications"
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id=db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    application_date=db.Column(db.DateTime, server_default=db.func.now())
    status=db.Column(db.String(20), default="Applied")
    interview_date=db.Column(db.DateTime, nullable=True)
    
class MonthlyReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_drives = db.Column(db.Integer)
    total_applications = db.Column(db.Integer)
    total_selected = db.Column(db.Integer)
    generated_on = db.Column(db.DateTime, default=datetime.utcnow)
    html_content = db.Column(db.Text)