from typing import List, Union

from sqlalchemy import or_

from app.database import session_scope
from app.models import Task
from app.schemas import TaskCreate, TaskSchema


def create_task(task: TaskCreate) -> TaskSchema:
    with session_scope() as db:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task


def retrieve_task(task_id: int) -> Union[TaskSchema, None]:
    with session_scope() as db:
        return db.query(Task).filter(Task.id == task_id, Task.deleted == False).first()


def save_task(task: TaskSchema) -> TaskSchema:
    with session_scope() as db:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task


def list_tasks() -> Union[List[TaskSchema], None]:
    with session_scope() as db:
        return db.query(Task).all()


def filter_tasks(looking_for: str) -> Union[List[TaskSchema], None]:
    with session_scope() as db:
        return (
            db.query(Task)
            .filter(
                or_(
                    Task.title.like(looking_for),
                    Task.description.like(looking_for),
                )
            )
            .all()
        )
