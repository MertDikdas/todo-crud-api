# Task API

A simple in-memory To-Do CRUD API built with **FastAPI**. It supports creating, listing, retrieving, updating, and deleting tasks through REST endpoints.

> Task data is stored in memory and resets when the application restarts.

## Requirements

- Python 3.10 or newer
- `pip`

## Install and Run

Clone the repository, open its directory, and run:

```bash
pip install -r requirements.txt && uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000` and its interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Endpoint | Description | Success status |
|---|---|---|---|
| `GET` | `/` | Returns the API name, version, and available task endpoint | `200 OK` |
| `GET` | `/health` | Checks whether the API is running | `200 OK` |
| `GET` | `/tasks` | Returns all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Returns a task by its ID | `200 OK` |
| `POST` | `/tasks` | Creates a new task | `201 Created` |
| `PUT` | `/tasks/{id}` | Updates a task's title and/or completion status | `200 OK` |
| `DELETE` | `/tasks/{id}` | Deletes a task | `204 No Content` |

Invalid or blank titles return `400 Bad Request`. Requests for task IDs that do not exist return `404 Not Found`.

## Example Request and Response

Request:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Write the README"}'
```

Output:

```http
HTTP/1.1 201 Created
date: Sat, 01 Aug 2026 12:00:00 GMT
server: uvicorn
content-length: 48
content-type: application/json

{"id":4,"title":"Write the README","done":false}
```

## Swagger UI

FastAPI automatically generates interactive API documentation. After starting the application, open:

`http://127.0.0.1:8000/docs`

![Task API Swagger UI](docs/swagger-ui.png)

## Task Model

```json
{
  "id": 1,
  "title": "Plan your day",
  "done": false
}
```

## Query
```sql
SELECT COUNT(*) FROM tasks;
```
- It returned the count of the tasks

## Notes

- New tasks are created with `done` set to `false`.
- `PUT /tasks/{id}` accepts `title`, `done`, or both fields.
- The API trims leading and trailing spaces from task titles.
- Deleting a task returns an empty response body with status `204`.
