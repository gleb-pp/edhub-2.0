from fastapi import HTTPException


# checking whether the user exists in our LMS
def check_user_exists(db_cursor, user_email: str) -> bool:
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)", (user_email,))
    user_exists = db_cursor.fetchone()[0]
    return user_exists

def assert_user_exists(db_cursor, user_email: str) -> None:
    user_exists = check_user_exists(db_cursor, user_email)
    if not user_exists:
        raise HTTPException(status_code=404, detail="No user with provided email")


# checking whether the course exists in our LMS
def check_course_exists(db_cursor, course_id: str) -> bool:
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM courses WHERE courseid = %s)", (course_id,))
    course_exists = db_cursor.fetchone()[0]
    return course_exists

def assert_course_exists(db_cursor, course_id: str) -> None:
    course_exists = check_course_exists(db_cursor, course_id)
    if not course_exists:
        raise HTTPException(status_code=404, detail="No course with provided ID")


# checking whether the material exists in the course
def check_material_exists(db_cursor, course_id: str, material_id: str) -> bool:
    try:
        material_id = int(material_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Material ID should be integer") from exc

    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM course_materials WHERE courseid = %s AND matid = %s)", (course_id, material_id)
    )
    material_exists = db_cursor.fetchone()[0]
    return material_exists

def assert_material_exists(db_cursor, course_id: str, material_id: str) -> None:
    material_exists = check_material_exists(db_cursor, course_id, material_id)
    if not material_exists:
        raise HTTPException(status_code=404, detail="No material with provided ID in this course")


# checking whether the assignment exists in the course
def check_assignment_exists(db_cursor, course_id: str, assignment_id: str) -> bool:
    try:
        assignment_id = int(assignment_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Assignment ID should be integer") from exc

    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM course_assignments WHERE courseid = %s AND assid = %s)",
        (course_id, assignment_id),
    )
    assignment_exists = db_cursor.fetchone()[0]
    return assignment_exists

def assert_assignment_exists(db_cursor, course_id: str, assignment_id: str) -> None:
    assignment_exists = check_assignment_exists(db_cursor, course_id, assignment_id)
    if not assignment_exists:
        raise HTTPException(status_code=404, detail="No assignment with provided ID in this course")


# checking whether the user has general access to the course,
def check_course_access(db_cursor, user_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, user_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM courses WHERE instructor = %s AND courseid = %s
            UNION
            SELECT 1 FROM teaches WHERE email = %s AND courseid = %s
            UNION
            SELECT 1 FROM student_at WHERE email = %s AND courseid = %s
            UNION
            SELECT 1 FROM parent_of_at_course WHERE parentemail = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (user_email, course_id, user_email, course_id, user_email, course_id, user_email, course_id, user_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_course_access(db_cursor, user_email: str, course_id: str) -> None:
    has_access = check_course_access(db_cursor, user_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User does not have access to this course")


# checking whether the user has teacher access to the course
def check_teacher_access(db_cursor, teacher_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, teacher_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM courses WHERE instructor = %s AND courseid = %s
            UNION
            SELECT 1 FROM teaches WHERE email = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (teacher_email, course_id, teacher_email, course_id, teacher_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_teacher_access(db_cursor, teacher_email: str, course_id: str) -> None:
    has_access = check_teacher_access(db_cursor, teacher_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no teacher rights in this course")


# checking whether the user has primary instructor access to the course
def check_instructor_access(db_cursor, user_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, user_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM courses WHERE instructor = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (user_email, course_id, user_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_instructor_access(db_cursor, user_email: str, course_id: str) -> None:
    has_access = check_instructor_access(db_cursor, user_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no primary instructor rights in this course")


# checking whether the user has student access to the course
def check_student_access(db_cursor, student_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, student_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM student_at WHERE email = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (student_email, course_id, student_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_student_access(db_cursor, student_email: str, course_id: str) -> None:
    has_access = check_student_access(db_cursor, student_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no student rights in this course")


# checking whether the user has parent access to the course
def check_parent_access(db_cursor, parent_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, parent_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM parent_of_at_course WHERE parentemail = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (parent_email, course_id, parent_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_parent_access(db_cursor, parent_email: str, course_id: str) -> None:
    has_access = check_parent_access(db_cursor, parent_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no parental access in this course")


# checking whether the user has parent access with the student in the course
def check_parent_student_access(db_cursor, parent_email: str, student_email: str, course_id: str) -> bool:
    assert_user_exists(db_cursor, parent_email)
    assert_user_exists(db_cursor, student_email)
    assert_course_exists(db_cursor, course_id)
    db_cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1 FROM parent_of_at_course WHERE parentemail = %s AND studentemail = %s AND courseid = %s
            UNION
            SELECT 1 FROM users WHERE email = %s AND isadmin
        )
    """,
        (parent_email, student_email, course_id, parent_email),
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_parent_student_access(db_cursor, parent_email: str, student_email: str, course_id: str) -> None:
    has_access = check_parent_student_access(db_cursor, parent_email, student_email, course_id)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no parental access to this student's course")


# checking if the submission exists
def check_submission_exists(db_cursor, course_id: str, assignment_id: str, student_email: str) -> bool:
    assert_assignment_exists(db_cursor, course_id, assignment_id)

    # check if the student is enrolled to course
    if not check_student_access(db_cursor, student_email, course_id):
        raise HTTPException(status_code=403, detail="Provided user is not a student at this course")

    db_cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM course_assignments_submissions WHERE courseid = %s AND assid = %s AND email = %s)",
        (course_id, int(assignment_id), student_email),
    )
    submitted = db_cursor.fetchone()[0]
    return submitted

def assert_submission_exists(db_cursor, course_id: str, assignment_id: str, student_email: str) -> None:
    submitted = check_submission_exists(db_cursor, course_id, assignment_id, student_email)
    if not submitted:
        raise HTTPException(status_code=404, detail="The given student has not made a submission to this assignment")


# checking whether the user has admin access
def check_admin_access(db_cursor, user_email: str) -> bool:
    assert_user_exists(db_cursor, user_email)
    db_cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s AND isadmin)", (user_email,)
    )
    has_access = db_cursor.fetchone()[0]
    return has_access

def assert_admin_access(db_cursor, user_email: str) -> None:
    has_access = check_admin_access(db_cursor, user_email)
    if not has_access:
        raise HTTPException(status_code=403, detail="User has no admin rights")
