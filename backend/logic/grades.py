from typing import Optional
import constraints
import repo.submissions as repo_submit
import logic.logging as logger


def grade_submission(
    db_conn,
    db_cursor,
    course_id: str,
    assignment_id: str,
    student_email: str,
    grade: str,
    comment: Optional[str],
    user_email: str,
):
    # checking constraints
    constraints.assert_teacher_access(db_cursor, user_email, course_id)
    constraints.assert_submission_exists(db_cursor, course_id, assignment_id, student_email)

    repo_submit.sql_update_submission_grade(db_cursor, grade, comment, user_email, course_id, assignment_id, student_email)

    logger.log(db_conn, logger.TAG_ASSIGNMENT_GRADE, f"Teacher {user_email} graded an assignment {assignment_id} in {course_id} by {student_email}")

    return {"success": True}
