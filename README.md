# Life Timeline

A personal long-range life planning app built around an interactive timeline. Map out campaign goals spanning decades, break them into sub-goals, track progress, and plan short-term milestones — all in one dark-themed local web app.

![Life Timeline](https://img.shields.io/badge/stack-FastAPI%20%2B%20SQLite-blue) ![vis-timeline](https://img.shields.io/badge/vis--timeline-7.7.3-green)

---

## What it does

- **Interactive timeline** — drag, resize, and zoom from day-level to 70-year view. Goals are laid out as bars across time.
- **Campaign goals** — major life objectives that span years. Each creates its own swim lane on the timeline.
- **Sub-goals** — steps that live inside a campaign goal's row. Can have exact start/end dates or be open-ended.
- **Compact monthly planner** — below the timeline, a month view shows short-term goals as dot indicators on their day. Click any day to see what's active and add new goals.
- **Day detail modal** — clicking a day opens a panel listing every goal active on that date, each clickable to view/edit.
- **Timeline notes** — a timestamped journal below the planner for decisions, updates, and reflections.
- **Achieved view** — a separate table of all completed goals.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [SQLModel](https://sqlmodel.tiangolo.com/) |
| Database | SQLite (`data/timeline.db`) |
| Frontend | Jinja2 template + [vis-timeline 7.7.3](https://visjs.github.io/vis-timeline/) (CDN) + vanilla JS |
| Styles | Custom dark CSS (no framework) |

No build step. No npm. Runs entirely from Python.

---

## Requirements

- Python 3.9+

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/life-timeline.git
cd life-timeline

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the data directory
mkdir -p data

# 5. Run the app
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

The database is created automatically on first run at `data/timeline.db`. No migration commands needed — the app self-migrates on startup.

---

## Project structure

```
life-timeline/
├── app/
│   ├── main.py          # FastAPI app, all API routes
│   ├── models.py        # SQLModel table definitions (Timeline, Milestone, TimelineNote)
│   ├── schemas.py       # Request/response schemas
│   ├── db.py            # DB init + auto-migration helper
│   ├── templates/
│   │   └── index.html   # Single-page frontend (vis-timeline + all JS)
│   └── static/
│       └── style.css    # Dark theme styles
├── data/
│   └── timeline.db      # SQLite database (auto-created, not committed)
├── requirements.txt
└── README.md
```

---

## Using the app

### Adding goals

Click **+ Add Goal** in the top-right header, or double-click anywhere on the timeline to open the goal modal.

**Goal types:**
- **Campaign Goal** — a major multi-year objective. Gets its own labeled row on the timeline.
- **Sub-goal** — a concrete step under a campaign goal. Appears inside the parent's swim lane.

**Horizon** sets the default end date relative to the start (1-year, 5-year, etc.). You can override it manually.

### Editing goals

- **Double-click** any bar on the timeline to open the edit modal.
- **Drag** a bar left/right to move it in time.
- **Drag the edges** of a bar to resize (change start or end date).
- A floating HUD shows exact start, end, duration, and delta while dragging.

### Zooming the timeline

Use the zoom preset buttons in the header (**1M**, **3M**, **1Y**, **5Y**, **10Y**, **All**) or scroll/pinch on the timeline itself. The time axis granularity adapts automatically (day → week → month → year ticks).

### Monthly planner

Scroll below the timeline to see the compact month view.

- **Dot indicators** on a day mean short-term goals are scheduled there.
- **Subtle pills** above the grid are long-range goals that span the current month (for context — edit them on the timeline).
- Click **any day** to open the Day Details panel: see all goals active that day, click one to edit it, or use **+ Add Goal** to schedule something new for that date.
- Use **‹ ›** to navigate months.

### Notes

The notes section below the planner is a simple timestamped journal. Write anything — decisions, reflections, context — and it stays attached to the timeline.

### Settings

Click the **⚙** button in the header to change the timeline name, description, and year range.

---

## API

The backend exposes a small REST API (also browsable at [http://localhost:8000/docs](http://localhost:8000/docs)):

| Method | Path | Description |
|---|---|---|
| GET | `/api/timeline` | Full timeline data (milestones + notes) |
| PUT | `/api/timeline` | Update timeline settings |
| POST | `/api/milestones` | Create a milestone |
| PUT | `/api/milestones/{id}` | Update a milestone |
| DELETE | `/api/milestones/{id}` | Delete a milestone |
| POST | `/api/notes` | Add a note |
| DELETE | `/api/notes/{id}` | Delete a note |

---

## Data & privacy

All data is stored locally in `data/timeline.db` (SQLite). Nothing is sent to any server. Add `data/` to your `.gitignore` if you want to keep your personal timeline out of version control.

---

## License

MIT
