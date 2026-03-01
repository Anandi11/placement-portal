from flask import Blueprint, jsonify
from models import PlacementDrive, Student
from services.student_service import get_student_placement_history
from extensions import cache
from tasks import export_student_applications
student_bp = Blueprint("student_bp", __name__)


# ===============================
# VIEW APPROVED DRIVES
# ===============================
@student_bp.route("/drives", methods=["GET"])
@cache.cached(timeout=60)
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
@student_bp.route("/placement_history/<int:student_id>", methods=["GET"])
def placement_history(student_id):
    
    student = Student.query.get(student_id)

    if not student:
        return jsonify([])

    return jsonify(get_student_placement_history(student.id))


@student_bp.route("/export/<int:student_id>", methods=["POST"])
def export_applications(student_id):
    export_student_applications.delay(student_id)
    return jsonify({"message": "Export started in background"})
