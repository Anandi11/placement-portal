from flask import Blueprint, jsonify
from services.admin_service import get_placement_report
from extensions import cache
from flask_jwt_extended import jwt_required, get_jwt
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
@cache.cached(timeout=30)
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_admin_dashboard_stats())


# ===============================
# COMPANY APIs
# ===============================
@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def list_companies():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_companies())


@admin_bp.route("/approve/company/<int:id>", methods=["PUT"])
@jwt_required()
def approve_company_route(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(approve_company(id))


@admin_bp.route("/reject/company/<int:id>", methods=["PUT"])
@jwt_required()
def reject_company_route(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(reject_company(id))


# ===============================
# DRIVE APIs
# ===============================
@admin_bp.route("/drives", methods=["GET"])
@jwt_required()
def list_drives():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_drives())


@admin_bp.route("/approve/drive/<int:id>", methods=["PUT"])
@jwt_required()
def approve_drive_route(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(approve_drive(id))


# ===============================
# STUDENT APIs
# ===============================
@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def list_students():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_students())


@admin_bp.route("/blacklist/<int:id>", methods=["PUT"])
@jwt_required()
def blacklist_user_route(id):
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(blacklist_user(id))


# ===============================
# APPLICATION APIs
# ===============================
@admin_bp.route("/applications", methods=["GET"])
@cache.cached(timeout=30)
@jwt_required()
def list_applications():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_applications())

@admin_bp.route("/placement_report", methods=["GET"])
@jwt_required()
def placement_report():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_placement_report())
