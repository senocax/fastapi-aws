from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"welcome":"welcome to fastAPI"}

@app.get('/posts')
def post():
    return "posts"



