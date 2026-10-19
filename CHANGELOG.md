# Changelog

All notable changes are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed
- AI coach and calorie estimates failing with "No module named 'mcp'": the AI library is now pinned to the tested version and `mcp` is installed with it.

## [1.1.0] - 2026-10-19

### Changed
- Renamed the project to **HYPERSET** (tagline: Train. Track. Fuel. Level Up.).
- New brand look across the app and admin: matte black, neon lime, Saira bold italic display type.

### Added
- HYPERSET logo, wordmark, favicons, app icons and a web app manifest, so it can be added to the home screen.
- Brand guide in `docs/brand.md`.

### Fixed
- Tests no longer need `collectstatic`: hashed static files are only used when `DEBUG=0`.

## [1.0.0] - 2026-10-19

### Added
- Daily log: planned workout per date, sets with reps and weight, completed flag, extra exercises and removing them.
- Food log with Gemini calorie and macro estimates, or manual calories.
- Weekly plan editor with the default 5-day Push / Pull / Legs / Upper / Lower plan.
- Exercise library with 353 exercises, search, filters, custom exercises, form guides and per-exercise history.
- AI coach chat that looks up profile, plan, food, workout and body-weight data with AI tool calls (Gemini).
- Profile with body stats, targets, weight and waist log, and a 7/30/90-day report with insights, charts, sets per muscle group and strength progress.
- Login, logout and forgot-password screens.
- Gemini API key and model configurable in the Django admin.
- Railway deployment config.
