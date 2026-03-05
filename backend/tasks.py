import csv
import os
from models import Application, PlacementDrive, Company, Student, User, MonthlyReport
from extensions import db, celery, mail
from datetime import datetime, timedelta
from flask_mail import Message

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

    print("🔥 REMINDER TASK RUNNING")

    upcoming = datetime.now() + timedelta(days=2)

    drives = PlacementDrive.query.filter(
        PlacementDrive.application_deadline.between(datetime.now(), upcoming),
        PlacementDrive.status == "Approved"
    ).all()

    for drive in drives:

        students = Student.query.all()

        for student in students:
            already_applied = Application.query.filter_by(
                student_id=student.id,
                drive_id=drive.id
            ).first()

            if already_applied:
                continue 
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

    print("📊 GENERATING MONTHLY REPORT")

    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    total_selected = Application.query.filter_by(status="Selected").count()

    html_report = f"""
    <h2>Monthly Placement Report</h2>
    <p><strong>Total Drives:</strong> {total_drives}</p>
    <p><strong>Total Applications:</strong> {total_applications}</p>
    <p><strong>Total Selected:</strong> {total_selected}</p>
    <p><em>Generated on: {datetime.now()}</em></p>
    """

    # ✅ Save in DB
    report = MonthlyReport(
        total_drives=total_drives,
        total_applications=total_applications,
        total_selected=total_selected,
        html_content=html_report
    )

    db.session.add(report)
    db.session.commit()

    # ✅ Send email to admin
    admin = User.query.filter_by(role="admin").first()

    if admin and admin.email:
        msg = Message(
            subject="Monthly Placement Report",
            recipients=[admin.email],
            html=html_report
        )
        mail.send(msg)
        print("Report emailed to admin:", admin.email)

    return "Monthly report generated and sent"