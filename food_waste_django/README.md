# Food Waste Management System (Django)

Front end: HTML, CSS, Bootstrap 5 and JavaScript (`tracker/templates/index.html`).  
Back end: Django. Local development uses SQLite; Vercel production should use managed PostgreSQL.

## Run locally (Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Deploy to Vercel

1. Push this project folder to a GitHub repository. The repository root should contain `manage.py`, `requirements.txt` and `vercel.json`.
2. In Vercel, select **Add New > Project**, import the repository, and keep the project root at the folder containing `manage.py`.
3. Add these environment variables in **Project Settings > Environment Variables**:
   - `DJANGO_SECRET_KEY`: a long, random secret key. Generate locally with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
   - `DJANGO_DEBUG`: `False`.
   - `DATABASE_URL`: your managed PostgreSQL connection string (for example, from Neon). Use the provider's pooled URL for runtime traffic if it provides one.
4. Deploy. Vercel detects Django from `manage.py` and the Django dependency. It collects configured static files during the build and serves them through its CDN.
5. Run database migrations against the production database once, from your local terminal using the production `DATABASE_URL`:

```powershell
$env:DATABASE_URL="YOUR_PRODUCTION_POSTGRES_URL"
$env:DJANGO_SECRET_KEY="YOUR_SECRET_KEY"
python manage.py migrate
```

6. Open your deployed URL. The Django admin is at `/admin/`.

## Important database note

Do not use the SQLite database file as the production database on Vercel. Function filesystems are not persistent between invocations/deployments. Configure PostgreSQL through `DATABASE_URL` before using the app with real data. Keep the connection string private and never commit it to GitHub.

## API

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/data/` | All inventory, waste and surplus |
| POST | `/api/inventory/` | Add stock |
| DELETE | `/api/inventory/<id>/` | Remove stock (used up) |
| POST | `/api/inventory/<id>/waste/` | Move stock to the waste log |
| POST | `/api/waste/` | Add a waste entry |
| POST | `/api/surplus/` | List surplus food |
| DELETE | `/api/surplus/<id>/` | Mark surplus done |
