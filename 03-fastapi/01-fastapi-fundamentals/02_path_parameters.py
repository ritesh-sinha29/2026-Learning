# ==========================================================
# FASTAPI STUDY GUIDE: 02. PATH PARAMETERS
# ==========================================================

# --- WHAT ARE PATH PARAMETERS? ---
# Path parameters are dynamic parts of the URL.
# Instead of hardcoding every URL like /items/1, /items/2, etc.,
# you can use curly brackets to capture values: /items/{item_id}.
#
# FastAPI will automatically:
# 1. Parse the parameter from the URL path.
# 2. Convert (cast) it to the Python type you specify (like `int`, `str`, `float`).
# 3. Validate it (if it's not the right type, it returns a clear error to the client).

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="FastAPI: Path Parameters")

# Let's create some dummy data to play with
ITEMS_DATABASE = {
    1: {"name": "Laptop", "price": 899.99},
    2: {"name": "Smartphone", "price": 499.99},
    3: {"name": "Wireless Headphones", "price": 149.99}
}

# ==========================================================
# 1. BASIC PATH PARAMETER WITH TYPE HINTING
# ==========================================================
# By declaring `item_id: int` in the function arguments, FastAPI does:
# - Casting: When you visit `/items/2`, the string "2" is converted to Python integer `2`.
# - Validation: If you visit `/items/keyboard`, FastAPI will see that "keyboard" cannot
#   be converted to an integer, and will return an automatic HTTP 422 error!
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Search database for the item_id
    item = ITEMS_DATABASE.get(item_id)
    
    if item is None:
        return {"error": f"Item with ID {item_id} not found."}
        
    return {
        "item_id": item_id,
        "details": item
    }


# ==========================================================
# 2. PATH MATCHING ORDER (CRITICAL PITFALL)
# ==========================================================
# FastAPI matches routes from TOP TO BOTTOM in the file.
# Imagine we want a special route for our featured item at "/items/featured".
#
# Rule: Hardcoded paths must ALWAYS go BEFORE dynamic paths!
# If we put "/items/featured" AFTER "/items/{item_id}", FastAPI will see "featured"
# as the `item_id`, try to parse it as an integer, and fail with a validation error!

# --- CORRECT ORDER ---
# First: The specific path "/items/featured"
@app.get("/items/featured")
async def get_featured_item():
    return {
        "message": "This is our featured item of the week!",
        "featured_item": ITEMS_DATABASE[1]
    }

# Second: The generic path "/items/{item_id}" (already declared above at line 34)
# Note: If we had placed the `/items/featured` route below the generic one,
# visiting `/items/featured` would result in a "422 Unprocessable Entity" error.


# ==========================================================
# 3. DYNAMIC DATA TYPES (e.g., File Paths)
# ==========================================================
# What if you want a path parameter to contain a whole file path (like "images/avatars/me.png")?
# You can use a path converter by adding `:path` inside the curly braces.
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {
        "file_path_received": file_path,
        "action": f"Reading contents of file at location: {file_path}"
    }


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 02_path_parameters.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try out `/items/1` (works!)
# 4. Try out `/items/featured` (works!)
# 5. Try out `/items/hello` (returns automatic validation error - standard HTTP 422)
# 6. Try out `/files/docs/notes/class1.pdf` (works, captures the whole path!)

if __name__ == "__main__":
    uvicorn.run("02_path_parameters:app", host="127.0.0.1", port=8000, reload=True)
