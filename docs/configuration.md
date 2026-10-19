# Configuration

HYPERSET runs with no configuration on your own computer. Everything below is optional locally and recommended when you put it online. See [`.env.example`](../.env.example) for a copy-ready list.

## Environment variables

| Variable | Default | What it does |
| --- | --- | --- |
| `SECRET_KEY` | a development key | Django's secret key. **Set a long random value in production.** |
| `DEBUG` | `1` | Set to `0` in production. Also turns on secure cookies. |
| `ALLOWED_HOSTS` | `*` | Comma-separated domains the app may serve, e.g. `myapp.up.railway.app`. |
| `CSRF_TRUSTED_ORIGINS` | empty | Comma-separated origins with scheme, e.g. `https://myapp.up.railway.app`. Needed for forms over HTTPS. |
| `DATABASE_PATH` | `db.sqlite3` in the project | Where the SQLite file lives. Point it at a persistent disk in production. |
| `EMAIL_HOST` | empty | SMTP server. When empty, emails are printed to the console. |
| `EMAIL_PORT` | `587` | SMTP port. |
| `EMAIL_HOST_USER` | empty | SMTP username. |
| `EMAIL_HOST_PASSWORD` | empty | SMTP password or app password. |
| `EMAIL_USE_TLS` | `1` | Use TLS for SMTP. |
| `DEFAULT_FROM_EMAIL` | `HYPERSET <noreply@hyperset.local>` | Sender of password reset emails. |
| `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` | none | Used by the Railway start command to create the first admin user. |

Set them before starting the server:

```bash
# Mac / Linux
export DEBUG=0
# Windows (Command Prompt)
set DEBUG=0
```

To generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## AI settings (in the app)

The Gemini API key and model are stored in the database, not in environment variables, so you can change them without restarting. Open **Settings → AI settings**.

| Field | Example |
| --- | --- |
| API key | your key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| Model | `gemini/gemini-2.5-flash` (default) or `gemini/gemini-2.5-pro` |

Any Gemini model works. Write it as `gemini/` followed by the model's name.

## Profile and targets

**Profile** (in the app, or Settings → Profile) holds weight, height, age, goal, daily calorie target and daily protein target. The report and the coach use these targets.

## Password reset emails

With no `EMAIL_HOST` set, reset emails are printed in the terminal running `runserver`. Copy the link from there.

To send real emails with Gmail:

1. Turn on 2-step verification for your Google account.
2. Create an app password: Google Account → Security → App passwords.
3. Set:

   | Variable | Value |
   | --- | --- |
   | `EMAIL_HOST` | `smtp.gmail.com` |
   | `EMAIL_PORT` | `587` |
   | `EMAIL_HOST_USER` | `you@gmail.com` |
   | `EMAIL_HOST_PASSWORD` | the 16-character app password |
   | `DEFAULT_FROM_EMAIL` | `HYPERSET <you@gmail.com>` |

A reset link works once and expires after 3 days. Only users with that email saved get a link.
