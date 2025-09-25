from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from auth import get_current_user, get_db, get_storage_db
import json_classes
import logic.submissions


router = APIRouter()


@router.post("/submit_assignment", response_model=json_classes.Success, tags=["Submissions"])
async def submit_assignment(
    course_id: str,
    assignment_id: str,
    submission_text: str = Query(
        ...,
        min_length=3,
        max_length=10000,
        description="Submission text must contain 3-10000 symbols"
    ),
    student_email: str = Depends(get_current_user),
):
    """
    Allows student to submit their assignment.

    Submission text must contains from 3 to 10000 symbols.

    Student role required.

    Student cannot submit already graded assignment.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.submissions.submit_assignment(db_conn, db_cursor, course_id, assignment_id, submission_text, student_email)


@router.get("/get_assignment_submissions", response_model=List[json_classes.Submission], tags=["Submissions"])
async def get_assignment_submissions(course_id: str, assignment_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the list of students submissions of provided assignments.

    Teacher OR Primary Instructor role required.

    Submissions are ordered by submission_time, newest submissions go first.

    Returns the list of submissions (course_id, assignment_id, student_email, student_name, submission_time, last_modification_time, submission_text, grade, comment, gradedby_email, gradedby_name).

    The format of submission_time and last_modification_time is TIME_FORMAT.

    `grade`, `comment`, and `gradedby_email` can be `null` if the assignment was not graded yet.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.submissions.get_assignment_submissions(db_cursor, course_id, assignment_id, user_email)


@router.get("/get_submission", response_model=json_classes.Submission, tags=["Submissions"])
async def get_submission(
    course_id: str,
    assignment_id: str,
    student_email: str,
    user_email: str = Depends(get_current_user),
):
    """
    Get the student submission of assignment by course_id, assignment_id and student_email.

    - Teacher OR Primary Instructor can get all submissions of the course
    - Parent can get the submission of their student
    - Student can get their submissions

    Returns the submission (course_id, assignment_id, student_email, student_name, submission_time, last_modification_time, submission_text, grade, comment, gradedby_email, gradedby_name).

    The format of submission_time and last_modification_time is TIME_FORMAT.

    `grade`, `comment`, and `gradedby_email` can be `null` if the assignment was not graded yet.
    """

    # connection to database
    with get_db() as (db_conn, db_cursor):
        return logic.submissions.get_submission(db_cursor, course_id, assignment_id, student_email, user_email)


@router.post("/create_submission_attachment", response_model=json_classes.SubmissionAttachmentMetadata, tags=["Submissions"])
async def create_submission_attachment(
    course_id: str,
    assignment_id: str,
    student_email: str,
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user),
):
    """
    Attach the provided file to provided course assignment submission.

    Filename should contain no more than 80 symbols.

    Student role required.

    Returns the (course_id, assignment_id, student_email, file_id, filename, upload_time) for the new attachment in case of success.

    The format of upload_time is TIME_FORMAT.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return await logic.submissions.create_submission_attachment(db_conn, db_cursor, storage_db_conn, storage_db_cursor, course_id, assignment_id, student_email, file, user_email)


@router.get("/get_submission_attachments", response_model=List[json_classes.SubmissionAttachmentMetadata], tags=["Submissions"])
async def get_submission_attachments(course_id: str, assignment_id: str, student_email: str, user_email: str = Depends(get_current_user)):
    """
    Get the list of attachments to the course assignment submission by provided course_id, assignment_id, student_email.

    - Teacher OR Primary Instructor can get all submission attachments of the course
    - Parent can get the submission attachments of their student
    - Student can get their submission attachments
    
    Returns list of attachments metadata (course_id, assignment_id, student_email, file_id, filename, upload_time).

    The format of upload_time is TIME_FORMAT.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.submissions.get_submission_attachments(db_cursor, course_id, assignment_id, student_email, user_email)


@router.get("/download_submission_attachment", tags=["Submissions"])
async def download_submission_attachment(course_id: str, assignment_id: str, student_email: str, file_id: str, user_email: str = Depends(get_current_user)):
    """
    Download the attachment to the course assignment submission by provided course_id, assignment_id, student_email, file_id.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return logic.submissions.download_submission_attachment(db_cursor, storage_db_cursor, course_id, assignment_id, student_email, file_id, user_email)
