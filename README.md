# AKATSUKI

Premium public website and management platform for the AKATSUKI student technology community. React/Vite is the public interface; Django REST Framework serves public data and Django Admin manages members, events, gallery content, applications, settings, and email logs.

## Stack
- React, TypeScript, Vite, Tailwind CSS, Framer Motion, Lucide
- Django, Django REST Framework, PostgreSQL (SQLite fallback for local development)
- SMTP via Django's configurable email backend

## Structure
- `frontend/`: responsive public website
- `backend/`: Django project and domain apps

## Local setup

Requirements: Python 3.11+, Node 20+, npm. PostgreSQL is optional locally.

1. Copy `.env.example` to `.env` and set a secret key.
2. Backend:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_data
   python manage.py createsuperuser
   python manage.py runserver
   ```
3. Frontend in another terminal:
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

Django Admin: `http://127.0.0.1:8000/admin/`; API: `http://127.0.0.1:8000/api/`. The frontend defaults to that API URL. No applicant accounts are required.

## Environment
See `.env.example`. `DATABASE_URL` accepts PostgreSQL URLs; when absent, SQLite is used. Never commit `.env` or credentials. Set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`, trusted hosts, CORS origins, and PostgreSQL in production. Configure a private media storage service for production resumes; local `MEDIA_ROOT` is development storage.

## Email
Django's email backend uses SMTP settings from environment variables. Leave `EMAIL_HOST` empty to use the console backend locally. The email helper is isolated in `core/emailing.py` for later provider replacement. Promotion attempts send a branded HTML/plain-text congratulations message and always record an `EmailLog`; failed sends do not fail promotion, and logs can be retried from Admin.

## Administration
Create an admin account with `python manage.py createsuperuser`. Manage active members, published events, visible gallery images, site settings, applications, and email logs in Django Admin. To promote a selected eligible application, use the Applications list action **Promote to Core Member**. The operation avoids duplicate members, changes the application status, sends congratulations, and records delivery outcome.

## API
- `GET /api/members/` active members, ordered by display order
- `GET /api/events/` published events
- `GET /api/gallery/` visible images
- `GET /api/settings/` public site settings
- `POST /api/applications/` public application submission (multipart form)
- `GET /api/applications/` requires an authenticated administrator

Application submission is throttled, validated on both sides, rejects non-PDF/oversized resumes, and blocks repeat submissions from the same email during a short cooldown. Applicant records and resumes are never exposed through public serializers. Use authenticated admin access to review them.

## Deployment
Deploy the frontend to Vercel with `VITE_API_URL` set to the backend API origin. Deploy Django to Render, Railway, AWS, or similar with PostgreSQL, persistent/private media storage, environment variables, HTTPS, and an explicit `CORS_ALLOWED_ORIGINS`. Run `python manage.py migrate` as a release step and serve Django through a production WSGI/ASGI server. Configure SMTP credentials only in the hosting secret store.

## Troubleshooting
- CORS error: include the exact frontend origin in `CORS_ALLOWED_ORIGINS`.
- Empty public content: add active members, published events, visible gallery images, and one SiteSettings record in Admin.
- SMTP issues: inspect Email Logs and check provider credentials; local console mode prints mail to the server terminal.
- PostgreSQL connection error: verify `DATABASE_URL`; unset it to use SQLite locally.

## Brand assets

The supplied AKATSUKI artwork is optimized into a full logo, crest crop, and logo wordmark under `frontend/public/`. The actual letterforms are used for the home hero wordmark; other headings use Space Grotesk.

## Admin and team content

Create an administrator with `python manage.py createsuperuser`, then open `/admin/`. Add or edit profiles under **Core members**: enter the name, position, domain, social profile URLs, optional photo and bio, then set Active and display order. Member email fields are private and are omitted from the public API. The included `python manage.py seed_data` command adds the supplied Suraj Kumar and Devesh Kumar profiles and official contact email; rerunning it does not overwrite profiles already edited in Admin.

## Email delivery and applicant verification

The project sends the congratulations email when an administrator promotes an accepted or shortlisted applicant. It does not currently send an applicant email-verification link or OTP. Email delivery uses Django SMTP settings from environment variables. For Gmail, use an App Password generated for the club Gmail account (with two-step verification enabled), never the normal Gmail password. Put it in `EMAIL_HOST_PASSWORD` in local `.env` or the deployment secret store. Do not commit credentials. Until SMTP is configured, Django uses its console backend in development.
