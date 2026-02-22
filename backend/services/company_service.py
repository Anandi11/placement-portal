from models import PlacementDrive, Application, Company
from extensions import db
from datetime import datetime

# ===============================
# CREATE DRIVE
# ===============================
def create_drive(data):
    deadline_str = data.get("deadline")
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

    drive = PlacementDrive(
        company_id=data.get("company_id"),
        job_title=data.get("job_title"),
        job_description=data.get("job_description"),
        branch_eligibility=data.get("branch"),
        cgpa_eligibility=float(data.get("cgpa")),
        year_eligibility=int(data.get("year")),
        application_deadline=deadline
    )

    db.session.add(drive)
    db.session.commit()

    return {"message": "Drive created. Await admin approval"}


# ===============================
# GET COMPANY DRIVES
# ===============================
def get_company_drives(company_id):
    drives = PlacementDrive.query.filter_by(company_id=company_id).all()

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status
        })

    return result


# ===============================
# GET APPLICANTS FOR DRIVE
# ===============================
def get_drive_applicants(drive_id):
    applications = Application.query.filter_by(drive_id=drive_id).all()

    result = []
    for a in applications:
        result.append({
            "application_id": a.id,
            "student_name": a.student.user.name,
            "status": a.status
        })

    return result


# ===============================
# UPDATE APPLICATION STATUS
# ===============================
def update_application_status(app_id, status):
    app = Application.query.get(app_id)

    if not app:
        return {"error": "Application not found"}

    app.status = status
    db.session.commit()

    return {"message": "Application updated"}
