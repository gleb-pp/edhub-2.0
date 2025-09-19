from typing import List
from fastapi import APIRouter, Depends
from auth import get_current_user, get_db
import json_classes
import logic.teachers


router = APIRouter()


@router.get("/get_course_teachers", response_model=List[json_classes.User], tags=["Teachers"])
async def get_course_teachers(course_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the list of teachers teaching the course with the provided course_id.

    Does not return the Primary Instructor.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.teachers.get_course_teachers(db_cursor, course_id, user_email)


@router.post("/invite_teacher", response_model=json_classes.Success, tags=["Teachers"])
async def invite_teacher(
    course_id: str,
    new_teacher_email: str,
    teacher_email: str = Depends(get_current_user),
):
    """
    Add the user with provided new_teacher_email as a teacher to the course with provided course_id.

    Primary Instructor role required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.teachers.invite_teacher(db_conn, db_cursor, course_id, new_teacher_email, teacher_email)


@router.post("/remove_teacher", response_model=json_classes.Success, tags=["Teachers"])
async def remove_teacher(
    course_id: str,
    removing_teacher_email: str,
    teacher_email: str = Depends(get_current_user),
):
    """
    Remove the teacher with removing_teacher_email from the course with provided course_id.

    Primary Instructor OR Teacher role required.

    Primary Instructor can't remove themself until they are Primary Instructor.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.teachers.remove_teacher(db_conn, db_cursor, course_id, removing_teacher_email, teacher_email)


@router.post("/change_course_instructor", response_model=json_classes.Success, tags=["Courses"])
async def change_course_instructor(course_id: str, teacher_email: str, instructor_email: str = Depends(get_current_user)):
    """
    Transfer the course ownership (Primary Instructor role) to other Teacher within the course.

    Primary Instructor role required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.teachers.change_course_instructor(db_conn, db_cursor, course_id, teacher_email, instructor_email)
