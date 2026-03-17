from datetime import date
from typing import Optional
from sqlmodel import SQLModel


class MilestoneCreate(SQLModel):
    timeline_id: int
    parent_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    end_date: Optional[date] = None
    target_year: int
    horizon_type: str = "year"
    category: str = "general"
    status: str = "planned"
    priority: str = "medium"
    position_order: int = 0
    color: Optional[str] = None
    notes: Optional[str] = None


class MilestoneUpdate(SQLModel):
    parent_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    end_date: Optional[date] = None
    target_year: Optional[int] = None
    horizon_type: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    position_order: Optional[int] = None
    color: Optional[str] = None
    notes: Optional[str] = None


class NoteCreate(SQLModel):
    timeline_id: int
    content: str


class TimelineUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
