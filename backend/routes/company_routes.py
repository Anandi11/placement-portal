from flask import Blueprint, request, jsonify
from models import Company, PlacementDrive
from services.company_service import (
    create_drive,
    get_company_drives,
    get_drive_applicants,
    update_application_status
)

company_bp = Blueprint("company_bp", __name__)


# ===============================
# CREATE DRIVE
# ===============================
@company_bp.route("/create_drive", methods=["POST"])
def create_drive_route():
    data = request.get_json()
    return jsonify(create_drive(data))


# ===============================
# VIEW COMPANY DRIVES
# ===============================
@company_bp.route("/drives/<int:company_id>", methods=["GET"])
def get_company_drives(company_id):

    company = Company.query.get(company_id)

    if not company:
        return jsonify([])

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    data = []

    for d in drives:
        data.append({
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status
        })

    return jsonify(data)



# ===============================
# VIEW APPLICANTS
# ===============================
@company_bp.route("/applicants/<int:drive_id>", methods=["GET"])
def drive_applicants(drive_id):
    return jsonify(get_drive_applicants(drive_id))


# ===============================
# UPDATE APPLICATION STATUS
# ===============================
@company_bp.route("/application/update/<int:app_id>", methods=["PUT"])
def update_application(app_id):
    data = request.get_json()
    status = data.get("status")
    return jsonify(update_application_status(app_id, status))
