from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    title: str
    content: str
    project_id: int

    class Config:
        from_attributes = True
