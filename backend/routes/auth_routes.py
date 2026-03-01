from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Student, Company
from flask_jwt_extended import create_access_token
auth_bp = Blueprint("auth_bp", __name__)


# ===============================
# STUDENT REGISTER
# ===============================
@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    year = data.get("year")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(name=name, email=email, role="student")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    student = Student(user_id=user.id, branch=branch, cgpa=cgpa, year=year)
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"}), 201


# ===============================
# COMPANY REGISTER
# ===============================
@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")
    hr_contact = data.get("hr_contact")
    website = data.get("website")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(name=name, email=email, role="company")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    company = Company(
        user_id=user.id,
        company_name=company_name,
        hr_contact=hr_contact,
        website=website
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered. Await admin approval."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": token,
        "role": user.role
    })

    # 🔥 ADD THIS PART
    if user.role == "company":
        company = Company.query.filter_by(user_id=user.id).first()
        response["company_id"] = company.id

    if user.role == "student":
        student = Student.query.filter_by(user_id=user.id).first()
        response["student_id"] = student.id

    return jsonify(response)