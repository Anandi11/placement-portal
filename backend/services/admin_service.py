from models import User, Company, PlacementDrive, Application
from extensions import db
from sqlalchemy import func

# ==============================
# DASHBOARD STATS
# ==============================
def get_admin_dashboard_stats():
    total_students = User.query.filter_by(role="student").count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    return {
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    }


# ==============================
# COMPANY MANAGEMENT
# ==============================
def get_all_companies():
    companies = Company.query.all()

    result = []
    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "approval_status": c.approval_status,
            "hr_contact": c.hr_contact,
            "website": c.website
        })
    return result


def approve_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return {"error": "Company not found"}

    company.approval_status = "Approved"
    db.session.commit()

    return {"message": "Company approved"}


def reject_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return {"error": "Company not found"}

    company.approval_status = "Rejected"
    db.session.commit()

    return {"message": "Company rejected"}


# ==============================
# DRIVE MANAGEMENT
# ==============================
def get_all_drives():
    drives = PlacementDrive.query.all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "company": d.company.company_name,
            "status": d.status
        })
    return result


def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return {"error": "Drive not found"}

    drive.status = "Approved"
    db.session.commit()

    return {"message": "Drive approved"}


# ==============================
# STUDENT MANAGEMENT
# ==============================
def get_all_students():
    students = User.query.filter_by(role="student").all()

    result = []
    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "active": s.is_active
        })
    return result


def blacklist_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    user.is_active = False
    db.session.commit()

    return {"message": "User blacklisted"}


# ==============================
# APPLICATION MANAGEMENT
# ==============================
def get_all_applications():
    apps = Application.query.all()

    result = []
    for a in apps:
        result.append({
            "application_id": a.id,
            "student": a.student.user.name,
            "company": a.drive.company.company_name,
            "drive": a.drive.job_title,
            "status": a.status
        })
    return result

def get_placement_report():

    total_drives = PlacementDrive.query.count()

    total_applications = Application.query.count()

    total_selected = Application.query.filter_by(status="Selected").count()

    # 🔥 FIXED explicit joins
    company_wise = db.session.query(
        Company.company_name,
        func.count(Application.id)
    ).select_from(Application)\
     .join(PlacementDrive, Application.drive_id == PlacementDrive.id)\
     .join(Company, PlacementDrive.company_id == Company.id)\
     .filter(Application.status == "Selected")\
     .group_by(Company.company_name)\
     .all()

    company_data = [
        {"company": c[0], "selections": c[1]}
        for c in company_wise
    ]

    return {
        "total_drives": total_drives,
        "applications": total_applications,
        "selected": total_selected,
        "company_wise": company_data
    }