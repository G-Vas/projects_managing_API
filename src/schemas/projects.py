from pydantic import BaseModel
from .tasks import TaskSchema


class BaseProjectSchema(BaseModel):
    name: str
    deskription: str


class ProjectSchema(BaseProjectSchema):
    id: int
    tasks: list[TaskSchema] = []

    class Config:
        from_attributes = True


class CreateProjectSchema(BaseProjectSchema):
    pass
