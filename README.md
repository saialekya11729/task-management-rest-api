# Task Management REST API

A Flask REST API for multi-user task management with JWT authentication, SQLAlchemy models, PostgreSQL support through Docker, role-based task access, and Pytest integration tests.

This project matches the resume bullet:

> Developed a multi-user task management REST API in Flask with PostgreSQL and SQLAlchemy, supporting full CRUD with role-based access, JWT-secured endpoints, Docker containerization, and Pytest integration tests covering auth flows.

## What You Are Building

The app has three main layers:

- `app/models.py`: database tables represented as Python classes.
- `app/auth/routes.py`: registration, login, and current-user endpoints.
- `app/tasks/routes.py`: task CRUD endpoints protected by JWTs.

The important design pattern is the app factory in `app/__init__.py`. `create_app()` builds a Flask app, attaches extensions, registers routes, and lets tests create a fresh app with a different database.

## Run Locally With Python

Create a virtual environment, install dependencies, initialize the database, and run Flask:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app wsgi.py init-db
flask --app wsgi.py run
```

By default, local Python runs against SQLite at `instance/tasks.db`. Docker uses PostgreSQL.

## Run With Docker And PostgreSQL

```powershell
docker compose up --build
```

The API will be available at:

```text
http://localhost:5000
```

## API Endpoints

### Health

```http
GET /health
```

### Auth

```http
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me
```

Example registration body:

```json
{
  "username": "alex",
  "email": "alex@example.com",
  "password": "password123"
}
```

Example login response:

```json
{
  "access_token": "...",
  "user": {
    "id": 1,
    "username": "alex",
    "email": "alex@example.com",
    "role": "user"
  }
}
```

Use the token on protected routes:

```http
Authorization: Bearer <access_token>
```

### Tasks

```http
GET /api/tasks
POST /api/tasks
GET /api/tasks/<task_id>
PATCH /api/tasks/<task_id>
DELETE /api/tasks/<task_id>
```

Example task body:

```json
{
  "title": "Finish Flask API",
  "description": "Build, test, and document the project",
  "status": "todo",
  "priority": "high",
  "due_date": "2026-06-01"
}
```

Allowed statuses:

```text
todo, in_progress, done
```

Allowed priorities:

```text
low, medium, high
```

## Role-Based Access

Normal users can only list, view, update, and delete their own tasks.

Admins can list and access all tasks. Public registration always creates a normal `user`, so admins are created from the command line:

```powershell
$env:ADMIN_USERNAME="admin"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="password123"
flask --app wsgi.py create-admin
```

## Run Tests

```powershell
pytest
```

The tests use an in-memory SQLite database so they do not require Docker. They cover:

- user registration and login
- rejected login attempts
- JWT protection on task endpoints
- task create/list/update/delete
- users being blocked from other users' tasks
- admin access to all tasks
- task validation

## Learning Map

Start with this order:

1. Read `app/models.py` to understand how `User` and `Task` become database tables.
2. Read `app/auth/routes.py` to see how passwords are hashed and JWTs are created.
3. Read `app/tasks/routes.py` to see how each endpoint checks the caller's identity.
4. Read `tests/test_auth.py` and `tests/test_tasks.py` to see how API behavior is proven.
5. Read `docker-compose.yml` to see how Flask and PostgreSQL run together.

The key mental model: every protected request carries a JWT. Flask-JWT-Extended verifies that token, then route code uses the user id and role from the token to decide what data the caller is allowed to touch.
