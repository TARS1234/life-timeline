import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import Session, select

from .auth import require_api_key, API_KEY
from .db import init_db, get_session
from .models import Timeline, Milestone, TimelineNote
from .schemas import MilestoneCreate, MilestoneUpdate, TimelineUpdate, NoteCreate

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="Life Timeline",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def on_startup():
    init_db()
    with next(get_session()) as session:
        timeline = session.exec(select(Timeline)).first()
        if not timeline:
            session.add(Timeline(
                name="My 50-Year Timeline",
                description="Primary life roadmap",
                start_year=datetime.now().year,
                end_year=datetime.now().year + 50,
            ))
            session.commit()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_session)):
    timeline = session.exec(select(Timeline)).first()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "timeline": timeline,
        "api_key": API_KEY,
    })


# ── Timeline ──────────────────────────────────────────────────────────────────

@app.get("/api/timeline", dependencies=[Depends(require_api_key)])
@limiter.limit("60/minute")
def get_timeline_data(request: Request, session: Session = Depends(get_session)):
    timeline = session.exec(select(Timeline)).first()
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline not found")
    milestones = session.exec(
        select(Milestone).where(Milestone.timeline_id == timeline.id)
    ).all()
    notes = session.exec(
        select(TimelineNote).where(TimelineNote.timeline_id == timeline.id)
    ).all()
    return {
        "timeline": timeline,
        "milestones": milestones,
        "notes": notes
    }


@app.get("/api/timeline/current", dependencies=[Depends(require_api_key)])
@limiter.limit("60/minute")
def get_current_timeline(request: Request, session: Session = Depends(get_session)):
    timeline = session.exec(select(Timeline)).first()
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline not found")
    return {
        "id": timeline.id,
        "name": timeline.name,
        "start_year": timeline.start_year,
        "end_year": timeline.end_year,
    }


@app.put("/api/timeline", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def update_timeline(request: Request, payload: TimelineUpdate, session: Session = Depends(get_session)):
    timeline = session.exec(select(Timeline)).first()
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(timeline, key, value)
    session.add(timeline)
    session.commit()
    session.refresh(timeline)
    return timeline


# ── Notes ─────────────────────────────────────────────────────────────────────

@app.post("/api/notes", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def create_note(request: Request, payload: NoteCreate, session: Session = Depends(get_session)):
    note = TimelineNote(timeline_id=payload.timeline_id, content=payload.content)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.delete("/api/notes/{note_id}", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def delete_note(request: Request, note_id: int, session: Session = Depends(get_session)):
    note = session.get(TimelineNote, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}


# ── Milestones ────────────────────────────────────────────────────────────────

@app.post("/api/milestones", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def create_milestone(request: Request, payload: MilestoneCreate, session: Session = Depends(get_session)):
    timeline = session.get(Timeline, payload.timeline_id)
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline not found")
    milestone = Milestone(**payload.model_dump())
    session.add(milestone)
    session.commit()
    session.refresh(milestone)
    return milestone


@app.put("/api/milestones/{milestone_id}", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def update_milestone(request: Request, milestone_id: int, payload: MilestoneUpdate, session: Session = Depends(get_session)):
    milestone = session.get(Milestone, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(milestone, key, value)
    milestone.updated_at = datetime.utcnow()
    session.add(milestone)
    session.commit()
    session.refresh(milestone)
    return milestone


@app.delete("/api/milestones/{milestone_id}", dependencies=[Depends(require_api_key)])
@limiter.limit("30/minute")
def delete_milestone(request: Request, milestone_id: int, session: Session = Depends(get_session)):
    milestone = session.get(Milestone, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    session.delete(milestone)
    session.commit()
    return {"ok": True}
