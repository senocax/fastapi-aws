import boto3
import psycopg2
from fastapi import FastAPI, UploadFile
import uvicorn

app = FastAPI(debug=True)

@app.get('/')
def read_root():
    return {"welcome":"welcome to fastAPI"}

@app.get('/posts')
def post():
    return "posts"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)




