# ProVerify Backend

A Django-based product verification system. All pages are served via Python routes — no `.html` file access needed.

## Setup

### 1. Prerequisites
- Python 3.10+
- PostgreSQL running locally

### 2. Configure Database
Edit `proverify/settings.py` and set your PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'proverify_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Install & Run
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # create your admin user
python manage.py runserver
```
Or just run: `bash run.sh`

## Routes

| URL | Description |
|-----|-------------|
| `/verify/` | Public product verification page |
| `/admin-login/` | Admin login |
| `/admin-dashboard/` | Admin dashboard |
| `/admin-upload/` | Upload codes (CSV/Excel) |
| `/admin-codes/` | View all codes |
| `/admin-details/` | Batch details |
| `/django-admin/` | Django built-in admin |
| `/api/verify/` | POST — verify a product code |
| `/api/codes/upload/` | POST — upload codes file |
| `/api/dashboard/stats/` | GET — dashboard statistics |
| `/api/auth/email-login/` | POST — login with email/password |

## Notes
- Static files are served from `/static/` (the `static/` folder)
- All API calls use relative URLs (e.g. `/api/verify/`) so they work on any host
