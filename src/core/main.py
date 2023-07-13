from typing import Union

from fastapi import FastAPI, APIRouter
from api.users import router as user_router
from api.tasks import router as task_router
from api.projects import router as project_router

main_router = APIRouter()
main_router.include_router(user_router, prefix='/user', tags=['user'])
main_router.include_router(task_router, prefix='/task', tags=['task'])
main_router.include_router(project_router, prefix='/project', tags=['project'])

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    return {"item_id": item_id, "q": q}
