from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict

Base = declarative_base()

# Many-to-many relationship table for projects and collaborators
project_collaborator_table = Table(
    "project_collaborator",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id")),
    Column("collaborator_id", ForeignKey("collaborators.id"))
)


class User(Base):
    """User model."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    projects = relationship("Project", back_populates="user")
    collaborators = relationship("Collaborator", back_populates="user")

    def to_dict(self) -> Dict:
        """Return a dictionary representation of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }


class Project(Base):
    """Project model."""
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        UniqueConstraint("name", name="unique_project_name")
    )

    user = relationship("User", back_populates="projects")
    collaborators = relationship("Collaborator", secondary=project_collaborator_table, back_populates="projects")

    def to_dict(self) -> Dict:
        """Return a dictionary representation of the project."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "user_id": self.user_id
        }


class Collaborator(Base):
    """Collaborator model."""
    __tablename__ = "collaborators"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="collaborators")
    projects = relationship("Project", secondary=project_collaborator_table, back_populates="collaborators")

    def to_dict(self) -> Dict:
        """Return a dictionary representation of the collaborator."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "user_id": self.user_id
        }


engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()