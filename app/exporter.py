import os
from dotenv import load_dotenv

load_dotenv()

firebase_config = os.environ.get("firebaseConfig")

real_cluster = os.environ.get("CLUSTER")
db_name = os.environ.get("DB")
collection = os.environ.get("USER_COLLECTION")