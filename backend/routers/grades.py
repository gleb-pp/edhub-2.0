from typing import Optional
from fastapi import APIRouter, Depends, Query
from auth import get_current_user, get_db
import json_classes
import logic.grades


router = APIRouter()


@router.post("/grade_submission", response_model=json_classes.Success, tags=["Grades"])
async def grade_submission(
    course_id: str,
    assignment_id: str,
    student_email: str,
    grade: str,
    comment: Optional[str] = Query(
        None,
        min_length=3,
        max_length=10000,
        description="Comment must contain 3-10000 symbols"
    ),
    user_email: str = Depends(get_current_user),
):
    """
    Allows teacher to grade student's submission.

    Teacher OR Primary Instructor role required.

    Comment must be None or contain from 3 to 10000 symbols.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.grades.grade_submission(
            db_conn,
            db_cursor,
            course_id,
            assignment_id,
            student_email,
            grade,
            comment,
            user_email
        )
