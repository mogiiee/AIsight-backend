from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyC_L7bacXhCfshzd35fJdyH_2prVU7FoeM",
  "authDomain": "ai-sight-471fa.firebaseapp.com",
  "projectId": "ai-sight-471fa",
  "storageBucket": "ai-sight-471fa.appspot.com",
  "messagingSenderId": "90293971390",
  "appId": "1:90293971390:web:04b27715f6059d448831ef",
  "measurementId": "G-14P2V3YKET",
  "serviceAccount": "serviceAccount.json",
  "databaseURL":"https://ai-sight-471fa-default-rtdb.asia-southeast1.firebasedatabase.app/"

}

app = FastAPI(max_request_size=10000000)
firebase = pyrebase.initialize_app(firebaseConfig)
storage= firebase.storage()

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


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    storage.child("picture").put(file)
    return {"filename": file.filename}