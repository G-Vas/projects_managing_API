from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.conf_db import get_db
from repositories.projects import ProjectRepository
from models.models import Project
from schemas.projects import ProjectSchema, CreateProjectSchema, ProjectDetailSchema, DeleteProjectSchema
from services.projects import ProjectService
router = APIRouter()


@router.post('/add', response_model=ProjectSchema)
async def create_project(project: CreateProjectSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    repo = ProjectRepository(db=db)
    response = await ProjectService(repo=repo).create_project(project=project)
    return response


@router.get('/list', response_model=list[ProjectSchema])
async def get_projects_list(skip: int, limit: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Project]:
    repo = ProjectRepository(db=db)
    response = await ProjectService(repo=repo).get_projects_list(skip=skip, limit=limit)
    return response


@router.get('/{project_id}/details', response_model=ProjectDetailSchema)
async def get_project(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    repo = ProjectRepository(db=db)
    response = await ProjectService(repo=repo).get_project_by_id(project_id=project_id)
    return response


@router.delete('/delete/{project_id}', response_model=DeleteProjectSchema)
async def delete_project(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    repo = ProjectRepository(db=db)
    response = await ProjectService(repo=repo).delete_project(id=project_id)
    return response
