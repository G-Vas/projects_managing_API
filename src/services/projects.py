from fastapi import HTTPException, status
import core.exceptions as exceptions
from repositories.base import IRepository
from models.models import Project
from schemas.projects import CreateProjectSchema


class ProjectService:

    repo: IRepository

    def __init__(self, repo: IRepository) -> None:
        self.repo: IRepository = repo

    async def create_project(self, project: CreateProjectSchema) -> Project:
        data = project.model_dump()
        project = await self.repo.add(data=data)
        return project

    async def get_projects_list(self, skip: int, limit: int) -> list[Project]:
        try:
            projects = await self.repo.get_list(skip=skip, limit=limit)
        except exceptions.TooBigRequest:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='the range exceeds the allowable limits'
            )
        return projects

    async def get_project_by_id(self, project_id: int) -> Project:
        try:
            project = await self.repo.get_detail(id=project_id)
        except exceptions.ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail=f'project with id:{project_id} does not exist')
        return project

    async def delete_project(self, id: int) -> dict:
        try:
            response = await self.repo.delete(id=id)
        except exceptions.ObjectDoesNotExist:
            raise HTTPException(status_code=404, detail=f'project with id:{id} does not exist')
        return response
