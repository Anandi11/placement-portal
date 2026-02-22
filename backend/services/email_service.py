import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"


def send_email(receiver_email, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print("Email error:", e)
        return False


# Reminder email
def send_deadline_reminder(email, drive_title):
    subject = "Placement Drive Deadline Reminder"
    message = f"Reminder: Application deadline approaching for {drive_title}"
    return send_email(email, subject, message)


# Monthly admin report
def send_admin_report(email, report_html):
    subject = "Monthly Placement Report"
    return send_email(email, subject, report_html)


# CSV export notification
def send_csv_ready_email(email):
    subject = "Placement Application Export Ready"
    message = "Your CSV export is ready for download."
    return send_email(email, subject, message)
