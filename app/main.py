from fastapi import FastAPI, File, HTTPException, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
import pyrebase
from fastapi.encoders import jsonable_encoder
import firebase_admin
from firebase_admin import credentials, storage
from . import ops,responses,database
import json
from datetime import datetime


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
async def create_upload_file(file: UploadFile = File(...), text_field: str = Form(...)):
    file_content = await file.read()  # Read the file's content
    file_size = len(file_content)  # Determine the file's size
    bucket = storage.bucket
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file_content, content_type='image/jpeg')
    blob.make_public()
    text_dict = json.loads(text_field)
    email = text_dict["email"]
    timern = datetime.now()

    url = blob.public_url
    full_profile = await ops.find_user_email(email)
    user_pictures = full_profile["user-pictures"]
    url_dict = {
        "picture link": url,
        "date and time": timern
    }

    user_pictures.append(url_dict)
    ops.user_picture_updater(text_dict["email"], user_pictures)
    return responses.response(True, "course created!", url_dict)




@app.post("/signup/user", tags=["user"])
async def signup(signup_details: Request):
    infoDict = await signup_details.json()
    infoDict['user-pictures'] = []
    infoDict['results'] = []
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
    phone_num = infoDict['phone_num']
    gender = infoDict['gender']
    height = infoDict['height']
    weight = infoDict['weight']
    # Verify credentials
    if await ops.verify_credentials(email, password):
        return responses.response(True, "logged in",
         {"email": email,
         "gender": gender,
         "phone_num": phone_num,
         "height": height,
         "weight": weight
        
        })
    else:
        raise HTTPException(401, "unauthorised login or email is wrong")


@app.get("/find-user")
async def find_user_email(user_deets:Request):
    infor_dict = await user_deets.json()
    infor_dict = dict(infor_dict)
    email = infor_dict["email"]
    user = database.user_collection.find_one({"email": email})
    print(user)
    if not user:
        return responses.response(False, "does not exist", email)
    del user["_id"]
    return user
    
