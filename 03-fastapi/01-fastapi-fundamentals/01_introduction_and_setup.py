# ==========================================================
# FASTAPI STUDY GUIDE: 01. INTRODUCTION & SETUP
# ==========================================================

# --- WHAT IS AN API? ---
# API stands for Application Programming Interface.
# It acts as a bridge that allows different software applications to talk to each other.
# Think of it like a waiter in a restaurant:
# 1. You (the client/frontend) look at the menu and order food (Request).
# 2. The waiter (the API) takes your order to the kitchen (database/server logic).
# 3. The kitchen cooks the food and gives it to the waiter.
# 4. The waiter brings the food back to your table (Response).

# --- WHAT IS FASTAPI? ---
# FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.
# Key benefits:
# * Extremely Fast: On par with NodeJS and Go (thanks to Starlette and Uvicorn).
# * Automatic Docs: Generates interactive API documentation (Swagger UI) automatically!
# * Type Hints: Uses standard Python type hints for automatic data validation and editor autocompletion.
# * Easy: Designed to be easy to learn and write.

# --- PRE-REQUISITES (HOW TO INSTALL) ---
# To run this code, you need to install two libraries:
# 1. fastapi - The framework itself.
# 2. uvicorn - An ASGI (Asynchronous Server Gateway Interface) web server that runs your code.
#
# Run this command in your terminal:
#   pip install fastapi uvicorn

import uvicorn
from fastapi import FastAPI

# 1. CREATE AN APP INSTANCE
# This `app` object is the main entry point of your web application.
# It manages all routing, configuration, and middleware.
app = FastAPI(
    title="FastAPI Learning Journey",
    description="Starting from absolute scratch!",
    version="1.0.0"
)

# 2. DEFINE A ROUTE (PATH OPERATION)
# @app.get("/") is a decorator. It tells FastAPI: "If someone visits the root URL (/)
# using the HTTP GET method, run the function below."
#
# Common HTTP Methods:
# - GET: Fetch data (read only)
# - POST: Create new data
# - PUT: Update existing data
# - DELETE: Remove data
@app.get("/")
async def root():
    # Inside FastAPI, we write standard or async functions.
    # FastAPI automatically converts dictionaries, lists, and strings into JSON format!
    return {
        "message": "Welcome to FastAPI, Ritesh!",
        "status": "Learning from scratch",
        "next_step": "Go to http://127.0.0.1:8000/docs in your browser!"
    }

# 3. ANOTHER ROUTE (ANOTHER ENDPOINT)
@app.get("/about")
async def about():
    return {
        "topic": "FastAPI Introduction",
        "difficulty": "Beginner",
        "description": "FastAPI is great because it has automatic validation!"
    }


# --- HOW TO RUN THIS APPLICATION ---
# You can run this file in two ways:
#
# Method A: From the Terminal (Recommended for development)
#   Open terminal in this directory and type:
#     uvicorn 01_introduction_and_setup:app --reload
#   * '01_introduction_and_setup' is the name of this Python file (without .py)
#   * 'app' is the FastAPI instance we created inside this file
#   * '--reload' makes the server restart automatically whenever you change the code!
#
# Method B: Direct Python Execution (Runs this main block)
#   Simply run this script directly with Python:
#     python 01_introduction_and_setup.py
#   This starts the server programmatically.

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("Visit Swagger Documentation at: http://127.0.0.1:8000/docs")
    print("Visit ReDoc Documentation at: http://127.0.0.1:8000/redoc")
    # Run the uvicorn server programmatically
    # host "127.0.0.1" is localhost, port "8000" is the default web port for FastAPI
    uvicorn.run("01_introduction_and_setup:app", host="127.0.0.1", port=8000, reload=True)
