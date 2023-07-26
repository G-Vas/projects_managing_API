from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.conf_db import get_db
from repository.project import ProjectRepository
from models.models import Project
from schemas.projects import ProjectSchema, CreateProjectSchema

router = APIRouter()


@router.post('/create', response_model=ProjectSchema)
async def create_project(project: CreateProjectSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    repo = ProjectRepository(db=db)
    resp = await repo.create(name=project.name, deskription=project.deskription)
    print(resp)
    return resp


@router.get('/list', response_model=list[ProjectSchema])
async def get_projects_list(skip: int, end: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Project]:
    repo = ProjectRepository(db=db)
    resp = await repo.get(skip=skip, end=end)
    print('resp')
    print(resp)
    # a = [i for i in await resp.tasks]
    # print(a)
    for i in resp:
        for j in iter(i.tasks):
            print(j)
    return resp


@router.get('/{project_id}', response_model=ProjectSchema)
async def get_project(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Project:
    repo = ProjectRepository(db=db)
    resp = await repo.get_by_id(id=project_id)
    print('resp')
    print(resp)
    for i in iter(resp.tasks):
        print(i)
    if not resp:
        raise HTTPException(status_code=404, detail="Item not found")
    resp = ProjectSchema(name=resp.name, deskription=resp.deskription, id=resp.id, tasks=resp.tasks)
    return resp
