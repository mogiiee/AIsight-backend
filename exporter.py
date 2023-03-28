import os
from dotenv import load_dotenv

load_dotenv()

firebase_config = os.environ.get("firebaseConfig")

cluster = os.environ.get("CLUSTER")
database = os.environ.get("DB")
collection = os.environ.get("USER_COLLECTION")