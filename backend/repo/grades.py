from typing import Tuple, Optional


def sql_select_submission_grade(db_cursor, course_id: str, assignment_id: str, student_email: str) -> Optional[Tuple[int]]:
    db_cursor.execute(
        "SELECT grade FROM course_assignments_submissions WHERE courseid = %s AND assid = %s AND email = %s",
        (course_id, assignment_id, student_email),
    )
    return db_cursor.fetchone()


def sql_update_submission_grade(db_cursor, grade: str | int, comment: Optional[str], user_email: str, course_id: str, assignment_id: str, student_email: str) -> None:
    db_cursor.execute(
        """
        UPDATE course_assignments_submissions
        SET grade = %s, comment = %s, gradedby = %s
        WHERE courseid = %s AND assid = %s AND email = %s
        """,
        (grade, comment, user_email, course_id, assignment_id, student_email),
    )
