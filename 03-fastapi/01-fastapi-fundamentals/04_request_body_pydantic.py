# ==========================================================
# FASTAPI STUDY GUIDE: 04. REQUEST BODY & PYDANTIC
# ==========================================================

# --- WHAT IS A REQUEST BODY? ---
# A request body is data sent by the client (like a browser or frontend app) 
# to your API in the HTTP request payload (usually as JSON).
# Unlike query parameters (which go in the URL), the request body is sent inside the request.
# We use a request body when we want to CREATE or UPDATE resources (via POST, PUT, PATCH).

# --- WHAT IS PYDANTIC? ---
# Pydantic is a powerful library used by FastAPI for data parsing and validation.
# To define a request body in FastAPI:
# 1. Import `BaseModel` from `pydantic`.
# 2. Create a class that inherits from `BaseModel`.
# 3. Define the fields and their types (using Python type hints).

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Union, List
import uvicorn

app = FastAPI(title="FastAPI: Request Body & Pydantic")

# Mock database
PRODUCTS_DATABASE = {}

# ==========================================================
# 1. DEFINING A PYDANTIC MODEL
# ==========================================================
# This class defines the structure (schema) of the JSON we expect from the client.
# We can use Pydantic's `Field` to add validation rules (like min_length, gt, lt).
class Product(BaseModel):
    name: str = Field(..., min_length=2, description="Name of the product")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    description: Union[str, None] = Field(default=None, description="Optional description of the product")
    tax: Union[float, None] = 0.0  # Default value if not provided
    tags: List[str] = []           # Default to an empty list of strings


# ==========================================================
# 2. POST ROUTE WITH REQUEST BODY
# ==========================================================
# By declaring `product: Product` in the arguments, FastAPI will:
# 1. Read the JSON from the request body.
# 2. Validate it against the `Product` model.
# 3. Convert it into a Pydantic object that you can access (like `product.name`, `product.price`).
@app.post("/products/{product_id}")
async def create_product(product_id: int, product: Product):
    if product_id in PRODUCTS_DATABASE:
        raise HTTPException(status_code=400, detail="Product ID already exists.")
        
    # Calculate price including tax
    total_price = product.price + (product.tax or 0.0)
    
    # Store it in our mock database (converting Pydantic object to a dictionary)
    PRODUCTS_DATABASE[product_id] = product.model_dump()
    
    return {
        "message": "Product created successfully!",
        "product_id": product_id,
        "product_data": PRODUCTS_DATABASE[product_id],
        "total_price_calculated": total_price
    }


# ==========================================================
# 3. MIXING PATH, QUERY, AND REQUEST BODY
# ==========================================================
# FastAPI is smart enough to know which parameter is what:
# - If parameter is declared in the path (like `{product_id}`), it's a PATH parameter.
# - If it's a simple type (like `int`, `str`) NOT in the path, it's a QUERY parameter.
# - If it's a subclass of `BaseModel`, it's a REQUEST BODY.
#
# Try this: Update an existing product, and also accept a query parameter `notify`
@app.put("/products/{product_id}")
async def update_product(
    product_id: int,          # PATH Parameter
    product: Product,         # REQUEST BODY (Pydantic model)
    notify: bool = False      # QUERY Parameter (Defaults to False)
):
    if product_id not in PRODUCTS_DATABASE:
        raise HTTPException(status_code=404, detail="Product not found.")
        
    PRODUCTS_DATABASE[product_id] = product.model_dump()
    
    response = {
        "message": "Product updated successfully!",
        "product_id": product_id,
        "updated_data": PRODUCTS_DATABASE[product_id]
    }
    
    if notify:
        response["notification"] = "Users have been notified about the product update!"
        
    return response


@app.get("/products")
async def list_products():
    return PRODUCTS_DATABASE


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 04_request_body_pydantic.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Look at the `/products/{product_id}` POST endpoint in Swagger. It automatically 
#    shows the JSON body schema required to make the request!
# 4. Try sending an invalid body (e.g. price: -10.0 or a name with only 1 letter). 
#    FastAPI will automatically block it and return a detailed validation error.

if __name__ == "__main__":
    uvicorn.run("04_request_body_pydantic:app", host="127.0.0.1", port=8000, reload=True)
