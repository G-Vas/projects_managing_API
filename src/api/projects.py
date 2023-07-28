from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.conf_db import get_db
from repositories.project import ProjectRepository
from models.models import Project
from schemas.projects import ProjectSchema, CreateProjectSchema, ProjectDetailSchema, DeleteProjectSchema
import core.exceptions as exceptions

router = APIRouter()


@router.post('/add', response_model=ProjectSchema)
async def create_project(project: CreateProjectSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    repo = ProjectRepository(db=db)
    data = project.model_dump()
    resp = await repo.add(data=data)
    return resp


@router.get('/list', response_model=list[ProjectSchema])
async def get_projects_list(skip: int, limit: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Project]:
    try:
        repo = ProjectRepository(db=db)
        resp = await repo.get_list(skip=skip, limit=limit)
    except exceptions.TooBigRequest:
        raise HTTPException(status_code=400, detail='the range exceeds the allowable limits')
    except Exception:
        raise HTTPException(status_code=500, detail='internal server error')
    return resp


@router.get('/{project_id}/details', response_model=ProjectDetailSchema)
async def get_project(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    try:
        repo = ProjectRepository(db=db)
        response = await repo.get_detail(id=project_id)
    except exceptions.ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail=f'project with id:{project_id} does not exist')
    except Exception:
        raise HTTPException(status_code=500, detail='internal server error')
    return response


@router.delete('/delete/{project_id}', response_model=DeleteProjectSchema)
async def delete_project(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    try:
        repo = ProjectRepository(db=db)
        response = await repo.delete(id=project_id)
    except exceptions.ObjectDoesNotExist:
        raise HTTPException(status_code=404, detail=f'project with id:{project_id} does not exist')
    except Exception:
        raise HTTPException(status_code=500, detail='internal server error')
    return response
