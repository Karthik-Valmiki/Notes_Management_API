# Notes Management API

> A RESTful API for managing personal notes with **JWT authentication** and **Role-Based Access Control**.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

---

## Setup

### 1. Install Docker

Download and install Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop). With Docker no other dependencies needed. 

After installation, open the Docker Desktop application.
  Important: Docker won't work until the app is open and you see the little whale icon in your taskbar/menu bar turn solid (it shouldn't be "animating" or "starting").

Make sure Docker is running on left bottom, then you can proceed with the next steps

### 2. Clone the repository

```bash
git clone https://github.com/Karthik-Valmiki/Notes_Management_API.git
cd Notes_Management_API
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/notes_db
SECRET_KEY=your_long_hex_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_SECRET=your_admin_bootstrap_secret
```

#### About `SECRET_KEY`

`SECRET_KEY` is the server-side key used to **sign and verify JWT tokens**. Every token issued by the API is signed with this key — if it changes, all existing tokens become invalid and every logged-in user gets logged out.

- Must be a long, random hex string — never a simple word or phrase
- Must stay consistent across restarts — do not auto-generate it on startup

Generate one by running this in your terminal:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the output directly into your `.env` as the `SECRET_KEY` value.

---

## Running the Application

```bash
docker compose up --build
```
Run the above command in Vs-Code Terminal

| | URL |
|-|-----|
| **API** | `http://localhost:8000` |
| **Swagger UI** | `http://localhost:8000/docs` |

> The database starts first — Docker's healthcheck ensures the API only comes up once PostgreSQL is fully ready.

---

## Authentication

### Register

```bash
Navigate to `http://localhost:8000/docs`, open the `POST /users/register` endpoint, Go with username, email, password and click **Execute**.
  -d '{"username": "karthik","email":"karthik@gmail.com", "password": "secret123"}'
```

**Response:**

```json
{
  "id": 1,
  "username": "karthik",
  "email":"karthik@gmail.com",
  "role": "user"
}
```

---

### Login

```bash
Navigate to `http://localhost:8000/docs`, open the `POST /users/login` endpoint, Go with email, password and click **Execute**.
  -d '{"username": "karthik", "password": "secret123"}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

> Use this token as `Authorization: Bearer <your_token>` in all requests below.
> open `http://localhost:8000/docs`, click the **Authorize** button on the top right, and paste your token there — Swagger handles the header automatically for every request.
---

## Creating Notes

```bash
Navigate to `http://localhost:8000/docs`, open the `POST /notes` endpoint, enter your title and content in the request body and click **Execute**.
  -d '{"title": "Meeting Notes", "content": "Discuss project milestones."}'
```

**Response:**

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

## Managing Notes

### Get All Notes

```bash
Navigate to `http://localhost:8000/docs`, open the `GET /notes` endpoint and click **Execute**.
```

**Response:**
This response shows all notes created so far
```json
[
  {
    "id": 1,
    "title": "Meeting Notes",
    "content": "Discuss project milestones.",
    "owner_id": 1,
    "user_note_number": 1,
    "created_at": "2026-03-09T16:27:59.569733+05:30"
  },
  {
    "id": 2,
    "title": "Ideas",
    "content": "New feature brainstorm.",
    "owner_id": 1,
    "user_note_number": 2,
    "created_at": "2026-03-09T17:10:22.123456+05:30"
  }
]
```
If your response failed to show the id number 2 then you haven't created yet..
---

### Search & Pagination

```bash
Navigate to `http://localhost:8000/docs`, open the `GET /notes` endpoint, fill in `page`, `limit`, and `search` params and click **Execute**.
```

| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number *(default: 1)* |
| `limit` | int | Results per page *(default: 10)* |
| `search` | string | search by title keyword |

**Response:**

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

### Get Note by ID

```bash
Navigate to `http://localhost:8000/docs`, open the `GET /notes/{id}` endpoint, enter the note ID and click **Execute**.
```

**Response:**

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

### Update a Note

```bash
Navigate to `http://localhost:8000/docs`, open the `PUT /notes/{id}` endpoint, enter the note ID and updated body and click **Execute**.
  -d '{"title": "Updated Title", "content": "Updated content."}'
