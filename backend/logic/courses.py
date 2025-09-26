from typing import Optional
from fastapi import HTTPException
from constants import TIME_FORMAT
import constraints
import repo.courses
import logic.logging as logger


def available_courses(db_cursor, user_email: str):
    courses = repo.courses.sql_select_available_courses(db_cursor, user_email)
    result = [{"course_id": crs} for crs in courses]
    return result


def get_all_courses(db_cursor, user_email: str):
    constraints.assert_admin_access(db_cursor, user_email)
    courses = repo.courses.sql_select_all_courses(db_cursor)
    result = [{"course_id": crs[0]} for crs in courses]
    return result


def create_course(db_conn, db_cursor, title: str, user_email: str, organization: Optional[str] = None):
    course_id = repo.courses.sql_insert_course(db_cursor, title, user_email, organization)

    logger.log(db_conn, logger.TAG_COURSE_ADD, f"User {user_email} created course {course_id}")

    return {"course_id": course_id}


def remove_course(db_conn, db_cursor, course_id: str, user_email: str):
    constraints.assert_instructor_access(db_cursor, user_email, course_id)
    repo.courses.sql_delete_course(db_cursor, course_id)

    logger.log(db_conn, logger.TAG_COURSE_DEL, f"User {user_email} deleted course {course_id}")

    return {"success": True}


def get_course_info(db_cursor, course_id: str, user_email: str):
    constraints.assert_course_access(db_cursor, user_email, course_id)
    course = repo.courses.sql_select_course_info(db_cursor, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    res = {
        "course_id": str(course[0]),
        "title": course[1],
        "instructor": course[2],
        "organization": course[3],
        "creation_time": course[4].strftime(TIME_FORMAT)
    }
    return res


def get_course_feed(db_cursor, course_id: str, user_email: str):
    constraints.assert_course_access(db_cursor, user_email, course_id)
    course_feed = repo.courses.sql_select_course_feed(db_cursor, course_id)
    res = [
        {
            "course_id": str(mat[0]),
            "post_id": mat[1],
            "section_id": mat[2],
            "section_name": mat[3],
            "section_order": mat[4],
            "type": mat[5],
            "timeadded": mat[6].strftime(TIME_FORMAT),
            "author": mat[7]
        }
        for mat in course_feed
    ]
    return res


def create_section(db_conn, db_cursor, course_id: str, title: str, user_email: str):
    # checking contraints
    constraints.assert_teacher_access(db_cursor, user_email, course_id)

    section_id = repo.courses.sql_insert_section(db_cursor, course_id, title)

    logger.log(db_conn, logger.TAG_SECTION_ADD, f"User {user_email} created a section {section_id} within the course {course_id}")
    return {"section_id": section_id}
