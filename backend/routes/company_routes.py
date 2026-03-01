from flask import Blueprint, request, jsonify
from models import Company, PlacementDrive
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from services.company_service import (
    create_drive,
    get_drive_applicants,
    update_application_status
)

company_bp = Blueprint("company_bp", __name__)

# ===============================
# CREATE DRIVE
# ===============================
@company_bp.route("/create_drive", methods=["POST"])
@jwt_required()
def create_drive_route():
    claims = get_jwt()
    if claims["role"] != "company":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())

    data = request.get_json()
    data["user_id"] = user_id  # inject from JWT

    return jsonify(create_drive(data))


# ===============================
# VIEW COMPANY DRIVES
# ===============================
@company_bp.route("/drives", methods=["GET"])
@jwt_required()
def view_company_drives():
    claims = get_jwt()
    if claims["role"] != "company":
        return jsonify({"error": "Unauthorized"}), 403

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify([])

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status
        })

    return jsonify(result)


# ===============================
# VIEW APPLICANTS
# ===============================
@company_bp.route("/applicants/<int:drive_id>", methods=["GET"])
@jwt_required()
def drive_applicants(drive_id):
    claims = get_jwt()
    if claims["role"] != "company":
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify(get_drive_applicants(drive_id))


# ===============================
# UPDATE APPLICATION STATUS
# ===============================
@company_bp.route("/application/update/<int:app_id>", methods=["PUT"])
@jwt_required()
def update_application(app_id):
    claims = get_jwt()
    if claims["role"] != "company":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    status = data.get("status")

    return jsonify(update_application_status(app_id, status))