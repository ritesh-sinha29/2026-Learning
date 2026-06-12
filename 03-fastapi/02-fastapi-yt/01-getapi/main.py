from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Learning FastAPI website"}


# About Route

@app.get("/about")
def about():
    return{"message": "This is a simple FastAPI application."}


# Users route 

@app.get ("/users")
def users():
    return {
        "users":[
            {"user_id":1, "name":"John Doe"},
            {"user_id":2, "name":"Jane Doe"},
            {"user_id":3, "name":"Bob Smith"},
            {"user_id":4, "name":"Alice Johnson"},
            {"user_id":5, "name":"Mike Williams"}
        ]
    }