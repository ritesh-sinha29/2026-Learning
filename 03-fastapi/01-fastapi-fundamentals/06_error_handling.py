# ==========================================================
# FASTAPI STUDY GUIDE: 06. ERROR HANDLING
# ==========================================================

# --- WHAT IS ERROR HANDLING? ---
# When something goes wrong (e.g., resource not found, user unauthorized, database timeout),
# your API should return a proper HTTP error code along with a descriptive error message.
#
# FastAPI provides:
# 1. `HTTPException`: A special exception class you can raise anywhere to stop request processing
#    and immediately send an error response to the client.
# 2. Custom Exception Handlers: Global hooks to catch custom Python errors and format them nicely.

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="FastAPI: Error Handling")

# Mock database
ITEMS_DATABASE = {
    "sword": {"name": "Excalibur", "type": "Weapon"},
    "shield": {"name": "Aegis", "type": "Armor"}
}

# ==========================================================
# 1. RAISING HTTP_EXCEPTION (THE COMMON WAY)
# ==========================================================
# If an item doesn't exist, we raise `HTTPException` with status code 404 (Not Found).
# If it does exist, we return it.
@app.get("/items/{item_key}")
async def get_item(item_key: str):
    if item_key not in ITEMS_DATABASE:
        # Raising this stops execution immediately and returns the error to the client
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item '{item_key}' does not exist in our inventory."
        )
    return ITEMS_DATABASE[item_key]


# ==========================================================
# 2. DEFINING A CUSTOM EXCEPTION CLASS
# ==========================================================
# Sometimes you want to raise your own Python exceptions throughout your business logic,
# without polluting your code with HTTP status codes.
# Let's create a custom exception representing a database outage.
class DatabaseConnectionError(Exception):
    def __init__(self, db_name: str):
        self.db_name = db_name


# ==========================================================
# 3. REGISTERING A GLOBAL EXCEPTION HANDLER
# ==========================================================
# This decorator tells FastAPI: "If any function in this app raises DatabaseConnectionError,
# catch it, pass it here, and return this JSONResponse instead of crashing the server."
@app.exception_handler(DatabaseConnectionError)
async def db_connection_exception_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error_type": "DATABASE_ERROR",
            "message": f"Could not connect to database: '{exc.db_name}'. Please try again later.",
            "documentation_url": "http://127.0.0.1:8000/docs"
        }
    )


# A route that simulates a database failure and raises our custom exception
@app.get("/simulate-db-error")
async def simulate_db_error():
    # Simulate database connection failure
    raise DatabaseConnectionError(db_name="Production_PostgreSQL")


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 06_error_handling.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Test `/items/sword` (returns weapon details).
# 4. Test `/items/potion` (returns 404 error and message in JSON: "detail": "...")
# 5. Test `/simulate-db-error` (returns 503 Service Unavailable, and our custom structured JSON error output).

if __name__ == "__main__":
    uvicorn.run("06_error_handling:app", host="127.0.0.1", port=8000, reload=True)
