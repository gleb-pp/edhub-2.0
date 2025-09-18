from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from auth import get_current_user, get_db, get_storage_db
import json_classes
import logic.assignments


router = APIRouter()


@router.post("/create_assignment", response_model=json_classes.AssignmentID, tags=["Assignments"])
async def create_assignment(
    course_id: str,
    title: str,
    description: str,
    user_email: str = Depends(get_current_user),
):
    """
    Create the assignment with provided title and description in the course with provided course_id.

    Teacher OR Primary Instructor role required.

    Returns the (course_id, assignment_id) for the new assignment in case of success.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.assignments.create_assignment(db_conn, db_cursor, course_id, title, description, user_email)


@router.post("/remove_assignment", response_model=json_classes.Success, tags=["Assignments"])
async def remove_assignment(course_id: str, assignment_id: str, user_email: str = Depends(get_current_user)):
    """
    Remove the assignment by the provided course_id and assignment_id.

    Teacher OR Primary Instructor role required.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.assignments.remove_assignment(db_conn, db_cursor, course_id, assignment_id, user_email)


@router.get("/get_assignment", response_model=json_classes.Assignment, tags=["Assignments"])
async def get_assignment(course_id: str, assignment_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the assignment details by the provided (course_id, assignment_id).

    Returns course_id, assignment_id, creation_time, title, description, and email of the author.

    Author can be NULL if the author deleted their account.

    The format of creation time is TIME_FORMAT.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.assignments.get_assignment(db_cursor, course_id, assignment_id, user_email)


@router.post("/create_assignment_attachment", response_model=json_classes.AssignmentAttachmentMetadata, tags=["Assignments"])
async def create_assignment_attachment(
    course_id: str,
    assignment_id: str,
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user),
):
    """
    Attach the provided file to provided course assignment.

    Teacher OR Primary Instructor role required.

    Returns the (course_id, assignment_id, file_id, filename, upload_time) for the new attachment in case of success.

    The format of upload_time is TIME_FORMAT.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return await logic.assignments.create_assignment_attachment(db_conn, db_cursor, storage_db_conn, storage_db_cursor, course_id, assignment_id, file, user_email)


@router.get("/get_assignment_attachments", response_model=List[json_classes.AssignmentAttachmentMetadata], tags=["Assignments"])
async def get_assignment_attachments(course_id: str, assignment_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the list of course assignment attachments by provided course_id, assignment_id.

    Returns list of attachments metadata (course_id, assignment_id, file_id, filename, upload_time).

    The format of upload_time is TIME_FORMAT.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.assignments.get_assignment_attachments(db_cursor, course_id, assignment_id, user_email)


@router.get("/download_assignment_attachment", tags=["Assignments"])
async def download_assignment_attachment(course_id: str, assignment_id: str, file_id: str, user_email: str = Depends(get_current_user)):
    """
    Download the course assignment attachment by provided course_id, assignment_id, file_id.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return logic.assignments.download_assignment_attachment(db_cursor, storage_db_cursor, course_id, assignment_id, file_id, user_email)
