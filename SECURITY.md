# Security Policy

## Reporting a vulnerability

Please **don't open a public issue** for security problems. Use GitHub's **Security → Report a vulnerability** (private advisory) on this repository, with steps to reproduce and the impact you see. You'll get a reply within a few days.

## Running it safely

- Set your own `SECRET_KEY`, set `DEBUG=0`, and list your domain in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` before putting the app online. See [docs/configuration.md](docs/configuration.md).
- Serve it over HTTPS only.
- Your Gemini API key is stored in the database (Settings → AI settings). Protect the database file and admin access, and never commit `db.sqlite3`.
- Only create logins for people you trust: every logged-in user can see and edit all data.
- Food descriptions and coach messages are sent to Google's Gemini API to get answers.
