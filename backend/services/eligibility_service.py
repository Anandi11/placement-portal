from models import Student, PlacementDrive


def check_student_eligibility(student_id, drive_id):

    student = Student.query.get(student_id)
    drive = PlacementDrive.query.get(drive_id)

    if not student or not drive:
        return False, "Invalid student or drive"

    # 🔥 NEW BRANCH LIST LOGIC
    if drive.branch_eligibility:
        eligible_branches = [
            b.strip().upper()
            for b in drive.branch_eligibility.split(",")
        ]

        if student.branch.upper() not in eligible_branches:
            return False, "Branch not eligible"

    # CGPA check
    if drive.cgpa_eligibility:
        if student.cgpa < drive.cgpa_eligibility:
            return False, "CGPA below required criteria"

    # Year check
    if drive.year_eligibility:
        if student.year != drive.year_eligibility:
            return False, "Year not eligible"

    return True, "Eligible"
