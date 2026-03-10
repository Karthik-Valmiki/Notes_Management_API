# Notes Management API

> A RESTful API for managing personal notes with **JWT authentication** and **Role-Based Access Control**.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

---

# Setup

## 1. Prerequisites

Before running the project, ensure the following tools are installed on your system.

### Python

Download Python from the official website:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

or

```bash
python3 --version
```

Expected output:

```
Python 3.x.x
```

---

### Git

Download Git from:

https://git-scm.com/downloads

Verify installation:

```bash
git --version
```

Expected output:

```
git version 2.x.x
```

---

### Docker

Download Docker Desktop from:

https://www.docker.com/products/docker-desktop

After installation, open the Docker Desktop application.

Important: Docker will not work until the application is running. Wait until the Docker whale icon in your taskbar/menu bar becomes stable.

Verify installation:

```bash
docker --version
```

---

# 2. Clone the Repository

```bash
git clone https://github.com/Karthik-Valmiki/Notes_Management_API.git
cd Notes_Management_API
```

---

# 3. Configure Environment Variables (Mandatory)

Before running the application, you **must create and configure the `.env` file**.

Copy the example file:

```bash
cp .env.example .env
```

Now open `.env` and update the values.

Example configuration:

```env
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/notes_db
SECRET_KEY=your_long_hex_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_SECRET=your_admin_bootstrap_secret
```

Important notes:

- `SECRET_KEY` must be a **long random string**
- `ADMIN_SECRET` can be **any value you choose**
- The `.env` file **must exist before running Docker**

If this step is skipped, the API will fail to start.

---

# 4. Generate a Secure SECRET_KEY

Run the following command in your terminal:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Example output:

```
4d4d4b67a7f6a93c7a4d98b51f1d7e6d0d78e4d8d6d2a5c33b2c71f8cdd6b62f
```

Paste this value into your `.env` file:

```env
SECRET_KEY=PASTE_GENERATED_KEY_HERE
```

---

# Running the Application

After configuring the `.env` file, run the following command inside the project folder:

```bash
docker compose up --build
```

Run the above command in the VS Code terminal.

Docker will start the PostgreSQL database first, and then the FastAPI application.

---

| | URL |
|-|-----|
| **API** | `http://localhost:8000` |
| **Swagger UI** | `http://localhost:8000/docs` |

> The database starts first — Docker's healthcheck ensures the API only comes up once PostgreSQL is fully ready.

---

# Authentication

## Register

Navigate to `http://localhost:8000/docs`, open the `POST /users/register` endpoint, fill in `username`, `email`, and `password`, then click **Execute**.

Example request body:

```json
{
  "username": "karthik",
  "email": "karthik@gmail.com",
  "password": "secret123"
}
```

**Response**

```json
{
  "id": 1,
  "username": "karthik",
  "email": "karthik@gmail.com",
  "role": "user"
}
```

---

## Login

Navigate to `http://localhost:8000/docs`, open the `POST /users/login` endpoint, fill in `email` and `password`, then click **Execute**.

Example request body:

```json
{
  "username": "karthik",
  "password": "secret123"
}
```

**Response**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use this token in requests as:

```
Authorization: Bearer <your_token>
```

In Swagger UI:

Click the **Authorize** button on the top-right and paste the token.
You can ignore the cliend_id, Don't fill the part

---

# Creating Notes

Navigate to `http://localhost:8000/docs`, open the `POST /notes` endpoint, enter the title and content, then click **Execute**.

Example request body:

```json
{
  "title": "Meeting Notes",
  "content": "Discuss project milestones."
}
```

**Response**

```json
{
  "id": 1,
  "title": "Meeting Notes",
  "content": "Discuss project milestones.",
  "owner_id": 1,
  "user_note_number": 1,
  "created_at": "2026-03-09T16:27:59.569733+05:30"
}
```

---

# Managing Notes

## Get All Notes

