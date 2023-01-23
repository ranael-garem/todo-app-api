from typing import List, Union

from crud import create_task as create_task_db
from crud import filter_tasks as filter_tasks_db
from crud import list_tasks as list_tasks_db
from crud import retrieve_task as retrieve_task_db
from crud import save_task as save_task_db
from helpers import utc_datetime
from schemas import Task, TaskCreate, TaskUpdate


def create_task(task: TaskCreate) -> Task:
    return create_task_db(task=task)


def retrieve_task(task_id: int) -> Union[Task, None]:
    return retrieve_task_db(task_id=task_id)


def delete_task(task_id: int) -> bool:
    task = retrieve_task(task_id)
    if not task:
        return False
    if task.deleted:
        return False

    task.deleted = True
    task.deleted_at = utc_datetime()
    save_task_db(task)
    return True


def update_task(task_id: int, params: TaskUpdate) -> Union[Task, None]:
    task = retrieve_task(task_id)
    if not task:
        return None

    for field, value in params.dict().items():
        if value is not None:
            setattr(task, field, value)

    save_task_db(task)
    return task


def list_tasks(search_term: Union[str, None] = None) -> Union[List[Task], None]:
    if search_term:
        search_terms_list = search_term.split(" ")
        looking_for = "%"
        for term in search_terms_list:
            looking_for += f"{term}%"
        return filter_tasks_db(looking_for)
    return list_tasks_db()


def toggle_complete(task_id: int) -> Union[Task, None]:
    task = retrieve_task(task_id)
    if not task:
        return None

    task.completed = not task.completed
    save_task_db(task)
    return task
