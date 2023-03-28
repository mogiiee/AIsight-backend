from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
from fastapi.encoders import jsonable_encoder
import firebase_admin
from firebase_admin import credentials, storage
from . import ops,responses,database


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
  "databaseURL":"gs://ai-sight-471fa.appspot.com/all_screenshots/"
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


@app.post("/signup/user", tags=["user"])
async def signup(signup_details: Request):
    infoDict = await signup_details.json()
    print(infoDict)
    infoDict = dict(infoDict)
    print(infoDict)
    # Checking if email already exists
    email_count = database.user_collection.count_documents(
        {"email": infoDict["email"]}
    )
    if email_count > 0:
        return responses.response(False, "duplicated user, email already in use", None)
    # Insert new user
    encoded_password = ops.hash_password(str(infoDict["password"]))
    infoDict['password'] = encoded_password
    print(infoDict)
    json_signup_details = jsonable_encoder(infoDict)
    await ops.inserter(json_signup_details)
    return responses.response(True, "inserted", 
        infoDict
    )


@app.post("/login", tags=["login"])
async def login(login_deets:Request):
    infoDict = await login_deets.json()
    print(infoDict)
    email = infoDict['email']
    password = infoDict['password']
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in", {"email": email})
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")