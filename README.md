# Task Management REST API

A multi-user task management REST API built with Flask and SQLAlchemy. Features JWT authentication, role-based access control (users vs. admins), PostgreSQL support via Docker, and Pytest integration tests.

## Tech Stack

- **API:** Flask, Flask-JWT-Extended, Flask-SQLAlchemy
- **Data:** PostgreSQL (Docker), SQLite (local development)
- **Testing:** Pytest

## Architecture

The app follows the Flask application factory pattern: `create_app()` in `app/__init__.py` builds the Flask app, attaches extensions, registers blueprints, and wires up CLI commands and error handlers. Tests create a fresh app instance against an in-memory database.

```text
app/
  __init__.py          App factory, blueprint registration, CLI commands
  config.py            Environment-based configuration
  extensions.py        SQLAlchemy and JWT extension instances
  models.py            User and Task database models
  auth/routes.py       Registration, login, current-user endpoints
  tasks/routes.py      Task CRUD endpoints protected by JWT
tests/
  conftest.py          App and database fixtures
  test_auth.py         Registration, login, and token tests
  test_tasks.py        Task CRUD, validation, and access-control tests
```

## Quickstart

### Option A: Local Python (SQLite)

Create and activate a virtual environment, then install dependencies:

**macOS / Linux (bash):**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Initialize the database and run:

```bash
flask --app wsgi.py init-db
flask --app wsgi.py run
```

Local Python runs against SQLite at `instance/tasks.db`.

### Option B: Docker (PostgreSQL)

```bash
docker compose up --build
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### Health

```http
GET /health
```

### Auth

```http
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
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
GET    /api/tasks
POST   /api/tasks
GET    /api/tasks/<task_id>
PATCH  /api/tasks/<task_id>
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

Allowed statuses: `todo`, `in_progress`, `done`. Allowed priorities: `low`, `medium`, `high`.

## Role-Based Access

Regular users can only list, view, update, and delete their own tasks. Admins can list and access all tasks. Public registration always creates a regular `user`; create an admin from the command line:

**macOS / Linux (bash):**

```bash
ADMIN_USERNAME="admin" ADMIN_EMAIL="admin@example.com" ADMIN_PASSWORD="password123" flask --app wsgi.py create-admin
```

**Windows (PowerShell):**

```powershell
$env:ADMIN_USERNAME="admin"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="password123"
flask --app wsgi.py create-admin
```

## Tests

```bash
pytest
```

Tests run against an in-memory SQLite database (no Docker required) and cover registration and login, rejected logins, JWT protection on task endpoints, task create/list/update/delete, users being blocked from other users' tasks, admin access to all tasks, and task validation.
