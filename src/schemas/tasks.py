from pydantic import BaseModel


class BaseTaskSchema(BaseModel):
    title: str
    content: str
    project_id: int


class TaskSchema(BaseTaskSchema):
    id: int
    is_done: bool = False

    class Config:
        from_attributes = True


class CreateTaskSchema(BaseTaskSchema):
    pass


class DeleteTaskSchema(BaseModel):
    ok: bool
