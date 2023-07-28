from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.conf_db import get_db
from repositories.tasks import TaskRepository
from models.models import Task
import schemas.tasks as schemas

router = APIRouter()


@router.post('/add', response_model=schemas.TaskSchema)
async def create_task(task: schemas.CreateTaskSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    data = task.model_dump()
    repo = TaskRepository(db=db)
    resp = await repo.add(data=data)
    return resp


@router.get('/list/{proj_id}', response_model=list[schemas.TaskSchema])
async def get_tasks_list(proj_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> list[Task]:
    repo = TaskRepository(db=db)
    resp = await repo.get_by_proj_id(proj_id=proj_id)
    return resp


@router.get('/{task_id}', response_model=schemas.TaskSchema)
async def get_task(task_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Task:
    repo = TaskRepository(db=db)
    resp = await repo.get(id=task_id)
    if not resp:
        raise HTTPException(status_code=404, detail="Item not found")
    return resp
