from models import Application


def get_student_applications(student_id):
    apps = Application.query.filter_by(student_id=student_id).all()

    result = []
    for a in apps:
        result.append({
            "application_id": a.id,
            "company": a.drive.company.company_name,
            "drive": a.drive.job_title,
            "status": a.status
        })

    return result

def get_student_placement_history(student_id):

    applications = Application.query.filter_by(student_id=student_id).all()

    history = []

    for app in applications:
        history.append({
            "company": app.drive.company.company_name,
            "job_title": app.drive.job_title,
            "status": app.status,
            "applied_on": app.application_date,
            "drive_deadline": app.drive.application_deadline
        })

    return history