Navigate to `http://localhost:8000/docs`, open the `GET /notes` endpoint and click **Execute**.

Example response:

```json
[
  {
    "id": 1,
    "title": "Meeting Notes",
    "content": "Discuss project milestones.",
    "owner_id": 1,
    "user_note_number": 1,
    "created_at": "2026-03-09T16:27:59.569733+05:30"
  }
]
```

---

## Search & Pagination

Navigate to `http://localhost:8000/docs`, open `GET /notes`, fill in parameters, and click **Execute**.

| Param | Type | Description |
|------|------|-------------|
| page | int | Page number (default: 1) |
| limit | int | Results per page (default: 10) |
| search | string | Search by title keyword |

Example response:

```json
[
  {
    "id": 1,
    "title": "Meeting Notes",
    "content": "Discuss project milestones.",
    "owner_id": 1,
    "user_note_number": 1,
    "created_at": "2026-03-09T16:27:59.569733+05:30"
  }
]
```

---

## Get Note by ID

Navigate to `GET /notes/{id}`, enter the note ID, and click **Execute**.

```json
{
  "id": 1,
  "title": "Meeting Notes",
  "content": "Discuss project milestones.",
  "owner_id": 1,
  "user_note_number": 1,
  "created_at": "2026-03-09T16:27:59.569733+05:30"
}
```

---

## Update a Note

Navigate to `PUT /notes/{id}`, enter the ID and updated data.

Example request:

```json
{
  "title": "Updated Title",
  "content": "Updated content."
}
```

---

# Deleting Notes

Navigate to `DELETE /notes/{id}` and click **Execute**.

Response:

```json
{
  "success": true,
  "message": "Note deleted successfully",
  "data": null
}
```

Users can only delete **their own notes**.

Attempting to delete another user's note returns **403 Forbidden**.

---

# Admin Role

An admin is a user first — everything a regular user can do, an admin can do.

Admins additionally can:

| Action | User | Admin |
|------|------|------|
| CRUD on own notes | ✅ | ✅ |
| View all users' notes | ❌ | ✅ |
| Delete any note | ❌ | ✅ |
| Manage users | ❌ | ✅ |

---

# Setting Up an Admin Account

Admin registration is protected.

### Step 1 — Set ADMIN_SECRET in `.env`

```
ADMIN_SECRET=your_admin_bootstrap_secret (I am going with pass@admin)
```

---

### Step 2 — Register Admin

Navigate to `POST /users/register-admin`

Add header:

```
x-admin-secret: your_admin_bootstrap_secret (pass@admin)
```

Example body:

```json
{
  "username": "admin",
  "email": "admin@gmail.com",
  "password": "adminpass123",
  "admin_secret": "pass@admin"
}
```

Response:

```json
{
  "id": 2,
  "username": "admin",
  "role": "admin"
}
```

---

### Step 3 — Login

Use `POST /users/login` with admin credentials.

The returned JWT token automatically contains **admin privileges**.

---

# Admin Endpoints

## Get All Notes

Navigate to `GET /admin/notes`.

Returns notes across all users.

---

## Delete Any Note

Navigate to:

```
DELETE /admin/notes/{note_id}
```

Response:

```json
{
  "success": true,
  "message": "Note deleted by admin",
  "data": null
}
```

---

# Edge Cases

| Scenario | Error | Fix |
|------|------|------|
| Wrong credentials | 401 Invalid username or password | Check credentials |
| Missing token | 401 Not authenticated | Add Authorization header |
| Expired token | 401 Token has expired | Login again |
| Accessing another user's note | 403 Not authorized | Users can only access their own notes |
| Wrong admin secret | 403 Invalid admin secret | Must match `.env` value |
| DATABASE_URL None | ArgumentError | Ensure `.env` exists |

---

# Author

**Karthik Valmiki**

GitHub:  
https://github.com/Karthik-Valmiki
