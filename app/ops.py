from . import database, responses
import bcrypt


async def find_user_email(email):
    user = database.user_collection.find_one({"email": email})
    if not user:
        return responses.response(False, "does not exist", email)
    return user


async def email_finder(email):
    existing_user = database.user_collection.find_one({"email": email})
    if existing_user is not None:
        return False
    else:
        return True


async def check_duplicate_email(email: str):
    existing_user = await database.user_collection.find_one({"email": email})
    return existing_user is not None


def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Return the hashed password as a string
    return hashed_password.decode("utf-8")


async def verify_credentials(username: str, password: str) -> bool:
    user = await find_user_email(username)
    if user is None:
        return False
    hashed_password = user["password"].encode("utf-8")
    is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return is_valid_password


async def inserter(metadata: dict):
    database.user_collection.insert_one(metadata)
    return responses.response(True, "inserted successfully", metadata)


def user_picture_updater(WrongValue, CorrectValue):
    print(CorrectValue)
    print(WrongValue)

    database.user_collection.update_one(
        {"email": WrongValue}, {"$set": {"user-pictures": CorrectValue}}, upsert=True
    )
