from flask import Blueprint, jsonify
from models import PlacementDrive, Student
from services.student_service import get_student_placement_history
from extensions import cache
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from tasks import export_student_applications

student_bp = Blueprint("student_bp", __name__)

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

    student = Student.query.filter_by(user_id=user_id).first()

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

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    export_student_applications.delay(student.id)

    return jsonify({"message": "Export started in background"})