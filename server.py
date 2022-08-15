from re import U
import boto3
import psycopg2
from fastapi import FastAPI, UploadFile
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

S3_BUCKET_NAME="store image"

class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: bool

@app.get('/')
async def read_root():
    return {"welcome":"welcome to fastAPI"}

@app.get('/photos', response_model= List[PhotoModel])
async def get_all_photos(PhotoModel):
    """ Get all photos stored in database"""

    conn = psycopg2.connect(
        host="0.0.0.0",
        database="exampledb",
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
        image_url= row[2],
        is_deleted= row[3]
        )
    cur.close()
    conn.close()
    return photoModel

@app.post('/photos')
async def upload(file: UploadFile):
    """upload file into S3"""

    s3= boto3.resource('s3')
    bucket= s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL":"public-read"})
    upload_file_url= f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    #store url
    conn = psycopg2.connect(
        database="imagedb",
        host="0.0.0.0",
        user="docker",
        password="docker"
    )

    cur= conn.cursor()
    f"INSERT INTO photo (photo_name, photo_url) VALUES ('{file.filename}', '{upload_file_url}' )"
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, reload=True)




