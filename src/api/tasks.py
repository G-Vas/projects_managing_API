from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.conf_db import get_db
from repository.tasks import TaskRepository
from models.models import Task
from schemas.tasks import TaskSchema

router = APIRouter()


@router.post('/create', response_model=TaskSchema)
async def create_project(task: TaskSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    repo = TaskRepository(db=db)
    resp = await repo.create(title=task.title, content=task.title, project_id=task.project_id)
    return resp


@router.get('/list', response_model=TaskSchema)
async def get_projects_list(proj_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Task]:
    repo = TaskRepository(db=db)
    resp = await repo.get(proj_id=proj_id)
    return resp


@router.get('/{task_id}', response_model=TaskSchema)
async def get_project(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    repo = TaskRepository(db=db)
    resp = await repo.get_by_id(id=task_id)
    if not resp:
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
