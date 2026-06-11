# ==========================================================
# FASTAPI STUDY GUIDE: 11. FILE UPLOADS & BACKGROUND TASKS
# ==========================================================

# --- WHAT IS UPLOADFILE? ---
# FastAPI lets you receive uploaded files using:
# 1. `bytes`: Reads the entire file into RAM. Good for small files only.
# 2. `UploadFile`: Recommended. It uses a temporary file on disk if the file exceeds a size limit.
#    This saves RAM. It also provides metadata like filename, content-type, and headers.
# Note: To use files, you must install the python-multipart package:
#   pip install python-multipart

# --- WHAT ARE BACKGROUND TASKS? ---
# Sometimes you need to perform a slow operation (like sending an email, writing logs,
# or processing an image) as a result of a request.
# You shouldn't make the user wait for this to finish before getting their response!
# FastAPI's `BackgroundTasks` lets you define a function to run *after* returning the response.

import time
import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from typing import List

app = FastAPI(title="FastAPI: File Uploads & Background Tasks")

# ==========================================================
# 1. FILE UPLOADS (SINGLE & MULTIPLE)
# ==========================================================

@app.post("/upload-single")
async def upload_single_file(file: UploadFile = File(...)):
    # You can read metadata:
    # - file.filename: Name of the file (e.g., "photo.jpg")
    # - file.content_type: MIME type (e.g., "image/jpeg")
    
    # To read file contents:
    contents = await file.read()  # Reads the file as bytes
    
    # Close the file to free up system resources
    await file.close()
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "message": "File received successfully!"
    }


@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    uploaded_files_info = []
    
    for file in files:
        # Just record the metadata (without reading all bytes to keep it fast)
        uploaded_files_info.append({
            "filename": file.filename,
            "content_type": file.content_type
        })
        await file.close()
        
    return {
        "files_count": len(files),
        "uploaded_files": uploaded_files_info
    }


# ==========================================================
# 2. BACKGROUND TASKS
# ==========================================================

# A standard Python function representing our slow background task
def write_log_report(email: str, message: str):
    # Simulate a slow email dispatch or PDF write (5 seconds)
    print(f"[Background Task] Start: Generating report for {email}...")
    time.sleep(5)
    print(f"[Background Task] Success: Report email sent to {email}! Message: '{message}'")


# Endpoint that schedules the background task
@app.post("/request-report")
async def request_report(email: str, background_tasks: BackgroundTasks):
    # Schedule the task: (task_function, arg1, arg2...)
    # The client will receive the return response IMMEDIATELY.
    # The function `write_log_report` will run in the background after the response is sent.
    background_tasks.add_task(write_log_report, email, "Your report is attached below.")
    
    return {
        "status": "Request received",
        "message": f"Your report request has been scheduled. An email will be sent to {email} shortly."
    }


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 11_background_tasks_and_files.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try `/upload-single` by uploading any small text file or image.
# 4. Try `/request-report` with your email.
#    * Watch Swagger return the success response immediately (0 seconds delay).
#    * Check your Python terminal! After 5 seconds, you will see the prints:
#      `[Background Task] Success: Report email sent to ...` showing it executed in the background.

if __name__ == "__main__":
    uvicorn.run("11_background_tasks_and_files:app", host="127.0.0.1", port=8000, reload=True)
