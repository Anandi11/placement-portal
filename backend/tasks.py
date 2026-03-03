import csv
import os
from models import Application, PlacementDrive, Company
from extensions import db
from extensions import celery
from models import PlacementDrive, Student
from datetime import datetime, timedelta

@celery.task
def export_student_applications(student_id):

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

@celery.task
def send_deadline_reminders():

    upcoming = datetime.now() + timedelta(minutes=1)

    drives = PlacementDrive.query.filter(
        PlacementDrive.application_deadline <= upcoming,
        PlacementDrive.status == "Approved"
    ).all()
    print("🔥 REMINDER TASK RUNNING")
    for drive in drives:
        print(f"Reminder: Drive {drive.job_title} deadline approaching!")

    return "Daily reminders sent"

@celery.task
def generate_monthly_report():

    from models import Application

    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    total_selected = Application.query.filter_by(status="Selected").count()

    html_report = f"""
    <h1>Monthly Placement Report</h1>
    <p>Total Drives: {total_drives}</p>
    <p>Total Applications: {total_applications}</p>
    <p>Total Selected: {total_selected}</p>
    """

    with open("monthly_report.html", "w") as f:
        f.write(html_report)

    print("Monthly report generated")

    return "Monthly report created"