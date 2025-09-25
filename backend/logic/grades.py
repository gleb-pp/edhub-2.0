from typing import Optional
from fastapi import HTTPException
import constraints
import repo.grades as repo_grades
import repo.assignments as repo_assignments
import repo.submissions as repo_submissions
import repo.students as repo_students
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

    repo_grades.sql_update_submission_grade(db_cursor, grade, comment, user_email, course_id, assignment_id, student_email)

    logger.log(db_conn, logger.TAG_ASSIGNMENT_GRADE, f"Teacher {user_email} graded an assignment {assignment_id} in {course_id} by {student_email}")

    return {"success": True}


# TODO: подумать над оптимизацией запросов
def get_all_course_grades(db_cursor, course_id: str, user_email: str):

    # checking constraints
    constraints.assert_teacher_access(db_cursor, user_email, course_id)

    # check if there are any students enrolled in the course
    students = repo_students.sql_select_enrolled_students(db_cursor, course_id)
    if len(students) == 0:
        raise HTTPException(status_code=404, detail="Empty grade table (there are no students enrolled)")

    # check if there are any assignments within the course
    assignments = repo_assignments.sql_select_course_assignments(db_cursor, course_id)
    if len(assignments) == 0:
        raise HTTPException(status_code=404, detail="Empty grade table (there are no assignments published)")

    table = []
    for student in students:
        grades = []
        for ass in assignments:
            grade = repo_grades.sql_select_submission_grade(db_cursor, course_id, ass[1], student[0])
            if grade is None:
                grades.append(None)
            else:
                grades.append(grade[0])

        table.append({"name": student[1],
                      "email": student[0], 
                      "grades": grades})
    return table


# TODO: подумать над оптимизацией запросов
def get_student_course_grades(db_cursor, course_id: str, student_email: str, user_email: str):
    # checking constraints
    if not (
        constraints.check_teacher_access(db_cursor, user_email, course_id)
        or constraints.check_parent_student_access(db_cursor, user_email, student_email, course_id)
        or student_email == user_email
    ):
        raise HTTPException(status_code=403, detail="User does not have access to the grades of this student")

    # check if the student is enrooled in the course
    if not constraints.check_student_access(db_cursor, student_email, course_id):
        raise HTTPException(status_code=403, detail="User is not a student at this course")

    # check if there are any assignments within the course
    assignments = repo_assignments.sql_select_course_assignments(db_cursor, course_id)
    if len(assignments) == 0:
        raise HTTPException(status_code=404, detail="Empty grade table (there are no assignments published)")

    table = [
        {
            "assignment_name": grade[0],
            "assignment_id": grade[1],
            "grade": grade[2],
            "comment": grade[3],
            "grader_name": grade[4],
            "grader_email": grade[5]
        }
        for grade in repo_grades.sql_select_student_grades(db_cursor, course_id, student_email)
    ]
    return table
