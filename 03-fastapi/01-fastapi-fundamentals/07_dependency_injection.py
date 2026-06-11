# ==========================================================
# FASTAPI STUDY GUIDE: 07. DEPENDENCY INJECTION (DI)
# ==========================================================

# --- WHAT IS DEPENDENCY INJECTION? ---
# Dependency injection is a design pattern where a function or object is given its 
# dependencies (things it needs to work) rather than creating them inside itself.
#
# In FastAPI, we use `Depends` to declare dependencies.
# Why is this useful?
# 1. Code Reuse: Write a utility once (like database connection or security checking) and share it.
# 2. Automatically Handles Parameters: Dependencies can read request headers, query params, etc.
# 3. Easy Testing: You can easily "override" dependencies when writing automated tests.

from fastapi import FastAPI, Depends, Header, HTTPException, status
from typing import Union
import uvicorn

app = FastAPI(title="FastAPI: Dependency Injection")

# ==========================================================
# 1. SIMPLE FUNCTION DEPENDENCY (Common Query Parameters)
# ==========================================================
# A reusable function that parses pagination parameters.
async def pagination_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

# To use it, we declare a parameter with type hints and call Depends()
@app.get("/items")
async def read_items(params: dict = Depends(pagination_parameters)):
    # `params` contains the dictionary returned by `pagination_parameters`
    return {
        "message": "Fetching items...",
        "filters_applied": params
    }

@app.get("/users")
async def read_users(params: dict = Depends(pagination_parameters)):
    return {
        "message": "Fetching users...",
        "filters_applied": params
    }


# ==========================================================
# 2. SUB-DEPENDENCY & SECURITY CHECKING
# ==========================================================
# Dependencies can depend on OTHER dependencies.
# Let's create an authentication check that looks for a "X-API-Key" header.

async def verify_api_key(x_api_key: str = Header(..., description="API Access Token")):
    # In a real app, you would check this key in a database.
    if x_api_key != "secret-token-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return x_api_key

# Now, let's create a dependency that depends on `verify_api_key`
async def get_admin_user(api_key: str = Depends(verify_api_key)):
    # This dependency only runs IF verify_api_key succeeds.
    # We can perform additional admin checks here.
    return {"username": "ritesh_admin", "api_key_used": api_key}

# An endpoint that is fully protected by dependencies!
@app.get("/admin/dashboard")
async def admin_dashboard(admin: dict = Depends(get_admin_user)):
    return {
        "message": f"Welcome, {admin['username']}! You have access to the secret admin dashboard."
    }


# ==========================================================
# 3. YIELD DEPENDENCIES (Database Sessions)
# ==========================================================
# Sometimes a dependency needs to do some cleanup after the request finishes.
# For example: open a DB connection -> run the route -> close the DB connection.
# We do this using `yield` instead of `return`.

class MockDatabaseSession:
    def __init__(self):
        print("[DB Connection] Opening connection session...")
    def query(self, data):
        return f"Database query result for: {data}"
    def close(self):
        print("[DB Connection] Closing connection session! (Cleanup done)")

# The dependency:
async def get_db_session():
    db = MockDatabaseSession()
    try:
        # FastAPI yields control back to the route function
        yield db
    finally:
        # After the route sends the response, this cleanup block runs automatically!
        db.close()

@app.get("/db-query/{query_text}")
async def query_db(query_text: str, db: MockDatabaseSession = Depends(get_db_session)):
    # The route uses the yielded database connection
    result = db.query(query_text)
    return {"status": "Success", "data": result}


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 07_dependency_injection.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try `/items` or `/users` — Swagger UI automatically detects the query parameters 
#    (`q`, `skip`, `limit`) even though they are inside the `Depends()` function!
# 4. Try `/admin/dashboard` — you must supply the header `x-api-key` with value `secret-token-123`.
# 5. Try `/db-query/hello`. Check your Python terminal output: you will see 
#    "[DB Connection] Opening connection session..." followed by 
#    "[DB Connection] Closing connection session!" proving the cleanup worked.

if __name__ == "__main__":
    uvicorn.run("07_dependency_injection:app", host="127.0.0.1", port=8000, reload=True)
