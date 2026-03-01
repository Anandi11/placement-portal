from flask import Blueprint, request, jsonify
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Application, Student
from services.eligibility_service import check_student_eligibility

drive_bp = Blueprint("drive_bp", __name__)

@drive_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_drive():

    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    drive_id = data.get("drive_id")

    # continue eligibility + duplicate check...

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