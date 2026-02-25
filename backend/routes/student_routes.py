from flask import Blueprint, jsonify
from models import PlacementDrive, Student
from services.student_service import get_student_placement_history

student_bp = Blueprint("student_bp", __name__)


# ===============================
# VIEW APPROVED DRIVES
# ===============================
@student_bp.route("/drives", methods=["GET"])
def view_drives():
    drives = PlacementDrive.query.filter_by(status="Approved").all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "company": d.company.company_name,
            "deadline": d.application_deadline
        })

    return jsonify(result)


# ===============================
# VIEW STUDENT APPLIED DRIVES
# ===============================
@student_bp.route("/placement_history/<int:user_id>", methods=["GET"])
def placement_history(user_id):

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify([])

    return jsonify(get_student_placement_history(student.id))