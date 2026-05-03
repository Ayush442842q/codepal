from pydantic import BaseModel, validator
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.exc import SQLAlchemyError

SQLALCHEMY_DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

class Project(Base):
    __tablename__ = 'projects'
    name = Column(String, primary_key=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

class UserRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, value, values, **kwargs):
        if not value:
            raise ValueError("Username cannot be empty")
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        db = SessionLocal()
        try:
            if db.query(User).filter(User.username == value).first():
                raise ValueError("Username is already taken")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            db.close()
        return value

    @validator("password")
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

class ProjectRequest(BaseModel):
    name: str
    description: str

    @validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Project name cannot be empty")
        if len(value) < 3:
            raise ValueError("Project name must be at least 3 characters long")
        db = SessionLocal()
        try:
            if db.query(Project).filter(Project.name == value).first():
                raise ValueError("Project name is already taken")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            db.close()
        return value

    @validator("description")
    def validate_description(cls, value):
        if not value:
            raise ValueError("Project description cannot be empty")
        if len(value) > 255:
            raise ValueError("Project description must be at most 255 characters long")
        return value

def validate_user_request(request: dict):
    try:
        UserRequest(**request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def validate_project_request(request: dict):
    try:
        ProjectRequest(**request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))