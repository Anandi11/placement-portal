import csv
import os
from models import Application


EXPORT_FOLDER = "exports"

if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)


def export_student_applications(student_id):
    applications = Application.query.filter_by(student_id=student_id).all()

    if not applications:
        return None

    file_path = f"{EXPORT_FOLDER}/student_{student_id}_applications.csv"

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Application ID",
            "Company",
            "Drive Title",
            "Status",
            "Application Date"
        ])

        for app in applications:
            writer.writerow([
                app.id,
                app.drive.company.company_name,
                app.drive.job_title,
                app.status,
                app.application_date
            ])

    return file_path
