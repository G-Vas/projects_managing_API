from fastapi import HTTPException, status
from models.models import Task
from schemas.tasks import CreateTaskSchema
import core.exceptions as exceptions
from repositories.base import IRepository


class TaskService:

    repo: IRepository

    def __init__(self, repo: IRepository) -> None:
        self.repo: IRepository = repo

    async def create_task(self, task: CreateTaskSchema) -> Task:
        data = task.model_dump()
        task = await self.repo.add(data=data)
        return task

    async def get_by_project_id(self, project_id: int) -> list[Task]:
        try:
            tasks = await self.repo.get_by_proj_id(proj_id=project_id)
        except exceptions.ObjectDoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'tasks with project_id:{project_id} does not exist')
        return tasks

    async def get_task_by_id(self, task_id: int) -> Task:
        try:
            task = await self.repo.get(id=task_id)
        except exceptions.ObjectDoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'task with id:{task_id} does not exist')
        return task
