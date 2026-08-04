# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A small Flask REST API for managing tasks, used as a learning project for CI/CD practices. It uses `uv` for dependency management (Python >= 3.14).

## Commands

```bash
# Install dependencies
uv sync

# Run the dev server (http://127.0.0.1:5000)
uv run python app.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest test_app.py::test_create_task
```

## Architecture

- `app.py` — the entire Flask application: a single-file REST API for `/tasks` (CRUD). State is an in-memory list of dicts (`tasks`), reset on every process restart — there is no database.
- `test_app.py` — pytest tests against the Flask app using `app.test_client()`. Tests share the module-level `tasks` list, so ordering matters (e.g. `test_delete_task` deletes task id 2 seeded in `app.py`).
- `.github/workflows/ci.yml` — a `workflow_dispatch` job named "Claude Jira" that takes a Jira ticket ID/summary/description as input and delegates to a reusable workflow (`Juzinn/claude-workflows/.github/workflows/claude-jira.yml`) to have Claude implement the ticket, run `uv sync` and `uv run pytest`, and open a PR. It is not a standard push/PR test-runner CI pipeline.
- `.claude/settings.ci.json` — the `claude-code-action` settings file required by the reusable Jira workflow above (passed as its `settings:` input). Its `permissions.allow` list should stay in sync with the `allowed_tools` string in `ci.yml`.
