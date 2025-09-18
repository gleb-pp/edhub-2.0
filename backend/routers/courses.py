from typing import List, Optional
from fastapi import APIRouter, Depends

from auth import get_current_user, get_db
import json_classes
import logic.courses
import logic.assignments

router = APIRouter()


@router.get("/available_courses", response_model=List[json_classes.CourseId], tags=["Courses"])
async def available_courses(user_email: str = Depends(get_current_user)):
    """
    Get the list of IDs of courses available for user (as a Primary Instructor, Teacher, Student, or Parent).
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.available_courses(db_cursor, user_email)


@router.get("/get_all_courses", response_model=List[json_classes.CourseId], tags=["Courses"])
async def get_all_courses(user_email: str = Depends(get_current_user)):
    """
    Get the list of IDs of all courses in the system.

    Admin role required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.get_all_courses(db_cursor, user_email)


@router.post("/create_course", response_model=json_classes.CourseId, tags=["Courses"])
async def create_course(title: str, organization: Optional[str] = None, user_email: str = Depends(get_current_user)):
    """
    Create the course with provided title and become a Primary Instructor in it.

    Organization parameter is optional / can be None.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.create_course(db_conn, db_cursor, title, user_email, organization)


# WARNING: update if new elements appear
@router.post("/remove_course", response_model=json_classes.Success, tags=["Courses"])
async def remove_course(course_id: str, user_email: str = Depends(get_current_user)):
    """
    Remove the course with provided course_id.

    All the course materials, teachers, students, and parents will be also removed.

    Primary Instructor role required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.remove_course(db_conn, db_cursor, course_id, user_email)


@router.get("/get_course_info", response_model=json_classes.Course, tags=["Courses"])
async def get_course_info(course_id: str, user_email: str = Depends(get_current_user)):
    """
    Get information about the course: course_id, title, primary instructor, organization, and creation date.

    Organization can be None.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.get_course_info(db_cursor, course_id, user_email)


@router.get("/get_course_feed", response_model=List[json_classes.CoursePost], tags=["Courses"])
async def get_course_feed(course_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the course feed with all its materials.

    Materials are ordered by creation_date, the first posts are new.

    Returns the list of (course_id, post_id, type, timeadded, author) for each material.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.courses.get_course_feed(db_cursor, course_id, user_email)
