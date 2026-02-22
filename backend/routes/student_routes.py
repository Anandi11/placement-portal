from flask import Blueprint, jsonify
from models import PlacementDrive

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/drives", methods=["GET"])
def view_drives():
    drives = PlacementDrive.query.filter_by(status="Approved").all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "company": d.company.company_name
        })

    return jsonify(result)

from services.student_service import get_student_placement_history


@student_bp.route("/placement_history/<int:student_id>", methods=["GET"])
def placement_history(student_id):
    return jsonify(get_student_placement_history(student_id))
