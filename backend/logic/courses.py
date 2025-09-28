from typing import Optional, List
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


def change_courses_order(db_conn, db_cursor, new_order: List[str], user_email: str):
    if not isinstance(new_order, list):
        raise HTTPException(status_code=400, detail="Provided parameter new_order is not a list")

    if not all(isinstance(i, str) for i in new_order):
        raise HTTPException(status_code=400, detail="Provided parameter new_order is not a list of strings")

    courses = repo.courses.sql_select_available_courses(db_cursor, user_email)
    if len(new_order) != len(courses) or set(new_order) != set(courses):
        raise HTTPException(status_code=400, detail="Provided parameter new_order does not match with the list of available courses")

    repo.courses.sql_update_courses_order(db_cursor, new_order, user_email)

    logger.log(db_conn, logger._TAG_COURSE_PERS_INFO_EDIT, f"User {user_email} changed an order of available courses")
    return {"success": True}
