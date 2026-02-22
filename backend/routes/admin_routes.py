from flask import Blueprint, jsonify
from services.admin_service import get_placement_report

from services.admin_service import (
    get_admin_dashboard_stats,
    get_all_companies,
    approve_company,
    reject_company,
    get_all_drives,
    approve_drive,
    get_all_students,
    blacklist_user,
    get_all_applications
)

admin_bp = Blueprint("admin_bp", __name__)


# ===============================
# DASHBOARD
# ===============================
@admin_bp.route("/dashboard", methods=["GET"])
def admin_dashboard():
    return jsonify(get_admin_dashboard_stats())


# ===============================
# COMPANY APIs
# ===============================
@admin_bp.route("/companies", methods=["GET"])
def list_companies():
    return jsonify(get_all_companies())


@admin_bp.route("/approve/company/<int:id>", methods=["PUT"])
def approve_company_route(id):
    return jsonify(approve_company(id))


@admin_bp.route("/reject/company/<int:id>", methods=["PUT"])
def reject_company_route(id):
    return jsonify(reject_company(id))


# ===============================
# DRIVE APIs
# ===============================
@admin_bp.route("/drives", methods=["GET"])
def list_drives():
    return jsonify(get_all_drives())


@admin_bp.route("/approve/drive/<int:id>", methods=["PUT"])
def approve_drive_route(id):
    return jsonify(approve_drive(id))


# ===============================
# STUDENT APIs
# ===============================
@admin_bp.route("/students", methods=["GET"])
def list_students():
    return jsonify(get_all_students())


@admin_bp.route("/blacklist/<int:id>", methods=["PUT"])
def blacklist_user_route(id):
    return jsonify(blacklist_user(id))


# ===============================
# APPLICATION APIs
# ===============================
@admin_bp.route("/applications", methods=["GET"])
def list_applications():
    return jsonify(get_all_applications())

@admin_bp.route("/placement_report", methods=["GET"])
def placement_report():
    return jsonify(get_placement_report())
