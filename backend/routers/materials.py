from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File
from auth import get_current_user, get_db, get_storage_db
import json_classes
import logic.materials


router = APIRouter()


@router.post("/create_material", response_model=json_classes.MaterialID, tags=["Materials"])
async def create_material(
    course_id: str,
    title: str = Query(
        ...,
        min_length=3,
        max_length=80,
        pattern=r"^[\p{L}0-9_ ]+$",
        description="Title can contain only letters, digits, spaces, and underscores, 3-80 symbols"
    ),
    description: str = Query(
        ...,
        min_length=3,
        max_length=10000,
        description="Description must contain 3-10000 symbols"
    ),
    user_email: str = Depends(get_current_user),
):
    """
    Create the material with provided title and description in the course with provided course_id.

    Title can contain only letters, digits, spaces, and underscores.

    Title must contains from 3 to 80 symbols.

    Description must contains from 3 to 10000 symbols.

    Teacher OR Primary Instructor role required.

    Returns the (course_id, material_id) for the new material in case of success.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.materials.create_material(db_conn, db_cursor, course_id, title, description, user_email)


@router.post("/remove_material", response_model=json_classes.Success, tags=["Materials"])
async def remove_material(course_id: str, material_id: str, user_email: str = Depends(get_current_user)):
    """
    Remove the material by the provided course_id and material_id.

    Teacher OR Primary Instructor role required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.materials.remove_material(db_conn, db_cursor, course_id, material_id, user_email)


@router.get("/get_material", response_model=json_classes.Material, tags=["Materials"])
async def get_material(course_id: str, material_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the material details by the provided (course_id, material_id).

    Returns course_id, material_id, creation_time, title, description, and email of the author.

    Author can be NULL if the author deleted their account.

    The format of creation time is TIME_FORMAT.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.materials.get_material(db_cursor, course_id, material_id, user_email)


@router.post("/create_material_attachment", response_model=json_classes.MaterialAttachmentMetadata, tags=["Materials"])
async def create_material_attachment(
    course_id: str,
    material_id: str,
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user),
):
    """
    Attach the provided file to provided course material.

    Teacher OR Primary Instructor role required.

    Returns the (course_id, material_id, file_id, filename, upload_time) for the new attachment in case of success.

    The format of upload_time is TIME_FORMAT.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return await logic.materials.create_material_attachment(db_conn, db_cursor, storage_db_conn, storage_db_cursor, course_id, material_id, file, user_email)


@router.get("/get_material_attachments", response_model=List[json_classes.MaterialAttachmentMetadata], tags=["Materials"])
async def get_material_attachments(course_id: str, material_id: str, user_email: str = Depends(get_current_user)):
    """
    Get the list of course material attachments by provided course_id, material_id.

    Returns list of attachments metadata (course_id, material_id, file_id, filename, upload_time).

    The format of upload_time is TIME_FORMAT.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor):
        return logic.materials.get_material_attachments(db_cursor, course_id, material_id, user_email)


@router.get("/download_material_attachment", tags=["Materials"])
async def download_material_attachment(course_id: str, material_id: str, file_id: str, user_email: str = Depends(get_current_user)):
    """
    Download the course material attachment by provided course_id, material_id, file_id.

    Course role (Primary Instructor, Teacher, Student, Parent) required.
    """
    with get_db() as (db_conn, db_cursor), get_storage_db() as (storage_db_conn, storage_db_cursor):
        return logic.materials.download_material_attachment(db_cursor, storage_db_cursor, course_id, material_id, file_id, user_email)
