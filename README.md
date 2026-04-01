# Finance Dashboard Backend

This is my submission for the backend developer intern assignment. I built it using Django and Django REST Framework because that's what I'm most comfortable with.

The idea is a finance dashboard where users with different roles (Admin, Analyst, Viewer) can interact with financial records. I also built a simple frontend using Django templates so you can actually see it working in a browser without needing to set up anything else.

---

## What I used

- Python / Django
- Django REST Framework for the API
- JWT authentication (djangorestframework-simplejwt)
- SQLite as the database (simple and works out of the box)
- django-filter for filtering records
- drf-spectacular for auto Swagger docs
- Django Templates + plain CSS for the frontend (no React or anything)
- WhiteNoise for static files in production

---

## How to run it

```bash
# clone the repo and go into the project folder
git clone <repo-url>
cd finance_project

# create and activate virtualenv
python -m venv venv
venv\Scripts\activate      # on Windows
# source venv/bin/activate   # on Mac/Linux

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# create an admin user to log in with
python manage.py createsuperuser

# start the server
python manage.py runserver
```

Go to http://localhost:8000/login/ in your browser and sign in.

API docs are at http://localhost:8000/api/docs/

---

## Project structure

```
finance_project/
├── finance_backend/        # project settings and main urls
├── api/                    # main app with all the logic
│   ├── models.py           # CustomUser and Record models
│   ├── serializers.py      # input/output validation
│   ├── views.py            # API views + HTML page views
│   ├── permissions.py      # role-based permission checks
│   ├── filters.py          # record filtering (date range, category)
│   ├── urls.py             # all routes
│   ├── templates/api/      # HTML pages
│   └── static/api/         # CSS
├── requirements.txt
├── Procfile
└── manage.py
```

---

## Roles and what they can do

I defined 3 roles. The permissions are enforced in `permissions.py` using DRF's BasePermission class.

| Role | Records | Users | Dashboard |
|---|---|---|---|
| ADMIN | Full CRUD | Full CRUD | Yes |
| ANALYST | Read only | No | Yes |
| VIEWER | No access | No | Yes (but no recent activity) |

The reason I restricted recent_activity for Viewer is that it shows individual transaction info, which felt like it should be protected.

---

## API endpoints

**Auth**
- `POST /api/auth/token/` - login and get JWT token
- `POST /api/auth/token/refresh/` - refresh expired token

**Records** (requires auth)
- `GET /api/records/` - list records, supports filters
- `POST /api/records/` - create record (admin only)
- `GET /api/records/{id}/` - get one record
- `PUT /api/records/{id}/` - update record (admin only)
- `DELETE /api/records/{id}/` - delete record (admin only)

Filter params you can use: `?transaction_type=INCOME&category=Salary&start_date=2024-01-01&end_date=2024-12-31`

**Users** (admin only)
- `GET /api/users/` - list users
- `POST /api/users/` - create user
- `PATCH /api/users/{id}/` - update user (role, is_active, etc)
- `DELETE /api/users/{id}/`

**Dashboard**
- `GET /api/dashboard/` - returns totals, category breakdown, monthly trends, recent activity

**Docs**
- `/api/docs/` - Swagger UI

---

## Database models

**CustomUser** - extends Django's AbstractUser, added a `role` field

**Record**
- amount (decimal)
- transaction_type (INCOME or EXPENSE)
- category (text)
- date
- notes (optional)
- created_by (foreign key to user)
- created_at, updated_at (auto)

---

## Assumptions I made

- SQLite is fine for this scale. In a real production app I'd switch to PostgreSQL.
- I'm storing JWTs in localStorage on the frontend. For a real app httpOnly cookies are safer but this keeps it simple.
- Viewers can see the dashboard (total income/expenses etc) but not individual transactions. Felt like the right call.
- I didn't implement soft delete - records are just deleted. Could add an `is_deleted` field later.

---

## Optional things I added

- JWT auth
- Pagination on both /api/users/ and /api/records/
- Date range filtering (start_date, end_date)
- Swagger docs at /api/docs/
- A working browser frontend (Django templates, no npm needed)
- Production-ready settings using environment variables

---

## Deployment

I set it up so it can be deployed to Railway or Render pretty easily.

The `Procfile` is already there:
```
web: gunicorn finance_backend.wsgi --log-file -
```

You'd need to set these env variables on the platform:
- `SECRET_KEY` = some long random string
- `DEBUG` = False
- `ALLOWED_HOSTS` = your-app.railway.app (or whatever domain)

Then run `python manage.py migrate` and `python manage.py createsuperuser` to set up the database.
