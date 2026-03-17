from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class Timeline(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    start_year: int
    end_year: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TimelineNote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timeline_id: int = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Milestone(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timeline_id: int = Field(index=True)
    parent_id: Optional[int] = Field(default=None, index=True)  # hierarchy
    title: str
    description: Optional[str] = None
    target_date: Optional[date] = None
    end_date: Optional[date] = None                              # range milestones
    target_year: int = Field(index=True)
    horizon_type: str = Field(default="year")
    color: Optional[str] = Field(default=None)          # custom hex color
    notes: Optional[str] = Field(default=None)          # long-form notes
    category: str = Field(default="general")
    status: str = Field(default="planned")
    priority: str = Field(default="medium")
    position_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
