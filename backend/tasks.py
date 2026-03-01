import csv
import os
from models import Application, PlacementDrive, Company
from extensions import db
from extensions import celery

@celery.task
def export_student_applications(student_id):
    from app import create_app
    from models import Student, Application, PlacementDrive, Company

    app = create_app()

    with app.app_context():

        student = Student.query.get(student_id)
        print("Student ID:", student_id)
        if not student:
            return "Student not found"

        applications = Application.query.filter_by(
            student_id=student.id
        ).all()

        export_folder = "exports"
        os.makedirs(export_folder, exist_ok=True)

        filename = f"{export_folder}/student_{student.id}_applications.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Application ID",
                "Company",
                "Job Title",
                "Status",
                "Applied Date"
            ])

            for app_obj in applications:
                drive = PlacementDrive.query.get(app_obj.drive_id)
                company = Company.query.get(drive.company_id)

                writer.writerow([
                    app_obj.id,
                    company.company_name,
                    drive.job_title,
                    app_obj.status,
                    app_obj.application_date
                ])

        return f"Export completed: {filename}"