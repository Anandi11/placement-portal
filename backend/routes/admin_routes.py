from flask import Blueprint, jsonify, request
from services.admin_service import get_placement_report
from extensions import cache
from sqlalchemy import or_
from models import MonthlyReport, Student, User, Company
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

def admin_required():
    claims=get_jwt()
    return claims.get("role")!="admin"

@admin_bp.route("/dashboard", methods=["GET"])
@cache.cached(timeout=30)
@jwt_required()
def admin_dashboard():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_admin_dashboard_stats())

@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
def list_companies():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_companies())

@admin_bp.route("/approve/company/<int:id>", methods=["PUT"])
@jwt_required()
def approve_company_route(id):
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(approve_company(id))

@admin_bp.route("/reject/company/<int:id>", methods=["PUT"])
@jwt_required()
def reject_company_route(id):
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(reject_company(id))

@admin_bp.route("/drives", methods=["GET"])
@jwt_required()
def list_drives():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_drives())

@admin_bp.route("/approve/drive/<int:id>", methods=["PUT"])
@jwt_required()
def approve_drive_route(id):
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(approve_drive(id))

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
def list_students():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_students())

@admin_bp.route("/blacklist/<int:id>", methods=["PUT"])
@jwt_required()
def blacklist_user_route(id):
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(blacklist_user(id))

@admin_bp.route("/applications", methods=["GET"])
@cache.cached(timeout=30)
@jwt_required()
def list_applications():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_all_applications())

@admin_bp.route("/placement_report", methods=["GET"])
@jwt_required()
def placement_report():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_placement_report())

@admin_bp.route("/reports", methods=["GET"])
def get_reports():
    reports = MonthlyReport.query.order_by(
        MonthlyReport.generated_on.desc()
    ).all()
    data = [
        {
            "id": r.id,
            "generated_on": r.generated_on,
            "total_drives": r.total_drives,
            "total_applications": r.total_applications,
            "total_selected": r.total_selected,
            "html_content": r.html_content
        }
        for r in reports
    ]
    return jsonify(data)

@admin_bp.route("/search/students")
@jwt_required()
def search_students():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    students = User.query.filter(
        User.role == "student",
        or_(
            User.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%")
        )
    ).limit(10).all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "active": s.is_active
        }
        for s in students
    ])

@admin_bp.route("/search/companies")
@jwt_required()
def search_companies():
    if admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    companies = Company.query.filter(
        Company.company_name.ilike(f"%{query}%")
    ).limit(10).all() 

    return jsonify([
        {
            "id": c.id,
            "company_name": c.company_name,
            "approval_status": c.approval_status
        }
        for c in companies
    ])