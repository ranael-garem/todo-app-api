from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, FastAPI, HTTPException

from . import logic, models, schemas
from .database import Base, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
task_router = APIRouter()


@task_router.post(
    "/tasks/", status_code=HTTPStatus.CREATED, response_model=schemas.TaskSchema
)
async def create_task(task: schemas.TaskCreate):
    return logic.create_task(task)


@task_router.get("/tasks/", response_model=List[schemas.TaskSchema])
async def list_tasks(search_term: Union[str, None] = None):
    return logic.list_tasks(search_term)


@task_router.get("/tasks/{task_id}", response_model=schemas.TaskSchema)
async def retrieve_task(task_id: int):
    task = logic.retrieve_task(task_id)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task


@task_router.delete("/tasks/{task_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_task(task_id: int):
    deleted = logic.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return ""


@task_router.patch("/tasks/{task_id}", response_model=schemas.TaskSchema)
async def update_task(task_id: int, task_params: schemas.TaskUpdate):
    task = logic.update_task(task_id, task_params)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task


@task_router.post("/tasks/{task_id}/complete", response_model=schemas.TaskSchema)
async def toggle_complete(task_id: int):
    task = logic.toggle_complete(task_id)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task


app.include_router(task_router)
