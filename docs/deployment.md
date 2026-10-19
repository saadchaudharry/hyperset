# Deployment

HYPERSET is a single Django app with a SQLite database, so any host that runs Python and keeps a file on disk works. This guide covers Railway (config included) and a generic Linux server.

## Before you deploy

- Set `SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` (see [configuration](configuration.md)).
- Store the database on **persistent storage** and point `DATABASE_PATH` at it. Without it, your data disappears on every redeploy.
- Serve over HTTPS.

## Railway

[`railway.json`](../railway.json) contains the start command. On every start it:

1. runs migrations,
2. collects static files (served by WhiteNoise),
3. creates the admin user from the `DJANGO_SUPERUSER_*` variables, skipping this if it already exists,
4. starts gunicorn on `$PORT`.

Steps:

1. Create a project and an empty service on [railway.com](https://railway.com).
2. Add a **volume** to the service, mounted at `/data`.
3. Under **Networking**, generate a domain, e.g. `myapp.up.railway.app`.
4. Set the service variables:

   | Variable | Value |
   | --- | --- |
   | `SECRET_KEY` | a long random string |
   | `DEBUG` | `0` |
   | `DATABASE_PATH` | `/data/db.sqlite3` |
   | `ALLOWED_HOSTS` | `myapp.up.railway.app` |
   | `CSRF_TRUSTED_ORIGINS` | `https://myapp.up.railway.app` |
   | `DJANGO_SUPERUSER_USERNAME` | your username |
   | `DJANGO_SUPERUSER_EMAIL` | your email |
   | `DJANGO_SUPERUSER_PASSWORD` | a strong password |
   | Email variables | optional, for real reset emails |

5. Deploy the code, either:
   - **GitHub:** connect the service to your repository; every push redeploys, or
   - **CLI:** from the project folder run `npm i -g @railway/cli`, then `railway login`, `railway link` (pick the project and service) and `railway up`.
6. Open the domain, log in, and add your Gemini key in **Settings → AI settings**.

## Any Linux server (VPS)

```bash
git clone https://github.com/saadchaudharry/hyperset.git
cd hyperset
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export SECRET_KEY=... DEBUG=0 ALLOWED_HOSTS=fit.example.com CSRF_TRUSTED_ORIGINS=https://fit.example.com
export DATABASE_PATH=/var/lib/hyperset/db.sqlite3

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
gunicorn config.wsgi --bind 127.0.0.1:8000 --timeout 120
```

Put Nginx or Caddy in front for HTTPS and keep gunicorn running with systemd. The `--timeout 120` gives the AI coach time to answer.

## Backups

Everything lives in one SQLite file. Copy `db.sqlite3` (or your `DATABASE_PATH`) somewhere safe regularly, ideally while the app is stopped, or use `sqlite3 db.sqlite3 ".backup backup.sqlite3"`.

## Updating

Pull the new code, install requirements, then run `python manage.py migrate` and `collectstatic`, and restart. On Railway the start command does this for you.
