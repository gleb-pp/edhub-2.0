from typing import List
from fastapi import APIRouter, Query, Depends
from auth import get_current_user, get_db
import json_classes
import logic.personalization
from constants import EMOJI_COUNT


router = APIRouter()


@router.post("/change_courses_order", response_model=json_classes.Success, tags=["Personalization"])
async def change_courses_order(
    new_order: List[str] = Query(...),
    user_email: str = Depends(get_current_user),
):
    """
    Change the order of courses.

    The list of course_ids should be passed as a new_order parameter.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.personalization.change_courses_order(db_conn, db_cursor, new_order, user_email)


@router.post("/set_course_emoji", response_model=json_classes.Course, tags=["Personalization"])
async def set_course_emoji(
    course_id: str,
    emoji_id: int = Query(..., ge=0, le=EMOJI_COUNT),
    user_email: str = Depends(get_current_user)
):
    """
    Set a personal emoji for a course.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.personalization.set_course_emoji(db_cursor, course_id, emoji_id, user_email)
