import random


def create_task(test_client, title="Dummy Task", description="Dummy Description"):
    """Possible improvement: Using factory instead of an API call"""
    url = test_client.app.url_path_for("create_task")
    response = test_client.post(url, json={"title": title, "description": description})
    return response.json()


def test_create_task_endpoint(test_client):
    url = test_client.app.url_path_for("create_task")
    response = test_client.post(
        url, json={"title": "Dummy Task", "description": "Lorem ipsum"}
    )
    assert response.status_code == 201


def test_create_task_title_required(test_client):
    url = test_client.app.url_path_for("create_task")
    response = test_client.post(url, json={"description": "Lorem ipsum"})
    assert response.status_code == 422


def test_retrieve_task(test_client):
    task_id = create_task(test_client)["id"]

    url = test_client.app.url_path_for("retrieve_task", task_id=task_id)
    response = test_client.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_retrieve_task_unknown_id(test_client):
    task_id = random.randint(1, 1000)
    url = test_client.app.url_path_for("retrieve_task", task_id=task_id)
    response = test_client.get(url)
    assert response.status_code == 404


def test_delete_task(test_client):
    task_id = create_task(test_client)["id"]

    url = test_client.app.url_path_for("delete_task", task_id=task_id)
    response = test_client.delete(url)
    assert response.status_code == 204

    # Test can't retrieve a deleted task
    url = test_client.app.url_path_for("retrieve_task", task_id=task_id)
    response = test_client.get(url)
    assert response.status_code == 404

    # Test can't delete an already deleted task
    url = test_client.app.url_path_for("delete_task", task_id=task_id)
    response = test_client.delete(url)
    assert response.status_code == 404


def test_update_task(test_client):
    task = create_task(test_client)
    task_id = task["id"]
    title = "New title"
    description = " New Description"

    url = test_client.app.url_path_for("update_task", task_id=task_id)
    response = test_client.patch(url, json={"title": title})
    assert response.status_code == 200
    assert response.json()["title"] == title
    assert response.json()["description"] is not None

    url = test_client.app.url_path_for("update_task", task_id=task_id)
    response = test_client.patch(url, json={"description": description})
    assert response.status_code == 200
    assert response.json()["description"] == description


def test_update_task_title_cannot_be_empty(test_client):
    task = create_task(test_client)
    task_id = task["id"]
    url = test_client.app.url_path_for("update_task", task_id=task_id)
    response = test_client.patch(url, json={"title": ""})
    assert response.status_code == 422


def test_update_task_description_can_be_empty(test_client):
    task = create_task(test_client)
    task_id = task["id"]
    url = test_client.app.url_path_for("update_task", task_id=task_id)
    response = test_client.patch(url, json={"description": ""})
    assert response.status_code == 200
    assert response.json()["description"] == ""


def test_update_task_not_found(test_client):
    task_id = random.randint(1, 1000)
    url = test_client.app.url_path_for("update_task", task_id=task_id)
    response = test_client.patch(url, json={"title": "New title"})
    assert response.status_code == 404


def test_list_tasks(test_client):
    create_task(test_client)
    create_task(test_client)

    url = test_client.app.url_path_for("list_tasks")
    response = test_client.get(url)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2


def test_complete_task_and_uncomplete(test_client):
    task = create_task(test_client)
    task_id = task["id"]
    assert not task["completed"]

    url = test_client.app.url_path_for("toggle_complete", task_id=task_id)
    response = test_client.post(url)

    # Assert Task is completed
    assert response.status_code == 200
    assert response.json()["completed"]

    # Toggle complete
    response = test_client.post(url)

    # Assert Task is now uncompleted
    assert response.status_code == 200
    assert not response.json()["completed"]


def test_complete_task_not_found(test_client):
    task_id = random.randint(1, 1000)
    url = test_client.app.url_path_for("toggle_complete", task_id=task_id)
    response = test_client.post(url)
    assert response.status_code == 404


def test_search_tasks(test_client):
    first_task_title = "Task one"
    second_task_title = "Task 2 Base title"
    third_task_title = "Lorem Ipsum"
    third_task_description = "Base description"
    create_task(test_client, title=first_task_title)
    create_task(test_client, title=second_task_title)
    create_task(test_client, title=third_task_title, description=third_task_description)

    # Search should return first and second task by matching with title
    search_term = "Task"
    url = test_client.app.url_path_for("list_tasks")
    response = test_client.get(url, params={"search_term": search_term})

    response_data = response.json()
    assert len(response_data) == 2

    # Search should return first task only by matching with title
    search_term = "One"
    url = test_client.app.url_path_for("list_tasks")
    response = test_client.get(url, params={"search_term": search_term})

    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["title"] == first_task_title

    # Search should two results, matching with title and description
    search_term = "Bas"
    url = test_client.app.url_path_for("list_tasks")
    response = test_client.get(url, params={"search_term": search_term})

    response_data = response.json()
    assert len(response_data) == 2
    assert search_term in response_data[0]["title"]
    assert search_term in response_data[1]["description"]

    # Search should match multiple terms, returing third task
    search_term = "Lor Ip"
    url = test_client.app.url_path_for("list_tasks")
    response = test_client.get(url, params={"search_term": search_term})

    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["title"] == third_task_title
