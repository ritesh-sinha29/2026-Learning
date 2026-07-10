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

There are **2 ways** to run a FastAPI file. Both give the same result.

---

### ▶️ Method A — Terminal Command (Recommended ✅)

```bash
uvicorn 01_introduction_and_setup:app --reload
```

Or with Poetry (if you haven't activated the shell):
```bash
poetry run uvicorn 01_introduction_and_setup:app --reload
```

- `01_introduction_and_setup` → the Python **filename** (without `.py`)
- `app` → the FastAPI **instance** created inside that file (`app = FastAPI()`)
- `--reload` → **auto-restarts** the server every time you save the file
- The `if __name__ == "__main__":` block inside the file is **NOT used** here

---

### ▶️ Method B — Run as Python Script

```bash
python 01_introduction_and_setup.py
```

Or with Poetry:
```bash
poetry run python 01_introduction_and_setup.py
```

- Python runs the file top to bottom
- When it reaches `if __name__ == "__main__":` → that condition is **True** → it calls `uvicorn.run()` internally
- Same result as Method A, just triggered differently

---

### 🤔 What is `if __name__ == "__main__":` ?

Every Python file has a built-in variable called `__name__`.

| Situation | Value of `__name__` | `if` block runs? |
|---|---|---|
| You run the file directly (`python file.py`) | `"__main__"` | ✅ Yes |
| Someone imports the file (`import file`) | `"file"` (filename) | ❌ No |

This guard **prevents the server from starting accidentally** when another file imports this one.

> **Simple rule:** Use **Method A** (terminal uvicorn command) for daily development.  
> The `if __name__` block is a convenience fallback for running the file as a plain script.

---

After starting the server, open your browser at:
- `http://127.0.0.1:8000/docs` → **Swagger UI** (interactive API playground)
- `http://127.0.0.1:8000/redoc` → **ReDoc** (clean documentation view)
