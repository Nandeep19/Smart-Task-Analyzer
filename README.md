# Singularium — Smart Task Analyzer

This repository contains a complete solution for the Smart Task Analyzer assignment:
- Backend: Django project exposing two API endpoints:
  - POST /api/tasks/analyze/ : Accepts a JSON list of tasks and returns them sorted by calculated priority score with explanations.
  - GET  /api/tasks/suggest/ : Returns the top 3 suggested tasks for today with brief explanations.
- Frontend: `frontend/index.html` with a small UI to input tasks (form or paste JSON), choose strategy, and call the API.
- Tests: Unit tests for the scoring algorithm (at least 3 tests).

## Quick setup (local)
1. Create and activate a Python virtualenv (Python 3.8+ recommended):

```bash
python3 -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run migrations and start server:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

3. Open the frontend:
- Open `frontend/index.html` in the browser OR
- Visit `http://127.0.0.1:8000/frontend/` (if running via Django static mapping)

## Algorithm summary (300-500 words)
The scoring algorithm balances four factors: urgency, importance, effort, and dependencies. Each factor is first normalized to a 0-1 range (with urgency able to exceed 1 for overdue tasks to increase priority). Urgency measures how close the due date is relative to a configurable window (default 30 days). Tasks due sooner get higher urgency; past-due tasks receive an amplified urgency to ensure they surface. Importance uses the user-provided 1-10 rating and is normalized by dividing by 10. Effort is inverted: smaller estimated hours become higher scores (quick wins), normalized against a practical maximum (default 40 hours). Dependencies are scored by counting how many other tasks list a given task as a dependency — tasks that block multiple others get higher scores.

These normalized values are combined using weighted sums. The default "Smart Balance" weights are: urgency 0.40, importance 0.30, effort 0.15, dependency 0.15. Alternative strategies (Fastest Wins, High Impact, Deadline Driven) adjust the weights to emphasize different factors. We also detect circular dependencies by constructing a graph and running DFS — if cycles are detected the API returns a clear error. Invalid or missing fields are handled gracefully: missing `importance` defaults to 5, missing `estimated_hours` defaults to 4, and missing `due_date` treats the task as low urgency unless specified. Tasks with invalid date formats are reported with friendly error messages.

Trade-offs: The algorithm is intentionally simple and explainable — this helps with predictability and testability. It biases overdue tasks to avoid neglect, but not to the extent that a high-importance task far in the future never appears. With more time, configurability (persisted user preferences), holiday-aware urgency, and a learning feedback loop would improve personalization.

## Files
- backend/: Django project and tasks app
- frontend/: static HTML/CSS/JS (interacts with API)
- requirements.txt
- run_demo.sh (optional helper)
