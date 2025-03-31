import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import glob
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
import json
import os
import shutil
import time
import threading
import uvicorn

base_results_dir = "/home/ubuntu/results"
base_users_dir = "/home/ubuntu/results"
app = FastAPI()
app.mount("/views", StaticFiles(directory="views"), name="frontend")
app.mount("/static", StaticFiles(directory="views"), name="static")
app.mount("/static", StaticFiles(directory="output_minions"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("views/index.html")

@app.get("/CSS/{file_name}")
async def serve_css(file_name: str):
    return FileResponse(f"views/CSS/{file_name}")

@app.get("/index.html")
async def serve_login():
    return FileResponse("views/index.html")

@app.get("/dashboard.js")
async def serve_js():
    return FileResponse("views/dashboard2.js")

@app.get("/dashboard2.html", response_class=HTMLResponse)
async def serve_dashboard():
    return FileResponse("views/dashboard2.html")

@app.get("/login.js")
async def serve_login_js():
    return FileResponse("views/login2.js")

base_dir = "results"
password_file_path = os.path.join(base_dir, "passwords.json")

if os.path.exists(password_file_path):
    with open(password_file_path, "r") as file:
        user_passwords = json.load(file)
else:
    user_passwords = {}

@app.get("/login")
async def login(user: str, password: str):
    user_dir = os.path.join(base_dir, user)
    if not os.path.exists(user_dir):
        raise HTTPException(status_code=404, detail=f"User directory does not exist: {user}")

    if user in user_passwords:
        stored_password = user_passwords[user]
        if password == stored_password:
            return JSONResponse(content={"message": "Login successful!"})
        else:
            raise HTTPException(status_code=401, detail="Invalid password.")
    else:
        raise HTTPException(status_code=404, detail="User not found. Please register.")

@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        user = data.get("user")
        password = data.get("password")

        if not user or not password:
            raise ValueError("Missing username or password.")

        if user in user_passwords:
            raise HTTPException(status_code=400, detail="User already exists. Please log in.")

        user_passwords[user] = password

        with open(password_file_path, "w") as file:
            json.dump(user_passwords, file)

        return JSONResponse(content={"message": "Password set successfully"})
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during registration.")

def move_files_to_user_folders():
    all_files = [f for f in os.listdir(base_results_dir) if f.endswith(".txt")]

    for file_name in all_files:
        username = file_name.split('_')[0]
        user_folder = os.path.join(base_users_dir, username)

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        source_path = os.path.join(base_results_dir, file_name)
        destination_path = os.path.join(user_folder, file_name)

        shutil.move(source_path, destination_path)

def move_files_periodically():
    while True:
        move_files_to_user_folders()
        time.sleep(10)

@app.get("/list_text_files")
async def list_text_files(user: str):
    user_directory = f"/home/ubuntu/results/{user}"

    if not os.path.exists(user_directory):
        raise HTTPException(status_code=404, detail=f"No directory found for user {user}")

    try:
        files = []
        for file_name in os.listdir(user_directory):
            if file_name.endswith(".txt"):
                file_path = os.path.join(user_directory, file_name)
                file_time = os.path.getmtime(file_path)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    sixth_line = lines[6].strip() if len(lines) > 5 else ""

                files.append({
                    "name": file_name,
                    "time": file_time,
                    "summary": sixth_line
                })
        if not files:
            return JSONResponse(content={"files": []})
        return JSONResponse(content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing text files: {str(e)}")

@app.get("/get_text_file_content")
async def get_text_file_content(user: str, file_name: str):
    directory = f"/home/ubuntu/results/{user}"
    file_path = os.path.join(directory, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_name}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return JSONResponse(content={"content": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.get("/get_minion_data")
async def get_minion_data():
    try:
        directory = "/home/ubuntu/output_minions"
        files = glob.glob(f"{directory}/*.txt")

        if not files:
            return JSONResponse(content={"output": "No files found."})

        latest_file = max(files, key=os.path.getmtime)

        with open(latest_file, 'r') as file:
            return JSONResponse(content={"output": file.read()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading minion data: {str(e)}")

if __name__ == "__main__":
    thread = threading.Thread(target=move_files_periodically)
    thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)