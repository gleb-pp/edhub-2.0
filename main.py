from fastapi import FastAPI, HTTPException
from database import db
from datetime import datetime

app = FastAPI()
db_connection = db()
db_cursor = db_connection.cursor()

# courses = [{'course_id': '0', 'name' : 'Intro to Python'}, {'course_id': '1', 'name' : 'Probability & Statistics'}]
# users = [{'email': 'tamaro4ka1973@gmail.com', 'name': 'Tamara Udina'}, {'email': 'i.ivanov@gmail.com', 'name': 'Ivan Ivanov'}]
# user_course = [{'email' : 'tamaro4ka1973@gmail.com', 'course_id' : '0'}, {'email' : 'tamaro4ka1973@gmail.com', 'course_id' : '1'}, {'email' : 'i.ivanov@gmail.com', 'course_id' : '0'}]
# materials = [{'course_id' : '0', 'material_id' : '0', 'creation_date' : '06-07-2025 17:31:25', 'title' : 'Important Announcement', 'description' : 'Attention! The lesson on June 7 is cancelled!'}]

@app.get('/available_courses')
async def available_courses(user_email: str):

    # looking for user with such email
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)", (user_email,))
    user_exists = db_cursor.fetchone()[0]
    if not user_exists:
        raise HTTPException(status_code=400, detail="No user with provided email")
    
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
async def get_course_feed(course_id: str):
    
    # looking for course with such course_id
    db_cursor.execute("SELECT EXISTS(SELECT 1 FROM courses WHERE courseid = %s)", (course_id,))
    course_exists = db_cursor.fetchone()[0]
    if not course_exists:
        raise HTTPException(status_code=400, detail="No course with provided ID")
    
    # finding course feed
    db_cursor.execute("SELECT courseid, matid FROM course_materials WHERE courseid = %s", (course_id,))
    course_feed = db_cursor.fetchall()
    res = [{'course_id': str(mat[0]), 'material_id': mat[1]} for mat in course_feed]
    return res

@app.get('/get_material')
async def get_material(course_id : str, material_id : str):

    db_cursor.execute("""
        SELECT courseid, matid, timeadded, name, description
        FROM course_materials
        WHERE courseid = %s AND matid = %s
    """, (str(course_id), material_id))

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

# @app.post('/create_material')
# async def create_material(course_id, title, description):
#     materials.append({'course_id' : course_id, 'material_id' : 5, 'creation_date' : str(datetime.now()), 'title' : title, 'description' : description})