```

**Response:**

```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content.",
  "owner_id": 1,
  "user_note_number": 1,
  "created_at": "2026-03-09T16:27:59.569733+05:30"
}
```

---

## Deleting Notes

```bash
Navigate to `http://localhost:8000/docs`, open the `DELETE /notes/{id}` endpoint, enter the note ID and click **Execute**.
```

**Response:**

```json
{
  "success": true,
  "message": "Note deleted successfully"
}
```

> Users can only delete their **own** notes. Attempting to delete another user's note returns `403 Forbidden`.

---

## Admin Role
 An admin is a user first — everything a regular user can do, an admin can do. The difference is admins can see and delete notes belonging to any user.

### Capabilities

| Action | User | Admin |
|--------|------|-------|
| CRUD on own notes | ✅ | ✅ |
| View all users' notes | ❌ | ✅ |
| Delete any note | ❌ | ✅ |
| Manage users | ❌ | ✅ |

### Setting Up an Admin Account

Admin registration is intentionally protected — it cannot be done through the normal register flow.

**Step 1** — Set `ADMIN_SECRET` in your `.env`

**Step 2** — Register admin with the secret in the header:

```bash
Navigate to `http://localhost:8000/docs`, open the `POST /users/register-admin` endpoint, enter `your_admin_bootstrap_secret` in the `x-admin-secret` header field, fill in username and password in the request body and click **Execute**.
  -d '{"username": "admin", "password": "adminpass123"}'
```

**Response:**

```json
{
  "id": 2,
  "username": "admin",
  "role": "admin"
}
```

**Step 3** — Login normally. The token returned carries admin privileges automatically.

```bash
Navigate to `http://localhost:8000/docs`, open the `POST /users/login` endpoint, enter admin credentials and click **Execute**. The token returned carries admin privileges automatically.
  -d '{"username": "admin", "password": "adminpass123"}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
#### Admin — Get All Notes

Navigate to `http://localhost:8000/docs`, open the `GET /admin/notes` endpoint and click **Execute**. This returns every note across all users in the system.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Meeting Notes",
    "content": "Discuss project milestones.",
    "owner_id": 1,
    "user_note_number": 1,
    "created_at": "2026-03-09T16:27:59.569733+05:30"
  },
  {
    "id": 2,
    "title": "Ideas",
    "content": "New feature brainstorm.",
    "owner_id": 3,
    "user_note_number": 1,
    "created_at": "2026-03-09T17:10:22.123456+05:30"
  }
]
```

### Admin — Delete Any Note

Navigate to `http://localhost:8000/docs`, open the `DELETE /admin/notes/{note_id}` endpoint, enter the note ID and click **Execute**.

**Response:**
```json
{
  "success": true,
  "message": "Note deleted by admin"
}
```

> Admin deletion happens through `/admin/notes/{note_id}` — a dedicated route separate from the regular user delete endpoint.
---

## Edge Cases

| Scenario | Error | Fix |
|----------|-------|-----|
| Wrong credentials | `401 Invalid username or password` | Check username and password — both are case-sensitive |
| Missing token | `401 Not authenticated` | Add `Authorization: Bearer <your_token>` header |
| Expired token | `401 Token has expired` | Login again to get a fresh token |
| Accessing another user's note | `403 Not authorized` | Users can only access their own notes |
| Wrong admin secret | `403 Invalid admin secret` | Value in `x-admin-secret` must match `ADMIN_SECRET` in `.env` |
| `DATABASE_URL` is None on startup | `ArgumentError: Expected string or URL` | Run `cp .env.example .env` and fill in your credentials |

---

## Author

**Karthik Valmiki** — [GitHub](https://github.com/Karthik-Valmiki)