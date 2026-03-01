from flask import Blueprint, request, jsonify
from extensions import db
from models import Application, Student
from services.eligibility_service import check_student_eligibility

drive_bp = Blueprint("drive_bp", __name__)

@drive_bp.route("/apply", methods=["POST"])
def apply_drive():

    data = request.get_json()
    student_user_id = data.get("student_id")
    drive_id = data.get("drive_id")

    student = Student.query.get(student_user_id)

    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Eligibility check
    eligible, message = check_student_eligibility(student.id, drive_id)

    if not eligible:
        return jsonify({"message": message}), 400

    # prevent duplicate application
    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing:
        return jsonify({"message": "Already applied"}), 400

    application = Application(
        student_id=student.id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted"})