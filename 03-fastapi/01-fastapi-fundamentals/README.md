# FastAPI Fundamentals Course 🚀

Welcome to your FastAPI learning folder! This folder is designed to take you from **absolute beginner** to **advanced backend development** step-by-step.

## 📦 Setting Up Your Environment with Poetry

To install dependencies and run the scripts using Poetry:

### Step 1: Install Dependencies
Open your terminal at the root of the workspace (`Python-Learning`) and run:
```bash
poetry install
```
This will automatically create a virtual environment and install all necessary packages (`fastapi`, `uvicorn`, `sqlalchemy`, etc.) defined in `pyproject.toml`.

### Step 2: Spawn the Poetry Shell (Optional)
If you want your terminal to run directly inside the virtual environment:
```bash
poetry shell
```

---

## 📚 Curriculum Roadmap

Here are the topics we will cover in order:
1. `01_introduction_and_setup.py` — Introduction to APIs, installing FastAPI, creating endpoints, and starting the server.
2. `02_path_parameters.py` — Dynamic URL paths, parameter typing, and route matching rules.
3. `03_query_parameters.py` — URL query arguments, default values, optional filters, and input validation.
4. `04_request_body_pydantic.py` — Creating resources using POST requests, structuring requests with Pydantic.
5. `05_response_models_and_status.py` — Setting status codes, formatting outputs, and hiding secret keys (like passwords).
6. `06_error_handling.py` — Handling exceptions, raising HTTP status errors, and custom exception outputs.
7. `07_dependency_injection.py` — Understanding `Depends` for reusable functions, authentication filters, or database connections.
8. `08_database_crud_sqlite.py` — Full SQLite integration with SQLAlchemy ORM (Create, Read, Update, Delete).
9. `09_middleware_cors.py` — Cross-Origin Resource Sharing (CORS) and writing custom request interceptors (middleware).
10. `10_security_jwt.py` — Password hashing, OAuth2 standards, JWT creation, and route protection.
11. `11_background_tasks_and_files.py` — File uploads and scheduling non-blocking tasks.

---

## 🛠️ How to Run Any Script
Every script in this folder has a built-in launcher! Run it with Poetry:
```bash
poetry run python "03-FastAPI Fundamentals/<script_name>.py"
```
For example, to run the first file:
```bash
poetry run python "03-FastAPI Fundamentals/01_introduction_and_setup.py"
```
This will start a local server at `http://127.0.0.1:8000`. 
Open `http://127.0.0.1:8000/docs` in your browser to view the interactive API playground (Swagger UI)!
