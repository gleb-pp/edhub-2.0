from typing import List, Tuple, Optional


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

def sql_select_student_grades(db_cursor, course_id: str, student_email: str) -> List[Tuple[str, int, Optional[int], Optional[str], Optional[str], Optional[str]]]:
    db_cursor.execute(
        """
        SELECT 
            ass.name AS assignment_name,
            ass.assid AS assignment_id,
            sbmt.grade,
            sbmt.comment,
            tch.publicname AS grader_name,
            sbmt.gradedby AS grader_email
        FROM course_assignments ass
        LEFT JOIN course_assignments_submissions sbmt
            ON ass.courseid = sbmt.courseid
           AND ass.assid = sbmt.assid
           AND sbmt.email = %s
        LEFT JOIN users tch
            ON sbmt.gradedby = tch.email
        WHERE ass.courseid = %s
        ORDER BY ass.assid
        """,
        (student_email, course_id),
    )
    return db_cursor.fetchall()
