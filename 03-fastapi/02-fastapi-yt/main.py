from fastapi import FastAPI

app = FastAPI()

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Learning FastAPI website"}