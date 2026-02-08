---
name: django-log-watcher
description: Automatically monitors Django logs for 500/404 errors and tracebacks during browser testing. Use this whenever the local server is running.
---

# Django Log Watcher Skill

## Goal
To identify and fix backend exceptions immediately after they occur during a browser session.

## Instructions
1. **Monitor Terminal:** Whenever a task involves the "Browser Agent," open a parallel terminal stream to watch `tail -f logs/django.log` (or your active terminal output).
2. **Detect Errors:** Look for keywords: `Internal Server Error`, `Traceback`, `DoesNotExist`, or `CSRF verification failed`.
3. **Automatic Fix:** If a 500 error is detected during a browser click:
   - Pause the browser test.
   - Read the traceback from the terminal.
   - Propose a fix in the `models.py` or `views.py`.
   - Re-run migrations if necessary and restart the test.

## Constraints
- Do not ignore 404 errors for static assets (images/CSS); fix the paths instead.
- If a database migration is missing, run `makemigrations` and `migrate` automatically.