import boto3
import psycopg2
from fastapi import FastAPI, UploadFile
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: bool

@app.get('/')
async def read_root():
    return {"welcome":"welcome to fastAPI"}

@app.get('/photos')
def get_all_photos(PhotoModel):
    conn = psycopg2.connect(
        hast="0.0.0.0",
        database="photodb",
        user="docker",
        password="docker"
    )
    #connect to database
    cur= conn.cursor()
    cur.execute("SELECT * FROM photo order BY id DESC")
    rows= cur.fetchall()
    photoModel= []
    for row in rows:
        photoModel.append(
        id= row[0],
        name= row[1],
        url= row[2],
        is_deleted= row[3]
        )
    cur.close()
    conn.close()
    return photoModel


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, reload=True)




