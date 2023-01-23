from sqlalchemy import or_
from models import Task
import schemas
from database import session_scope


def create_task(task: schemas.TaskCreate):
    with session_scope() as db:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task


def retrieve_task(task_id: int) -> Task:
    with session_scope() as db:
        return db.query(Task).filter(Task.id == task_id, Task.deleted == False).first()


def save_task(task: Task) -> Task:
    with session_scope() as db:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task


def list_tasks():
    with session_scope() as db:
        return db.query(Task).all()


def filter_tasks(looking_for: str):
    with session_scope() as db:
        return (
            db.query(Task)
            .filter(
                or_(Task.title.like(looking_for), Task.description.like(looking_for))
            )
            .all()
        )
