# Contributing to HYPERSET

Thanks for helping. This project values simple, readable code over clever code, so small focused changes are the easiest to review and merge.

## Ground rules

- **Keep it simple.** Plain Django views and templates, plain CSS and JavaScript. Please don't add a frontend framework, build step or new dependency without opening an issue first.
- **Follow the existing patterns.** Look at how a similar feature is already built and do the same thing. New pages follow the existing views and templates; new numbers for the report go in `tracker/reports.py`; anything that calls Gemini goes in `tracker/ai.py`.
- **One change per pull request.** A bug fix shouldn't also refactor unrelated code.
- **Add or update a test** for behaviour you change.

## Local setup

Follow [docs/setup.md](docs/setup.md), then:

```bash
python manage.py test tracker
```

Tests mock Gemini, so you don't need an API key to run them.

## Making a change

1. Fork the repo and create a branch: `git checkout -b fix-calorie-total`.
2. Make your change and run the tests.
3. If you changed a screen, update the screenshot in `docs/screenshots/` (390 × 844 phone viewport at 2× is what the existing ones use).
4. If you changed a model, run `python manage.py makemigrations tracker` and commit the migration.
5. Add a line under **Unreleased** in [CHANGELOG.md](CHANGELOG.md).
6. Open a pull request and fill in the template.

## Code style

- Python: PEP 8, 4-space indents, descriptive names, small functions. Comments only where the logic isn't obvious.
- Templates: extend `tracker/base.html`; reuse the existing CSS classes (`tile`, `btn`, `chip`, `stat`, `bento`) before adding new ones.
- CSS: colours come from the variables at the top of `style.css`; follow [docs/brand.md](docs/brand.md). Mobile first; desktop tweaks go in the `min-width` media queries at the bottom.
- JavaScript: plain browser JavaScript in `app.js`, no libraries.

## Adding exercises to the built-in library

Add a line to `EXERCISE_LIBRARY` in `tracker/seed_data.py` (`name | muscle | equipment | category`). The seed runs only once on a new database, so for existing installs also add a small data migration, or add the exercise through the app.

## Reporting bugs and ideas

Use the issue templates on GitHub. For security problems, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

By contributing you agree that your contributions are licensed under the [MIT License](LICENSE) and that you'll follow the [Code of Conduct](CODE_OF_CONDUCT.md).
