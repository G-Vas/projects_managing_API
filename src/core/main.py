from fastapi import FastAPI, APIRouter
from api.users import router as user_router
from api.tasks import router as task_router
from api.projects import router as project_router

main_router = APIRouter()
main_router.include_router(user_router, prefix='/user', tags=['user'])
main_router.include_router(task_router, prefix='/task', tags=['task'])
main_router.include_router(project_router, prefix='/project', tags=['project'])

app = FastAPI()

app.include_router(main_router)
