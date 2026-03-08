from flask import Blueprint, request, jsonify
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Application, Student, PlacementDrive

drive_bp = Blueprint("drive_bp", __name__)

@drive_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_drive():

    claims = get_jwt()
    if claims["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    user_id=int(get_jwt_identity())

    student=Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data=request.get_json()
    drive_id=data.get("drive_id")

    eligible, message=check_student_eligibility(student.id, drive_id)

    if not eligible:
        return jsonify({"message": message}), 400

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing:
        return jsonify({"message": "Already applied"}), 400

    application=Application(
        student_id=student.id,
        drive_id=drive_id
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Application submitted"})

def check_student_eligibility(student_id, drive_id):

    student = Student.query.get(student_id)
    drive = PlacementDrive.query.get(drive_id)

    if not student or not drive:
        return False, "Invalid student or drive"
    if drive.branch_eligibility:
        eligible_branches = [
            b.strip().upper()
            for b in drive.branch_eligibility.split(",")
        ]

        if student.branch.upper() not in eligible_branches:
            return False, "Branch not eligible"

    if drive.cgpa_eligibility:
        if student.cgpa < drive.cgpa_eligibility:
            return False, "CGPA below required criteria"
    if drive.year_eligibility:
        if student.year != drive.year_eligibility:
            return False, "Year not eligible"

    return True, "Eligible"