# Upload This Project To GitHub

Your GitHub profile is:

```text
https://github.com/saialekya11729
```

That is your account page. To upload this project, first create a repository inside that account.

## Option 1: GitHub Desktop

This is the easiest path if `git` is not installed in your terminal.

1. Install GitHub Desktop from `https://desktop.github.com/`.
2. Sign in with your GitHub account: `saialekya11729`.
3. Choose `File` > `Add local repository`.
4. Select this folder:

```text
C:\Users\aleky\OneDrive\Documents\Task Management REST API
```

5. If GitHub Desktop says it is not a Git repository, click `create a repository`.
6. Use this repository name:

```text
task-management-rest-api
```

7. Commit the files with this message:

```text
Build task management REST API
```

8. Click `Publish repository`.
9. Make sure `Keep this code private` is unchecked if you want recruiters to see it.
10. After publishing, your repo should be here:

```text
https://github.com/saialekya11729/task-management-rest-api
```

## Option 2: Command Line

Use this path after installing Git from `https://git-scm.com/downloads`.

Open PowerShell in this folder:

```powershell
cd "C:\Users\aleky\OneDrive\Documents\Task Management REST API"
```

Initialize Git and make the first commit:

```powershell
git init
git add .
git commit -m "Build task management REST API"
git branch -M main
```

Create a new empty repository on GitHub:

1. Go to `https://github.com/new`.
2. Repository owner: `saialekya11729`.
3. Repository name: `task-management-rest-api`.
4. Do not add a README, `.gitignore`, or license on GitHub because this project already has local files.
5. Click `Create repository`.

Connect this local folder to the GitHub repo and push:

```powershell
git remote add origin https://github.com/saialekya11729/task-management-rest-api.git
git push -u origin main
```

## What Not To Upload

These are already ignored by `.gitignore`:

- `.venv/`
- `.env`
- `instance/`
- `__pycache__/`
- `.pytest_cache/`

That matters because `.env` can contain secrets, `.venv` is huge, and `instance/` may contain your local SQLite database.

## Quick Check Before Sharing

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected result:

```text
7 passed
```

Then share this URL on your resume or portfolio:

```text
https://github.com/saialekya11729/task-management-rest-api
```
