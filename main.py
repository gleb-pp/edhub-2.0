from fastapi import FastAPI, HTTPException
app = FastAPI()

lst = ['привет', 'тимур', 'как', 'твои', 'дела', 'hello', 'world', 'pip', 'install', 'python']

# @app.get('/')
# async def landing():
#     return {"This is": "the landing page!",
#             "JSON by": "Timur",
#             "recommended": [
#                 "/hello",
#                 "/goodbye?times=5&excl=3"
#             ]}

# @app.get("/hello")
# async def hello():
#     return {'Hello': 'World',
#             'recommended': "Go touch grass"}

@app.get('/get')
async def goodbye(index):
    ind = int(index)
    assert ind >= 0 and ind <= 9 and float(index) == int(index)
    return {'lst_num': lst[ind]}

@app.get('/len')
async def lenn():
    return len(lst)

@app.post("/register")
async def register(email: str, password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    if email in users_db:
        raise HTTPException(status_code=400, detail="Email already exists")
    users_db[email] = {"password": password}  # Хэшируйте пароль на практике!
    return {"message": "User created"}