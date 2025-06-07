from fastapi import FastAPI, HTTPException
app = FastAPI()

courses = [{'course_id': 0, 'name' : 'Intro to Python'}, {'course_id': 1, 'name' : 'Probability & Statistics'}]
users = [{'email': 'tamaro4ka1973@gmail.com', 'name': 'Tamara Udina'}, {'email': 'i.ivanov@gmail.com', 'name': 'Ivan Ivanov'}]
user_course = [{'email' : 'tamaro4ka1973@gmail.com', 'course_id' : 0}, {'email' : 'tamaro4ka1973@gmail.com', 'course_id' : 1}, {'email' : 'i.ivanov@gmail.com', 'course_id' : 0}]
materials = [{'course_id' : 0, 'material_id' : 0, 'title' : 'Important Announcement', 'describtion' : 'Attention! The lesson on June 7 is cancelled!'}]

@app.get('/available_courses')
async def available_courses(user_email):

    # looking for user with such email
    found = False
    for user in users:
        if user['email'] == user_email:
            found = True
    if not found:
        raise HTTPException(status_code=400, detail="No user with provided email")
    
    # finding available courses
    res = [uc['course_id'] for uc in user_course if uc['email'] == user_email]
    return res

@app.get('/get_course_feed')
async def get_course_feed(course_id):
    
    # looking for course with such course_id
    found = False
    for course in courses:
        if course['course_id'] == course_id:
            found = True
    if not found:
        raise HTTPException(status_code=400, detail="No course with provided ID")
    
    # finding course feed
    res = [(mat['course_id'], mat['material_id']) for mat in materials if mat['course_id'] == course_id]
    return res

@app.get('/get_course_feed')
async def get_course_feed(course_id):
    