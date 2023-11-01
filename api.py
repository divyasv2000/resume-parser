from typing import Union
from new import get_json
import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Naruto"}


@app.post("/upload")
def upload_file(file: UploadFile = File()):
    # try:
    contents = file.file.read()
    with open("uploads/"+file.filename, 'wb') as f:
        f.write(contents)
    data = get_json("uploads", file.filename)
    os.remove("uploads/"+file.filename)
    file.file.close()
    return data