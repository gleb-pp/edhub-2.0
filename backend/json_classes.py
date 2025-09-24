from typing import Optional, List
from pydantic import BaseModel

class Success(BaseModel):
    success: bool


class User(BaseModel):
    email: str
    name: str


class CourseRole(BaseModel):
    is_instructor: bool
    is_teacher: bool
    is_student: bool
    is_parent: bool
    is_admin: bool


class CourseID(BaseModel):
    course_id: str


class Course(CourseID):
    title: str
    instructor: str
    organization: Optional[str]
    creation_time: str


class CoursePost(BaseModel):
    course_id: str
    post_id: int
    type: str
    timeadded: str
    author: Optional[str]


class MaterialID(BaseModel):
    course_id: str
    material_id: int


class Material(MaterialID):
    creation_time: str
    title: str
    description: str
    author: Optional[str]


class MaterialAttachmentMetadata(BaseModel):
    course_id: str
    material_id: int
    file_id: str
    filename: str
    upload_time: str


class AssignmentID(BaseModel):
    course_id: str
    assignment_id: int


class Assignment(AssignmentID):
    creation_time: str
    title: str
    description: str
    author: Optional[str]


class AssignmentAttachmentMetadata(BaseModel):
    course_id: str
    assignment_id: int
    file_id: str
    filename: str
    upload_time: str


class Submission(BaseModel):
    course_id: str
    assignment_id: int
    student_email: str
    student_name: str
    submission_time: str
    last_modification_time: str
    submission_text: str
    grade: Optional[int]
    comment: Optional[str]
    gradedby_email: Optional[str]
    gradedby_name: Optional[str]


class SubmissionAttachmentMetadata(BaseModel):
    course_id: str
    assignment_id: int
    student_email: str
    file_id: str
    filename: str
    upload_time: str


class Account(BaseModel):
    email: str
    access_token: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserNewPassword(BaseModel):
    email: str
    password: str
    new_password: str

class StudentsGrades(BaseModel):
    name: str
    email: str
    grades: List[Optional[int]]

class AssignmentGrade(BaseModel):
    assignment_name: str
    assignment_id: int
    grade: Optional[int]
    comment: Optional[str]
    grader_name: Optional[str]
    grader_email: Optional[str]
