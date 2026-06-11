# ==========================================================
# FASTAPI STUDY GUIDE: 05. RESPONSE MODELS & STATUS CODES
# ==========================================================

# --- WHY USE RESPONSE MODELS? ---
# When you return data from a database, it often contains internal columns 
# (like password_hash, created_at, or secret_key) that you do NOT want to send to the client.
# By defining a `response_model`, FastAPI will:
# 1. Filter out all data that is not declared in the response model.
# 2. Validate the output data to ensure it matches the model structure.
# 3. Generate correct schemas in the Swagger UI.

# --- HTTP STATUS CODES ---
# HTTP status codes tell the client the result of their request:
# - 200 OK: Request succeeded.
# - 201 Created: Resource created (commonly used for POST).
# - 400 Bad Request: Client sent invalid data or request.
# - 404 Not Found: Resource does not exist.
# - 500 Internal Server Error: Server crashed.

from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr
from typing import Union
import uvicorn

app = FastAPI(title="FastAPI: Response Models & Status Codes")

# ==========================================================
# 1. SCHEMAS: INPUT (CREATE) vs OUTPUT (RESPONSE)
# ==========================================================

# Model representing the client's input (includes password)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # We need the password during user creation

# Model representing the API's response (excludes password for security!)
class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool = True  # We can also add default fields for the output


# Mock database
USERS_DATABASE = {}


# ==========================================================
# 2. CUSTOM STATUS CODE & RESPONSE MODEL
# ==========================================================
# We set:
# - `status_code=status.HTTP_201_CREATED` (resends HTTP 201 instead of default 200).
# - `response_model=UserResponse` (FastAPI automatically strips out the `password` field
#   from whatever we return before sending it to the client).
@app.post(
    "/users", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(user_in: UserCreate):
    # Simulate saving to database
    # (Note: In a real database, we would encrypt/hash this password before saving)
    db_user = {
        "username": user_in.username,
        "email": user_in.email,
        "password": user_in.password + "hashed_secret_salt",  # Hashed in DB
        "is_active": True
    }
    
    # Save user by username
    USERS_DATABASE[user_in.username] = db_user
    
    # We return the ENTIRE db_user dictionary (which contains "password").
    # But because of `response_model=UserResponse`, FastAPI will AUTOMATICALLY 
    # filter out "password" and only return username, email, and is_active!
    return db_user


# ==========================================================
# 3. GET ROUTE WITH RESPONSE MODEL
# ==========================================================
@app.get(
    "/users/{username}", 
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user(username: str):
    if username not in USERS_DATABASE:
        # In the next tutorial, we will study error handling in depth.
        return {"error": "Not found"}  # Just a placeholder for now
        
    return USERS_DATABASE[username]


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 05_response_models_and_status.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try creating a user using the POST `/users` endpoint. Look at the output:
#    It returns HTTP code 201 (Created), and the JSON payload contains only `username`, 
#    `email`, and `is_active`. The `password` key is completely hidden!

if __name__ == "__main__":
    uvicorn.run("05_response_models_and_status:app", host="127.0.0.1", port=8000, reload=True)
