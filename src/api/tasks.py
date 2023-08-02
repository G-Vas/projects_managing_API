from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.conf_db import get_db
from repositories.tasks import TaskRepository
from models.models import Task
from services.tasks import TaskService
import schemas.tasks as schemas

router = APIRouter()


@router.post('/add', response_model=schemas.TaskSchema)
async def create_task(task: schemas.CreateTaskSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    repo = TaskRepository(db=db)
    response = await TaskService(repo=repo).create_task(task=task)
    return response


@router.get('/list/{project_id}', response_model=list[schemas.TaskSchema])
async def get_tasks_list(project_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Task]:
    repo = TaskRepository(db=db)
    response = await TaskService(repo=repo).get_by_project_id(project_id=project_id)
    return response


@router.get('/{task_id}', response_model=schemas.TaskSchema)
async def get_task(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    repo = TaskRepository(db=db)
    response = await TaskService(repo=repo).get_task_by_id(task_id=task_id)
    return response
