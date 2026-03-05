from flask import Blueprint, jsonify, request, current_app
from models import PlacementDrive, Student, User, Company, Application
from extensions import db
from sqlalchemy import or_
from services.student_service import get_student_placement_history
from extensions import cache
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from tasks import export_student_applications
import os
from werkzeug.utils import secure_filename

student_bp = Blueprint("student_bp", __name__)

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_student_or_404(user_id):
    """Helper — returns (student, user) tuple or raises early."""
    user = User.query.get(user_id)
    student = Student.query.filter_by(user_id=user_id).first()
    return student, user


# ===============================
# VIEW APPROVED DRIVES
# ===============================
@student_bp.route("/drives", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60)
def view_drives():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "company": d.company.company_name if d.company else "N/A",
            "deadline": d.application_deadline
        })

    return jsonify(result)


# ===============================
# VIEW STUDENT APPLIED DRIVES
# ===============================
@student_bp.route("/placement_history", methods=["GET"])
@jwt_required()
def placement_history():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())
    student, _ = get_student_or_404(user_id)

    if not student:
        return jsonify([])

    return jsonify(get_student_placement_history(student.id))


# ===============================
# EXPORT APPLICATIONS (ASYNC)
# ===============================
@student_bp.route("/export", methods=["POST"])
@jwt_required()
def export_applications():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())
    student, _ = get_student_or_404(user_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    export_student_applications.delay(student.id)
    return jsonify({"message": "Export started in background"})


# ===============================
# SEARCH DRIVES
# ===============================
@student_bp.route("/search/drives")
@jwt_required()
def search_drives():
    query = request.args.get("q", "").strip()

    drives = db.session.query(PlacementDrive, Company.company_name)\
        .join(Company)\
        .filter(
            PlacementDrive.status == "Approved",
            or_(
                PlacementDrive.job_title.ilike(f"%{query}%"),
                Company.company_name.ilike(f"%{query}%")
            )
        ).limit(10).all()

    return jsonify([
        {
            "id": d.id,
            "job_title": d.job_title,
            "company": company,
            "deadline": d.application_deadline
        }
        for d, company in drives
    ])


# ===============================
# GET PROFILE
# ===============================
@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())
    student, user = get_student_or_404(user_id)

    if not student or not user:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        # From User table
        "name":       user.name,
        "email":      user.email,
        # From Student table
        "branch":     student.branch,
        "cgpa":       student.cgpa,
        "year":       student.year,
        "phone":      student.phone,
        "skills":     student.skills,
        "bio":        student.bio,
        "resume_url": student.resume_link   # served path, e.g. /uploads/resumes/filename.pdf
    })


# ===============================
# UPDATE PROFILE
# ===============================
@student_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())
    student, user = get_student_or_404(user_id)

    if not student or not user:
        return jsonify({"error": "Profile not found"}), 404

    data = request.get_json()

    # Update User table fields
    if "name" in data:
        user.name = data["name"].strip()
    if "email" in data:
        # Check the new email isn't already taken by someone else
        existing = User.query.filter(User.email == data["email"], User.id != user_id).first()
        if existing:
            return jsonify({"error": "Email already in use"}), 409
        user.email = data["email"].strip()

    # Update Student table fields
    if "branch" in data:
        student.branch = data["branch"].strip()
    if "cgpa" in data:
        student.cgpa = float(data["cgpa"])
    if "year" in data:
        student.year = int(data["year"])
    if "phone" in data:
        student.phone = data["phone"].strip()
    if "skills" in data:
        student.skills = data["skills"].strip()
    if "bio" in data:
        student.bio = data["bio"].strip()

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})


# ===============================
# UPLOAD RESUME
# ===============================
@student_bp.route("/upload_resume", methods=["POST"])
@jwt_required()
def upload_resume():
    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())
    student, _ = get_student_or_404(user_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    if "resume" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF, DOC, DOCX files are allowed"}), 400

    if file.content_length and file.content_length > 5 * 1024 * 1024:
        return jsonify({"error": "File too large. Max 5MB"}), 413

    # Build a unique filename: resume_<student_id>.<ext>
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"resume_{student.id}.{ext}")

    upload_folder = os.path.join(current_app.root_path, "uploads", "resumes")
    os.makedirs(upload_folder, exist_ok=True)   # create folder if it doesn't exist

    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    # Delete the student's old resume file if it was a different extension
    if student.resume_link:
        old_filename = os.path.basename(student.resume_link)
        if old_filename != filename:
            old_path = os.path.join(upload_folder, old_filename)
            if os.path.exists(old_path):
                os.remove(old_path)

    # Save the URL path in DB — serve this via Flask static or a dedicated route
    student.resume_link = f"/uploads/resumes/{filename}"
    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume_url": student.resume_link
    })