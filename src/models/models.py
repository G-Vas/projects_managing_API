from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

Base = declarative_base()


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    deskription = Column(String(length=4000))
    tasks = relationship('Tasks', back_populates="projects")


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=4000))
    project_id = mapped_column(ForeignKey('projects.id'))
    projects = relationship('Projects', back_populates="tasks")


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email = Column(String, index=True)
