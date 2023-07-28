from pydantic import BaseModel
from .tasks import TaskSchema


class BaseProjectSchema(BaseModel):
    name: str
    deskription: str


class ProjectSchema(BaseProjectSchema):
    id: int

    class Config:
        from_attributes = True


class ProjectDetailSchema(ProjectSchema):
    tasks: list[TaskSchema] = []


class CreateProjectSchema(BaseProjectSchema):
    pass


class DeleteProjectSchema(BaseModel):
    ok: bool
