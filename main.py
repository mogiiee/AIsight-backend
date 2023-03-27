from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
import io
import firebase_admin
from firebase_admin import credentials, storage

mainAccount=  "serviceAccount.json"


firebaseConfig = {
  "apiKey": "AIzaSyC_L7bacXhCfshzd35fJdyH_2prVU7FoeM",
  "authDomain": "ai-sight-471fa.firebaseapp.com",
  "projectId": "ai-sight-471fa",
  "storageBucket": "ai-sight-471fa.appspot.com",
  "messagingSenderId": "90293971390",
  "appId": "1:90293971390:web:04b27715f6059d448831ef",
  "measurementId": "G-14P2V3YKET",
  "serviceAccount": mainAccount,
  "databaseURL":"gs://ai-sight-471fa.appspot.com"
}

app = FastAPI()

firebase = pyrebase.initialize_app(firebaseConfig)
storage= firebase.storage()
cred = credentials.Certificate("serviceAccount.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://ai-sight-471fa.appspot.com'
})

origins = ["*"]



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],

)

@app.get("/")
def root():
    return{
        "message": "hello world"
    }


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     storage.child("picture").put(file)
#     return {"filename": file.filename}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_content = await file.read()  # Read the file's content
    file_size = len(file_content)  # Determine the file's size
    bucket = storage.bucket
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file_content, content_type='image/jpeg')
    blob.make_public()
    
    # Get the download URL of the uploaded file
    url = blob.public_url
    
    # Return the download URL to the client
    return {'url': url}