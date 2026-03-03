import csv
import os
from models import Application, PlacementDrive, Company
from extensions import db, celery, mail
from models import PlacementDrive, Student
from datetime import datetime, timedelta
from flask_mail import Message
from models import Student, User

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

    from flask_mail import Message
    from extensions import mail
    from models import User, Student, Application
    from datetime import datetime, timedelta

    print("🔥 REMINDER TASK RUNNING")

    upcoming = datetime.now() + timedelta(days=2)

    drives = PlacementDrive.query.filter(
        PlacementDrive.application_deadline <= upcoming,
        PlacementDrive.status == "Approved"
    ).all()

    for drive in drives:

        students = Student.query.all()

        for student in students:

            # Check if already applied
            already_applied = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first()

            if already_applied:
                continue  # Skip

            # Basic eligibility check (adjust as per your logic)
            if (
                student.cgpa >= drive.cgpa_eligibility
                and str(student.year) == str(drive.year_eligibility)
                and student.branch.lower() in drive.branch_eligibility.lower()
            ):

                user = User.query.get(student.user_id)

                if user and user.email:

                    print("Sending reminder to:", user.email)

                    msg = Message(
                        subject="Placement Drive Deadline Reminder",
                        recipients=[user.email],
                        body=f"""
Hello {user.name},

The placement drive '{drive.job_title}' is closing soon.

Deadline: {drive.application_deadline}

Please apply before it closes.

Placement Portal
"""
                    )

                    mail.send(msg)

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

    admin = User.query.filter_by(role="admin").first()

    if admin:

        msg = Message(
            subject="Monthly Placement Activity Report",
            recipients=[admin.email]
        )

        msg.html = html_report
        mail.send(msg)

        print("Monthly report emailed to admin")

    return "Monthly report sent"