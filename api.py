from typing import Union
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Header
from new import get_json
import os
import urllib.request
from pydantic import BaseModel

class S3Url(BaseModel):
    url: str

app = FastAPI()

SECRET_API_KEY = "resumeapi@2023"

def api_key_dependency(api_key: str = Header(...)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

@app.post("/upload")
def upload_file(file: UploadFile = File(), api_key: str = Header(..., convert_underscores=False, description="API Key")):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    
    contents = file.file.read()
    with open("uploads/"+file.filename, 'wb') as f:
        f.write(contents)
    data = get_json("uploads", file.filename)
    os.remove("uploads/"+file.filename)
    file.file.close()
    return data

@app.post("/s3file")
def s3File(s3url: S3Url):
    urllib.request.urlretrieve(s3url.url, "uploads/resume.pdf")
    data = get_json("uploads", "resume.pdf")
    os.remove("uploads/resume.pdf")
    return data