I am fixing the backend layer.
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from logging import getLogger
import sqlite3
import os
import re

# Set up logging
logger = getLogger(__name__)

# Set up environment variables
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Set up the database connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects
    (id TEXT PRIMARY KEY, name TEXT, description TEXT, user_id INTEGER)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS collaborators
    (id TEXT PRIMARY KEY, project_id TEXT, email TEXT, name TEXT)
''')

conn.commit()

# Set up the FastAPI application
app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Define the User model
class User(BaseModel):
    id: int
    username: str
    password: str

# Define the Project model
class Project(BaseModel):
    id: str
    name: str
    description: str

# Define the Collaborator model
class Collaborator(BaseModel):
    id: str
    project_id: str
    email: str
    name: str

# Define the Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Define the TokenData model
class TokenData(BaseModel):
    username: str | None = None

# Define the UserRequest model
class UserRequest(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        if not re.match('^[a-zA-Z0-9_]+$', v):
            raise ValueError('Invalid username')
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be between 3 and 20 characters')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', v):
            raise ValueError('Invalid password')
        return v

# Define the ProjectRequest model
class ProjectRequest(BaseModel):
    id: str
    name: str
    description: str

    @validator('name')
    def validate_name(cls, v):
        if not re.match('^[a-zA-Z0-9_ ]+$', v):
            raise ValueError('Invalid project name')
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Project name must be between 3 and 50 characters')
        return v

    @validator('description')
    def validate_description(cls, v):
        if len(v) > 200:
            raise ValueError('Project description must be less than or equal to 200 characters')
        return v

# Set up the authentication function
def authenticate_user(username: str, password: str):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None

# Set up the get_current_user function
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise credentials_exception
    user = authenticate_user(token_data.username, "")
    if user is None:
        raise credentials_exception
    return user

# Set up the get_current_active_user function
def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

# Set up the login endpoint
@app.post("/login", response_model=Token)
async def login(form_data: UserRequest):
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required",
        )
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = encode(
        {"sub": user.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Set up the projects endpoint
@app.get("/projects", response_model=List[Project])
async def read_projects(current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE user_id = ?', (current_user.id,))
    projects = cursor.fetchall()
    return [{"id": project[0], "name": project[1], "description": project[2]} for project in projects]

# Set up the projects endpoint (POST)
@app.post("/projects", response_model=Project)
async def create_project(project: ProjectRequest, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('INSERT INTO projects (id, name, description, user_id) VALUES (?, ?, ?, ?)', (project.id, project.name, project.description, current_user.id))
    conn.commit()
    return project

# Set up the project endpoint (GET)
@app.get("/projects/{project_id}", response_model=Project)
async def read_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    project = cursor.fetchone()
    if project:
        return {"id": project[0], "name": project[1], "description": project[2]}
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )

# Set up the project endpoint (PUT)
@app.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project: ProjectRequest, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    existing_project = cursor.fetchone()
    if existing_project:
        cursor.execute('UPDATE projects SET name = ?, description = ? WHERE id = ? AND user_id = ?', (project.name, project.description, project_id, current_user.id))
        conn.commit()
        return project
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )

# Set up the project endpoint (DELETE)
@app.delete("/projects/{project_id}")
async def delete_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    project = cursor.fetchone()
    if project:
        cursor.execute('DELETE FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
        conn.commit()
        return {"message": "Project deleted successfully"}
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )

# Set up the collaborators endpoint (POST)
@app.post("/projects/{project_id}/collaborators", response_model=Collaborator)
async def add_collaborator(project_id: str, collaborator: Collaborator, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    project = cursor.fetchone()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    if not collaborator.project_id == project_id:
        raise HTTPException(
            status_code=400,
            detail="Collaborator project id does not match the project id in the url",
        )
    cursor.execute('INSERT INTO collaborators (id, project_id, email, name) VALUES (?, ?, ?, ?)', (collaborator.id, collaborator.project_id, collaborator.email, collaborator.name))
    conn.commit()
    return collaborator

# Set up the collaborators endpoint (GET)
@app.get("/projects/{project_id}/collaborators", response_model=List[Collaborator])
async def read_collaborators(project_id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    project = cursor.fetchone()
    if project:
        cursor.execute('SELECT * FROM collaborators WHERE project_id = ?', (project_id,))
        collaborators = cursor.fetchall()
        return [{"id": collaborator[0], "project_id": collaborator[1], "email": collaborator[2], "name": collaborator[3]} for collaborator in collaborators]
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )

# Set up the collaborator endpoint (DELETE)
@app.delete("/projects/{project_id}/collaborators/{collaborator_id}")
async def remove_collaborator(project_id: str, collaborator_id: str, current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="User not authenticated",
        )
    cursor.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, current_user.id))
    project = cursor.fetchone()
    if project:
        cursor.execute('SELECT * FROM collaborators WHERE id = ? AND project_id = ?', (collaborator_id, project_id))
        collaborator = cursor.fetchone()
        if collaborator:
            cursor.execute('DELETE FROM collaborators WHERE id = ? AND project_id = ?', (collaborator_id, project_id))
            conn.commit()
            return {"message": "Collaborator removed successfully"}
        raise HTTPException(
            status_code=404,
            detail="Collaborator not found",
        )
    raise HTTPException(
        status_code=404,
        detail="Project not found",
    )