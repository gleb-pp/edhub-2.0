from fastapi import FastAPI, HTTPException
import psycopg2

def db():
    conn = psycopg2.connect(
        dbname="edhub",
        user="postgres",
        password="12345678",
        host="db",
        port="5432"
    )
    return conn

app = FastAPI()
db_connection = db()
db_cursor = db_connection.cursor()

# checking whether the user exists in our LMS
def check_user_exists(user_email: str):
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)", (user_email,))
    user_exists = db_cursor.fetchone()[0]
    if not user_exists:
        raise HTTPException(status_code=404, detail="No user with provided email")
    return True

# checking whether the course exists in our LMS
def check_course_exists(course_id: str):
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM courses WHERE courseid = %s)", (course_id,))
    course_exists = db_cursor.fetchone()[0]
    if not course_exists:
        raise HTTPException(status_code=404, detail="No course with provided ID")
    return True

# checking whether the user has access to course in our LMS
def check_course_access(user_email: str, course_id: str, is_teacher : bool = False, is_student : bool = False, is_parent : bool = False):

    if is_teacher:
        db_cursor.execute("SELECT EXISTS(SELECT 1 FROM teaches WHERE email = %s AND courseid = %s)", (user_email, course_id))
        has_access = db_cursor.fetchone()[0]
        if not has_access:
            raise HTTPException(status_code=403, detail="User is not teacher at this course")
        return True
    
    elif is_student:
        db_cursor.execute("SELECT EXISTS(SELECT 1 FROM student_at WHERE email = %s AND courseid = %s)", (user_email, course_id))
        has_access = db_cursor.fetchone()[0]
        if not has_access:
            raise HTTPException(status_code=403, detail="User is not student at this course")
        return True

    elif is_parent:
        db_cursor.execute("SELECT EXISTS(SELECT 1 FROM parent_of_at_course WHERE parentemail = %s AND courseid = %s)", (user_email, course_id))
        has_access = db_cursor.fetchone()[0]
        if not has_access:
            raise HTTPException(status_code=403, detail="User is not parent at this course")
        return True

    else:
        db_cursor.execute("""
            SELECT EXISTS(
                SELECT 1 FROM teaches WHERE email = %s AND courseid = %s
                UNION
                SELECT 1 FROM student_at WHERE email = %s AND courseid = %s
                UNION
                SELECT 1 FROM parent_of_at_course WHERE parentemail = %s AND courseid = %s
            )
        """, (user_email, course_id, user_email, course_id, user_email, course_id))
        has_access = db_cursor.fetchone()[0]
        if not has_access:
            raise HTTPException(status_code=403, detail="User does not have access to this course")
        return True

@app.get('/available_courses')
async def available_courses(user_email: str):

    check_user_exists(user_email)
    
    # finding available courses
    db_cursor.execute("""
        SELECT courseid AS cid FROM teaches WHERE email = %s
        UNION
        SELECT courseid AS cid FROM student_at WHERE email = %s
        UNION
        SELECT courseid AS cid FROM parent_of_at_course WHERE parentemail = %s
    """, (user_email, user_email, user_email))
    result = [{'course_id': row[0]} for row in db_cursor.fetchall()]
    return result

@app.get('/get_course_feed')
async def get_course_feed(course_id: str, user_email: str):

    check_user_exists(user_email)
    check_course_exists(course_id)
    check_course_access(user_email=user_email, course_id=course_id)
    
    # finding course feed
    db_cursor.execute("SELECT courseid, matid FROM course_materials WHERE courseid = %s", (course_id,))
    course_feed = db_cursor.fetchall()
    res = [{'course_id': str(mat[0]), 'material_id': mat[1]} for mat in course_feed]
    return res

@app.get('/get_material')
async def get_material(course_id : str, material_id : str, user_email: str):

    check_user_exists(user_email)
    check_course_exists(course_id)
    check_course_access(user_email=user_email, course_id=course_id)

    db_cursor.execute("""
        SELECT courseid, matid, timeadded, name, description
        FROM course_materials
        WHERE courseid = %s AND matid = %s
    """, (course_id, material_id))

    material = db_cursor.fetchone()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    res = [{
        "course_id": str(material[0]),
        "material_id": material[1],
        "creation_date": material[2].strftime("%m-%d-%Y %H:%M:%S"),
        "title": material[3],
        "description": material[4]
    }]
    return res

@app.post('/create_material')
async def create_material(course_id : str, title : str, description : str, user_email: str):

    check_user_exists(user_email)
    check_course_exists(course_id)
    check_course_access(user_email=user_email, course_id=course_id, is_teacher=True)
    
    db_cursor.execute(
        "INSERT INTO course_materials (courseid, name, description, timeadded) VALUES (%s, %s, %s, now()) RETURNING matid",
        (course_id, title, description)
    )
    material_id = db_cursor.fetchone()[0]
    db_connection.commit()
    return {"material_id": material_id}

@app.post('/create_course')
async def create_course(title : str, user_email : str):

    check_user_exists(user_email)

    # create course
    db_cursor.execute(
        "INSERT INTO courses (courseid, name, timecreated) VALUES (gen_random_uuid(), %s, now()) RETURNING courseid",
        (title,)
    )
    course_id = db_cursor.fetchone()[0]
    db_connection.commit()

    # add teacher
    db_cursor.execute(
        "INSERT INTO teaches (email, courseid) VALUES (%s, %s)",
        (user_email, course_id)
    )
    db_connection.commit()

    return {"course_id": course_id}

@app.post('/invite_student')
async def invite_student(course_id : str, teacher_email : str, student_email : str):
    
    check_user_exists(teacher_email)
    check_user_exists(student_email)
    check_course_exists(course_id)
    check_course_access(user_email=teacher_email, course_id=course_id, is_teacher=True)

    # invite student
    db_cursor.execute(
        "INSERT INTO student_at (email, courseid) VALUES (%s, %s)",
        (student_email, course_id)
    )
    db_connection.commit()

    return {"course_id": course_id, 'student_email' : student_email, 'success' : True}

@app.post('/invite_parent')
async def invite_parent(course_id : str, teacher_email : str, student_email : str, parent_email : str):

    check_user_exists(teacher_email)
    check_user_exists(student_email)
    check_user_exists(parent_email)
    check_course_exists(course_id)
    check_course_access(user_email=teacher_email, course_id=course_id, is_teacher=True)
    check_course_access(user_email=student_email, course_id=course_id, is_student=True)

    # invite parent
    db_cursor.execute(
        "INSERT INTO parent_of_at_course (parentemail, studentemail, courseid) VALUES (%s, %s, %s)",
        (parent_email, student_email, course_id)
    )
    db_connection.commit()

    return {"course_id": course_id, 'student_email' : student_email, 'parent_email' : parent_email, 'success' : True}

# TODO : авторизация
# @app.post('/create_user')
# async def create_user(name : str):
#     return 0