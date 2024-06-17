from typing import Union
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Header
from new import get_json
import os
import nltk
##
import spacy 
nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_lg")
nltk.download('stopwords')
##
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
