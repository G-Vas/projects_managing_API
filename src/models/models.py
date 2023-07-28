from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column
from db.conf_db import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    deskription = Column(String(length=4000))
    tasks = relationship('Task', back_populates='projects')


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=70))
    content = Column(String(length=4000))
    is_done = Column(Boolean(), nullable=False, default=False)
    project_id = mapped_column(ForeignKey('project.id', ondelete='CASCADE'))
    projects = relationship(
        'Project',
        back_populates='tasks',
        cascade='all, delete',
        passive_deletes=True,
    )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
